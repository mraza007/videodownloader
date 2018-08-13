import os

from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem, QApplication
from PyQt5.QtGui import QPixmap

from pytube import YouTube, Playlist, extract
from pytube.exceptions import RegexMatchError
from pytube.helpers import regex_search
from utils import get_thumbnail, get_thumbnail_url, download_youtube_video


class StreamLoader(QObject):

    sig_step = pyqtSignal(int, str)
    sig_done = pyqtSignal(int)
    sig_msg = pyqtSignal(str)
    sig_progress_status = pyqtSignal(int)
    sig_progress_total = pyqtSignal(int)
    current_file_size = 0

    def __init__(self, id: int, download_manager):
        super().__init__()
        self.__id = id
        self.__abort = False
        self.__download_manager = download_manager

    @pyqtSlot()
    def load_url(self):
        thread_name = QThread.currentThread().objectName()
        thread_id = int(QThread.currentThreadId())
        self.__download_manager.videos = []
        self.__download_manager.streams = []
        top_level_item_count = self.__download_manager.stream_tree.topLevelItemCount()
        for i in range(top_level_item_count):
            self.__download_manager.stream_tree.takeTopLevelItem(i)
        self.__download_manager.stream_tree.clear()
        try:
            print('get video id')
            print(extract.video_id(self.__download_manager.url.text()))
            loaded_url = YouTube(self.__download_manager.url.text())
            self.sig_msg.emit(f'Found {loaded_url.title}')
            self.__download_manager.videos.append(loaded_url)
        except RegexMatchError:
            print('playlist')
            if 'playlist' in self.__download_manager.url.text():
                regex_search(r'(?:list=|\/)([0-9A-Za-z_-]{11}).*', self.__download_manager.url.text(), group=1)
                loaded_url = Playlist(self.__download_manager.url.text())
                self.sig_msg.emit(f'Loaded playlist. Discovering videos...')
                loaded_url.populate_video_urls()
                i = 0
                self.sig_progress_status.emit(0)
                for video_url in loaded_url.video_urls:
                    self.sig_progress_total.emit(int((i / len(loaded_url.video_urls)) * 100))
                    QApplication.instance().processEvents()
                    vid = YouTube(video_url)
                    self.sig_msg.emit(f'Found {vid.title}')
                    self.__download_manager.videos.append(vid)
                    self.sig_progress_status.emit(100)
                    i += 1
                self.sig_progress_total.emit(100)
        except Exception as e:
            pass

        self.sig_msg.emit(f'Loading Streams..')
        print('loading streams')

        for video in self.__download_manager.videos:
            QApplication.instance().processEvents()
            if self.__abort:
                self.sig_msg.emit(f'Aborting...')
                break
            audio_streams = QTreeWidgetItem(['Audio Only'])
            tree_item = StreamTreeWidgetItem([video.title], self.__download_manager, video, None)
            self.__download_manager.streams = video.streams.all()
            for stream in self.__download_manager.streams:
                self.sig_msg.emit(f'Loading stream: {stream.itag}')
                QApplication.instance().processEvents()
                if stream.video_codec is None:
                    stream_item = StreamTreeWidgetItem([
                        f'Codec: {stream.audio_codec}, '
                        f'ABR: {stream.abr}, '
                        f'File Type: {stream.mime_type.split("/")[1]}, '
                        f'Size: {stream.filesize // 1024} KB'
                    ], self.__download_manager, video, stream)
                    audio_streams.addChild(stream_item)
                else:
                    stream_item = StreamTreeWidgetItem([
                        f'Res: {stream.resolution}, FPS: {stream.fps}, '
                        f' Video Codec: {stream.video_codec}, Audio Codec: {stream.audio_codec}, '
                        f'File Type: {stream.mime_type.split("/")[1]}, '
                        f'Size: {stream.filesize // 1024} KB'
                    ], self.__download_manager, video, stream)
                    tree_item.addChild(stream_item)
                stream_item.setCheckState(0, Qt.Unchecked)
            tree_item.addChild(audio_streams)
            self.__download_manager.stream_tree.addTopLevelItem(tree_item)
        self.sig_msg.emit(f'Streams Loaded!')

    @pyqtSlot()
    def download_streams(self):
        streams_to_download = []
        top_level_count = self.__download_manager.stream_tree.topLevelItemCount()
        print(top_level_count)
        for i in range(top_level_count):
            print('get child')
            top_level_item = self.__download_manager.stream_tree.topLevelItem(i)
            child_count = top_level_item.childCount()
            for x in range(child_count):
                child_item = top_level_item.child(x)
                if child_item.checkState(0) == Qt.Checked:
                    streams_to_download.append(child_item)
        i = 0
        self.sig_progress_total.emit(0)
        for stream_item in streams_to_download:
            self.current_file_size = stream_item.stream.filesize
            filename = f'{stream_item.video.title}_{i}'
            download_youtube_video(itag=stream_item.stream.itag,
                                   output_path=os.path.abspath(self.__download_manager.output_path.text()),
                                   filename=filename, progress_callback=self.update_progress_bar,
                                   video_and_stream=(stream_item.video, stream_item.stream))
            i += 1
            self.sig_progress_total.emit(int((i / len(streams_to_download)) * 100))

    def update_progress_bar(self, stream, chunk, file_handle, bytes_remaining):
        percentage = int(((self.current_file_size - bytes_remaining) / self.current_file_size) * 100)
        self.sig_progress_status.emit(percentage)

    def abort(self):
        self.sig_msg.emit(f'Stream Loader({self.__id}): Received Abort Message...')
        self.__abort = True


class StreamTreeWidgetItem(QTreeWidgetItem, QObject):
    UserType = 1000

    def __init__(self, tree_strings, download_manager, video_object, stream_object):
        super().__init__(tree_strings)
        self.video = video_object
        self.stream = stream_object
        self.download_manager = download_manager
        self.video_title = self.video.title

    def __repr__(self):
        return 'Mine'


class DownloadTab(QWidget):

    display_name = 'Downloader'
    videos = None
    streams = None
    sig_abort_workers = pyqtSignal()
    current_thumbnail = None

    def __init__(self):
        super().__init__()
        self.__threads = []
        QThread.currentThread().setObjectName('tab_downloader')
        loadUi(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tab_download.ui')), self)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.btn_load_url.clicked.connect(self.load_url)
        self.btn_browse.clicked.connect(self.browse_folder)
        self.btn_download.clicked.connect(self.download_streams)

        self.output_path.setText(os.path.abspath(os.getcwd()))

        self.stream_tree.setHeaderLabel('Stream List')
        self.stream_tree.itemClicked.connect(self.check_for_checked)

    def load_url(self):
        self.load_streams()

    def load_streams(self):
        print('a a load streams')
        worker = StreamLoader(1, self)
        thread = QThread()
        thread.setObjectName(f'thread_{1}')
        self.__threads.append((thread, worker))
        print('move to thread')
        worker.moveToThread(thread)

        worker.sig_step.connect(self.on_worker_step)
        worker.sig_done.connect(self.on_worker_done)
        worker.sig_msg.connect(self.status_text.setText)
        worker.sig_progress_status.connect(self.progress_status.setValue)
        worker.sig_progress_total.connect(self.progress_total.setValue)
        self.sig_abort_workers.connect(worker.abort)

        print('connect thread')
        thread.started.connect(worker.load_url)
        print('starting thread')
        thread.start()

    def download_streams(self):
        worker = StreamLoader(2, self)
        thread = QThread()
        self.__threads.append((thread, worker))
        worker.moveToThread(thread)

        worker.sig_step.connect(self.on_worker_step)
        worker.sig_done.connect(self.on_worker_done)
        worker.sig_msg.connect(self.status_text.setText)
        worker.sig_progress_status.connect(self.progress_status.setValue)
        worker.sig_progress_total.connect(self.progress_total.setValue)

        thread.started.connect(worker.download_streams)
        thread.start()

    def browse_folder(self):
        self.output_path.setText(os.path.abspath(str(QFileDialog.getExistingDirectory(self, 'Select Output Directory'))))

    @pyqtSlot(QTreeWidgetItem, int)
    def check_for_checked(self, item, column):
        any_checked = False
        print('get child count')
        top_level_count = self.stream_tree.topLevelItemCount()
        print(top_level_count)
        for i in range(top_level_count):
            print('get child')
            top_level_item = self.stream_tree.topLevelItem(i)
            child_count = top_level_item.childCount()
            for x in range(child_count):
                child_item = top_level_item.child(x)
                if child_item.checkState(0) == Qt.Checked:
                    any_checked = True
                    break
        self.btn_download.setEnabled(any_checked)
        self.set_thumbnail(item, column)

    @pyqtSlot(QTreeWidgetItem, int)
    def set_thumbnail(self, item, column):
        print('get_thumbnail')
        self.current_thumbnail = QPixmap()
        print(item.video)
        self.current_thumbnail.loadFromData(get_thumbnail(get_thumbnail_url(video=item.video)).read())
        self.thumbnail_preview.setPixmap(self.current_thumbnail)

    @pyqtSlot(int, str)
    def on_worker_step(self, worker_id: int, data: str):
        pass

    @pyqtSlot(int)
    def on_worker_done(self, worker_id):
        pass

    @pyqtSlot()
    def abort_workers(self):
        self.sig_abort_workers.emit()
        for thread, worker in self.__threads:
            thread.quit()
            thread.wait()
