from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from datetime import datetime

# Import your utility functions as needed
from api.utils import *
class WebAutomation:
    def __init__(self, driver_path='D:\\chromedriver_win32\\chromedriver.exe'):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Use headless mode for Chrome
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.USERNAME = 'l32524'
        self.PASSWORD = 'Qw@114159266'

    def __del__(self):
        try:
            self.driver.quit()
        except Exception as e:
            print("Error while closing the driver: ", str(e))

    def anyInit(self):
        try:
            button = self.driver.find_element(By.XPATH,
                                              "//button[@class='el-button tools-text el-button--text el-button--mini']/span/span[text()='知识快读']")
            button.click()
            time.sleep(2)
            button = self.driver.find_element(By.XPATH,
                                              "//button[contains(@class, 'el-button--default') and contains(@class, 'el-button--mini') and contains(@class, 'is-plain') and contains(@class, 'is-round') and .//span[text()='网页链接']]")
            button.click()
            time.sleep(2)
        except NoSuchElementException:
            print("[anyInit] Element not found.")
        except ElementClickInterceptedException:
            print("[anyInit] Element not clickable.")

    def anyCancel(self):
        try:
            all_buttons = self.driver.find_elements(By.CLASS_NAME, 'el-button--text')
            if all_buttons:
                last_button = all_buttons[-1]
                last_button.click()
            else:
                print("No matching button elements found")
        finally:
            self.driver.quit()

    def AIh3cInit(self):
        try:
            self.driver.get('http://ai.h3c.com/')
            time.sleep(2)
            username_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入账号"]')
            username_field.clear()
            username_field.send_keys(self.USERNAME)
            password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入密码"]')
            password_field.clear()
            password_field.send_keys(self.PASSWORD)
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'div.loginIn.ripple')
            login_button.click()
            time.sleep(5)
        except NoSuchElementException:
            print("[AIh3cInit] Element not found.")
        except ElementClickInterceptedException:
            print("[AIh3cInit] Element not clickable.")

    def wait_for_elements(self, max_attempts=60, delay=1):
        attempts = 0
        while attempts < max_attempts:
            if self.check_elements():
                return True
            attempts += 1
            time.sleep(delay)
        return False

    def check_elements(self):
        try:
            span_element = self.driver.find_element(By.XPATH, "//span[contains(text(), '停止回答')]")
            if span_element:
                return False
        except NoSuchElementException:
            pass

        try:
            div_element = self.driver.find_element(By.XPATH,
                                                   "//div[contains(@class, 'text')]//div[@element-loading-spinner='el-icon-loading']")
            if div_element:
                return False
        except NoSuchElementException:
            pass

        return True

    def element_exists(self, text):
        try:
            self.driver.find_element(By.XPATH, f"//span[text()='{text}']")
            return True
        except NoSuchElementException:
            return False

    def analysisWeb(self, URL):
        try:
            input_element = self.driver.find_element(By.XPATH,
                                                     "//input[@placeholder='一次支持添加一个网址，请确保添加的网址符合合规要求']")
            input_element.clear()
            input_element.send_keys(URL)
            button = self.driver.find_element(By.XPATH,
                                              "//button[contains(@class, 'el-button') and contains(@class, 'el-button--default') and contains(@class, 'el-button--mini') and contains(@class, 'is-plain') and contains(@class, 'is-round') and span[text()='解析']]")
            button.click()
        except NoSuchElementException:
            print("[analysisWeb] Element not found.")
            return False
        except ElementClickInterceptedException:
            print("[analysisWeb] Element not clickable.")
            return False
        finally:
            time.sleep(10)
            return self.element_exists("已解析")

    def removeWebText(self):
        try:
            remove_button = self.driver.find_element(By.XPATH,
                                                     "//div[contains(@class, 'remove-btn') and .//i[contains(@class, 'el-icon-close')]]")
            remove_button.click()
            return True
        except NoSuchElementException:
            print("[removeWebText] Element not found.")
            return False
        except ElementClickInterceptedException:
            print("[removeWebText] Element not clickable.")
            return False

    def sendAsk(self, param):
        try:
            input_element = self.driver.find_element(By.ID, "common-chat_input")
            input_element.clear()
            input_element.send_keys(param)
            time.sleep(2)
            button = self.driver.find_element(By.XPATH,
                                              "//button[contains(@class, 'el-button') and contains(@class, 'el-button--primary') and contains(@class, 'el-button--small') and contains(@class, 'is-round') and .//i[@class='el-icon-s-promotion']]")
            button.click()
        finally:
            time.sleep(5)
            return self.wait_for_elements(max_attempts=10, delay=3)

    def getResult(self, callback=None):
        elements = self.driver.find_elements(By.CSS_SELECTOR,
                                             "div.info-wrapper.clearfix .text .common.html-content.no-pre-wrap.vditor-reset")
        if elements:
            latest_element = elements[-1]
            text_content = latest_element.text
            text_content = remove_whitespace_and_newlines(text_content)
            if callback:
                return callback(text_content)
            else:
                return text_content
        else:
            print("[getResult] No matching elements found.")
            return {}

    def todoAsk(self, ss):
        if not self.driver:
            self.driver = webdriver.Chrome()

        try:
            if len(ss) == 0:
                print('No usable URL found')
                return

            time.sleep(5)
            self.AIh3cInit()
            time.sleep(5)
            result = []
            failText = []
            cnt = 1
            for s, url in ss:
                print(f"{cnt} out of total {len(ss)}, time: {datetime.now()}")
                getDataStr = '帮我将上述内容总结为问题现象、问题描述、结论、解决办法,要求尽量详细'
                ask = self.sendAsk(s + getDataStr)
                if not ask:
                    print('Ask error or overTime')
                    failText.append([s, url])
                    continue
                time.sleep(2)
                data = {}
                temp = self.getResult(extract_problem_details)
                if temp == {}:
                    print('Ask error or overTime')
                    failText.append([s, url])
                    continue
                data.update(temp)
                data['原始网站'] = url
                data['备注'] = ''
                result.append(data)
                print(data)
                time.sleep(2)

                if cnt % 20 == 0:
                    save_result_to_file(result, getNowTimeStr() + 'AIresult1.txt')
                    result.clear()

                cnt += 1

            save_result_to_file(result, getNowTimeStr() + 'AIresult1.txt')
            save_result_to_file(failText, getNowTimeStr() + 'failText1.txt')
            print(result)
        finally:
            self.driver.quit()

    # Add other required methods as needed

def done(start, end):
    fileName = list_txt_files_sorted_by_creation_time(None, 'Odata.txt')[-1]
    ss = load_result_from_file(fileName)[start:end]
    webauto = WebAutomation()
    webauto.todoAsk(ss)

if __name__ == '__main__':
    fileName = list_txt_files_sorted_by_creation_time(None, 'Odata.txt')[-1]
    ss = load_result_from_file(fileName)[0:200]
    webauto = WebAutomation()
    webauto.todoAsk(ss)