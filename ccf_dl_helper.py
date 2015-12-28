#!/usr/bin/env python
#-*-coding:utf-8-*-
__author__ = 'ZhangHe'
import urllib2,re,os


def download_with_url(src_url, dest_file):
    """
    Download the file of src_url and save as dest_file
    :param src_url:
    :param dest_file:
    :return:
    """
    f = urllib2.urlopen(src_url)
    data = f.read()
    with open(dest_file, "wb") as code:
        code.write(data)


def parse_urls_from_volume_url(src_url):
    """
    parse the urls of a concrete volume with src_url
    :param src_url:
    :return:[urls, titles]
    """
    request = urllib2.Request(src_url)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')

    print 'parsing paper IDs...'
    pattern_str1 = '<a target=.*?title=.*?href=.*?contentId=(.*?)">'
    pattern_str2 = '<span id=.*?class="cfqwz">(.*?)</span>'
    pattern_str3 = '<title>(.*?)-.*?</title>'
    pattern1 = re.compile(pattern_str1, re.S)
    pattern2 = re.compile(pattern_str2, re.S)
    pattern3 = re.compile(pattern_str3, re.S)
    ids =  re.findall(pattern1, content)
    titles =  re.findall(pattern2, content)
    name =  re.findall(pattern3, content)

    return [ids,titles,name[0].strip()]


def parse_url_from_paper_id(id):
    """
    parse the download url from a concrete paper id
    :param src_url:
    :return:
    """
    src_url = 'http://www.ccf.org.cn/sites/ccf/freexiazai.jsp?contentId='+str(id)
    request = urllib2.Request(src_url)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')

    # print 'parsing download url...'
    pattern_str = 'class=""><a href="(.*?)">.*?</a></span>'
    pattern = re.compile(pattern_str, re.S)
    urls =  re.findall(pattern, content)
    return 'http://www.ccf.org.cn/sites/ccf/download.jsp?file='+urls[0]

if __name__=='__main__':
    print 'Input a journal ID:',
    id = str(raw_input())
    url = 'http://www.ccf.org.cn/sites/ccf/jsjtbbd.jsp?contentId='+id
    res = parse_urls_from_volume_url(url)
    print 'Start Download...'
    try:
        os.mkdir(res[2])
    except WindowsError as e:
        pass
    for i in xrange(len(res[0])):
        id = res[0][i]
        title = res[1][i].strip()
        print 'Downloading ('+str(i+1)+'/'+str(len(res[0]))+') ID:'+id+' Title:'+title
        dl_url = parse_url_from_paper_id(id)
        download_with_url(dl_url, res[2]+'\\'+title+'.pdf')
    print 'Done.'