import tkinter as tk
from tkinter import font as tkFont
from tkinter import scrolledtext
from selenium import webdriver
from tkinter import END
import time, requests, os, re
import threading as td


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
    piclist = []
    videolist = []
    datetime = '0000-00-00 00:00:00'

    driver.get(url)

    try:
        eledate = driver.find_element_by_xpath("//time[@class='_1o9PC Nzb55']").get_attribute('datetime')
        eledate = re.sub(r'T', ' ', eledate)[:19]
        timestamp = time.mktime(time.strptime(eledate, '%Y-%m-%d %H:%M:%S'))
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp + 32400))
    except:
        print_text.insert('end', '\n' + 'Failed to get post time,URL:' + url)
        print_text.see(END)
        failedlist.append(url)

    while is_nextpage():
        driver.find_element_by_xpath("//div[contains(@class,'coreSpriteRightChevron')]").click()

    try:
        picele = driver.find_elements_by_class_name('KL4Bh')
        piclist = [s.find_element_by_tag_name('img').get_attribute('src') for s in picele]
    except:
        print_text.insert('end', '\n' + 'Failed to find picture links,URL:' + url)
        print_text.see(END)
        failedlist.append(url)

    lenpiclist = len(piclist)
    # print(lenpiclist)

    if lenpiclist > 0:
        try:
            print_text.insert('end', '\n' + 'Found ' + str(lenpiclist) + ' picuture(s) in post: ' + url)
            print_text.see(END)
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
                print_text.insert('end', '\n' + 'Saved instagram picture ' + picname + '.jpg')
                print_text.see(END)
        except:
            print_text.insert('end', '\n' + 'Failed to save pictures,URL:' + url)
            print_text.see(END)
            failedlist.append(url)
    else:
        pass

    try:
        videoele = driver.find_elements_by_class_name('_5wCQW')
        videolist = [s.find_element_by_tag_name('video').get_attribute('src') for s in videoele]
    except:
        print_text.insert('end', '\n' + 'Failed to find video links:' + url)
        print_text.see(END)
        failedlist.append(url)

    lenvideolist = len(videolist)
    # print(videolist)

    if lenvideolist > 0:
        try:
            print_text.insert('end', '\n' + 'Found ' + str(lenvideolist) + ' video(s) in post: ' + url)
            print_text.see(END)
            num = 1
            for i in videolist:
                videoname = datetime + ' ' + str(num)
                videoname = re.sub(r'[\\/:*?"<>|]', '', videoname)
                # print(videoname)
                r = requests.get(i)
                with open(path + '/' + videoname + '.mp4', 'wb') as f:
                    f.write(r.content)
                num += 1
                print_text.insert('end', '\n' + 'Saved Instagram video ' + videoname + '.mp4')
                print_text.see(END)
        except:
            print_text.insert('end', '\n' + 'Failed to save video,URL:' + url)
            print_text.see(END)
            failedlist.append(url)
    else:
        pass


def makefolder(path):
    path = re.sub(r'[\\/:*?"<>|]', '', path)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print_text.insert('end', '\n' + 'Created folder ' + path + ' successfully')
            print_text.see(END)
        else:
            print_text.insert('end', '\n' + 'Folder existed')
            print_text.see(END)
    except:
        print_text.insert('end', '\n' + 'Creating Folder Failed')
        print_text.see(END)
        driver.quit()


def failedlistfun(failedlist):
    failedlist = list(set(failedlist))
    failedlistlen = len(failedlist)
    # print(failedlistlen)
    if failedlistlen > 0:
        print_text.insert('end', '\n' + 'Saved Part of Instagram Media')
        print_text.insert('end', '\n' + '----------Failed to save URL list-----------')
        print_text.see(END)
        for i in failedlist:
            print_text.insert('end', '\n' + i)
            print_text.see(END)
    else:
        print_text.insert('end', '\n' + 'Saved All Instagram Media')
        print_text.see(END)


def usernamelabel(name):
    usernamelabel2 = tk.StringVar()
    usernamelabel2.set(name)
    tk.Label(window, text='User name: ', anchor='w', width=10, height=1).place(x=3, y=65, anchor='nw')
    tk.Label(window, textvariable=usernamelabel2, anchor='w', width=25, height=1).place(x=3, y=90, anchor='nw')


def is_ins_url(url):
    flag = 0
    ret = re.match("https://www.instagram.com/(.+)", url)
    url_info_text = tk.StringVar()
    if ret == None:
        tk.Label(window, width=30, fg='red', anchor='w', textvariable=url_info_text).place(x=150, y=40, anchor='nw')
        url_info_text.set('Error URL')
        return flag
    elif ret.group(1).startswith('p/'):
        tk.Label(window, width=30, anchor='w', textvariable=url_info_text).place(x=150, y=40, anchor='nw')
        url_info_text.set('This is an Instagram post URL')
        flag = 1
        return flag
    else:
        tk.Label(window, width=30, anchor='w', textvariable=url_info_text).place(x=150, y=40, anchor='nw')
        url_info_text.set('This is an Instagram account URL')
        flag = 2
        return flag


def ins_save_post(url):
    try:
        driver.get(url)
        driver.find_element_by_xpath("//a[contains(@class,'nJAzx')]").click()
        Firsttitle = driver.title
        title = driver.title
        while title == Firsttitle:
            title = driver.title
            if not title == Firsttitle:
                driver.back()
                break

        title = re.findall(r'(.*?)[•·]', title)[0]
        path = title + 'Instagram'
        usernamelabel(title)

        makefolder(path)
        findsavemedia(url, path)
        failedlistfun(failedlist)
    except:
        print_text.insert('end', '\nError URL')
        print_text.see(END)
        driver.quit()


def ins_save_account(url):
    global postlink
    postlink = []
    try:
        driver.get(url)

        ySN3v1 = is_postexsits()
        ySN3v2 = is_postexsits(ySN3vnum=2)
        ySN3v3 = is_postexsits(ySN3vnum=3)

        if ySN3v1 == False and ySN3v2 == False and ySN3v3 == False:
            print_text.insert('end', '\n' + 'No post in this instagram account')
            print_text.see(END)
        else:
            print_text.insert('end', '\n' + 'Loading...')
            print_text.see(END)

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
        print_text.insert('end', '\n' + 'Failed to load posts')
        print_text.see(END)
        driver.quit()

    print_text.insert('end', '\n' + 'Loaded')
    print_text.see(END)
    postlink = list(set(postlink))
    postlinklen = len(postlink)

    title = driver.title
    title = re.findall(r'(.*?)[•·]', title)[0]
    path = title + 'Instagram'
    usernamelabel(title)

    print_text.insert('end', '\n' + 'Found' + str(postlinklen) + 'post(s) in this instagram account')
    print_text.see(END)
    # print(postlink)

    makefolder(path)
    for i in postlink:
        findsavemedia(i, path)

    failedlistfun(failedlist)

    driver.quit()


def help():
    window_help = tk.Toplevel(window)
    window_help.geometry('400x180')
    window_help.title('Help')
    ft = tkFont.Font(family='Fixdsys', size=12, weight=tkFont.BOLD)
    tk.Label(window_help, width=100, text="使用方法", font=ft).pack(side='top')
    tk.Label(window_help, width=100, justify='left', text="输入instagram的用户URL\n"
                                                          "eg:https://www.instagram.com/egochan_329/\n"
                                                          "或者单条投稿\n"
                                                          "eg:https://www.instagram.com/p/B6IQESkFhQz/\n\n"
                                                          "*以日本时间(GMT+9)作为文件名保存\n"
                                                          "*若有保存失败的投稿会在最后失败列表列出").place(x=200, y=90, anchor='center')


def about():
    window_about = tk.Toplevel(window)
    window_about.geometry('250x100')
    window_about.title('About')
    tk.Label(window_about, width=30, text='Instagram Saver').place(x=125, y=10, anchor='n')
    tk.Label(window_about, width=30, text='Author : Nakateru (2019.12.17)').place(x=125, y=50, anchor='n')


def startwork():
    Firsturl = entryurl.get()
    isinsurl = is_ins_url(Firsturl)
    if isinsurl == 0:
        pass
    else:
        global driver, failedlist
        failedlist = []
        print_text.insert('end', '\n' + 'Start saving')
        print_text.see(END)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=options)
        if isinsurl == 1:
            ins_save_post(Firsturl)
        else:
            ins_save_account(Firsturl)



def tdfun():
    thread = td.Thread(target=startwork, name='startwork')
    thread.start()


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Instagram saver')
    window.geometry('620x250')

    tk.Label(window, width=20, text='Input Instagram URL:').place(x=5, y=20, anchor='nw')

    entryurl = tk.Entry(window, width=45, show=None)
    entryurl.place(x=150, y=20, anchor='nw')

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=filemenu)
    filemenu.add_command(label='Help', command=help)
    filemenu.add_command(label='About', command=about)
    filemenu.add_command(label='Exit', command=window.quit)
    window.config(menu=menubar)

    print_text = scrolledtext.ScrolledText(window, width=58, height=12)
    print_text.place(x=185, y=80, anchor='nw')
    tk.Button(window, text='Start', width=8, height=1, command=tdfun).place(x=500, y=15, anchor='nw')

    window.mainloop()
