# -*- encoding: utf-8 -*-

import os, time
from time import sleep
from PIL import Image
import math
import operator
from functools import reduce
import cv2
import pyautogui as pag
from pyautogui import click
from pyautogui import dragTo
from pyautogui import scroll


def compare_pic(pic1, pic2):
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(
        reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))

    print(differ)
    return differ


def cut_img():
    img = pag.screenshot(region=[238, 1025, 80, 60])  # x,y,w,h
    img.save('src_pc/img/tmp.png')
    # cmd1 = "adb -s " + serial + " shell screencap -p /data/tmp.png"
    # cmd2 = "adb -s " + serial + " pull /data/tmp.png " + os.path.join(src_path, "tmp.png")
    # os.system(cmd1)
    # os.system(cmd2)
    # img = cv2.imread("src_pc/img/tmp.png")
    # newimg = img[1124:384, 1210:599]
    # cv2.imwrite("look_ad.png", newimg)


def look_ad_diff():
    img = pag.screenshot(region=[238, 1025, 80, 60])  # x,y,w,h
    img.save('src_pc/img/look_ad_tmp.png')
    # img = cv2.imread("src/img/tmp.png")
    # newimg = img[1124:1210, 384:599]
    # cv2.imwrite("src/img/look_ad_tmp.png", newimg)
    return compare_pic("src_pc/img/look_ad_tmp.png", "src_pc/img/look_ad.png")

def reset_ad_diff():
    reset = pag.screenshot(region=[423, 1010, 84, 44])  # x,y,w,h
    # ad = pag.screenshot(region=[238, 1025, 80, 60])  # x,y,w,h
    reset.save('src_pc/img/reset_tmp.png')
    # ad.save('src_pc/img/ad_tmp.png')
    # ad_diff = compare_pic("src_pc/img/ad_tmp.png", "src_pc/img/look_ad.png")
    reset_diff = compare_pic("src_pc/img/reset_tmp.png", "src_pc/img/reset.png")
    return reset_diff

def long_ad():
    long_ad = pag.screenshot(region=[119, 1039, 141, 50])
    long_ad.save('src_pc/img/long_ad_tmp.png')
    long_ad_diff = compare_pic("src_pc/img/long_ad_tmp.png", "src_pc/img/long_ad.png")
    return long_ad_diff

def auto_click():
    start = time.time()
    time_power = 0.5
    time_add_goods = 2
    while True:
        for j in range(3):
            for i in range(10):
                click(162 + i * 36, 1251 + j * 40)
        # if time.time() - start > 20:
        #     break
        # sleep(0.5)

        # look ad
        if time.time() - start > 60 * time_power:
            click(336, 1132)
            sleep(2)
            if look_ad_diff() < 50:
                click(344, 1051)
                sleep(33)
                click(591, 393)
                sleep(1)
                long_ad_handle()
                sleep(2)
                time_power += 0.5
            time_power += 1

        # add goods
        if time.time() - start > 60 * time_add_goods:
            # canteen
            click(492, 1033)
            sleep(1)
            click(492, 1033)
            sleep(2)
            for i in range(2):
                pag.mouseDown(130, 1305)
                pag.moveTo(455, 1305)
                sleep(1)
                click(158, 1316)
                sleep(1)
            click(285, 973)
            sleep(1)
            click(155, 875)
            sleep(1)
            click(511, 692)
            sleep(1)
            # money
            click(446, 1033)
            click(367, 984)
            click(401, 910)
            click(478, 866)
            sleep(1)
            click(158, 1316)
            sleep(1)
            click(61, 1434)
            sleep(2)

            # bash_room
            click(445, 928)
            sleep(1)
            click(445, 928)
            sleep(2)
            for i in range(3):
                pag.mouseDown(130, 1305)
                pag.moveTo(455, 1305)
                sleep(1)
                click(158, 1316)
                sleep(1)
            click(338, 1061)
            sleep(1)
            click(225, 945)
            sleep(1)
            click(362, 880)
            sleep(1)
            # money
            click(513, 1150)
            sleep(1)
            click(456, 907)
            sleep(1)
            for i in range(2):
                pag.mouseDown(455, 1305)
                pag.moveTo(130, 1305)
                sleep(1)
                click(158, 1316)
                sleep(1)
            click(290, 1028)
            sleep(1)
            click(61, 1434)
            sleep(2)

            time_power += 0.5
            time_add_goods += 2

        if time_power > 600:
            break

def get_position():
    try:
        while True:
            print('Press Ctrl-C to end')
            screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
            x, y = pag.position()  # 返回鼠标的坐标
            print('Screen size: (%s %s), Position : (%s, %s)' % (screenWidth, screenHeight, x, y))  # 打印坐标
            time.sleep(1)  # 每个1s中打印一次 , 并执行清屏
            os.system('cls')  # 执行系统清屏指令
    except KeyboardInterrupt:
        print('end')

def long_ad_handle():
    """如果是长广告"""
    if long_ad() < 50:
        click(197, 1061)
        sleep(11)
        click(591, 393)
        sleep(1)

def canteen_material():
    """餐厅泰坦菜品"""
    while True:
        while True:
            # 增加体力到满
            click(316, 436)
            sleep(1)
            if look_ad_diff() < 100:
                click(330, 1053)
                sleep(2)
                if look_ad_diff() > 100:
                    sleep(31)
                    click(591, 393)
                    sleep(1)
                    # 判断是否是长广告
                    long_ad_handle()
                    click(320, 1159)
                    sleep(1)
                else:
                    click(320, 1159)
                    sleep(1)
                    break
            else:
                click(320, 1159)
                sleep(10)
                break
        count = 1
        stop_flag = False
        all_stop_flag = False
        while True:
            if all_stop_flag:
                break
            for j in range(8):
                for i in range(6):
                    click(95 + i * 100, 629 + j * 100)
                for i in range(6):
                    if count > 30:
                        click(95 + i * 100, 629 + j * 100)
                        sleep(0.2)
                        if reset_ad_diff() < 100:
                            click(464, 1031)
                            sleep(1)
                            stop_flag = True
                            count = 1
                            break
                    else:
                        click(95 + i * 100, 629 + j * 100)
                count += 6
                if stop_flag:
                    all_stop_flag = True
                    break
                # if j == 3 and i




if __name__ == '__main__':
    auto_click()
    # get_position()
    # canteen_material()
    # print(reset_ad_diff())
    # long_ad()
    # cut_img()
# pag.mouseDown(130, 1305)
# pag.moveTo(455, 1305)
# scroll(100, x=235, y=1311)
#
