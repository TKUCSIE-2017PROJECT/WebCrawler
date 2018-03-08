import requests
from bs4 import BeautifulSoup
import sys

def changepage(pr,ad):
    print("------------------------------------------------------------------------")
    payload={
        'from':ad ,
        'yes':'yes'
    }
    address='https://www.ptt.cc'+ad
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
    res = rs.get(address)
    soup=BeautifulSoup(res.text,"lxml")
    page=soup.select('.r-ent')
    length=len(page)
    num2=1
    while num2>0:
        print("------------------------------------------------------------------------")
        for se in page[num2-1:num2+9]:
            print("(", num2 ,")" , se.select('.title a')[0].text)
            num2+=1
        while 1:
            print('上一頁:-  下一頁:+  最前頁:first  最末頁:last  上一層:back  離開:esc')
            put=input("input>>")
            if put == "+" :
                break

            elif put == "-" and num2 > 10 :
                if num2 == length+1:
                    num2=num2-(10+length%10)
                    break
                else:
                    num2-=20
                    break

            elif put == "esc" :
                sys.exit()

            elif put == "back" :
                mainpage(pr)

            elif put == "first" :
                num2=1
                break

            elif put == "last" :
                num2=length-(length%10)+1
                break
            
            if put.isdigit():
                if int(put) in range(num2-10,num2):
                    temp=1
                    for choose in page[0:length-1]:
                        if temp==int(put):
                            prreaddress=pr
                            preaddress=ad
                            address=choose.find('a')['href']
                            #print(address)
                            break
                        temp+=1
                    if address is None:
                        print("Article is not exist")
                        continue
                    articlepage(prreaddress,preaddress,address)
                else:
                    print(put,"is not in this page")
            continue

def mainpage(ad):
    print("------------------------------------------------------------------------")
    address='https://www.ptt.cc'+ad
    res = requests.get(address)
    soup=BeautifulSoup(res.text,"lxml")
    num=1
    page=soup.select('.b-ent')
    length=len(page)
    #print(length)
    while num>0:
        print("------------------------------------------------------------------------")
        for se in page[num-1:num+9]:
            print("<" , num , ">" , se.select('.board-name')[0].text , se.select('.board-class')[0].text , ":" , se.select('.board-title')[0].text)
            num+=1
        #print(num)
        while 1:
            print('上一頁:-  下一頁:+  最前頁:first  最末頁:last  離開:esc')
            put=input("input>>")
            if put == "+" :
                break

            elif put == "-" and num >= 10 :
                if num == length+1:
                    num=num-(10+length%10)
                    break
                else:
                    num-=20
                    break

            elif put == "esc" :
                sys.exit()

            elif put == "first" :
                num=1
                break

            elif put == "last" :
                num=length-(length%10)+1
                break
            
            if put.isdigit():
                if int(put) in range(num-10,num):
                    temp=1
                    for choose in page[0:length-1]:
                        if temp==int(put):
                            preaddress=ad
                            address=choose.find('a')['href']
                            #print(address)
                            break
                        temp+=1
                    changepage(preaddress,address)
                else:
                    print(put,"is not in this page")
            continue

mainpage('/bbs/index.html')