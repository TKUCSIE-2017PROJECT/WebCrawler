# -*- coding: utf-8 -*-
#d_card_api_ver1.8.py
#1.3breakdate的問題改為breakdate2,3;仍然存在沒有breakdate的問題,待新增:日期搜索範圍,range_From_To_
#1.4新增搜尋功能,搜尋所有版,可改為搜尋指定版
#1.7新增以多個關鍵字各自搜尋文章的功能
#1.8新增資料夾內所有JSON檔的合併與刪除重覆文章的功能
#1.9新增更新json檔內所有文章的留言的功能
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import datetime
import os

def findforum():
    url='https://www.dcard.tw/_api/forums'
    res= requests.get(url)
    data=[]
    data=res.json()
    max_num=len(data)
    print("\nDcard可選擇的看板如下:\n")
    number=0
    for i in range(0,max_num):
        number+=1
        if(number==199 or number==203 or number==207 or number==212):
            print("\n"+str(number)+str(data[i]['name']),end=' ')
        else:
            print(number,data[i]['name'],end=' ')
        if (number%4==0 and number!=212):
            print("\n")
    print("\n")
    while True:
        forum_num=input("請輸入你想要搜尋的看板編號(如:12 或 exit 離開):")
        if forum_num=="exit":
            return "exit"
            break
        if int(forum_num)>=1 and int(forum_num)<=max_num:
            forum_num=int(int(forum_num)-1)
            search_name=data[forum_num]['name']
            forum_name=data[forum_num]['alias']
            print("\n你所輸入的編號是"+str(forum_num+1)+":"+str(search_name)+str(forum_name)+"(版)\n")
            url="https://www.dcard.tw/_api/forums/"+forum_name+"/posts"
            return url
            break
        else:
            print("\nDcard並不存在看板編號:"+str(forum_num)+"，請在下列重新輸入!!!\n")

def newestpoststop100(url):
    limit=100
    url=url+"?limit="+str(limit)
    print("url=",url)
    res= requests.get(url)
    data=[]
    data=res.json()
    eachdata=[]
    print("eachdata type is",type(eachdata))
    print(type(data))
    print(type(data[0]))
    for i in range(0,limit):
        eachpostdate=data[i]['createdAt'][0:10]
        if eachpostdate==breakdate or eachpostdate==breakdate2 or eachpostdate==breakdate3:
            break
        else: 
            temp_data=[]
            temp_data=data[i]
            eachdata.append(temp_data)
    return eachdata

def newestpostsafter100():
    print("num_of_articles=",num_of_articles)
    last_post_id=data[num_of_articles-1]['id']
    print(last_post_id)
    limit=100
    new_url=url+"?limit="+str(limit)+"&before="+str(last_post_id)
    print(new_url)
    new_res= requests.get(new_url)
    new_data=[]
    new_data=new_res.json()
    eachdata=[]
    for i in range(0,limit):
        eachpostdate=new_data[i]['createdAt'][0:10]
        if eachpostdate==breakdate or eachpostdate==breakdate2 or eachpostdate==breakdate3:
            break
        else: 
            temp_data=[]
            temp_data=new_data[i]
            eachdata.append(temp_data)
    return eachdata



def dcard_funtion4(data):
    max_num=len(data)
    #print(max_num)
    #count_number=1
    #print(type(count_number))
    #while(count_number!=total_number):
    #jsonfile_name_list=[]
    #temp_filename=[]
    #temp_str=" "
    '''for z in range(count_number,int(total_number)):
        temp=count_number+1
        #temp_str=input("請輸入第"+str(temp)+"個JSON檔案的名稱(如:abc):")
        temp_filename=input("請輸入第"+str(temp)+"個JSON檔案的名稱(如:abc):")
        if temp==2:
            jsonfile_name_list[0]=temp_filename
        else:
            jsonfile_name_list.append(temp_filename)
    '''
    '''
    for x in range(count_number,int(total_number)):
       
        with open(jsonfile_name_list[x-1]+".json", 'r',encoding='utf-8') as fp:
            data2 = json.load(fp)
        max_num2=len(data2)
        '''
    controller=1
    repeated_article_id=[]
    while controller!=(int(total_number)):
        print("正在合併"+file_name_list[controller]+"的文章與刪除重覆文章")
        with open(file_name_list[controller], 'r',encoding='utf-8') as fp:
            data2 = json.load(fp)
        max_num2=len(data2)
        for i in range(0,max_num2):
            max_num=len(data)
            count=0
            for j in range(0,max_num):
                if data2[i]['id']==data[j]['id']:
                    #print(data2[i]['id'])
                    repeated_article_id.append(data2[i]['id'])
                    break
                else:
                    count=count+1
                    if count==max_num:
                        data.append(data2[i])
                        break    
        controller=controller+1
        if controller==(int(total_number)):
            repeated_article_num=len(repeated_article_id)
            print("重覆文章的數目為"+str(repeated_article_num)+",重覆文章的ID如下:")
            #print(type(repeated_article_id))
            for repeatedarticleid in repeated_article_id:
                print(repeatedarticleid)
    return data
    
    
    
    '''
    json_file_name2=input("請輸入第2個JSON檔案的名稱(如:abc):")
    with open(json_file_name2+".json", 'r',encoding='utf-8') as fp:
        data2 = json.load(fp)
    max_num2=len(data2)
    for i in range(0,max_num2):
        max_num=len(data)
        count=0
        for j in range(0,max_num):
            if data2[i]['id']==data[j]['id']:
                print(data2[i]['id'])
                break
            else:
                count=count+1
                if count==max_num:
                    data.append(data2[i])
                    break    
    
    return data    
    '''
def dcard_funtion5():
    max_num=len(data)
    print(max_num)
    done_num=0
    #error_dict={}
    #error_list=[]
    for i in range(0,max_num):
        try:
            post_id=data[i]['id']
            url="https://www.dcard.tw/_api/posts/"+str(post_id)
            res=requests.get(url)
            post_data=[]
            post_data=res.json()
            if(len(post_data)!=3):
                data[i]['excerpt']=post_data['content'].replace('\n',' ')
                done_num+=1
                print(done_num)
            else:
                done_num+=1
                print(done_num)
        except:
            while True:
                post_id=data[i]['id']
                url="https://www.dcard.tw/_api/posts/"+str(post_id)
                res=requests.get(url)
                post_data=[]
                post_data=res.json()
                if data[i]['id']==post_data['id'] or (len(post_data)!=3):
                    data[i]['excerpt']=post_data['content'].replace('\n',' ')
                    done_num+=1
                    print(done_num)
                    break
                elif (len(post_data)==3):
                    done_num+=1
                    print(done_num)
                    break
    return data

def dcard_funtion6():
    print(len(data))
    for i in range (0,len(data)):
        try:
            post_id=data[i]['id']
            percentage=(i/len(data)*100)
            print("已完成:"+str(round(percentage))+"%,正在處理第"+str(i)+"筆資料:",post_id)

            #post_id="227958333"
            url="https://www.dcard.tw/_api/posts/"+str(post_id)+"/comments?limit=100"
            res=requests.get(url)
            comment_data=[]
            comment_data=res.json()
            comment_data_num=len(comment_data)
            #print(comment_data_num) 不要刪
            if comment_data_num!=0:
                if comment_data_num==100:
                    loop=0
                    after_floor=comment_data_num #after_floor=100 初始值
                    while loop==0:
                        #print("loop")
                        url2="https://www.dcard.tw/_api/posts/"+str(post_id)+"/comments?limit=100&&after="+str(after_floor)
                        res2=requests.get(url2)
                        after_comment_data=[]
                        after_comment_data=res2.json()
                        after_comment_data_num=len(after_comment_data)
                        #print(after_comment_data_num)
                        for i in range(0,after_comment_data_num):
                            comment_data.append(after_comment_data[i])
                        if after_comment_data_num<100:
                            loop=1
                        elif after_comment_data_num==100:
                            after_floor=after_floor+100
                    data[i]["comments"]=comment_data

                    #https://www.dcard.tw/_api/posts/227956818/comments?limit=100&after=100
                elif comment_data_num<100:
                    #json_file_name=post_id+".json"
                    data[i]["comments"]=comment_data
            elif comment_data_num==0:
                print("Comment內容為空")
        except:
                while True:
                    post_id=data[i]['id']
                    percentage=(i/len(data)*100)
                    print("已完成:"+str(round(percentage))+"%,正在處理第"+str(i)+"筆資料:",post_id)

                    #post_id="227958333"
                    url="https://www.dcard.tw/_api/posts/"+str(post_id)+"/comments?limit=100"
                    res=requests.get(url)
                    comment_data=[]
                    comment_data=res.json()
                    comment_data_num=len(comment_data)
                    #print(comment_data_num) 不要刪
                    if comment_data_num!=0:
                        if comment_data_num==100:
                            loop=0
                            after_floor=comment_data_num #after_floor=100 初始值
                            while loop==0:
                                #print("loop")
                                url2="https://www.dcard.tw/_api/posts/"+str(post_id)+"/comments?limit=100&&after="+str(after_floor)
                                res2=requests.get(url2)
                                after_comment_data=[]
                                after_comment_data=res2.json()
                                after_comment_data_num=len(after_comment_data)
                                #print(after_comment_data_num)
                                for i in range(0,after_comment_data_num):
                                    comment_data.append(after_comment_data[i])
                                if after_comment_data_num<100:
                                    loop=1
                                elif after_comment_data_num==100:
                                    after_floor=after_floor+100
                            data[i]["comments"]=comment_data
                            break
                            #https://www.dcard.tw/_api/posts/227956818/comments?limit=100&after=100
                        elif comment_data_num<100:
                            #json_file_name=post_id+".json"
                            data[i]["comments"]=comment_data
                            break
                    elif comment_data_num==0:
                        #print("Comment內容為空")
                        break
    return data

def keyword_100():
    url='https://www.dcard.tw/_api/search/posts?query="'+search_keyword+'"&limit=100'
    res=requests.get(url)
    data=[]
    data=res.json()
    print("已完成:",round(100/1000*100),"%")
    return data

def keyword_after_100(i):
    i=100*i
    print("已完成:",round((i+100)/1100*100),"%")    
    url='https://www.dcard.tw/_api/search/posts?query="'+search_keyword+'"&limit=100'+"&offset="+str(i)
    res= requests.get(url)
    data2=[]
    data2=res.json()
    return data2

        #print(data[i]['id'])

if __name__=='__main__':
    when= datetime.datetime.now()
    #print ("%s_%s_%s.%s.%s.%s" %(when.day, when.month, when.year,when.hour,when.minute,when.second) )
    #time="%s_%s_%s.%s.%s.%s" %(when.day, when.month, when.year,when.hour,when.minute,when.second) 
    #print(time)
    
    while True:        
        print("==================================")
        print("\tDcard API 之功能列表")
        print("==================================")
        print("1) 選擇指定看板，抓最新文章(by日期)")
        print("2) 使用單個或多個關鍵字搜尋文章")
        print("3) 抓指定文章(by post_id)")
        print("4) 合併json檔的所有文章並刪除重覆文章")
        print("5) 選擇json檔案，更新其完整的內文content")
        print("6) 選擇json檔案，更新其完整的留言comment")
        print("0) 離開本程式")
        choose=input("\n請輸入功能編號(0-6):")
        print("你選擇的功能為",choose)

        if choose=="1":
            url=findforum()
            if url=="exit":     
                print("\n你已選擇exit,回到主功能列表\n")
            else:
                time="%s_%s_%s.%s.%s.%s" %(when.day, when.month, when.year,when.hour,when.minute,when.second) 
                #print(time)
                print(url)
                data=[]
                breakdate=input("\n若要找2017年7月1號之後的文章，則輸入其的前一天:2017-06-30\n請輸入日期:")
                print(breakdate[8:10])
                pre_date=breakdate[0:8]
                print(pre_date)
                temp_data=breakdate[8:10]
                print(type(temp_data))
                num=0
                breakdate2='0'
                breakdate3='0'
                if(temp_data!='01'):
                    num=int(temp_data)-1
                    print('num=',num)
                    breakdate2=str(num)
                    if breakdate2=='1':
                        breakdate2='01'
                    elif breakdate2=='2':
                        breakdate2=='02'
                    elif breakdate2=='3':
                        breakdate2=='03'
                    elif breakdate2=='4':
                        breakdate2=='04'
                    elif breakdate2=='5':
                        breakdate2=='05'
                    elif breakdate2=='6':
                        breakdate2=='06'
                    elif breakdate2=='7':
                        breakdate2=='07'
                    elif breakdate2=='8':
                        breakdate2=='08'
                    elif breakdate2=='9':
                        breakdate2=='09'    
                    print(breakdate2)
                    print(type(breakdate2))
                    breakdate2=pre_date+breakdate2
                    print(breakdate2)
                    if breakdate2[8:10]!='01':
                        pre_date=breakdate2[0:8]
                        temp_data=breakdate2[8:10]
                        num=int(temp_data)-1
                        breakdate3=str(num)
                        if breakdate3=='1':
                            breakdate3='01'
                        elif breakdate3=='2':
                            breakdate3=='02'
                        elif breakdate3=='3':
                            breakdate3=='03'
                        elif breakdate3=='4':
                            breakdate3=='04'
                        elif breakdate3=='5':
                            breakdate3=='05'
                        elif breakdate3=='6':
                            breakdate3=='06'
                        elif breakdate3=='7':
                            breakdate3=='07'
                        elif breakdate3=='8':
                            breakdate3=='08'
                        elif breakdate3=='9':
                            breakdate3=='09'
                        breakdate3=pre_date+breakdate3
                        print(breakdate3)
                data=newestpoststop100(url)
                while True:
                        num_of_articles=len(data)
                        if int(num_of_articles)%100==0:
                            print("num_of_articles="+str(num_of_articles))
                            print("已抓TOP"+str(num_of_articles))
                            print("\n")
                            #print("請繼續執行函數")
                            data=data+newestpostsafter100()
                        else:
                            print("DONE,獲得文章數量為",num_of_articles)
                            print("\n")
                            break
                forum_name=data[0]['forumAlias']
                with open(str(forum_name)+"FromDcard_"+str(num_of_articles)+"_"+time+".json", 'w',encoding='utf-8') as fp:
                        json.dump(data,fp,sort_keys=False,indent=10,ensure_ascii=False)
        
        elif choose=='2':
            multi_keyword_choose=input("使用多個關鍵字各別搜尋文章?(Y/N):")
            if multi_keyword_choose=='Y':
                multi_keyword_num=input("請輸入關鍵字的數目:")
                keyword_list=[]
                for i in range(0,int(multi_keyword_num)):
                    temp_keyword=input("請輸入第"+str(i+1)+"個關鍵字:")    
                    keyword_list.insert(i,temp_keyword)
                print("已完成所有關鍵字的輸入")
                print("所輸入的關鍵字為如下:")
                print(keyword_list)

                for j in range(0,int(multi_keyword_num)):
                    search_keyword=keyword_list[j]
                    data=keyword_100()
                    for i in range(1,11):
                        data2=keyword_after_100(i)
                        data=data+data2
                    max_num=len(data)
                    print("DONE,共有"+str(max_num)+"筆有關:"+search_keyword+"的資料")
                    with open("dcard_"+search_keyword+"_"+str(max_num)+".json", 'w',encoding='utf-8') as fp:
                        json.dump(data,fp,sort_keys=False,indent=10,ensure_ascii=False)

            elif multi_keyword_choose=='N': 
                search_keyword=input("請輸入要搜尋的關鍵字:")
                data=keyword_100()
                #print(data)
                for i in range(1,11):
                    data2=keyword_after_100(i)
                    data=data+data2
                #for j in range(0,1100):
                #   getcontent(j)
                max_num=len(data)
                #print("總共抓到共",max_num,"筆的資料")
                #for j in range(0,max_num):
                #    print(data[j]['id'])
                print("DONE,共有"+str(max_num)+"筆有關:"+search_keyword+"的資料")
                with open("dcard_"+search_keyword+"_"+str(max_num)+".json", 'w',encoding='utf-8') as fp:
                        json.dump(data,fp,sort_keys=False,indent=10,ensure_ascii=False)
                        
        elif choose=='3':
            post_id=input("請輸入文章的編號id:")
            url="https://www.dcard.tw/_api/posts/"+str(post_id)
            res=requests.get(url)
            post_data=[]
            post_data=res.json()
            with open(str(post_id)+".json", 'w',encoding='utf-8') as fp:
                json.dump(post_data,fp,sort_keys=False,indent=10,ensure_ascii=False)
            print("已完成文章ID:"+str(post_id)+"的json檔的輸出")

        elif choose=='4':
            inputbyfile=input("是否合併所有文章與刪除重覆文章在同一資料夾的所有JSON檔?(Y/N):")
            if  inputbyfile=='Y':
                YorN=input("預設JSON檔資料夾為(./JSON),是否需要修改?(Y/N):")
                if YorN=='Y':
                    dirname=input("請輸入JSON檔資料夾的路徑:")
                elif YorN=='N':
                    dirname="json"
                file_name_list=[]
                for filename in os.listdir(dirname):
                    #print(os.path.join(dirname, filename))
                    file_name_list.append(os.path.join(dirname, filename))
                print(file_name_list)
                total_number=len(file_name_list)
                #print(total_number)
                with open(file_name_list[0], 'r',encoding='utf-8') as fp:
                    data = json.load(fp)
                alldata=dcard_funtion4(data)

                print("合併與刪除文章已經完成")
                output_json_name=input("請輸入即將輸出的JSON檔案名稱(如:cba):")
                max_num3=len(alldata)
                with open(output_json_name+"_"+str(max_num3)+".json", 'w',encoding='utf-8') as fp:
                    json.dump(alldata,fp,sort_keys=False,indent=10,ensure_ascii=False)
                #print(type(data))
                print("最終data的資料大小為",len(data),"筆")
                print("\nDONE,已完成輸出JSON檔案:"+str(output_json_name)+"_"+str(max_num3)+".json\n")
            
            elif inputbyfile=='N':
                total_number=input("請輸入要合併所有文章與刪除重覆文章的JSON數目(如:5):")
                file_name_list=[]
                for i in range(0,int(total_number)):
                    temp_num=int(i)+1
                    #print(type(temp_num))
                    temp_str=(str(temp_num))
                    question="請輸入第"+temp_str+"個JSON檔名稱(如:abc.json):"
                    temp_str2=input(question)
                    file_name_list.append(temp_str2)

                #json_file_name=input("請輸入第1個JSON檔案的名稱(如:abc.json):")
                with open(file_name_list[0], 'r',encoding='utf-8') as fp:
                    data = json.load(fp)
                alldata=dcard_funtion4(data)
                print("合併與刪除文章已經完成")
                output_json_name=input("請輸入即將輸出的JSON檔案名稱(如:cba):")
                max_num3=len(alldata)
                with open(output_json_name+"_"+str(max_num3)+".json", 'w',encoding='utf-8') as fp:
                    json.dump(alldata,fp,sort_keys=False,indent=10,ensure_ascii=False)
                #print(type(data))
                print("最終data的資料大小為",len(data),"筆")
                print("\nDONE,已完成輸出JSON檔案:"+str(output_json_name)+"_"+str(max_num3)+".json\n")

        elif choose=='5':
            #done_num=0
            json_file_name=input("請輸入JSON檔案名稱(如:abc.json):")
            with open(json_file_name, 'r',encoding='utf-8') as fp:
                data = json.load(fp)
            data=dcard_funtion5()
            with open(json_file_name, 'w',encoding='utf-8') as fp:
                json.dump(data,fp,sort_keys=False,indent=10,ensure_ascii=False)
            #print(type(data))
            print("\nDONE,已完成JSON檔案:"+str(json_file_name)+"的更改\n")
            #print(data)
        
        elif choose=='6':
            #post_id="227958333" #Comment內容為空 :[]
            json_file_name=input("請輸入json檔的名稱(abc.json):")
            with open(json_file_name, 'r',encoding='utf-8') as fp:
                data = json.load(fp)
            data=dcard_funtion6()
            json_file_name=input("請輸入輸出的JSON檔名(cba.json):")
            with open(json_file_name, 'w',encoding='utf-8') as fp:
                json.dump(data,fp,sort_keys=False,indent=10,ensure_ascii=False)

        elif choose=='0':
            break
        else:
            print("\n輸入錯誤，請重新輸入!!\n")
            continue
    print("\n你已選擇離開本程式,再見~")

