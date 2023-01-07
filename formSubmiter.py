#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/07 17:57:58
# @Author: wd-2711
'''

import os
import yaml
import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from configLoader import getYamlData

class submitter:
    def __init__(self):
        config = getYamlData('config.yaml')

        self.site = config['FormUrl']
        self.username = config['UserName']
        self.passwd = config['PassWd']
        self.firefox_path = config['FirefoxPath']
        self.geck_path = config['GeckoDriverPath']
        self.image_path = config['FormImagePath']
        self.info_path = config['InfoPath']
        self.number = config['Number']

        self.model = None
        self.name_and_phone_data = []
        self.image_data = []
    
    def run(self):
        """
            0. Import config
            1. Load data
            2. Init webdriver
            3. Login account
            4. Start fill table
        """
        print("[+] Start formSubmiter.")
        self.__dataLoader()
        print("[+] Init selenium.")
        self.__init()
        print("[+] Login account {}.".format(self.username))
        self.__login()
        print("[+] Begin fill form...")
        self.__fillAndRepeat()
        print("[+] Done.")

    def __getYamlData(self, config_path):
        """
            Get SecretId and SecretKey from yaml.
        """
        with open(config_path, 'r', encoding = 'utf-8') as f:
            return yaml.load(f.read())

    def __init(self):
        """
            Define firefox and geckodriver path 
        """
        binaryPath = FirefoxBinary(self.firefox_path)
        self.model = webdriver.Firefox(executable_path = self.geck_path, firefox_binary = binaryPath)

    def __login(self):
        """
            Login by selenium
        """
        self.model.get('https://account.wps.cn')
        time.sleep(random.randrange(500, 2000)/1000)
        self.model.find_element_by_id('loginProtocal').click()
        time.sleep(random.randrange(500, 2000)/1000)
        self.model.find_element_by_css_selector("[class='f_icon icon_login_more']").click()
        time.sleep(random.randrange(500, 2000)/1000)
        self.model.find_element_by_id('account').click()
        time.sleep(random.randrange(2000, 4000)/1000)
        self.model.switch_to.frame(self.model.find_element_by_css_selector("[class='account_frame js_account_frame']"))
        self.model.find_element_by_id('SM_BTN_1').click()
        time.sleep(random.randrange(500, 2000)/1000)
        self.model.find_element_by_id('email').send_keys(self.username)
        time.sleep(random.randrange(500, 2000)/1000)
        self.model.find_element_by_id('password').send_keys(self.passwd)
        time.sleep(random.randrange(500, 2000)/1000)
        self.model.find_element_by_id('login').click()
        time.sleep(random.randrange(500, 2000)/1000)

    def __dataLoader(self):
        """
            Load data from 'info.txt', which created by infoExtracter
        """
        with open(self.info_path, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = eval(line)
            self.name_and_phone_data.append([line['name'], line['phone']])
        for f in os.listdir(self.image_path):
            self.image_data.append(os.path.join(self.image_path, f))
        return

    def __selecter(self):
        """
            Select name, phone, img_path for your need
        """
        choose = random.randrange(20, 100)
        np_len = len(self.name_and_phone_data)
        im_len = len(self.image_data)
        [name, phone] = self.name_and_phone_data[choose % np_len]
        img_path = self.image_data[choose % im_len]
        return name, phone, img_path

    def __fillAndRepeat(self):
        """
            Use data fill the table
        """
        self.model.get(self.site)
        time.sleep(random.randrange(2000, 4000)/1000)
        for i in range(self.number):
            name, phone, img_path = self.__selecter()
            print("[*] | Id: {:4} | Name: {:4} | Phone: {} | Img_path: {:20} |".format(i, name, phone, img_path))
            try:
                again = self.model.find_element_by_css_selector("[class='src-base-components-pc-button-index__button src-base-components-pc-button-index__confirm src-newform-pc-pages-form-write-components-FormPreview-index__btn']")
                again.click()
            except:
                pass
            time.sleep(random.randrange(4000, 5000)/1000)
            self.model.find_element_by_css_selector(".ant-input.pc-input_O7WzV.write-model-input_ybOWm").send_keys(name)
            time.sleep(random.randrange(1000, 2000)/1000)
            self.model.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div/div/div/div/div/div[6]/div/div[1]/div[3]/div/input").send_keys(phone)
            time.sleep(random.randrange(1000, 2000)/1000)
            self.model.find_element_by_xpath('//*[@type="file"]').send_keys(os.path.abspath(img_path))
            time.sleep(random.randrange(1000, 2000)/1000)
            try:
                self.model.find_element_by_xpath('/html/body/div[10]/div/div[2]/div').click()
            except:
                pass
            time.sleep(random.randrange(1000, 2000)/1000)
            self.model.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div/div/div/div/div/div[7]/div[1]/span[2]").click()
            time.sleep(random.randrange(3000, 4000)/1000)
            self.model.find_element_by_xpath("/html/body/div[10]/div/div[2]/div/div[2]/div[2]/div/div[2]/span[2]").click()
            time.sleep(random.randrange(1000, 2000)/1000)
            try:
                self.model.find_element_by_xpath("/html/body/div[10]/div/div[2]/div/div[2]/div[2]/div/div[2]/span[1]").click()
            except:
                pass
            time.sleep(random.randrange(1000, 2000)/1000)
            self.model.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div/div[4]/span[5]").click()
            time.sleep(random.randrange(2000, 4000)/1000)

if __name__ == "__main__":
    model = submitter()
    model.run()