"""
获取源码，关注公众号：程序员晚枫，后台回复：世界杯
24小时自动获取~
"""

import webbrowser
from win10toast import *
import office
import time
import pygame

import schedule


def play_song(song):
    file_name = song
    pygame.mixer.init()  # 只初始化音频部分
    # 载入的音乐不会全部放到内容中，而是以流的形式播放的，即在播放的时候才会一点点从文件中读取。
    track = pygame.mixer.music.load(file_name)
    # 播放载入的音乐。该函数立即返回，音乐播放在后台进行。
    pygame.mixer.music.play()
    time.sleep(50)
    pygame.mixer.music.stop()


def notice(url):
    office.video.video2mp3(path='./video.mp4', mp3_name='song.mp3')

    toaster = ToastNotifier()
    webbrowser.open_new_tab(url)  # 打开浏览器

    # while True:
    # Add a URL of JavaTpoint to open it in a browser
    # Open the URL using open() function of module
    toaster.show_toast(
        title='世界杯开始',
        msg='大兄弟，看球了！',
        icon_path=r'./icon.jpg',
    )
    # break

    play_song('./song.mp3')  # 播放语音提示


def sche_notice(notice_time, url='https://www.baidu.com/s?ie=UTF-8&wd=%E4%B8%96%E7%95%8C%E6%9D%AF'):
    schedule.every().day.at(notice_time).do(notice, url)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    sche_notice(notice_time='13:10:00',url='www.python-office.com')
