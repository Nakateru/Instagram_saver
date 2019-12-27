from selenium import webdriver
import time
import requests
import os
import re


def is_postexsits(ySN3vnum=1, row=1, column=1):
    flag = True
    elementcss = "section._9eogI.E3X2T:nth-child(2) main.SCxLW.o64aR:nth-child(2) div.v9tJq div._2z6nI article.ySN3v:nth-child(" + str(
        ySN3vnum) + ") div:nth-child(1) div:nth-child(1) div.Nnq7C.weEfm:nth-child("
    postcss = elementcss + str(row) + ") > div.v1Nh3.kIKUG._bz0w:nth-child(" + str(column) + ")"
    try:
        driver.find_element_by_css_selector(postcss)
        return flag
    except:
        flag = False
        return flag


def findpost(ySN3vnum=1):
    i = 1
    l = []
    while is_postexsits(ySN3vnum, i, 1):
        for j in range(1, 4):
            if is_postexsits(ySN3vnum, i, j):
                elementcss = "section._9eogI.E3X2T:nth-child(2) main.SCxLW.o64aR:nth-child(2) div.v9tJq div._2z6nI article.ySN3v:nth-child(" + str(
                    ySN3vnum) + ") div:nth-child(1) div:nth-child(1) div.Nnq7C.weEfm:nth-child("
                postcss = elementcss + str(i) + ") > div.v1Nh3.kIKUG._bz0w:nth-child(" + str(j) + ")"
                # print(postcss)
                ele = driver.find_element_by_css_selector(postcss)
                url = ele.find_element_by_tag_name('a').get_attribute('href')
                l.append(url)
            else:
                break
        i += 1
    # print('Searching row',i)
    l = list(set(l))
    return l


def is_nextpage():
    flag = True
    try:
        driver.find_element_by_xpath("//div[contains(@class,'coreSpriteRightChevron')]")
        return flag
    except:
        flag = False
        return flag


def findsavemedia(url, path='save'):
    piclist=[]
    videolist=[]
    datetime='0000-00-00 00:00:00'
    driver.get(url)

    try:
        eledate = driver.find_element_by_xpath("//time[@class='_1o9PC Nzb55']").get_attribute('datetime')
        eledate = re.sub(r'T', ' ', eledate)[:19]
        timestamp = time.mktime(time.strptime(eledate, '%Y-%m-%d %H:%M:%S'))
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp + 32400))
    except:
        print('Failed to get post time,URL:', url)
        failedlist.append(url)

    while is_nextpage():
        driver.find_element_by_xpath("//div[contains(@class,'coreSpriteRightChevron')]").click()

    try:
        picele = driver.find_elements_by_class_name('KL4Bh')
        piclist = [s.find_element_by_tag_name('img').get_attribute('src') for s in picele]
    except:
        print('Failed to find picture links,URL:', url)
        failedlist.append(url)

    lenpiclist = len(piclist)
    # print(lenpiclist)

    if lenpiclist > 0:
        try:
            print('Found ' + str(lenpiclist) + ' picuture(s) in post: ' + url)
            # print(piclist)

            num = 1
            for i in piclist:
                picname = datetime + ' ' + str(num)
                picname = re.sub(r'[\\/:*?"<>|]', '', picname)
                # print(picname)
                r = requests.get(i)
                with open(path + '/' + picname + '.jpg', 'wb') as f:
                    f.write(r.content)
                num += 1
                print('Saved instagram picture ' + picname + '.jpg')
        except:
            print('Failed to save pictures,URL:', url)
            failedlist.append(url)
    else:
        pass

    try:
        videoele = driver.find_elements_by_class_name('_5wCQW')
        videolist = [s.find_element_by_tag_name('video').get_attribute('src') for s in videoele]
    except:
        print('Failed to find video links:', url)
        failedlist.append(url)

    lenvideolist = len(videolist)
    # print(videolist)

    if lenvideolist > 0:
        try:
            print('Found ' + str(lenvideolist) + ' video(s) in post: ' + url)
            num = 1
            for i in videolist:
                videoname = datetime + ' ' + str(num)
                videoname = re.sub(r'[\\/:*?"<>|]', '', videoname)
                # print(videoname)
                r = requests.get(i)
                with open(path + '/' + videoname + '.mp4', 'wb') as f:
                    f.write(r.content)
                num += 1
                print('Saved Instagram video ' + videoname + '.mp4')
        except:
            print('Failed to save video,URL:', url)
            failedlist.append(url)
    else:
        pass


def makefolder(path):
    path = re.sub(r'[\\/:*?"<>|]', '', path)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print('Created folder ' + path + ' successfully')
        else:
            print('Folder existed')
    except Exception:
        print('Creating Folder Failed')
        driver.quit()
        exit()


if __name__ == '__main__':
    postlink = []
    failedlist = []
    print('Instagram Saver')
    print('Author  :  Nakateru (2019.12.17)')
    Firsturl = input('Input Instagram URL:')

    '''how to find post url'''
    # <div <class=" _2z6nI"  <article class="ySN3v"(nth-child(1)) <article class="ySN3v"(nth-child(2))
    # <div <div <div class="Nnq7C weEfm" <div class="v1Nh3 kIKUG  _bz0w"
    # section._9eogI.E3X2T:nth-child(2) main.SCxLW.o64aR:nth-child(2) div.v9tJq div._2z6nI article.ySN3v:nth-child(2) div:nth-child(1) div:nth-child(1) div.Nnq7C.weEfm:nth-child(row) > div.v1Nh3.kIKUG._bz0w:nth-child(i)
    # if none in post of (row,i):
    # <div class="_bz0w"
    # section._9eogI.E3X2T:nth-child(2) main.SCxLW.o64aR:nth-child(2) div.v9tJq div._2z6nI article.ySN3v:nth-child(ySN3vnum) div:nth-child(1) div:nth-child(1) div.Nnq7C.weEfm:nth-child(row) > div._bz0w:nth-child(i)
    # -----ySN3vum==1-------
    # post(1,1) post(1,2) post(1,3)
    # post(2,1) post(2,2) post(2,3)
    # post(3,1) post(3,2) post(3,3)
    # -----ySN3vum==2-------
    # post(1,1) post(1,2) post(1,3)
    # post(2,1) post(2,2) post(2,3)
    # post(3,1) post(3,2) post(3,3)
    # .............

    ret = re.match("https://www.instagram.com/(.+)", Firsturl)

    if ret == None:
        print('Error URL')
        exit()

    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=options)

        if ret.group(1).startswith('p/'):  # post
            print('This is an Instagram post URL')
            try:
                driver.get(Firsturl)
                driver.find_element_by_xpath("//a[contains(@class,'nJAzx')]").click()
                Firsttitle = driver.title
                title = driver.title
                while title == Firsttitle:
                    title = driver.title
                    if not title == Firsttitle:
                        driver.back()
                        break

                path = re.findall(r'(.*?)[•·]', title)[0] + 'Instagram'
                print('Instagram username:', path)

                makefolder(path)
                findsavemedia(Firsturl, path)
            except:
                print('Error URL')
                driver.quit()
                exit()

        else:  # account
            print('This is an Instagram account URL')
            try:
                driver.get(Firsturl)

                ySN3v1 = is_postexsits()
                ySN3v2 = is_postexsits(ySN3vnum=2)
                ySN3v3 = is_postexsits(ySN3vnum=3)

                if ySN3v1 == False and ySN3v2 == False and ySN3v3 == False:
                    print('No post in this instagram account')
                else:
                    print('Loading...')

                if ySN3v1 == True:
                    result = findpost()
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.8)
                        postlink = postlink + findpost()
                        if result == findpost():
                            break
                        else:
                            result = findpost()
                    postlink = postlink + findpost()

                if ySN3v2 == True:
                    result = findpost(ySN3vnum=2)
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.8)
                        postlink = postlink + findpost(ySN3vnum=2)
                        if result == findpost(ySN3vnum=2):
                            break
                        else:
                            result = findpost(ySN3vnum=2)
                    postlink = postlink + findpost(ySN3vnum=2)

                if ySN3v3 == True:
                    result = findpost(ySN3vnum=3)
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.8)
                        postlink = postlink + findpost(ySN3vnum=3)
                        if result == findpost(ySN3vnum=3):
                            break
                        else:
                            result = findpost(ySN3vnum=3)
                    postlink = postlink + findpost(ySN3vnum=3)
            except:
                print('Failed to load posts')
                driver.quit()
                exit()

            print('Loaded')
            postlink = list(set(postlink))
            postlinklen = len(postlink)

            title = driver.title
            path = re.findall(r'(.*?)[•·]', title)[0] + 'Instagram'
            print('Instagram username:', path)
            print('Found', postlinklen, 'post(s) in this instagram account')
            # print(postlink)

            makefolder(path)
            for i in postlink:
                findsavemedia(i, path)
        driver.quit()

        failedlist = list(set(failedlist))
        failedlistlen = len(failedlist)
        # print(failedlistlen)
        if failedlistlen > 0:
            print('Saved Part of Instagram Media')
            print('----------Failed to save URL list-----------')
            for i in failedlist:
                print(i)
        else:
            print('Saved All Instagram Media')
