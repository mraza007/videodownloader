# A simple Python Script that will allow you download video

import sys ,os
from pytube import YouTube
x = """\
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
print(x)
while True:
	user = input('To Download Video/Audio Y/n: ')
	if user.lower() in ['yes', 'y']:
		url = input('Enter Url: ')
		link = YouTube(url)
		form = input('Do you want to download video or audio: ')
		if form.lower() in ['video', 'v']:
			download_video = link.streams.first()
			print('Download Started')
			download_video.download()
		elif form.lower() in ['audio', 'a']:
			warn = input('Audio Downloads take longer Do you want to Continue Y/n: ')
			if warn.lower() in ['yes', 'y']:
				download_mp3 = link.streams.filter(only_audio=True).first()
				print('Download Started')
				download_mp3.download('audio/')
			elif warn.lower() in ['no', 'n']:
				vid = input('To Download Vid Y/n ')
				if vid.lower() in ['yes', 'y']:
					download_video = link.streams().first()
					print('Download Started')
					download_video.download('videos/')
				elif vid.lower() in ['no', 'n']:
					exit()
	if user.lower() in ['no', 'n']:
		print("""

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



						""")
		exit()
