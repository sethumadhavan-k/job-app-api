import requests as req
from bs4 import BeautifulSoup
import json

def page_content(url,url_verify=True):
    res = req.get(url, verify=url_verify)
    if res.status_code == 200:
        return res.text
    else:
        return False


def generate_techno_park_jobs():
    url = 'https://www.technopark.org/job-search'
    try:
        pContent = page_content(url,False)
        jobs = []
        if(pContent):
            html =  BeautifulSoup(pContent,"html.parser")
            div = html.find('div',{"id":"tableJobId"})
            trs = div.find('table').find_all('tr',{"class":"companyList"})
            for tr in trs:
                tds = tr.find_all('td')
                jobs.append({
                    'title':tds[0].contents[0].contents[0],
                    'company':tds[1].contents[0].contents[0],
                    'last_date':tds[2].contents[0],
                    'ref_link':"https://www.technopark.org/"+tds[0].contents[0]['href']
                })
        return jobs
    except:
        return []
             
def technopark_job_details(url):
    pContent = page_content(url,False)
    html = BeautifulSoup(pContent,'html.parser')
    try:
        job_container = html.find('div',{"class":"det-text"})
        divs = job_container.find_all('div',{"class":"block"})
        img = html.find('div',{"class":'shade'}).find('img')
        lis = html.find("ul",{"class":"list-sx"}).find_all("li")
        details = {
            "success"   :True,
            "title"     :divs[0].contents[1].string,
            "company"   :lis[0].contents[3].string,
            "website"   :lis[2].contents[3].string,
            "address"   :lis[1].contents[2].string.strip(),
            "logo"      :img['src'],
            "posted_on" :divs[2].contents[3].string,
            "closing_on":divs[3].contents[3].string,
            "email"     :divs[4].contents[3].string,
            "description"   : divs[6].prettify(),
            "apply"     :"",
        }
    except:
        details = { "success":False }

    return details



def generate_infopark_jobs():
    urls = [
        'https://www.infopark.in/companies/jobs/kochi-phase-1',
        'https://www.infopark.in/companies/jobs/kochi-phase-2',
        'https://www.infopark.in/companies/jobs/tbc-kaloor',
        'https://www.infopark.in/companies/jobs/cherthala',
        'https://www.infopark.in/companies/jobs/thrissur'
    ]
    places = ['Kochi Phase 1','Kochi Phase 2','TBC Kaloor','Infopark Cherthala','Infopark Thrissur']
    jobs = []
    p_index = 0
    for url in urls:
        try:
            pContent = page_content(url,False)
            if(pContent):
                html =  BeautifulSoup(pContent,"html.parser")
                divs = html.find_all('div',{"class":"joblist"})
                for div in divs:
                    d = div.find_all('div')
                    jobs.append({
                        'title':d[0].contents[0].string,
                        'company':d[1].contents[0].string,
                        'last_date':d[2].string,
                        'ref_link':d[0].contents[0]['href']
                    })
            p_index+=1
        except:
            print("error")
        
    return jobs

def infopark_job_details(url):
    pContent = page_content(url,False)
    html = BeautifulSoup(pContent,'html.parser')
    try:

        company = html.find('div',{"class":"company-list-details"})
        logo = company.find('div',{"class":"company-list-details-logo"}).find('img')
        name = company.find_all('div',{"class":"address_details"})[0].find('h5')
        address = company.find_all('div',{"class":"address_details"})[1]
        website = company.find_all('div',{"class":"address_details"})[1].find('div',{"class":"compant_cnt_details"}).find('a')
        job_details = html.find('div',{"class":"company-list-details-Bottom"}).find_all('p')
        # print(" ".join(address.find('p').text.split()[:-1]))
        details = {
            "success"       :True,
            "company"       : name.string,
            "address"       : " ".join(address.find('p').text.split()[:-1]),
            "website"       : website.string,
            "logo"          : logo['src'],
            "title"         : job_details[1].string,
            "posted_on"     : "",
            "closing_on"    : "",
            "email"         : job_details[3].string.split(':')[1].strip(),
            "description"   : job_details[2].prettify(),
            "apply"         :""
        }
    except:
        details = { "success":False }
    return details



def generate_ulpark_jobs():
    url = 'https://ulcyberpark.com/jobs/'
    try:
        pContent = page_content(url,False)
        jobs = []
        if(pContent):
            html =  BeautifulSoup(pContent,"html.parser")
            div = html.find('div',{"class":"table-job"})
            trs = div.find('table').find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                jobs.append({
                    'title':tds[0].contents[0].string.strip(),
                    'company':tds[1].contents[0].string,
                    'last_date':tds[0].contents[2].string.split(':')[1].strip(),
                    'ref_link':tds[2].contents[0]['href']
                })
            
            return jobs
    except:
        return []

def ulpark_job_details(url):
    pContent = page_content(url,False)
    html = BeautifulSoup(pContent,'html.parser')
    try:
        job_details = html.find('div',{"class":"job_border"})
        details = {
            "success"   :True,
            "title"     :job_details.find('h2',{"class":"main_title_head"}).string,
            "posted_on" :"",
            "closing_on":job_details.find('h4',{"class":"sub_title"}).string.split(":")[1],
            "email"     :job_details.find('h4',{"class":"email_title"}).find('a').string,
            "logo"      :job_details.find('img',{"class":"img_lt"})['src'],
            "description":job_details.find('div',{"class":"c2_left_padd"}).prettify(),
            "apply"     :"",
            "address"   :"",
            "company"   : "",
            "website"   : "",
        }
    except:
        details = { "success":False }

    return details


def generate_cyberpark_jobs():
    url = 'http://www.cyberparkkerala.org/jm-ajax/get_listings/'
    try:
        pContent = page_content(url,False)
        jobs = []
        if(pContent):
            resJson = json.loads(pContent)
            html =  BeautifulSoup(resJson['html'],"html.parser")
            lis = html.find_all('li',{"class":"job_listing"})
            for li in lis:
                tds = li.find('a').find('div')
                date = li.find('a').find('ul')
                contains = tds.contents
                jobs.append({
                    'title':contains[1].string,
                    'company':contains[3].contents[1].string,
                    'last_date':date.contents[3].contents[0].string,
                    'ref_link':li.find('a')['href']
                })
            
            return jobs
    except:
        return []

def cyberpark_job_details(url):
    pContent = page_content(url,False)
    try:
        html = BeautifulSoup(pContent,'html.parser')
        job_details = html.find('div',{"class":"single_job_listing"})
        company = job_details.find('div',{"class":"company"})
        description = job_details.find('div',{"class":"job_description"})

        details = {
            "success"   : True,
            "company"   : company.find('p',{"class":"name"}).contents[3].string,
            "website"   : company.find('p',{"class":"name"}).contents[1]['href'],
            "logo"      : company.find('img',{"class":"company_logo"})['src'],
            "title"     : description.find('p').string,
            "address"   : "",
            "description" : description.prettify(),
            "apply"     : job_details.find('div',{"class":"job_application"}).div.find('p').prettify(),
            "email"     : "",
            "posted_on" : "",
            "closing_on": ""

        }
    except:
        details = { "success": False}

    return details

