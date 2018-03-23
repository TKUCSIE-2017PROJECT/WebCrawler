import requests
from bs4 import BeautifulSoup
import sys
import time
import datetime,calendar
import calendar
import json
import demjson
def get_date():
    global date_data
    start = datetime.date(2009,4,21)
    end = datetime.date(2018,3,8)
    oneday = datetime.timedelta(days=1)
    days = (end - start).days
    date_data = []
    for i in range(0,days+1):
        date_asc = time.asctime( start.timetuple() )
        date_data.append( date_asc[0:10] + date_asc[19:24] )
        #date_data.append(str(start))
        start = start+oneday

def enter(art_url):
    try:
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
        #檔名
        article_number = art_url.split('/')[3].split('.') 
        del article_number[-1]
        file_name = '.'.join(article_number)
        #作者
        userid = detail[0].text.split(" ")[0]
        #時間
        article_time = detail[3].text
        #版名
        board_name = art_url.split('/')[2]  
        ##
        checktime = article_time[0:10]+article_time[19:24]
        if len(checktime)<15:
            return None
        if checktime not in date_data:
            raise EOFError
        ####################################
        article_dict = {
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
        print(file_name)
        article_dict = demjson.decode(str(article_dict))   #tofile
        with open(file_name+".json",'w',encoding='utf-8') as f:
            json.dump(article_dict,f,indent=5, sort_keys=False,ensure_ascii=False)
        time.sleep(0.5)
    except EOFError:
        sys.exit(0)

    except:
        pass

if __name__ == "__main__" :
    global out_of_date
    out_of_date=0
    get_date()
    print("=============================")
    print(date_data)
    payload = {
        'from': "/bbs/BabyMother/index.html",
        'yes':'yes'
    }
    page = 0
    delet_num = 5 #開頭要刪除的數量
    while(1):
        url = "https://www.ptt.cc/bbs/Pet_Get/index"+str(243-page)+".html"
        rs = requests.session()
        res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
        res = rs.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"lxml")
        
        article_title = soup.select(".r-ent")
        article_url_data = []
        for each in article_title:
            #print(each.select(".title")[0].text.strip())   # 標題
            #print(each.select(".date")[0].text)            # 時間
            #print(each.select(".author")[0].text)          # 作者
            #print(each.find('a')['href'])                  # 網址
            try:
                article_url = each.find('a')['href']
                article_url_data.append(article_url)
            except:
                pass

        if page == 0:
            for d in range(0,delet_num):
                del article_url_data[-1]

        print("===================")
        print("page:",page)
        print("===================")

        length = len(article_url_data)
        for i in range(0,length):
            enter(article_url_data[length-1-i])

        page +=1