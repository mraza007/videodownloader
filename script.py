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
	if user == 'Y':
		url = input('Enter Url: ')
		link = YouTube(url)
		form = input('Do you want to download video or audio: ')
		if form == 'video':
			download_video = link.streams.first()
			print('Download Started')
			download_video.download()
		elif form == 'audio':
			warn = input('Audio Downloads take longer Do you want to Continue Y/n: ')
			if warn == 'Y':
				download_mp3 = link.streams.filter(only_audio=True).first()
				print('Download Started')
				download_mp3.download('audio/')
			elif warn == 'n':
				vid = input('To Download Vid Y/n ')
				if vid == 'Y':
					download_video = link.streams().first()
					print('Download Started')
					download_video.download('videos/')
				elif vid == 'n':
					exit()
	if user == 'n':
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