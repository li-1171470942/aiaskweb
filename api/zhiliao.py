import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Import your utility functions as needed
from api.utils import *


class WebScraper:
    def __init__(self, driver_path='D:\\chromedriver_win32\\chromedriver.exe'):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Use headless mode for Chrome
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        })

    def __del__(self):
        try:
            self.driver.quit()
        except Exception as e:
            print("Error while closing the driver: ", str(e))

    def webmock(self, url, callback):
        print("Accessing URL:", url)
        try:
            self.driver.get(url)
            try:
                self.driver.add_cookie({'name': 'PHPSESSID', 'value': 'g6ls9th7vo6j600co7tu2ceebd'})
                self.driver.add_cookie({'name': 'SSOToken', 'value': 'QYknuHH5HGYokLKy2uaslBhJk8YC1+...'})
            except InvalidCookieDomainException as e:
                print("Cookie domain invalid:", e)
                return ""

            self.driver.get(url)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            return callback(soup)

        except Exception as e:
            print("Error while accessing the webpage: ", str(e))
            return ""

    def getPageSizeFromHtml(self, soup):
        target_div = soup.find('div', class_='section_two_f1')
        if target_div:
            p_tags = target_div.find_all('p')
            last_p = p_tags[-1]
            last_a = last_p.find('a')
            value = last_a.text if last_a else None
            return value
        else:
            print("The target <div> was not found.")
            return 0

    def getPageSize(self):
        base_url = 'https://zhiliao.h3c.com'
        sub_url = '/theme/index/6_1______all?themeSearchKey=&search_type=1&p=1'
        return self.webmock(base_url + sub_url, self.getPageSizeFromHtml)

    def getSubUrl(self, soup):
        res = []
        # 假设标题链接在 class 为指定类名的 <a> 标签中
        for link in soup.find_all('a', class_='s_t_one1 highlight_em'):
            title = link.get_text()
            href = link.get('href')
            res.append(href)
        return res

    def grepText(self, soup):
        res = ""

        # 查找<h1>标签，可能使用class name来查找
        h1_tag = soup.find('h1', class_='title3_')

        # 提取并打印<h1>标签中的文本
        if h1_tag:
            title = h1_tag.get_text(strip=True)
            res += "标题内容:" + title
        else:
            print("未找到<h1>标签")

        # 查找带有特定类名的<div>标签
        div_tag = soup.find('div', class_='pp_answer_gg pc_content')

        # 提取并打印<div>标签中的文本内容
        if div_tag:
            text_content = div_tag.get_text(strip=True)
            res += "盒子中的文本内容:" + text_content
        else:
            print("未找到指定的<div>标签")

        return res


if __name__ == '__main__':
    scraper = WebScraper()
    page_size = scraper.getPageSize()
    print("Page size:", page_size)
