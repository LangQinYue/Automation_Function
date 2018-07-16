
from selenium import webdriver
import time
import os

def savePngName():
    day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    fp = os.path.dirname(os.getcwd())+'\\result\\' + day + '\\image'
    tm = time.strftime('%H:%M:%S', time.localtime(time.time()))
    type = '.png'
    if os.path.exists(fp):
        filename = str(fp) + '\\'   +str(tm) +str(type)
        return filename
    else:
        os.makedirs(fp)
        filename = str(fp) + '\\' +str(tm)+'a'   +str(type)
        return filename



browser = webdriver.Firefox()
url = "http://www.baidu.com"

browser.get(url)
tm = time.strftime('%H:%M:%S', time.localtime(time.time()))
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
fp = os.path.dirname(os.getcwd()) + "\\result\\" + day + "\\image"
#print fp
if os.path.exists(fp):
    pic_path = str(fp) + "\\" + str(tm) + ".png"
else:
    os.makedirs(fp)
    pic_path = str(fp) + "\\" + str(tm) + ".png"
            #driver.get_screenshot_as_file(pic_path)
print pic_path
b = savePngName()
tm = str(tm)+'.png'
print tm
browser.save_screenshot(tm)
browser.close()
