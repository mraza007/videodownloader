#!/usr/bin/env python3.6
import tkinter as tk
import os.path


from threading import Thread
from tkinter import filedialog, messagebox
from download_youtube_video import download_youtube_video
from pytube.exceptions import PytubeError, RegexMatchError


class YouTubeDownloadGUI(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.btn_download = None
        self.btn_output_browse = None
        self.text_url = None
        self.text_output_path = None
        self.text_filename_override = None
        self.text_proxy = None
        self.radio_video_audio = []
        self.audio_only = tk.BooleanVar(self)
        self.output_path = tk.StringVar(self)
        self.filename_override = tk.StringVar(self)
        self.proxy = tk.StringVar(self)

        self.quit = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='YouTube URL/ID').grid(row=0, column=0)
        self.text_url = tk.Entry(self, width=60)
        self.text_url.grid(row=0, column=1, columnspan=2)

        tk.Label(self, text='Output Directory').grid(row=1, column=0)
        self.text_output_path = tk.Entry(self, width=60, textvariable=self.output_path)
        self.text_output_path.grid(row=1, column=1, columnspan=2)
        self.btn_output_browse = tk.Button(self)
        self.btn_output_browse['text'] = 'Browse...'
        self.btn_output_browse['command'] = self.browse_output_path
        self.btn_output_browse.grid(row=1, column=3)

        tk.Label(self, text='Filename Override').grid(row=2, column=0)
        self.text_filename_override = tk.Entry(self, width=60, textvariable=self.filename_override)
        self.text_filename_override.grid(row=2, column=1, columnspan=2)

        tk.Label(self, text='Proxy').grid(row=3, column=0)
        self.text_proxy = tk.Entry(self, width=60, textvariable=self.proxy)
        self.text_proxy.grid(row=3, column=1, columnspan=2)

        self.radio_video_audio.append(tk.Radiobutton(self, text='Video', variable=self.audio_only, value=False))
        self.radio_video_audio.append(tk.Radiobutton(self, text='Audio (Takes Longer)', variable=self.audio_only,
                                                     value=True))

        self.radio_video_audio[0].grid(row=4, column=1)
        self.radio_video_audio[1].grid(row=4, column=2)

        self.btn_download = tk.Button(self)
        self.btn_download['text'] = 'Download'
        self.btn_download['command'] = self.download
        self.btn_download.grid(row=5, column=1, columnspan=2)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.grid(row=6, column=1, columnspan=2)

    def browse_output_path(self):
        self.output_path.set(filedialog.askdirectory(initialdir='/', title='Select Output Folder'))
        self.text_output_path.delete(0, tk.END)
        self.text_output_path.insert(0, self.output_path.get())

    def download(self):
        self.btn_download['text'] = 'Downloading...'
        self.btn_download.config(state=tk.DISABLED)
        Thread(target=self.threaded_download).start()

    def threaded_download(self):
        try:
            if self.proxy.get() != '':
                proxy = {self.proxy.get().split(':')[0]: self.proxy.get()}
            else:
                proxy = None
            filename = download_youtube_video(self.text_url.get(), audio_only=self.audio_only.get(),
                                              output_path=self.output_path.get(),
                                              filename=self.filename_override.get()
                                              if self.filename_override.get() != '' else None,
                                              proxies=proxy)
            messagebox.showinfo('Download Complete!', 'Download Complete!\n%s' % filename)
        except PytubeError as e:
            messagebox.showerror('Something went wrong...', e)
        except RegexMatchError as e:
            messagebox.showerror('Something went wrong...', e)
        except Exception as e:
            messagebox.showerror('Something went wrong',
                                 'Something unknown went wrong. Is this a live stream? Wait until the stream ends.'
                                 '\n\n%s' % e)
        finally:
            self.btn_download['text'] = 'Download'
            self.btn_download.config(state=tk.NORMAL)


if __name__ == '__main__':
    root = tk.Tk()
    app = YouTubeDownloadGUI(master=root)
    app.master.title('YouTube Video/Audio Downloader')
    app.master.tk.call('wm', 'iconphoto', app.master._w, tk.PhotoImage(file=os.path.abspath('assets/ytdl.png')))
    app.mainloop()
