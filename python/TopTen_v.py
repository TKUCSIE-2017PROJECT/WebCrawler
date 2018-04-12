# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import time
import json
import demjson
def GetMessage(TopUrl,Rank):
    res=requests.get(TopUrl)
    soup=BeautifulSoup(res.text,'lxml')
    comment=soup.select('.review-container')

    DetailDict={   #地點資訊
        "rank" : Rank,
        "name" : soup.select('#HEADING')[0].text,
        "form" : soup.select('.detail')[0].text,
        "address" : soup.select('.address')[0].text
    }

    Commentlist=[]
    for c in comment:   #第一頁評論
        CommentDict={
            "user" : c.select('.username')[0].text,
            "title" : c.select('.noQuotes')[0].text,
            "content" : c.select('.partial_entry')[0].text.replace("\n","")
        }
        Commentlist.append(CommentDict)
    DetailDict["comment"]=Commentlist
    return DetailDict
#####################################################
def City(Cityurl,Name):
    res=requests.get(Cityurl)
    soup=BeautifulSoup(res.text,'lxml')
    PlaceList=soup.select('.listing_info')
    length=len(PlaceList)
    for p in PlaceList:
        try:
            PlaceName=p.select('.listing_title')[0].getText()
            if "\n" in PlaceName:
                PlaceName=PlaceName.replace("\n","")

            CommentText=p.select('.more')[0].getText()
            if "\n" in CommentText:
                CommentText=CommentText.replace("\n","")

            Placeurl=p.find('a')['href']
            txtlen=len(CommentText)
            PlaceCommentNum=int(CommentText[:txtlen-3].replace(",","")) #取數字部分

            print("---------- "+"("+Name+")"+PlaceName+'  '+CommentText+" ----------")
            for i in range(0,10):
                if PlaceCommentNum > TopTenComment[i]:
                    TopTenName.insert(i,"("+Name+")"+PlaceName)
                    TopTenComment.insert(i,PlaceCommentNum)
                    TopTenUrl.insert(i,Placeurl)
                    break
            
            if len(TopTenComment) >11: #10+比較用的數字=11
                TopTenName.pop()
                TopTenComment.pop()
                TopTenUrl.pop()
            print("地名:",TopTenName)
            print("評論數量:",TopTenComment[:len(TopTenComment)-1],"\n")
        #time.sleep(1)
        except:
            print("\njump\n")
            continue
        #sys.exit(0) 

if __name__ == "__main__" :
    global TopTenName
    global TopTenComment
    global TopTenUrl
    global TopTenDict
    TopTenName=[]
    TopTenComment=[0]
    TopTenUrl=[]
    home='https://www.tripadvisor.com.tw'
    cityname=[
            '台北市','台中市','新北市','高雄市','台南市','花蓮縣','宜蘭縣','桃園市','屏東縣','台東縣',
            '南投縣','新竹市','彰化縣','苗栗縣','澎湖縣','新竹縣','嘉義市','嘉義縣','基隆市','金門縣',
            '雲林縣','馬祖縣']
    citynamelist=' 1.台北市  2.台中市  3.新北市  4.高雄市  5.台南市  6.花蓮縣  7.宜蘭縣  8.桃園市  9.屏東縣 10.台東縣\n11.南投縣 12.新竹市 13.彰化縣 14.苗栗縣 15.澎湖縣 16.新竹縣 17.嘉義市 18.嘉義縣 19.基隆市 20.金門縣\n21.雲林縣 22.馬祖縣 '
    citylist=[
        '/Attractions-g293913-Activities-Taipei.html',         #台北市 1
        '/Attractions-g297910-Activities-Taichung.html',       #台中市 2
        '/Attractions-g1432365-Activities-Xinbei.html',        #新北市 3
        '/Attractions-g297908-Activities-Kaohsiung.html',      #高雄市 4
        '/Attractions-g293912-Activities-Tainan.html',         #台南市 5
        '/Attractions-g297907-Activities-Hualien_County.html', #花蓮縣 6
        '/Attractions-g608526-Activities-Yilan_County.html',   #宜蘭縣 7
        '/Attractions-g297912-Activities-Taoyuan.html',        #桃園市 8
        '/Attractions-g297909-Activities-Pingtung_County.html',#屏東縣 9
        '/Attractions-g304163-Activities-Taitung_County.html', #台東縣 10
        '/Attractions-g304160-Activities-Nantou_County.html',  #南投縣 11
        '/Attractions-g297906-Activities-Hsinchu.html',        #新竹市 12
        '/Attractions-g304153-Activities-Changhua_County.html',#彰化縣 13
        '/Attractions-g616038-Activities-Miaoli_County.html',  #苗栗縣 14
        '/Attractions-g1437280-Activities-Penghu_County.html', #澎湖縣 15
        '/Attractions-g1433865-Activities-Hsinchu_County.html',#新竹縣 16
        '/Attractions-g297904-Activities-Chiayi.html',         #嘉義市 17
        '/Attractions-g1433864-Activities-Chiayi_County.html', #嘉義縣 18
        '/Attractions-g317130-Activities-Keelung.html',        #基隆市 19
        '/Attractions-g1152699-Activities-Kinmen_County.html', #金門縣 20
        '/Attractions-g616037-Activities-Yunlin_County.html',  #雲林縣 21
        '/Attractions-g1731586-Activities-Matsu_Islands.html', #馬祖縣 22
    ]
    print(citynamelist)
    choose=''
    choose=input("輸入選擇的城市(用空白隔開,可複選)>>")
    if choose =="exit":
        sys.exit(0)
    choose=choose.split()
    chooselen=len(choose)
    st=[]
    for ch in choose:
        st.append(cityname[int(ch)-1])
    print(st)

    filname=input("輸入檔名(預設TopTen)>>")
    if filname =="exit":
        sys.exit(0)
    elif filname == None or filname == "":
        filname="TopTen"
    count=0
    for i in choose:
        City(home+citylist[int(i)-1],cityname[int(i)-1])
        if count==0 :
            TopTenComment.pop()  #去除第11筆,為了比較大小多出來的
        if count>0 and count < chooselen-1:
            print("\n******************** Change City ********************\n")
        count+=1
    print("轉檔中...")
    ############################
    TopTenDict={
        "topten" : TopTenName,
    }

    detial=[]
    for i in range(0,len(TopTenName)):
        cach=GetMessage(home+TopTenUrl[i],i+1)
        detial.append(cach)

    TopTenDict['detial']=detial

    TopTenDict=demjson.decode(str(TopTenDict))
    with open(filname+".json",'w',encoding='utf-8') as f:
        json.dump(TopTenDict,f,indent=5, sort_keys=False,ensure_ascii=False)