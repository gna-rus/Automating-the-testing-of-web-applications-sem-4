import functools
from datetime import timedelta, date

import pytest
import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests
from logger import log_all
import logging

FORMAT = '{levelname:<8} - {asctime}. В модуле "{name}" в строке {lineno:03d} функция "{funcName}()" в {created} секунд записала сообщение: {msg}'

logging.basicConfig(format=FORMAT, style='{',filename='project.log', filemode='w', level=logging.INFO) # сохранаяю результаты лоиггирования в отдельный файл

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Логгирование')
logger.info('___')

FORMAT = '{levelname:<8} - {asctime}. В модуле "{name}" в строке {lineno:03d} функция "{funcName}()" в {created} секунд записала сообщение: {msg}'
logging.basicConfig(format=FORMAT, style='{',filename='project.log.', filemode='w', encoding='utf-8', level=logging.INFO) # сохранаяю результаты лоиггирования в отдельный файл
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Логгирование')
logger.info('___')

with open("./locators.yaml") as f:
    locators = yaml.safe_load(f)

class Site:
    # проверка на то какой браузер используется в тесте
    def __init__(self, browser, address):
        logger.info('Инициализация теста')
        self.browser = browser
        self.address = address

        if self.browser == 'chrome':
            logger.info('Browser: Chrome')
            self.driver = webdriver.Chrome()
        elif self.browser == 'firefox':
            logger.info('Browser: Firefox')
            self.driver = webdriver.Chrome()

        self.driver.implicitly_wait(testdata['sleep_time'])
        self.driver.maximize_window()
        self.driver.get(address)


    def registration_on_the_website(self):
        x_selector1 = locators['LOCATOR_USER_NAME']  # вводим Username
        input1 = self.find_element("xpath", x_selector1)
        input1.send_keys(username)

        x_selector2 = locators['LOCATOR_PASSWORD']  # вводим passwd
        input2 = self.find_element("xpath", x_selector2)
        input2.send_keys(passwd)

        btn_selector = "button"
        btn = self.find_element("css", btn_selector)
        btn.click()

    def bed_registration_on_the_website(self):
        x_selector1 = locators['LOCATOR_USER_NAME']  # вводим Username
        input1 = self.find_element("xpath", x_selector1)
        input1.send_keys("test")

        x_selector2 = locators['LOCATOR_PASSWORD']  # вводим passwd
        input2 = self.find_element("xpath", x_selector2)
        input2.send_keys("test")

        btn_selector = "button"
        btn = self.find_element("css", btn_selector)
        btn.click()


    def find_element(self, mode, path):
        print(f'find element, {mode} = {path}')
        if mode == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, path)
        elif mode == "xpath":
            element = self.driver.find_element(By.XPATH, path)
        else:
            element = None
        return element

    def get_element_property(self, mode, path, property):
        element = self.find_element(mode, path)
        return element.value_of_css_property(property)

    def go_to_site(self):
        return self.driver.get(self.address)

    def close(self):
        self.driver.close()

class Side_API:

    def get_token(self):
        response_post = requests.post(testdata['url_login'], data={'username': testdata['username'], 'password': testdata['passwd']})
        return response_post.json()['token']

    def generate_post(self, token = 0):

        # функция создающая пост
        in_post = {"title": "test_title", "description": "test_description",
                   "content": "test_content"}  # передаваемые данные

        # передача поста (передается токкен регистрации и данные)
        response_post = requests.post(testdata['url_post'], headers={"X-Auth-Token": self.get_token()}, data=in_post)
        answer_code = response_post.status_code
        return response_post.json(), answer_code


    def find_post(self, token = 0):
        resource = requests.get(testdata['url_profil'], headers={"X-Auth-Token": self.get_token()})
        return resource.json()


    def get_post(self, token = 0):
        # возрвращае состояние поста
        resource = requests.get(testdata['url_post'], headers={"X-Auth-Token": self.get_token()}, params={"owner": "notMe"})
        return resource.json()

    def find_id(self, find_id = 0):
        # функция ищет переданный в нее id в посте
        result = self.get_post()
        flag = False
        for item in result['data']:
            print(item)
            if find_id == item['id']:
                flag = True
        return flag

# файл конфигурации теста
with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)
    browser = testdata["browser"]
    username = testdata['user_name']
    passwd = testdata['passwd']
    addres = testdata['addres']

# файл конфигурации теста
with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)
    browser = testdata["browser"]
    username = testdata['user_name']
    passwd = testdata['passwd']
    addres = testdata['addres']

test_API = Side_API()


def test_find_id():
    #Тест на поиск id в ответе
    assert test_API.find_id(98826) == True, 'Test of find id - False'

def test_generate_post_code():
    #Тест на определение кода ответа
    print(test_API.generate_post)
    assert test_API.generate_post()[1] == 200, 'Test code of generate post - False'

def test_generate_post_title():
    # Тест на поиск Title в созданном посте

    assert test_API.generate_post()[0]['title'] == 'test_title', 'Test: Title - False'

def test_generate_post_description():
    # Тест на поиск description в созданном посте
    assert test_API.generate_post()[0]['description'] == 'test_description', 'Test: Description - False'

def test_generate_post_content():
    # Тест на поиск content в созданном посте
    assert test_API.generate_post()[0]['content'] == 'test_content', 'Test: Content - False'

# def test_step1():
#     # Тест при не правильном вводе данных пользователя
#     site_bed = Site(testdata["browser"], testdata['addres'])
#     site_bed.bed_registration_on_the_website()
#
#     site_bed.driver.implicitly_wait(testdata['sleep_time'])
#
#     # /html/body/div/main/div/div/div[2]/h2
#     x_selector3 = locators['LOCATOR_ERROR_401']  # Поиск сообщения об ошибке после неверного ввода
#     err_label = site_bed.find_element("xpath", x_selector3)
#
#     print(err_label.text)
#     site_bed.driver.implicitly_wait(testdata['sleep_time'])
#     assert str(err_label.text) == '401'
#     site_bed.close()
#
#
# def test_step2(site_connect):
#     # Тест при правильном вводе данных пользователя
#
#     # Ищу слово Blog, которое высвечивается после успешной регистрации
#     site_connect.registration_on_the_website()
#     x_selector3 = locators['LOCATOR_WORD_BLOCK']
#     flag_text_blog = site_connect.find_element("xpath", x_selector3)
#     site_connect.driver.implicitly_wait(testdata['sleep_time'])
#     assert flag_text_blog.text == "Blog"
#
#
# def test_step3(site_connect):
#     # Тест создание нового поста
#
#     # Нажимаю на кнопку Нового поста
#
#     btn_selector = locators['LOCATOR_BOTTOM_NEWPOST']
#     btn = site_connect.find_element("xpath", btn_selector)
#     btn.click()
#     btn.click()
#
#     site_connect.driver.implicitly_wait(testdata['sleep_time'])
#
#     # Создание тайтла у поста
#     x_titel = locators['LOCATOR_TITEL_IN_NEWPOST']
#     input_titel = site_connect.find_element("xpath", x_titel)
#     input_titel.send_keys("test_titel")
#
#     # Создание дискрипшена
#     x_discription = locators['LOCATOR_DISCCRIPTION_IN_NEWPOST']
#     input_discription = site_connect.find_element("xpath", x_discription)
#     input_discription.send_keys("test_discription")
#
#     # Создание контента
#     x_content = locators['LOCATOR_CONTENT_IN_NEWPOST']
#     input_content = site_connect.find_element("xpath", x_content)
#     input_content.send_keys("test_content")
#
#     # Кликаю на кнопку Save
#     x_btm_save = locators['LOCATOR_BOTTOM_SAVE']
#     btn_save = site_connect.find_element("xpath", x_btm_save)
#     btn_save.click()
#
#     site_connect.driver.implicitly_wait(testdata['sleep_time'])
#
#     # Ищу название нового поста, если посту успешно будет создан то название поста будет верное
#     x_name_post =locators['LOCATOR_FIND_NAME_NEWPOST_CSS']
#     flag_name_post = site_connect.find_element("css", x_name_post)
#     site_connect.driver.implicitly_wait(testdata['sleep_time'])
#     print(f"{flag_name_post.text = } | {flag_name_post.text}")
#     time.sleep(2)
#
#     assert flag_name_post.text == "test_titel"
#
# def test_step4(site_connect):
#     a = True
#     btn_selector = locators['LOCATOR_BOTTOM_CONTACT']
#     btn = site_connect.find_element("xpath", btn_selector)
#     btn.click()
#     site_connect.driver.implicitly_wait(testdata['sleep_time'])
#
#     # Заполнить поле имени
#     x_name = locators['LOCATOR_YOUR_CONTACT_NAME']
#     input_name= site_connect.find_element("xpath", x_name)
#     input_name.send_keys("test_name")
#
#     # Заполнить поле email
#     x_email = locators['LOCATOR_YOUR_CONTACT_EMAIL']
#     input_email = site_connect.find_element("xpath", x_email)
#     input_email.send_keys("test_email@test")
#
#     # Заполнить поле contant
#     x_contant = locators['LOCATOR_YOUR_CONTACT_CONTENT']
#     input_contant = site_connect.find_element("xpath", x_contant)
#     input_contant.send_keys("TEST!")
#
#     # Кликнуть на кнопку Contact Us
#     btn_selector_contact = locators['LOCATOR_BOTTOM_IN_CONTACT_US']
#     btn_contact = site_connect.find_element("xpath", btn_selector_contact)
#     btn_contact.click()
#
#     site_connect.driver.implicitly_wait(testdata['sleep_time'])
#     time.sleep(1)
#
#     alert = site_connect.driver.switch_to.alert  # отлавливаю контекстное окно alert
#     alert_text = alert.text
#     site_connect.driver.implicitly_wait(testdata['sleep_time'])
#     alert.dismiss() # клик на кнопку ОК в alert
#
#     time.sleep(2)
#     assert alert_text == 'Form successfully submitted'

################


    #
# mail
# import smtplib
# from os.path import basename
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
#
# fromaddr = " address@mail.ru "
# to_address = " addresss@mail.ru "
# mypass = "bypass"
# report_name = "report.xml"
# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = to_address
# msg['Subject'] = "Привет от питона"
#
# # Формирования отчета-файла
# with open(report_name, "rb") as f:
#     part = MIMEApplication(f.read(), Name=basename(report_name))
#     part['Content-Disposition'] = 'attachment; filename="%s"' % basename(report_name)
#     msg.attach(part)
#
# body = "Это пробное сообщение"
# msg.attach(MIMEText(body, 'plain'))
#
# # Передача отчета-файла
# server = smtplib.SMTP_SSL(' smtp.mail.ru ', 465)
# server.login(fromaddr, mypass)
# text = msg.as_string()
# server.sendmail(fromaddr, to_address, text)
# server.quit()


log_all()


log_all()
