import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from loguru import logger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


logger.remove()
logger.add('univers_school.log', rotation='700kb', level='WARNING')
logger.add(sys.stderr, level='INFO')


class Univers:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def get_yaounde1(self):
        url = "https://www.uy1.uninet.cm/"
        try:
            self.driver.get(url)
            univ_tag = '//*[@id="content"]/div/div/div[4]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/p'
            university_description = self.wait.until(ec.presence_of_element_located((By.XPATH, univ_tag))).text
            name = self.wait.until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="masthead"]/div[2]/div/div/div[1]/div/a/img')))
            name_text = name.get_attribute('alt')
            self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="menu-item-11283"]/a'))).click()

            # get the list of faculty and urls
            try:
                f_path = '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul'
                faculty_element = self.wait.until(ec.presence_of_element_located((By.XPATH, f_path)))
                faculty_tag = faculty_element.find_elements(By.TAG_NAME, 'li')
                faculty_list = []
                faculty_link = []
                for i in faculty_tag:
                    link = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    faculty_link.append(link)
                    faculty_list.append(i.text)
                faculty_name_link = list(zip(faculty_list, faculty_link))
                logger.info(f"l'{name_text} compte {len(faculty_list)} "
                            f"facultes et formations la list: {faculty_name_link} et son lien est:{url}.\n"
                            f"The description is: {university_description}")
            except Exception as e:
                logger.error(f'something went wrong to fetch the list of college {url}: {e}')

            try:
                f_path = '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul/li[1]'
                name_1 = self.wait.until(ec.presence_of_element_located((By.XPATH, f_path)))
                name_1.click()
                school_name = name_1.text
                falsh_link = name_1.find_element(By.TAG_NAME, 'a').get_attribute('href')
                time.sleep(3)
                falsh_des_tag = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="falsh"]/div[2]/div[8]/div/p')))
                falsh_description = falsh_des_tag.text.strip()

                falsh_depart = name_1.find_element(By.XPATH,
                                                   '//*[@id="falsh"]/div[2]/div[10]/div[2]/div/div/div[3]/div/ul')
                elements = falsh_depart.find_elements(By.TAG_NAME, 'li')
                falsh_depart_list = []
                falsh_depart_link = []
                time.sleep(3)
                for element in elements:
                    dep = element.find_element(By.TAG_NAME, 'strong').find_element(By.TAG_NAME, 'a')
                    falsh_depart_link.append(dep.get_attribute('href'))
                    falsh_depart_list.append(dep.text)
                falsh_depart_list_link = list(zip(falsh_depart_list, falsh_depart_link))

                logger.info(f" The {school_name} count {len(falsh_depart_list_link)} "
                            f"Departments the list: {falsh_depart_list_link} and its link:{falsh_link}."
                            f"\nThe description is: {falsh_description} ")

            except Exception as e:
                logger.error(f'Something went wrong to scrape the F.A.L.S.H of {url}: {e}')

            try:
                fs_path = '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul/li[2]'
                fs_button = self.wait.until(ec.element_to_be_clickable((By.XPATH, fs_path)))
                fs_button.click()
                fs_name = fs_button.text
                fs_link = fs_button.find_element(By.TAG_NAME, 'a').get_attribute('href')
                time.sleep(3)
                fs_des_tag = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="facsciences"]/div[2]/div[8]/div/p')))
                fs_description = fs_des_tag.text.strip()
                ul_path = '//*[@id="facsciences"]/div[2]/div[10]/div[2]/div/div/div[3]/div/ul'
                fs_ul = self.wait.until(ec.presence_of_element_located((By.XPATH, ul_path)))
                elements = fs_ul.find_elements(By.TAG_NAME, 'li')
                fs_depart_list = []
                fs_depart_link = []
                time.sleep(3)
                for element in elements:
                    fs_dep = element.find_element(By.TAG_NAME, 'strong').find_element(By.TAG_NAME, 'a')
                    fs_depart_list.append(fs_dep.text)
                    fs_depart_link.append(fs_dep.get_attribute('href'))
                fs_depart_list_link = list(zip(fs_depart_list, fs_depart_link))
                logger.info(f" The {fs_name} count {len(fs_depart_list_link)} "
                            f"Departments the list: {fs_depart_list_link} and its link:{fs_link}."
                            f"\n The description is: {fs_description}")

            except Exception as er:
                logger.error(f'Something went wrong to scrape the FS of {url}: {er}')

            try:
                fse_button = self.wait.until(ec.element_to_be_clickable(
                    (By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul/li[3]')))

                fse_button.click()
                fse_name = fse_button.text
                fse_link = fse_button.find_element(By.TAG_NAME, 'a').get_attribute('href')
                time.sleep(3)
                fse_des_tag = self.wait.until(ec.presence_of_element_located((By.XPATH,
                                                                              '//*[@id="fse"]/div[2]/div[8]/div/p')))
                fse_description = fse_des_tag.text.strip()
                fs_ul = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="fse"]/div[2]/div[10]/div[2]/div/div/div[3]/div/ul')))

                elements = fs_ul.find_elements(By.TAG_NAME, 'li')
                fse_depart_list = []
                fse_depart_link = []
                time.sleep(3)
                for element in elements:
                    fs_dep = element.find_element(By.TAG_NAME, 'strong').find_element(By.TAG_NAME, 'a')
                    fse_depart_list.append(fs_dep.text)
                    fse_depart_link.append(fs_dep.get_attribute('href'))
                fse_depart_list_link = list(zip(fse_depart_list, fse_depart_link))
                logger.info(f" The {fse_name} count {len(fse_depart_list_link)} "
                            f"Departments the list: {fse_depart_list_link} and its link:{fse_link}."
                            f"\n The descriptin is: {fse_description}")

            except Exception as er:
                logger.error(f'Something went wrong to scrape the FSE of {url}: {er}')
            try:
                fmsp_button = self.wait.until(ec.element_to_be_clickable(
                    (By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul/li[4]')))
                fmsp_button.click()
                fmsp_name = fmsp_button.text
                fmsp_link = fmsp_button.find_element(By.TAG_NAME, 'a').get_attribute('href')
                time.sleep(3)
                fmsp_des_tag = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="fmsb"]/div[2]/div[10]/div')))
                fmsp_description = fmsp_des_tag.text.strip()
                logger.info(f"The description of {fmsp_name} is: {fmsp_description}.Its link:{fmsp_link}")
            except Exception as er:
                logger.error(f'Something went wrong to scrape the FMSB of {url}: {er}')

            try:
                ens_button = self.wait.until(ec.element_to_be_clickable(
                    (By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul/li[5]')))

                ens_button.click()
                ens_name = ens_button.text
                ens_link = ens_button.find_element(By.TAG_NAME, 'a').get_attribute('href')
                time.sleep(3)
                ens_des_tag = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="ens"]/div[2]/div[8]/div')))
                ens_description = ens_des_tag.text.strip()
                ens_ul = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="ens"]/div[2]/div[10]/div[2]/div/div/div[3]/div/ul')))

                elements = ens_ul.find_elements(By.TAG_NAME, 'li')
                ens_depart_list = []
                time.sleep(3)
                for element in elements:
                    ens_dep = element.find_element(By.TAG_NAME, 'strong')
                    if ens_dep:
                        ens_depart_list.append(ens_dep.text)
                logger.info(f" The {ens_name} count {len(ens_depart_list)} "
                            f"Departments the list: {ens_depart_list} and its link:{ens_link}.\n "
                            f"The description is: {ens_description}")
            except Exception as er:
                logger.error(f'Something went wrong to scrape the ENS of {url}: {er}')

            try:
                ptch_button = self.wait.until(ec.element_to_be_clickable(
                    (By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul/li[6]')))
                ptch_button.click()
                ptch_name = ptch_button.text
                ptch_link = ptch_button.find_element(By.TAG_NAME, 'a').get_attribute('href')
                time.sleep(3)
                ptch_des_tag = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="ensp"]/div[2]/div[10]/div')))
                ptch_description = ptch_des_tag.text.strip()
                ptch_ul = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="ensp"]/div[2]/div[14]/div/ul[1]')))

                elements = ptch_ul.find_elements(By.TAG_NAME, 'li')
                ptch_depart_list = []
                time.sleep(3)
                for element in elements:
                    ens_dep = element.find_element(By.TAG_NAME, 'strong')
                    if ens_dep:
                        ptch_depart_list.append(ens_dep.text.replace(' ;', ''))
                logger.info(f" The {ptch_name} count {len(ptch_depart_list)} "
                            f"Departments the list: {ptch_depart_list} and its link:{ptch_link}.\n"
                            f"The description is: {ptch_description}")

            except Exception as er:
                logger.error(f'Something went wrong to scrape the PTCH of {url}: {er}')

            try:
                ed_button = self.wait.until(ec.element_to_be_clickable(
                    (By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/ul/li[8]')))

                ed_button.click()
                ed_name = ed_button.text
                ed_link = ed_button.find_element(By.TAG_NAME, 'a').get_attribute('href')
                ed_ul = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="ecoles-doctorales"]/div[2]/div[4]/div/div')))

                elements = ed_ul.find_elements(By.CSS_SELECTOR, '.wpb_wrapper div p strong')
                ed_depart_list = []
                time.sleep(3)
                for element in elements:
                    content = element.text
                    if content.startswith(('1.', '2.', '3.', '4.')):
                        content = content.replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '')
                        ed_depart_list.append(content)

                logger.info(f" The {ed_name} count {len(ed_depart_list)} "
                            f"Departments the list: {ed_depart_list} and its link:{ed_link}")

            except Exception as er:
                logger.error(f'Something went wrong to scrape the ED of {url}: {er}')

        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_ubuea(self):
        url = "http://ubuea.cm/"
        try:
            self.driver.get(url)
            b_path = '//*[@id="content"]/div/div[2]/h1/span/strong'
            name = self.wait.until(ec.presence_of_element_located((By.XPATH, b_path))).text
            self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="menu-item-4399"]/a'))).click()
            f_div = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="post-2515"]/div[2]')))
            f_tag = f_div.find_elements(By.XPATH, "//div[@class='entry-content']//h2")

            f_list = []
            f_link = []
            for i in f_tag:
                f_list.append(i.text)
                f_link.append(i.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            f_name_link = list(zip(f_list, f_link))
            logger.info(f"Welcome to {name} it has {len(f_name_link)} "
                        f"faculties and schools, the list: {f_name_link}, and its website is: {url}")
        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_udouala(self):
        url = 'http://www.univ-douala.cm/'
        try:
            self.driver.get(url)
            name = self.driver.title
            print(name)
            # get the faculty list
            f_path = '//*[@id="footer-part"]/div/div/div/div[3]/div/ul'
            ul_tag = self.wait.until(ec.presence_of_element_located((By.XPATH, f_path)))
            f_div = ul_tag.find_elements(By.XPATH, './li/a')
            fac_list = []
            fac_link = []
            for element in f_div:
                fac_list.append(element.text)
                fac_link.append(element.get_attribute("href"))
            fac_name_link = list(zip(fac_list, fac_link))
            p_path = '//*[@id="footer-part"]/div/div/div/div[4]/div/ul'
            ul_tag = self.wait.until(ec.presence_of_element_located((By.XPATH, p_path)))
            f_div = ul_tag.find_elements(By.XPATH, './li/a')
            trai_list = []
            trai_link = []
            for element in f_div:
                trai_list.append(element.text)
                trai_link.append(element.get_attribute("href"))
            trai_name_link = list(zip(trai_list, trai_link))
            fac_name_link.extend(trai_name_link)
            logger.info(f"L'{name} compte {len(fac_name_link)} "
                        f"facultes et formations. La list: {fac_name_link} et son lien est: {url}")
        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_udschang(self):
        url = 'http://www.univ-dschang.org'
        try:
            self.driver.get(url)
            t_path = '//*[@id="main-header"]/div/div/div[1]/a/img'
            name_el = self.wait.until(ec.presence_of_element_located((By.XPATH, t_path)))
            name = name_el.get_attribute('alt')

            f_path = '//*[@id="menu-les-etablissemens"]'
            ul_tag = self.wait.until(ec.presence_of_element_located((By.XPATH, f_path)))
            f_div = ul_tag.find_elements(By.XPATH, './li/a')
            fac_list = []
            fac_link = []
            for element in f_div:
                fac_list.append(element.text)
                fac_link.append(element.get_attribute("href"))

            fac_name_link = list(zip(fac_list, fac_link))
            logger.info(f"L'{name} compte {len(fac_name_link)} "
                        f"facultes et formations. La list: {fac_name_link} et son lien est: {url}")

        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_ugaoundere(self):
        url = 'http://www.univ-ndere.cm/'
        try:
            self.driver.get(url)
            n_path = '//*[@id="td-outer-wrap"]/div[1]/div/div[2]/div/div/div[1]/h1/a/span'
            name = self.wait.until(ec.presence_of_element_located((By.XPATH, n_path))).text
            self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="text-2"]/div/p[3]/a[4]'))).click()

            print(name)
        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_yaounde2(self):
        url = 'http://www.univ-yaounde2.org/'
        try:
            self.driver.get(url)
            t_path = '//*[@id="header_main"]/div/div/span/a/img'
            name_el = self.wait.until(ec.presence_of_element_located((By.XPATH, t_path)))
            name = name_el.get_attribute('alt')
            fac_div = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="1"]/div[2]')))
            articles = fac_div.find_elements(By.TAG_NAME, 'article')
            fac_list = []
            fac_link = []
            for article in articles:
                element = article.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a')
                f_element = element.text
                fac_list.append(f_element)
                f_link = element.get_attribute('href')
                fac_link.append(f_link)

            fac_name_link = list(zip(fac_list, fac_link))
            logger.info(f"L'{name} compte {len(fac_name_link)} "
                        f"facultes et formations. La list: {fac_name_link} et son lien est: {url}")

        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_ubamenda(self):
        url = 'https://uniba.cm/'
        try:
            self.driver.get(url)
            name = self.driver.title
            action_tag = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="m_menu_active"]/li[3]')))
            ActionChains(self.driver).move_to_element(action_tag).perform()
            self.driver.implicitly_wait(3)

            sch_path = '//*[@id="m_menu_active"]/li[3]/ul'
            sch_div = self.wait.until(ec.presence_of_element_located((By.XPATH, sch_path)))
            li_tag = sch_div.find_elements(By.TAG_NAME, 'li')
            fac_list = []
            fac_link = []
            for element in li_tag:
                f_element = element.find_element(By.TAG_NAME, 'a')
                fac_list.append(f_element.text)
                fac_link.append(f_element.get_attribute('href'))
            fac_name_link = list(zip(fac_list, fac_link))

            logger.info(f"{name} count {len(fac_name_link)} "
                        f"faculties and trainings. The list: {fac_name_link} and its website: {url}")

        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_ubertoua(self):
        url = 'https://www.univ-bertoua.cm'
        try:
            self.driver.get(url)
            self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="navbar"]/ul/li[3]'))).click()
            name = self.driver.title
            try:
                f_path = '//*[@id="departments"]/div/div/div[1]/ul'
                f_tag = self.wait.until(ec.presence_of_element_located((By.XPATH, f_path)))
                li_tag = f_tag.find_elements(By.TAG_NAME, 'li')
                fac_list = []
                fac_link = []
                for element in li_tag:
                    f_element = element.find_element(By.TAG_NAME, 'a')
                    fac_list.append(f_element.text)
                    fac_link.append(f_element.get_attribute('href'))

                fac_name_link = list(zip(fac_list, fac_link))
                logger.info(f"L'{name} compte {len(fac_name_link)} "
                            f"facultes et formations. La list: {fac_name_link} et son lien est: {url}")

            except AttributeError as e:
                logger.error(f'error to fetch formation button: {e}')

        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_ugaroua(self):
        url = 'http://univ-garoua.cm'
        try:
            self.driver.get(url)
            name = self.driver.title
            print(name)
            school_path = '//*[@id="main-wrapper"]/header/div[3]/div/div/div[2]/nav/ul/li[4]/a'
            school_tag = self.wait.until(ec.presence_of_element_located((By.XPATH, school_path)))
            ActionChains(self.driver).move_to_element(school_tag).perform()
            self.driver.implicitly_wait(3)

            # get the name of schools
            sch_path = '//*[@id="main-wrapper"]/header/div[3]/div/div/div[2]/nav/ul/li[4]/ul/li[1]/ul'
            sch_div = self.wait.until(ec.presence_of_element_located((By.XPATH, sch_path)))
            li_tag = sch_div.find_elements(By.TAG_NAME, 'li')
            fac_list = []
            fac_link = []
            for element in li_tag:
                f_element = element.find_element(By.TAG_NAME, 'a')
                fac_list.append(f_element.text)
                fac_link.append(f_element.get_attribute('href'))
            fac_name_link = list(zip(fac_list, fac_link))

            # get the name of trainings
            trai_path = '//*[@id="main-wrapper"]/header/div[3]/div/div/div[2]/nav/ul/li[4]/ul/li[2]/ul'
            ul_tag = self.wait.until(ec.presence_of_element_located((By.XPATH, trai_path)))
            f_div = ul_tag.find_elements(By.XPATH, 'li')
            trai_list = []
            trai_link = []
            for element in f_div:
                f_element = element.find_element(By.TAG_NAME, 'a')
                trai_list.append(f_element.text)
                trai_link.append(f_element.get_attribute("href"))
            trai_name_link = list(zip(trai_list, trai_link))
            fac_name_link.extend(trai_name_link)
            logger.info(f"L'{name} compte {len(fac_name_link)} "
                        f"facultes et formations. La list: {fac_name_link} et son lien est: {url}")

        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def get_umarou(self):
        url = 'http://www.univ-maroua.cm'
        try:
            self.driver.get(url)
            name = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="logo"]/div[1]'))).text
            school_path = '//*[@id="block-mainmenu"]/div[2]/div/div/ul/li[3]/a'
            self.wait.until(ec.element_to_be_clickable((By.XPATH, school_path))).click()

            sch_path = '//*[@id="block-mainmenu"]/div[2]/div/div/ul/li[3]/ul'
            sch_div = self.wait.until(ec.presence_of_element_located((By.XPATH, sch_path)))
            li_tag = sch_div.find_elements(By.TAG_NAME, 'li')
            fac_list = []
            fac_link = []
            for element in li_tag:
                f_element = element.find_element(By.TAG_NAME, 'a')
                fac_list.append(f_element.text)
                fac_link.append(f_element.get_attribute('href'))
            fac_name_link = list(zip(fac_list, fac_link))

            logger.info(f"L'{name} compte {len(fac_name_link)} "
                        f"facultes et formations. La list: {fac_name_link} et son lien est: {url}")

        except Exception as e:
            logger.error(f'Access error to {url}: {e}')

    def close(self):
        self.driver.quit()


yaou = Univers()
yaou.get_yaounde1()
yaou.close()