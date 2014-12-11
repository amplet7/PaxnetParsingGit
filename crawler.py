# _*_ coding: euc-kr _*_

'''
Created on 2014. 10. 8.
# _*_ coding: euc-kr _*_
@author: Ricky
'''


from bs4 import BeautifulSoup
import urllib2
import os
import re
from HTMLParser import HTMLParser
import time
import winsound
import traceback
import pdb

##===============태그 제거 코드
#타인의 코드
# by Peter Mortensen from : http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
##=================




def crawler():
    
    try:
        PATH1 = './data/'
        now = time.localtime()
        
        logFileName = './log/log %d.%d.%d %d_%d_%d.txt' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min , now.tm_sec)
        flog = open(logFileName, 'a')
        
        flog.write('\n')
        logStr = "시작 : %d.%d.%d %d:%d:%d\n" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min , now.tm_sec)
        flog.write(logStr)
        
        ferrorInfo = open('./errorInfo.txt', 'a')
        ferrorInfo.write('=================================')
        ferrorInfo.write(logStr)
        ferrorInfo.close()
                    
        url = 'http://paxnet.moneta.co.kr/stock/intro/BBSTotalRank.jsp'
        handle = urllib2.urlopen(url)
        data = handle.read()
        soup = BeautifulSoup(data)
        
        table1 = soup('table', {'bgcolor':"f7f7f7"})
        codeList = re.findall('code=(\d+)',table1[1].encode('euc-kr'))
    
        print codeList
        #============= 한종목만 할 때
        #codeList = []
        #codeList.append('011000')
        
        
        #=================
        logStr = ""
        
        for c in codeList:
            logStr = logStr + c + ' '
        logStr = logStr[:-1] + '\n'
        flog.write(logStr)
        
        totaltime = 0 # 실행하는데 걸린 총 시간
        doneCount = 0 # 파싱한 게시글 갯수
        for code in codeList:
            if not os.path.isdir(PATH1+code): 
                os.mkdir(PATH1+code) 
           
            codeindex = codeList.index(code) + 1
            ymd = 20990101
            
            
            url = 'http://finance.naver.com/item/main.nhn?code=' + code
            
            while 1:
                try:
                    handle = urllib2.urlopen(url)
                except urllib2.URLError as e:
                    logStr = "urllib2.URLError 응답없음 에러 : 네이버 재실행\n"
                    flog.write(logStr)
                    errTraceBack1 = traceback.format_exc()
                    flog.write(errTraceBack1)
                    continue
                break
            
            html2 = handle.read()
            name = re.findall('<title>([\s\S]*?) :', html2)
            name = name[0]
            

            endpageCount = 0 # 끝페이지인지 반복 검사하는 카운터, 끝페이지 아님에도 indexerror로 종목 skip하는 경우 방지 
            t_temp = 0 # 시간 임시
            diff = 0 # 시간 차이
            i=0
            while i < 200:    # 게시판 페이지 탐색
  
                exceptCount = 0     # 한페이지 당 오류 카운터 : 페이지가 넘어가면 0으로 초기화
                pgIndex = i + 1
                
                #======== 종목별 목록 페이지 지정하는 곳
                #if code == '011000':
                #   pgIndex = i+0
                    
                
                #======================================
                
                t1 = time.localtime()
                
                if t_temp:
                    diff = time.mktime(t1) - time.mktime(t_temp)
                    if diff > 22:
                        print'한페이지 당 22초가 넘어서. waiting...'
                        flog.write('한페이지 당 22초가 넘어서. waiting...\n')
                        
                        ferrorInfo = open('./errorInfo.txt', 'a')
                        errtime = time.localtime()
                        ferrorInfo.write('%s %d 22초 이상 걸림. 시간 : %d:%d:%d\n ' % (code, pgIndex, errtime.tm_hour, errtime.tm_min , errtime.tm_sec)) 
                        ferrorInfo.close()
                        
                        time.sleep(5)
                    #diff = diff + 5 # 20초 넘었나 판단할 때는 sleep 시간을 빼고 하고, log 기록은 원상복구

                    totaltime = totaltime + int(diff)
                    print '==이번 페이지 걸린시간 : %d 초 === 여기까지 걸린 시간 : %d 초==== 게시글 : %d\n' % (diff, totaltime, doneCount)
                    flog.write('==이번 페이지 걸린시간 : %d 초 === 여기까지 걸린 시간 : %d 초==== 게시글 : %d\n' % (diff, totaltime, doneCount))
                    
                logStr = "%d 페이지 파싱 시작 시간 : %d.%d.%d %d:%d:%d\n" % (pgIndex, t1.tm_year, t1.tm_mon, t1.tm_mday, t1.tm_hour, t1.tm_min , t1.tm_sec)
                flog.write(logStr)
                t_temp = t1
                
                url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulList.cgi?mode=list&boardid=' +code+'&code=' +code+'&page='+ str(pgIndex)
                while 1:
                    try:
                        handle = urllib2.urlopen(url)
                    except urllib2.URLError as e:
                        logStr = "urllib2.URLError 응답없음 에러 : 이번 페이지 재실행\n"
                        flog.write(logStr)
                        errTraceBack1 = traceback.format_exc()
                        flog.write(errTraceBack1)
                        continue
                    break
                
                data = handle.read()
                soup = BeautifulSoup(data)
                html1 = str(soup)
                
                articList = re.findall('billId=(\d+)', html1)
                print code, articList
          
                if len(articList) <= 4:     # 리스트의 맨 뒷페이지인지 단순에러인지 검사 
                    endpageCount += 1
                    logStr = "len(articList) <= 4 : 뒷페이지 검사 반복 %d회 중... : %s %d\n" % (endpageCount, code, pgIndex)
                    print logStr[:-1]
                    flog.write(logStr)
                    if endpageCount >=3:    
                        logStr = "len(articList) <= 4 : 맨 뒷페이지 : %s %s\n" % (code, pgIndex)
                        flog.write(logStr)
                        endpageCount = 0
                        break    # 다음 종목으로
                    time.sleep(4)
                    continue
                else:
                    endpageCount = 0
                    

                    
                flag = 0
                for article in articList:
                    if os.path.isfile(PATH1+code+'/'+article+'.txt'):
                        pass
                    else:   # 신규 게시글이 있으면
                        flag = 1
                
                # === 한 목록페이지에서 신규 게시글이 한개도 없다면 종목 스킵( 이부분을 주석처리하면 모든페이지 탐색)=====1
                if flag == 0:   
                    logStr = '신규 게시글이 없어 종목 스킵 : %s %d\n' % (code, pgIndex)
                    flog.write(logStr)
                    print logStr
                    #================ 한 종목만 끝까지 크롤할 때, 한 종목 완료시 프로그램 종료
                    #winsound.PlaySound('./HomerWoohoo.wav', winsound.SND_FILENAME)
                    #exit()
                    #================
                    break
                
                #===1
                
                    
                # 신규 게시글이 하나라도 있으면 ======
                for article in articList:
                      
                    flog.close()        # 중간에 프로그램 stop 해도 그 전까지의 기록은 남도록
                    flog = open(logFileName, 'a') # ;;
                     
                    if os.path.isfile(PATH1+code+'/'+article+'.txt'):
                        logStr = 'already exist! : %s %d %s\n' % (code, pgIndex, article )
                        flog.write(logStr)
                        print logStr[:-1]
                        
                    else:
                        #time.sleep(0.1) 
                        # 제목, 날짜, 조회수, 내용, 좋아요, 글쎄요
                        
                        url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=' +code+'&code=' +code+'&&billId='+article

                            
                        while 1:
                            try:
                                handle = urllib2.urlopen(url)
                            except urllib2.URLError as e:
                                logStr = "urllib2.URLError 응답없음 에러 : 이번 게시글 재실행\n"
                                flog.write(logStr)
                                errTraceBack1 = traceback.format_exc()
                                flog.write(errTraceBack1)
                                continue
                            break    
                        
                        
                        try:    
                            html2 = handle.read()
   
                            title1 = re.findall('<h3 id="titlebox"><p>([\s\S]*?)</p></h3>' , html2)  
                            title1 = title1[0]
                            #print title1
                            
                            temp1 = re.findall('<div class="info">([\s\S]*?)</div>',html2)
                            temp1 = re.findall('<span>([\s\S]*?)</span>', temp1[0])
                            date = temp1[0]
                        
                            viewCount = temp1[1]
                            #print code, pgIndex, date, viewCount
                            
                            #temp1 = soup.find('div', {'class':'view'})    # 수프 이용 시 인코딩 실패
                             
                            isMobile = re.findall('<div class="mobile_quote">' , html2)
                            try:
                                if isMobile:   # 팍스넷 앱으로 작성한 글인 경우
                                    temp1 = re.findall(r'<span class="dw_file">([\S\s]*?)<style type="text/css">' , html2) 
                                    temp1 = temp1[0]
                                    temp1 = re.sub('<br>', '\n', temp1)
                                    temp1 = re.sub('&#160;', ' ', temp1)
                                    temp1 = re.sub('</br>', '', temp1)
                                    temp1 = re.sub('</p>', '\n', temp1)
                                    content = strip_tags(temp1)  
                                    #print content
                                else:   # 컴퓨터로 작성한 글인 경우
                                    temp1 = re.findall(r'<span class="dw_file">([\S\s]*?)<div class="view_inlist">' , html2)
                                    temp1 = temp1[0]
                                    temp1 = re.sub('&#160;', ' ', temp1)
                                    temp1 = re.sub('</p>', '\n', temp1)
                                    temp1 = re.sub('<br>', '\n', temp1)
                                    temp1 = re.sub('</br>', '', temp1)
                                    
                                    content = strip_tags(temp1)  
                                    #print content
                                
                            except UnicodeDecodeError, e:   #content = strip_tags(temp1) 에서 유니코드 디코드 에러
                                print e
                                errTraceBack1 = traceback.format_exc()
                                logStr = "UnicodeDecodeError : %s %s %d %s %s\n" % (e, code, pgIndex, article, date)
                                flog.write(logStr)
                                flog.write(errTraceBack1)
                                
                                ferrorInfo = open('./errorInfo.txt', 'a')
                                errtime = time.localtime()
                                ferrorInfo.write('%s %d %s UnicodeDecodeError 시간 : %d:%d:%d\n ' % (code, pgIndex, article, errtime.tm_hour, errtime.tm_min , errtime.tm_sec)) 
                                ferrorInfo.close()
                                content = temp1
                                
                            temp1 = re.findall(r'<em id="rcmCnt">(\d+?)</em>' , html2)
                            good = temp1[0]    #좋아요
                            temp1 = re.findall(r'<em id="oppCnt">(\d+?)</em>' , html2)
                            bad = temp1[0]     #글쎄요
                            #print good, bad
                            
                            fout1 = open(PATH1+code+'/'+article+'.txt', 'w')
                            # 제목, 날짜, 조회수, 내용, 좋아요, 글쎄요
                            str1 = "%s\n%s\n%s\n%s\n%s\n%s\n%s" % (name, date, viewCount, title1, good, bad, content)
                            fout1.write(str1)
                            fout1.close()
                            
                            doneCount += 1
                            logStr = "file write done! : %s %d %s %s %s %s\n" % (name, codeindex, code, pgIndex, article, date)
                            flog.write(logStr)
                            print logStr[:-1]
                            
                            ymd = date.split()   #year month day
                            ymd = ymd[0]
                            ymd = ymd.replace('/', '')
                            ymd = int(ymd)
                        except IndexError as e: #IndexError: list index out of range
                            exceptCount = exceptCount + 1
                            
                            print e
                            errTraceBack1 = traceback.format_exc()
                            if 'date' in locals():
                                logStr = "IndexError : %s %s %d %s %s\n" % (e, code, pgIndex, article, date)
                            else:
                                logStr = "IndexError : %s %s %d %s\n" % (e, code, pgIndex, article)
                            
                            flog.write(logStr)
                            flog.write(errTraceBack1)
                            
                            fhtml = open('./html2.txt', 'a')
                            fhtml.write('==========================start======')
                            fhtml.write(logStr)
                            fhtml.write(html2)
                            fhtml.write('\n=================end======= \n\n\n')
                            fhtml.close()
                            
                            # 에러 정보 출력
                            ferrorInfo = open('./errorInfo.txt', 'a')
                            errtime = time.localtime()
                            ferrorInfo.write('%s %d %s index에러 시간 : %d:%d:%d\n ' % (code, pgIndex, article, errtime.tm_hour, errtime.tm_min , errtime.tm_sec)) 
                            ferrorInfo.close()

             
                    if ymd < 20130101:  # 날짜가 지정일 이전이면 수집하지 않음
                        break
                    
                if ymd < 20130101:
                    logStr = "ymd < 20130101 : %s %s %d\n" % (code, pgIndex, ymd)
                    flog.write(logStr)
                    break
                
                if exceptCount>= 2: # 한 페이지 당 에러난 게시글이 X개이상이면 : 보통 드물게 특정 게시물은 영구적으로 에러발생. SO, 1개는 skip
                    logStr = "한 페이지 당 에러난 게시글이 2개이상, waiting 후 재실행\n"
                    flog.write(logStr)
                    print 'waiting... sleep line222'
                    time.sleep(3)
                    i -= 1
                    #break # 게시글 리스트 break
                
                i += 1   #while 페이지
                 
                
                        
    
        winsound.PlaySound('./HomerWoohoo.wav', winsound.SND_FILENAME)    
        flog.close()
        
        
  

    except IndexError as e: #IndexError: list index out of range
        errTraceBack2 = traceback.format_exc()
        print e
        winsound.PlaySound('./Homer - Doh.wav', winsound.SND_FILENAME)
        logStr = "IndexError : %s\n" % (e)
        flog.write(logStr)
        flog.write(errTraceBack2)
        flog.close()
      

if __name__=='__main__':
    
    crawler()
    
    #os.system('shutdown -f -s -t 10')
    
    
       
                
    #테스트 URL
    #컴:파일첨부#url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=054670&code=054670&&billId=141266929225381'
    #컴:이미지#url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=054670&code=054670&&billId=141266939992871'
    
    #모바일:제목에 엔터 들어간 게시글http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=032790&code=032790&&page=43&&billId=140055656896592
    #===============
    #141291378466081
    # html strip 에러 : http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=002700&code=002700&&page=57&&billId=140685539150571
  
    '''
    url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=150840&code=150840&&billId=140175315017291'
    handle = urllib2.urlopen(url)
    html2 = handle.read()

        
    title1 = re.findall('<h3 id="titlebox"><p>([\s\S]*?)</p></h3>' , html2)  
    
    title1 = title1[0]
    #print title1
    
    
    temp1 = re.findall('<div class="info">([\s\S]*?)</div>',html2)
    temp1 = re.findall('<span>([\s\S]*?)</span>', temp1[0])
    date = temp1[0]

    viewCount = temp1[1]
    #print code, pgIndex, date, viewCount
    

                    
                    

    isMobile = re.findall('<div class="mobile_quote">' , html2)
    if isMobile:   # 팍스넷 앱으로 작성한 글인 경우
        temp1 = re.findall(r'<span class="dw_file">([\S\s]*?)<style type="text/css">' , html2) 
        temp1 = temp1[0]
        temp1 = re.sub('<br>', '\n', temp1)
        temp1 = re.sub('&#160;', ' ', temp1)
        temp1 = re.sub('</br>', '', temp1)
        temp1 = re.sub('</p>', '\n', temp1)
        content = strip_tags(temp1)  
        print content
    else:   # 컴퓨터로 작성한 글인 경우
        temp1 = re.findall(r'<span class="dw_file">([\S\s]*?)<div class="view_inlist">' , html2)
        temp1 = temp1[0]
        temp1 = re.sub('&#160;', ' ', temp1)
        temp1 = re.sub('</p>', '\n', temp1)
        temp1 = re.sub('<br>', '\n', temp1)
        temp1 = re.sub('</br>', '', temp1)
        #pdb.set_trace()
        content = temp1 
        print content
        
    temp1 = re.findall(r'<em id="rcmCnt">(\d+?)</em>' , html2)
    good = temp1[0]    #좋아요
    temp1 = re.findall(r'<em id="oppCnt">(\d+?)</em>' , html2)
    bad = temp1[0]     #글쎄요
    print good, bad

 
    '''
    
    