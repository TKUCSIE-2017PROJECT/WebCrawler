import requests
from bs4 import BeautifulSoup
import sys
import time
import datetime,calendar
import calendar
import json
import demjson
import multiprocessing as mp 
import os
def get_time():
    global current_time
    global back_time
    global date_data
    current_time=time.localtime(time.time())
    current_time = time.asctime( current_time )

    back_time = time.localtime(time.time()-10*60)  #10個60秒 => 10分鐘
    back_time = time.asctime( back_time )
    #print(current_time >=test and test>= back_time)

    date_data=[0,0]     
    date_data[0]=str(datetime.datetime.strptime(current_time[4:10],"%b %d"))[5:10]       #取數字  月/日
    date_data[1]=str(datetime.datetime.strptime(back_time[4:10],"%b %d"))[5:10]
    for i in range(2):
        date_data[i]=date_data[i].split('-')
        date_data[i]=str(int(date_data[i][0]))+"/"+str(int(date_data[i][1]))
    print(date_data)
    print("=====================")
def enter(art_url):
    try:
        userid=''
        article_time=''
        board_name=''
        payload = {
            'from': art_url,
            'yes':'yes'
        }
        rs = requests.session()
        res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
        res = rs.get('https://www.ptt.cc'+art_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"lxml")
        detail = soup.select('.article-meta-value')
        ###################################
        #編號
        article_number = art_url.split('/')[3].split('.') 
        del article_number[-1]
        article_number = '.'.join(article_number)
        #作者
        userid = detail[0].text.split(" ")[0]
        #時間
        article_time = detail[3].text
        #版名
        board_name = art_url.split('/')[2]  
        ##
        if not(current_time >= article_time and article_time >=back_time): #超過10分鐘跳過
            return None
        ####################################
    except EOFError:
        sys.exit(0)
    except:
        pass
    print(article_number)
    article_dict = {
        'number':article_number,
        'userid' :  userid,            
        'time' : article_time ,
        'board' : board_name
    }
    #推文
    push_list = soup.select(".push")
    push_dict = []
    for push in push_list:
        pre_dict = {
            'tag': push.contents[0].text ,                             
            'userid': push.contents[1].text ,
            'content': push.contents[2].text 
        }
        push_dict.append(pre_dict)
        push.extract()                               #del push
    ####################################
    for message in soup.select('.article-metaline'):    
        message.extract()                            #del detial
    for frm in soup.select('.f2'):                                    
        frm.extract()                                #del from
    #內文
    article_text = soup.select('#main-content')[0].text.replace("\n"," ")
    ####################################
    article_dict['content'] = article_text
    article_dict['push'] = push_dict
    ####################################
    page_check_dict.append(article_dict)
    total_dict.append(article_dict)

def tofile(foldername):
    if len(total_dict) == 0:
        print(foldername," nothing")
        return 0
    time_detail = str(datetime.datetime.strptime(current_time,"%a %b %d %H:%M:%S %Y"))
    filname = "".join(time_detail[:10].split("-"))+"".join(time_detail[11:16].split(":"))

    print(foldername," complete")
    total = demjson.decode(str(total_dict))   #tofile
    with open(foldername+"/"+filname+".json",'w',encoding='utf-8') as f:
        json.dump(total,f,indent=5, sort_keys=False,ensure_ascii=False)
    time.sleep(0.5)

def job(choose):
    global total_dict
    total_dict=[]
    global page_check_dict
    page_check_dict=[]

    choose_url = choose[0]
    delet_num = choose[1]
    get_time()

    folder=choose_url.split('/')[4]
    if not os.path.isdir(folder):
        os.mkdir(folder)

    payload = {
        'from': choose_url[18:],
        'yes':'yes'
    }
    delet=0
    while(1):
        page_chaeck_dict=[]
        print(choose_url)
        url = choose_url
        rs = requests.session()
        res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
        res = rs.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"lxml")
        
        article_title = soup.select(".r-ent")
        article_url_data = []
        
        if delet == 0:
            for d in range(0,delet_num):
                del article_title[-1]
            delet = 1
        OUT=0
        length=len(article_title)
        for i in range(length-1,-1,-1):
            each = article_title[i]
            try:
                date = each.select(".date")[0].text[1:]
                if date not in date_data:
                    OUT=1
                    break
                article_url = each.find('a')['href']
                #print(date,":",article_url)
                article_url_data.append(article_url)
            except:
                pass
        
        length = len(article_url_data)
        for u in article_url_data:
            enter(u)

        if OUT == 1:
            break

        if len(page_check_dict) == 0:
            break

        button = soup.select('.wide')
        for b in button:
            if b.text[-2:] == "上頁":
                choose_url="https://www.ptt.cc"+b.get('href')
        print("================")
    tofile(folder)
if __name__ == '__main__':
    while(1):
        ai_list=[("https://www.ptt.cc/bbs/MakeUp/index.html",4),         #美妝

                ##("https://www.ptt.cc/bbs/Japan_Travel/index.html",4),   #旅遊

                #("https://www.ptt.cc/bbs/Finance/index.html",2),        #經濟

                #("https://www.ptt.cc/bbs/Baseball/index.html",4),       #運動
                #("https://www.ptt.cc/bbs/NBA/index.html",4),

                #("https://www.ptt.cc/bbs/TW_Entertain/index.html",3),   #綜藝

                #("https://www.ptt.cc/bbs/Tech_Job/index.html",5),       #科技

                #("https://www.ptt.cc/bbs/C_Chat/index.html",3),         #動漫

                #("https://www.ptt.cc/bbs/DMM_GAMES/index.html",5),      #遊戲

                #("https://www.ptt.cc/bbs/car/index.html",5),            #汽車

                #("https://www.ptt.cc/bbs/movie/index.html",2),          #電影

                #("https://www.ptt.cc/bbs/Boy-Girl/index.html",5),       #男女
                #("https://www.ptt.cc/bbs/Talk/index.html",3),           #聊天
                ("https://www.ptt.cc/bbs/Gossiping/index.html",5),      #八卦

                ("https://www.ptt.cc/bbs/Food/index.html",4),           #美食

                ("https://www.ptt.cc/bbs/e-shopping/index.html",4),     #網路購物   
                ]
        pool = mp.Pool()
        pool.map(job,ai_list)
        print("pool done")
        time.sleep(600)