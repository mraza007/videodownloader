
# A simple Python Script that will allow you download video
import argparse

from pytube import YouTube


def get_header():
    return """\
      $$\     $$\                $$$$$$$$\        $$\                        $$$$$$\                      $$\            $$\     
      \$$\   $$  |               \__$$  __|       $$ |                      $$  __$$\                     \__|           $$ |    
       \$$\ $$  /$$$$$$\  $$\   $$\ $$ |$$\   $$\ $$$$$$$\   $$$$$$\        $$ /  \__| $$$$$$$\  $$$$$$\  $$\  $$$$$$\ $$$$$$\   
        \$$$$  /$$  __$$\ $$ |  $$ |$$ |$$ |  $$ |$$  __$$\ $$  __$$\       \$$$$$$\  $$  _____|$$  __$$\ $$ |$$  __$$\\_$$  _|  
         \$$  / $$ /  $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |       \____$$\ $$ /      $$ |  \__|$$ |$$ /  $$ | $$ |    
          $$ |  $$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$   ____|      $$\   $$ |$$ |      $$ |      $$ |$$ |  $$ | $$ |$$\ 
          $$ |  \$$$$$$  |\$$$$$$  |$$ |\$$$$$$  |$$$$$$$  |\$$$$$$$\       \$$$$$$  |\$$$$$$$\ $$ |      $$ |$$$$$$$  | \$$$$  |
          \__|   \______/  \______/ \__| \______/ \_______/  \_______|       \______/  \_______|\__|      \__|$$  ____/   \____/ 
                                                                                                              $$ |               
                                                                                                              $$ |               
                                                                                                              \__|               
    """


def get_footer():
    return """\n
    $$$$$$$$\ $$\                           $$\                       $$$$$$$$\                        $$\   $$\           $$\                     
    \__$$  __|$$ |                          $$ |                      $$  _____|                       $$ |  $$ |          \__|                    
       $$ |   $$$$$$$\   $$$$$$\  $$$$$$$\  $$ |  $$\  $$$$$$$\       $$ |    $$$$$$\   $$$$$$\        $$ |  $$ | $$$$$$$\ $$\ $$$$$$$\   $$$$$$\  
       $$ |   $$  __$$\  \____$$\ $$  __$$\ $$ | $$  |$$  _____|      $$$$$\ $$  __$$\ $$  __$$\       $$ |  $$ |$$  _____|$$ |$$  __$$\ $$  __$$\ 
       $$ |   $$ |  $$ | $$$$$$$ |$$ |  $$ |$$$$$$  / \$$$$$$\        $$  __|$$ /  $$ |$$ |  \__|      $$ |  $$ |\$$$$$$\  $$ |$$ |  $$ |$$ /  $$ |
       $$ |   $$ |  $$ |$$  __$$ |$$ |  $$ |$$  _$$<   \____$$\       $$ |   $$ |  $$ |$$ |            $$ |  $$ | \____$$\ $$ |$$ |  $$ |$$ |  $$ |
       $$ |   $$ |  $$ |\$$$$$$$ |$$ |  $$ |$$ | \$$\ $$$$$$$  |      $$ |   \$$$$$$  |$$ |            \$$$$$$  |$$$$$$$  |$$ |$$ |  $$ |\$$$$$$$ |
       \__|   \__|  \__| \_______|\__|  \__|\__|  \__|\_______/       \__|    \______/ \__|             \______/ \_______/ \__|\__|  \__| \____$$ |
                                                                                                                                         $$\   $$ |
                                                                                                                                         \$$$$$$  |
                                                                                                                                          \______/ 
    \n\n\n
    """


def interactive_mode():
    print(get_header())
    while True:
        user = input('To Download Video/Audio Y/n: ')
        if user.lower() in ['yes', 'y']:
            url = input('Enter Url: ')
            form = input('Do you want to download video or audio: ')
            if form.lower() in ['video', 'v']:
                download_youtube_stream(url, output_path='videos/')

            elif form.lower() in ['audio', 'a']:
                warn = input('Audio Downloads take longer Do you want to Continue Y/n: ')
                if warn.lower() in ['yes', 'y']:
                    download_youtube_stream(url, audio_only=True, output_path='audio/')

                elif warn.lower() in ['no', 'n']:
                    vid = input('To Download Vid Y/n ')
                    if vid.lower() in ['yes', 'y']:
                        download_youtube_stream(url, output_path='videos/')

                    elif vid.lower() in ['no', 'n']:
                        exit()
        if user.lower() in ['no', 'n']:
            print(get_footer())
            exit()


def download_youtube_stream(url, audio_only=False, output_path=None, filename=None, filename_prefix=None):
    video = YouTube(url)
    if audio_only:
        stream = video.streams.filter(only_audio=True).first()
    else:
        stream = video.streams.first()
    print('Download Started')
    stream.download(output_path=output_path, filename=filename, filename_prefix=filename_prefix)
    print('Download Complete')


def parse_args():
    parser = argparse.ArgumentParser(description='YouTube Video/Audio Downloader')
    parser.add_argument('-u', '--url', help='YouTube URL to download.', default=None)
    parser.add_argument('-o', '--output-path', help='Output Directory Path', default=None)
    parser.add_argument('-f', '--filename', help='Override the output filename. Does not override file extension',
                        default=None)
    parser.add_argument('-p', '--prefix', help='Filename Prefix', default=None)
    parser.add_argument('-a', '--audio-only', help='Download Audio Only', action='store_true', default=False)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.url:
        if args.audio_only:
            download_youtube_stream(args.url, audio_only=True,
                                    output_path=args.output_path, filename=args.filename,
                                    filename_prefix=args.filename_prefix)
        else:
            download_youtube_stream(args.url, audio_only=False,
                                    output_path=args.output_path, filename=args.filename,
                                    filename_prefix=args.filename_prefix)
    else:
        interactive_mode()
