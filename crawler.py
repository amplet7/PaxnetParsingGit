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

##===============�±� ���� �ڵ�
#Ÿ���� �ڵ�
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
        logStr = "���� : %d.%d.%d %d:%d:%d\n" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min , now.tm_sec)
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
        #============= ������ �� ��
        #codeList = []
        #codeList.append('011000')
        
        
        #=================
        logStr = ""
        
        for c in codeList:
            logStr = logStr + c + ' '
        logStr = logStr[:-1] + '\n'
        flog.write(logStr)
        
        totaltime = 0 # �����ϴµ� �ɸ� �� �ð�
        doneCount = 0 # �Ľ��� �Խñ� ����
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
                    logStr = "urllib2.URLError ������� ���� : ���̹� �����\n"
                    flog.write(logStr)
                    errTraceBack1 = traceback.format_exc()
                    flog.write(errTraceBack1)
                    continue
                break
            
            html2 = handle.read()
            name = re.findall('<title>([\s\S]*?) :', html2)
            name = name[0]
            

            endpageCount = 0 # ������������ �ݺ� �˻��ϴ� ī����, �������� �ƴԿ��� indexerror�� ���� skip�ϴ� ��� ���� 
            t_temp = 0 # �ð� �ӽ�
            diff = 0 # �ð� ����
            i=0
            while i < 200:    # �Խ��� ������ Ž��
  
                exceptCount = 0     # �������� �� ���� ī���� : �������� �Ѿ�� 0���� �ʱ�ȭ
                pgIndex = i + 1
                
                #======== ���� ��� ������ �����ϴ� ��
                #if code == '011000':
                #   pgIndex = i+0
                    
                
                #======================================
                
                t1 = time.localtime()
                
                if t_temp:
                    diff = time.mktime(t1) - time.mktime(t_temp)
                    if diff > 22:
                        print'�������� �� 22�ʰ� �Ѿ. waiting...'
                        flog.write('�������� �� 22�ʰ� �Ѿ. waiting...\n')
                        
                        ferrorInfo = open('./errorInfo.txt', 'a')
                        errtime = time.localtime()
                        ferrorInfo.write('%s %d 22�� �̻� �ɸ�. �ð� : %d:%d:%d\n ' % (code, pgIndex, errtime.tm_hour, errtime.tm_min , errtime.tm_sec)) 
                        ferrorInfo.close()
                        
                        time.sleep(5)
                    #diff = diff + 5 # 20�� �Ѿ��� �Ǵ��� ���� sleep �ð��� ���� �ϰ�, log ����� ���󺹱�

                    totaltime = totaltime + int(diff)
                    print '==�̹� ������ �ɸ��ð� : %d �� === ������� �ɸ� �ð� : %d ��==== �Խñ� : %d\n' % (diff, totaltime, doneCount)
                    flog.write('==�̹� ������ �ɸ��ð� : %d �� === ������� �ɸ� �ð� : %d ��==== �Խñ� : %d\n' % (diff, totaltime, doneCount))
                    
                logStr = "%d ������ �Ľ� ���� �ð� : %d.%d.%d %d:%d:%d\n" % (pgIndex, t1.tm_year, t1.tm_mon, t1.tm_mday, t1.tm_hour, t1.tm_min , t1.tm_sec)
                flog.write(logStr)
                t_temp = t1
                
                url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulList.cgi?mode=list&boardid=' +code+'&code=' +code+'&page='+ str(pgIndex)
                while 1:
                    try:
                        handle = urllib2.urlopen(url)
                    except urllib2.URLError as e:
                        logStr = "urllib2.URLError ������� ���� : �̹� ������ �����\n"
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
          
                if len(articList) <= 4:     # ����Ʈ�� �� ������������ �ܼ��������� �˻� 
                    endpageCount += 1
                    logStr = "len(articList) <= 4 : �������� �˻� �ݺ� %dȸ ��... : %s %d\n" % (endpageCount, code, pgIndex)
                    print logStr[:-1]
                    flog.write(logStr)
                    if endpageCount >=3:    
                        logStr = "len(articList) <= 4 : �� �������� : %s %s\n" % (code, pgIndex)
                        flog.write(logStr)
                        endpageCount = 0
                        break    # ���� ��������
                    time.sleep(4)
                    continue
                else:
                    endpageCount = 0
                    

                    
                flag = 0
                for article in articList:
                    if os.path.isfile(PATH1+code+'/'+article+'.txt'):
                        pass
                    else:   # �ű� �Խñ��� ������
                        flag = 1
                
                # === �� ������������� �ű� �Խñ��� �Ѱ��� ���ٸ� ���� ��ŵ( �̺κ��� �ּ�ó���ϸ� ��������� Ž��)=====1
                if flag == 0:   
                    logStr = '�ű� �Խñ��� ���� ���� ��ŵ : %s %d\n' % (code, pgIndex)
                    flog.write(logStr)
                    print logStr
                    #================ �� ���� ������ ũ���� ��, �� ���� �Ϸ�� ���α׷� ����
                    #winsound.PlaySound('./HomerWoohoo.wav', winsound.SND_FILENAME)
                    #exit()
                    #================
                    break
                
                #===1
                
                    
                # �ű� �Խñ��� �ϳ��� ������ ======
                for article in articList:
                      
                    flog.close()        # �߰��� ���α׷� stop �ص� �� �������� ����� ������
                    flog = open(logFileName, 'a') # ;;
                     
                    if os.path.isfile(PATH1+code+'/'+article+'.txt'):
                        logStr = 'already exist! : %s %d %s\n' % (code, pgIndex, article )
                        flog.write(logStr)
                        print logStr[:-1]
                        
                    else:
                        #time.sleep(0.1) 
                        # ����, ��¥, ��ȸ��, ����, ���ƿ�, �۽��
                        
                        url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=' +code+'&code=' +code+'&&billId='+article

                            
                        while 1:
                            try:
                                handle = urllib2.urlopen(url)
                            except urllib2.URLError as e:
                                logStr = "urllib2.URLError ������� ���� : �̹� �Խñ� �����\n"
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
                            
                            #temp1 = soup.find('div', {'class':'view'})    # ���� �̿� �� ���ڵ� ����
                             
                            isMobile = re.findall('<div class="mobile_quote">' , html2)
                            try:
                                if isMobile:   # �Ž��� ������ �ۼ��� ���� ���
                                    temp1 = re.findall(r'<span class="dw_file">([\S\s]*?)<style type="text/css">' , html2) 
                                    temp1 = temp1[0]
                                    temp1 = re.sub('<br>', '\n', temp1)
                                    temp1 = re.sub('&#160;', ' ', temp1)
                                    temp1 = re.sub('</br>', '', temp1)
                                    temp1 = re.sub('</p>', '\n', temp1)
                                    content = strip_tags(temp1)  
                                    #print content
                                else:   # ��ǻ�ͷ� �ۼ��� ���� ���
                                    temp1 = re.findall(r'<span class="dw_file">([\S\s]*?)<div class="view_inlist">' , html2)
                                    temp1 = temp1[0]
                                    temp1 = re.sub('&#160;', ' ', temp1)
                                    temp1 = re.sub('</p>', '\n', temp1)
                                    temp1 = re.sub('<br>', '\n', temp1)
                                    temp1 = re.sub('</br>', '', temp1)
                                    
                                    content = strip_tags(temp1)  
                                    #print content
                                
                            except UnicodeDecodeError, e:   #content = strip_tags(temp1) ���� �����ڵ� ���ڵ� ����
                                print e
                                errTraceBack1 = traceback.format_exc()
                                logStr = "UnicodeDecodeError : %s %s %d %s %s\n" % (e, code, pgIndex, article, date)
                                flog.write(logStr)
                                flog.write(errTraceBack1)
                                
                                ferrorInfo = open('./errorInfo.txt', 'a')
                                errtime = time.localtime()
                                ferrorInfo.write('%s %d %s UnicodeDecodeError �ð� : %d:%d:%d\n ' % (code, pgIndex, article, errtime.tm_hour, errtime.tm_min , errtime.tm_sec)) 
                                ferrorInfo.close()
                                content = temp1
                                
                            temp1 = re.findall(r'<em id="rcmCnt">(\d+?)</em>' , html2)
                            good = temp1[0]    #���ƿ�
                            temp1 = re.findall(r'<em id="oppCnt">(\d+?)</em>' , html2)
                            bad = temp1[0]     #�۽��
                            #print good, bad
                            
                            fout1 = open(PATH1+code+'/'+article+'.txt', 'w')
                            # ����, ��¥, ��ȸ��, ����, ���ƿ�, �۽��
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
                            
                            # ���� ���� ���
                            ferrorInfo = open('./errorInfo.txt', 'a')
                            errtime = time.localtime()
                            ferrorInfo.write('%s %d %s index���� �ð� : %d:%d:%d\n ' % (code, pgIndex, article, errtime.tm_hour, errtime.tm_min , errtime.tm_sec)) 
                            ferrorInfo.close()

             
                    if ymd < 20130101:  # ��¥�� ������ �����̸� �������� ����
                        break
                    
                if ymd < 20130101:
                    logStr = "ymd < 20130101 : %s %s %d\n" % (code, pgIndex, ymd)
                    flog.write(logStr)
                    break
                
                if exceptCount>= 2: # �� ������ �� ������ �Խñ��� X���̻��̸� : ���� �幰�� Ư�� �Խù��� ���������� �����߻�. SO, 1���� skip
                    logStr = "�� ������ �� ������ �Խñ��� 2���̻�, waiting �� �����\n"
                    flog.write(logStr)
                    print 'waiting... sleep line222'
                    time.sleep(3)
                    i -= 1
                    #break # �Խñ� ����Ʈ break
                
                i += 1   #while ������
                 
                
                        
    
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
    
    
       
                
    #�׽�Ʈ URL
    #��:����÷��#url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=054670&code=054670&&billId=141266929225381'
    #��:�̹���#url = 'http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=054670&code=054670&&billId=141266939992871'
    
    #�����:���� ���� �� �Խñ�http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=032790&code=032790&&page=43&&billId=140055656896592
    #===============
    #141291378466081
    # html strip ���� : http://board.moneta.co.kr/cgi-bin/paxBulletin/bulView.cgi?mode=list&boardid=002700&code=002700&&page=57&&billId=140685539150571
  
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
    if isMobile:   # �Ž��� ������ �ۼ��� ���� ���
        temp1 = re.findall(r'<span class="dw_file">([\S\s]*?)<style type="text/css">' , html2) 
        temp1 = temp1[0]
        temp1 = re.sub('<br>', '\n', temp1)
        temp1 = re.sub('&#160;', ' ', temp1)
        temp1 = re.sub('</br>', '', temp1)
        temp1 = re.sub('</p>', '\n', temp1)
        content = strip_tags(temp1)  
        print content
    else:   # ��ǻ�ͷ� �ۼ��� ���� ���
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
    good = temp1[0]    #���ƿ�
    temp1 = re.findall(r'<em id="oppCnt">(\d+?)</em>' , html2)
    bad = temp1[0]     #�۽��
    print good, bad

 
    '''
    
    