from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv
import pandas as pd

from preprocessing_controllers import preprocess_document

excpt = []

def get_link_dictionary(web_links, url):
    title_links = {}
    for web_link in web_links:
        if web_link.has_attr('title') and web_link.attrs['href'][0] != '#':
            if web_link.attrs['href'].endswith('.php') and not url.endswith('.php'):
                title_links[web_link.attrs['title']] = url + web_link.attrs['href']
            else:
                title_links[web_link.attrs['title']] = web_link.attrs['href']
        elif web_link.has_attr('href'):
            if web_link.attrs['href'][0] != '#':
                if len(web_link.contents) == 1:
                    if web_link.attrs['href'].endswith('.php') and not url.endswith('.php'):
                        title_links[web_link.contents[0]] = url + web_link.attrs['href']
                    else:
                        title_links[web_link.contents[0]] = web_link.attrs['href']
                elif (len(str(web_link.find('h4')).split('</')) >= 1) and (len(str(web_link.find('h4')).split('</')[0].split('>'))) >= 2:
                    ttl = str(web_link.find('h4')).split('</')[0].split('>')[1]
                    if web_link.attrs['href'].endswith('.php') and not url.endswith('.php'):
                        title_links[ttl] = url + web_link.attrs['href']
                    else:
                        title_links[ttl] = web_link.attrs['href']
                else:
                    if web_link.attrs['href'].endswith('.php') and not url.endswith('.php'):
                        title_links[web_link] = url + web_link.attrs['href']
                    else:
                        title_links[web_link] = web_link.attrs['href']
        else:
            excpt.append(web_link)
    return title_links

def get_link_dictionary_2(web_links, url, home_url='https://careers.humber.ca/'):
    title_links = {}
    for web_link in web_links:
        try:
            if web_link.has_attr('title') and web_link.attrs['href'][0] != '#':
                if web_link.attrs['href'].endswith('.php'):
                    if url.endswith('/'):
                        title_links[web_link.attrs['title']] = url + web_link.attrs['href']
                    elif str(web_link.attrs['href']) not in str(url):
                        title_links[web_link.attrs['title']] = url + '/' + web_link.attrs['href']
                else:
                    title_links[web_link.attrs['title']] = web_link.attrs['href']
            elif web_link.has_attr('href'):
                if web_link.attrs['href'][0] != '#':
                    if len(web_link.contents) == 1:
                        if web_link.attrs['href'].endswith('.php') and not url.endswith('.php'):
                            if url.endswith('/'):
                                title_links[web_link.contents[0]] = url + web_link.attrs['href']
                            elif str(web_link.attrs['href']) not in str(url):
                                title_links[web_link.contents[0]] = url + '/' + web_link.attrs['href']
                        else:
                            if web_link.contents[0] in title_links.keys():
                                if web_link.attrs['href'].endswith('.php'):
                                    title_links[web_link.contents[0] + web_link.attrs['href']] = home_url + web_link.attrs['href']
                                else:
                                    title_links[web_link.contents[0] + web_link.attrs['href']] = web_link.attrs['href']
                            else:
                                if web_link.attrs['href'].endswith('.php'):
                                    title_links[web_link.contents[0]] = home_url + web_link.attrs['href']
                                else:
                                    title_links[web_link.contents[0]] = web_link.attrs['href']
                    elif (len(str(web_link.find('h4')).split('</')) >= 1) and (len(str(web_link.find('h4')).split('</')[0].split('>'))) >= 2:
                        ttl = str(web_link.find('h4')).split('</')[0].split('>')[1]
                        if web_link.attrs['href'].endswith('.php') and not url.endswith('.php'):
                            if url.endswith('/'):
                                title_links[ttl] = url + web_link.attrs['href']
                            elif str(web_link.attrs['href']) not in str(url):
                                title_links[ttl] = url + '/' + web_link.attrs['href']
                        else:
                            title_links[ttl] = web_link.attrs['href']
                    else:
                        if web_link.attrs['href'].endswith('.php') and not url.endswith('.php'):
                            if url.endswith('/'):
                                title_links[web_link] = url + web_link.attrs['href']
                            elif str(web_link.attrs['href']) not in str(url):
                                title_links[web_link] = url + '/' + web_link.attrs['href']
                        else:
                            title_links[web_link] = web_link.attrs['href']
            else:
                excpt.append(web_link)
        except:
            continue
    return title_links

def get_web_links(url):
    try:
        page = urlopen(url)
        html = page.read()
        soup = BeautifulSoup(html, "html.parser")
        web_links = soup.select('a')
        return web_links
    except:
        return []
    
def link_to_purpose_mapping(link_dictionary):
    link_to_purpose = {}
    for key in link_dictionary.keys():
        value = link_dictionary[key]
        if value not in link_to_purpose.keys():
            link_to_purpose[value] = [key]
        else:
            link_to_purpose[value].append(key)
    return link_to_purpose

def split_and_form_url(joined_urls):
    urls_now = []
    if 'https' in joined_urls:
        splitted = joined_urls.split('https')
        for i in splitted:
            if len(i) > 0:
                urls_now.append('https' + i)
    else:
        urls_now.append(joined_urls)
    return urls_now

def add_new_to_old(old_dict, new_dict, url_chkd, last_part, depth):
    new_urls = []
    for i in new_dict.keys():
        if '//' in i and '/' in i.split('//')[1]:
            add = i.split('//')[1].split('/')[0]
            if len(i) < 100 and ('careers.humber' in add or 'devant' in add):
                if i not in old_dict.keys():
                    if i not in url_chkd and i.split('/')[-1] not in last_part and len(i.split('.php')) < depth:
                        new_urls += split_and_form_url(i)
                    old_dict[i] = new_dict[i]
                else:
                    old_dict[i] = old_dict[i] + new_dict[i]
                    unique_purpose = list(dict.fromkeys(old_dict[i]))
                    old_dict[i] = unique_purpose
    return old_dict, new_urls

def all_paths(url, depth):
    link_to_purpose = {}
    link_to_purpose[url] = ['Home Page']
    link_to_purpose
    url_checked = []
    last_part = []
    last_part.append('index.php')
    web_pages = []
    
    urls = list(link_to_purpose.keys())
    while(len(urls) != 0):
        
        new_urls = []
        i = urls[0]
        urls.remove(i)
        print(i)
        if i not in url_checked:
            wb_lnk = get_web_links(i)
            url_checked.append(i)
            if len(wb_lnk) > 0:
                lnk_dict = get_link_dictionary_2(wb_lnk, i)
                lnk_purps = link_to_purpose_mapping(lnk_dict)
                link_to_purpose, new_urls = add_new_to_old(link_to_purpose, lnk_purps, url_checked, last_part, depth)
        urls = list(set(urls + new_urls))
    return link_to_purpose

def limited_paths(url):
    link_to_purpose = {}
    link_to_purpose[url] = ['Home Page']
    link_to_purpose
    url_checked = []
    web_pages = []
    new_urls = list(link_to_purpose.keys())
    urls = []
    while(len(new_urls) != 0):
        urls = new_urls
        new_urls = []
        for i in urls:
            print(i)
            if i not in url_checked:
                wb_lnk = get_web_links(i)
                url_checked.append(i)
                if len(wb_lnk) > 0:
                    lnk_dict = get_link_dictionary(wb_lnk, i)
                    lnk_purps = link_to_purpose_mapping(lnk_dict)
                    link_to_purpose, new_urls = add_new_to_old(link_to_purpose, lnk_purps, url_checked)
    return link_to_purpose

def get_web_document(url):
    try:
        page = urlopen(url)
        html = page.read()
        soup = BeautifulSoup(html, "html.parser")
        web_doc = soup.get_text()
        return re.sub(r'\n\n+', '', str(web_doc))
    except:
        return ''

def get_text_as_doc_from_websites(all_url):
    link_doc_dict = {'Link':'Document'}
    doc_link_dict = {'Document': ['Link']}
    lnk_dc = {'Link':'Document'}
    all_doc = []
    exception_links = []
    for i in set(all_url):
        doc = get_web_document(i)
        if len(doc) > 0:
            lnk_dc[i] = doc
        if len(doc) != 0 and doc not in all_doc:
            link_doc_dict[i] = doc
            all_doc.append(doc)
        if len(doc) != 0 and doc not in doc_link_dict.keys():
            doc_link_dict[doc] = [i]
        elif len(doc) != 0:
            doc_link_dict[doc].append(i)
        else:
            exception_links.append(i)
    return link_doc_dict, doc_link_dict, all_doc, exception_links, lnk_dc

def get_all_urls(all_urls):
    unique_urls = []
    for i in all_urls:
        if len(i.split('/')) < 5:
            unique_urls.append(i)
    return unique_urls

def generate_document_from_scraped_data(csv_file):
    dct_links = pd.read_csv(csv_file)
    home_url = ['https://careers.humber.ca/']
    links_other = dct_links['https://careers.humber.ca/']
    all_url = home_url + list(links_other)

    unique_urls = get_all_urls(all_url)

    lnk_dc_dct, dc_lnk_dct, all_dc, ex_lnks, lnk_dc = get_text_as_doc_from_websites(unique_urls)

    del lnk_dc['Link']

    link_doc_df = pd.DataFrame(lnk_dc_dct.items())
    doc_link_df = pd.DataFrame(dc_lnk_dct.items())
    link_document_df = pd.DataFrame(lnk_dc.items())

    link_doc_df.to_excel('Link_to_doc.xlsx', engine='xlsxwriter')
    doc_link_df.to_excel('Doc_to_link.xlsx', engine='xlsxwriter')
    link_document_df.to_excel('Link_Document_Complete_Processed.xlsx', engine='xlsxwriter')

    return './Link_Document_Complete_Processed.xlsx'

def web_scrapper(root):
    link_to_purpose = all_paths(root, 3)

    all_one_val = {}
    for k,v in link_to_purpose.items():
        for val in v:
            if k not in all_one_val.keys():
                all_one_val[k] = str(val)
            else:
                all_one_val[k] = all_one_val[k] + ', ' + str(val)

    long_dict, short_dict = {}, {}
    for k,v in all_one_val.items():
        if len(v) > 200:
            long_dict[k] = v
        else:
            short_dict[k] = v

    all_link_purpose = {}
    for k,v in short_dict.items():
        all_link_purpose[k]=v
    for k,v in long_dict.items():
        all_link_purpose[k]=v

    with open('link-dict-2.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in all_link_purpose.items():
            writer.writerow([key, value])

    with open('dict-2.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in link_to_purpose.items():
            writer.writerow([key, value])

    url_to_document = generate_document_from_scraped_data('dict-2.csv')
    return url_to_document
