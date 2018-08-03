from os import makedirs
from os import getcwd, path
from pytube import YouTube
from pytube.compat import urlopen
from pytube.helpers import safe_filename
from pytube.extract import video_id as get_video_id
import moviepy.editor as mpe


THUMBNAIL_QAULITY_LOW = 'sddefault'
THUMBNAIL_QAULITY_MED = 'mqdefault'
THUMBNAIL_QAULITY_HI = 'hqdefault'
THUMBNAIL_QAULITY_MAX = 'maxresdefault'


def get_thumbnail_url(url=None, video=None, quality=THUMBNAIL_QAULITY_MED):
    if url is None and video is None:
        raise ValueError('You must provide either a url or YouTube object.')
    if video:
        return f'{video.thumbnail_url.rsplit("/", 1)[0]}/{quality}.jpg'
    if 'http' in url:
        video_id = get_video_id(url)
        return f'https://i.ytimg.com/vi/{video_id}/{quality}.jpg'
    return f'https://i.ytimg.com/vi/{url}/{quality}.jpg'


def get_thumbnail(url):
    response = urlopen(url)
    return response


def download_youtube_video(url, itag=None, audio_only=False, output_path=None,
                           filename=None, filename_prefix=None,
                           proxies=None, progress_callback=None):
    """
    Download a YouTube Video.
    :param url: Full URL to YouTube Video or YouTube Video ID
    :type url: str
    :param itag: YouTube Stream ITAG to Download
    :type itag: int
    :param audio_only: Download only the audio for the video. Takes longer than video.
    :type audio_only: bool
    :param output_path: Path to folder to output file.
    :type output_path: str
    :param filename: Filename override. Does not override extension.
    :type filename: str
    :param filename_prefix: Currently Does Not Work on pytube
    :type filename_prefix: str
    :param proxies: Dictionary containing protocol (key) and address (value) for the proxies
    :type proxies: dict
    :return: Filename of downloaded video/audio
    :rtype: str
    """
    if output_path:
        makedirs(output_path, exist_ok=True)
    if 'http' not in url:
        url = 'https://www.youtube.com/watch?v=%s' % url
    if proxies:
        video = YouTube(url, proxies=proxies)
    else:
        video = YouTube(url)
    if progress_callback:
        video.register_on_progress_callback(progress_callback)
    if itag:
        itag = int(itag)
        stream = video.streams.get_by_itag(itag)
    else:
        stream = video.streams.filter(only_audio=audio_only).first()
    print('Download Started: %s' % video.title)
    if filename:
        filename = safe_filename(filename)
    stream.download(output_path=output_path, filename=filename)
    file_type = '.' + stream.mime_type.split('/')[1]
    filename = stream.default_filename if filename is None else filename + file_type
    print('Download Complete! Saved to file: %s' % filename)
    return filename


def download_fhd_plus(url, output_path=None,
                           filename=None, filename_prefix=None,
                           proxies=None, progress_callback=None,
                           resolution='1080p'):
    """
    Download a YouTube Video.
    :param url: Full URL to YouTube Video or YouTube Video ID
    :type url: str
    :param output_path: Path to folder to output file.
    :type output_path: str
    :param filename: Filename override. Does not override extension.
    :type filename: str
    :param filename_prefix: Currently Does Not Work on pytube
    :type filename_prefix: str
    :param proxies: Dictionary containing protocol (key) and address (value) for the proxies
    :type proxies: dict
    :param resolution: User selected resolution
    :type resolution: str
    :return: Filename of downloaded video/audio
    :rtype: str
    """
    makedirs('videos', exist_ok=True)
    if 'http' not in url:
        url = 'https://www.youtube.com/watch?v=%s' % url
    if proxies:
        yt = YouTube(url, proxies=proxies)
    else:
        yt = YouTube(url)
    if progress_callback:
        yt.register_on_progress_callback(progress_callback)
    if filename:
        filename = safe_filename(filename)
    else:
        filename = yt.title
    if filename_prefix:
        filename = filename_prefix+filename
    for stream in yt.streams.filter(type='video').filter(adaptive=True).all():
        if stream.resolution == resolution:
            video_stream = stream
            break
    audio_stream = yt.streams.filter(type='audio').filter(adaptive=True).order_by('abr').first()
    print('Download Started: %s' % yt.title)
    # video_stream.download(filename=filename+'_video')
    print('[Step 1/3]: Finished Video Download')
    # audio_stream.download(filename=filename+'_audio')
    print('[Step 2/3]: Finished Audio Download')
    video_track = mpe.VideoFileClip(filename+'_video'+'.'+video_stream.mime_type.split('/')[1])
    audio_track = mpe.AudioFileClip(filename+'_audio'+'.'+audio_stream.mime_type.split('/')[1])
    merged_video = video_track.set_audio(audio_track)
    merged_video.write_videofile(path.join(getcwd(), 'videos', filename+'.avi'),
                                 threads=4, progress_bar=False, codec='mpeg4', bitrate="50000k")
    print('[Step 3/3]: Finished Merging')
    return filename
