import sys
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
from loguru import logger

logger.remove()
logger.add('univers_school.log', rotation='700kb', level='WARNING')
logger.add(sys.stderr, level='INFO')
url_cache = {}


def get_url_content(url: str):
    if url in url_cache:
        return url_cache[url]
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

        with requests.Session() as session:
            try:
                response = session.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    if soup:
                        url_cache[url] = soup
                        return soup
                    else:
                        logger.error('Error to fetch page content')
            except requests.exceptions.RequestException as e:
                logger.error(f'Access error to {url}: {e}')


def link_wiki_university(soup) -> list:
    div_univ = soup.find('div', attrs={'class': "mw-content-ltr mw-parser-output"})
    ele_univ = div_univ.select_one("ul").select('li')
    university_link = []
    base_url = "https://fr.wikipedia.org"
    wiki_link = []
    for element in ele_univ:
        for a in element.find_all('a', title=True):
            link = a['href']
            absolute_link = urljoin(base_url, link)
            wiki_link.append(absolute_link)
            university_link.append(absolute_link)
            time.sleep(3)
    return wiki_link


def get_list_university_website(links: list) -> list:
    list_website = []
    for link in links:
        response = get_url_content(link)
        title = response.find('h1')
        web_site = response.find('div', attrs={'class': "mw-content-ltr mw-parser-output"})
        try:
            link_website = web_site.find_all('table')[1]
            last_row = link_website.find_all('tr')[-1]
            link_university = last_row.find('a')
            list_website.append(link_university['href'])
            time.sleep(3)
        except AttributeError as e:
            logger.error(f"error to fetch the website link of '{title.text}': {e}")
            continue
    return list_website


def urls_list() -> list:
    base_url = "https://fr.wikipedia.org/wiki/Enseignement_sup%C3%A9rieur_et_recherche_au_Cameroun"
    content = get_url_content(base_url)
    time.sleep(2)
    list_url = link_wiki_university(content)
    time.sleep(2)
    all_link = get_list_university_website(list_url)
    return all_link


def ubuea(url: str):
    if url in urls_list():
        response = get_url_content(url)
        name = response.find('h1').text
        website = url


def udouala(url: str):
    if url in urls_list():
        response = get_url_content(url)
        name = response.find('h1').text
        website = url


def udschang(url: str):
    if url in urls_list():
        response = get_url_content(url)
        website = url
        name = response.select_one('header').select_one('img')
        name = name['alt']
        aside = response.find('div', attrs={'class': "menu-les-etablissemens-container"})
        school = aside.find_all('li')
        school_name = []
        for i in school:
            element = i.text
            school_name.append(element)
        print(name, school_name, website)
    else:
        logger.error(f"{url} doesn't match to university")


def ungaoundere(url: str):
    if url in urls_list():
        response = get_url_content(url)
        name = response.find('h1').text
        website = url


def uyaounde1(url: str):
    if url in urls_list():
        response = get_url_content(url)
        website = url
        try:
            header = response.find('header', attrs={'id': "masthead"})
            name = header.find('h1', attrs={'class': "site-title"}).find('a').text
            print(name)

            div_element = header.find('div', attrs={"class": "primary-nav nav"})
            time.sleep(3)
            ul_element = div_element.find('ul', attrs={"id": "menu-primary-menu"})
            faculty_school = ul_element.find('li', attrs={'id': "menu-item-11283"})
            link = faculty_school.find('a')['href']
            time.sleep(3)
            print(link)
            if link:
                list_fac = faculty_yaounde1(url)
                print(list_fac)
        except AttributeError as e:
            logger.error(f'Error to get header: {e}')

    else:
        logger.info(f"{url} doesn't match")


def faculty_yaounde1(url: str) -> list:
    resp = get_url_content(url)
    with open('index.html', 'w') as f:
        data = f.write(resp.text)
    try:
        div_faculty = resp.find('div', attrs={'class': "vc_tta-tabs-container"})
        ul_faculty = div_faculty.find('ul', attrs={"class": "vc_tta-tabs-list"})
        li_element = ul_faculty.select('li')
        faculty_list = []
        for i in li_element:
            faculty_list.append(i.text)

        print(faculty_list)
        return faculty_list
    except AttributeError as e:
        logger.error(f'Error to get faculty from {url}: {e}')
        return []


def uyaounde2(url: str):
    if url in urls_list():
        response = get_url_content(url)
        name_tag = response.find('a').find('img')
        name = name_tag['alt']
        website = url
        school_div = response.find('div', attrs={"class": "av-magazine-group sort_all"})
        article_tag = school_div.find_all('article')
        list_faculty = []
        for i in article_tag:
            faculty = i.find('h3')
            list_faculty.append(faculty.text)
        print(name, website, list_faculty)


def ubertoua(url: str):
    if url in urls_list():
        response = get_url_content(url)
        name = response.find('div', attrs={'class', 'copyright'}).find('strong').text.strip()
        website = url
        try:
            training_link = response.find('div', attrs={"class": "container d-flex justify-content-center align-items-center"})
            training = training_link.find_all('li')[2]
            link = training.find('a')
            link_f = urljoin(url, link['href'])
            if link_f:
                resp = get_url_content(link_f)
                try:
                    faculty_div = resp.find('div', attrs={'class': "col-lg-3 depart"}).find('ul', attrs={'class': "nav nav-tabs flex-column"}).find_all('li')
                    faculty_list = []
                    for i in faculty_div:
                        element = i.find('a')
                        faculty_list.append(element.text.strip())
                    print(name, faculty_list, website)
                except AttributeError as e:
                    logger.error(f'Error to get faculty: {e}')

            else:
                logger.info('training url not found')
        except AttributeError as e:
            logger.error(f'Error to get faculty of "{name}" : {e}')


ubertoua('https://www.univ-bertoua.cm/')

