import urllib2
import re
import urlparse
import time
import robotparser

def download(url, num_retires = 2):
    print 'Downloading:' + url

    # Add http request proxy
    headers = {'User-agent': 'user_agent'}
    request = urllib2.Request(url, headers=headers)

    try:
        time.sleep(5)
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error: ', e.reason
        html = None

        if num_retires > 0:
            #If there is 500 error, then retry to download the html
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retires - 1)

    return html



#website map crawl
def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemaplink
    links = re.findall('<loc>(.*?)</loc>', sitemap)

    # download each link
    for link in links:
        html = download(link)

def links_crawler(seed_url, link_regex):
    """
    Crawl from the given seed URL following links matched by link_regex
    :param seed_url: 
    :param link_regex: 
    :return: 
    """
    crawl_queue = [seed_url]

    #keep track which URL's have been before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # filter for links matching our regular expression
        print "download html: " + html

        links = get_links(html)
        for link in links:
            if re.match(link_regex, link):
                #get absolute url link
                link = urlparse.urljoin(seed_url, link)

                #check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)



def get_links(html):
    """
    Return a list of links from html
    :param html: 
    :return: 
    """
    #a regular expression to extract all linkd from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    #list of all links from the webpage
    return webpage_regex.findall(html)