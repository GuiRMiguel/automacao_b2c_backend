import re
import time
import subprocess
from datetime import datetime
# from types import Nonetype
#from tkinter.tix import Select
from ..AskeyECNT import HGU_AskeyECNT
from json import JSONEncoder
import json
import requests
import sys
import pandas as pd
from collections import namedtuple
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from paramiko.ssh_exception import SSHException
import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config

session = MainSession()

mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()


class HGU_AskeyECNT_functionalProbe(HGU_AskeyECNT):


    # 17
    def checkSpeedEthernetCable_17(self, flask_username):
        """
            Check the transmission speed on the ethernet network cable
        :return : A dict with the result of the test
        """
        speed_test = "https://www.speedtest.net/"
        try:
            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            user_input = self._driver.find_element_by_id('txtUser')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)
            
            # Desabling 2.4GHz WiFi

            self._driver.find_element_by_xpath('//*[@id="radWifiEn0"]').click()
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            self._driver.switch_to_alert().accept()
            
            # Desabling 5GHz WiFi
            time.sleep(3)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            self._driver.switch_to_alert().accept()

            self._driver.set_page_load_timeout(10)
            try:
                self._driver.execute_script("window.stop();")
            except Exception as e:
                print(e)
                self._driver.get('http://' + self._address_ip + '/')

            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down'])

            # Executing a Speed Test
            try:
                self._driver.get(speed_test)
                time.sleep(10)
                self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
                time.sleep(60)
                download_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
                upload_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text)
                print('#####################################################################')
                print('Download Speed   -   ', download_speed)
                print('Upload Speed     -   ', upload_speed)
                print('#####################################################################')
            except Exception as e:
                print(e)
            
            # Verificar a velocidade contratada
            down_speed_exp = 300
            up_speed_exp = 300

            if download_speed < 0.8*down_speed_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A velocidade de Download está abaixo do esperado'})
            elif upload_speed < 0.8*up_speed_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A velocidade de Upload está abaixo do esperado'})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result


    # 23
    def uninterruptedPing_23(self, flask_username):
        """
            Generate ping (IPv4 and IPv6) from machines connected via WiFi (2.4 and 5GHz) to the 
            IP of the box and external (Two different sites) ex. google for 6 hours
        :return : A dict with the result of the test
        """
        self._driver.get('http://ipv6-test.com/pingtest/')


    # 25
    def testStreaming_25(self, flask_username):
        """
            Play video connected to WiFi 2.4 and 5GHz for 1 hour (NetFlix and YouTube).
            Test with different equipment (PlayStation, Notebook, Cellular, etc...)
        :return : A dict with the result of the test
        """
        try:
            # Making a request
            self._driver.get('https://www.youtube.com/watch?v=dV_0KOMeejA&ab_channel=SamukaBoss')
            time.sleep(3)
            self._driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player').click()
            time.sleep(3)
            time.sleep(3600)
            self._driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player').click()
            time.sleep(3)
            progress_bar = self._driver.find_element_by_class_name('ytp-progress-bar')
            time_spent = int(progress_bar.get_attribute('aria-valuenow'))
            print(time_spent)
            time.sleep(2)
            if time_spent < 3599:
                self._driver.quit()
                self._dict_result.update({"obs": 'Ocorreu algum erro na reprodução do vídeo'})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result


    # 27
    def useWhatsAPP_27(self, flask_username):
        """
            Using the WPSApp app,Using the WPSApp app (available on the Play Store) to close a WiFi connection via WPS
        :return : A dict with the result of the test
        """
        try:
            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down'])

            # Making a request
            self._driver.get('https://web.whatsapp.com/')
            response = requests.get('https://web.whatsapp.com/').status_code
            time.sleep(2)

            if response != 200:
                self._driver.quit()
                self._dict_result.update({"obs": 'Não foi possível acessar o site'})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result

    
    # 33
    def swapWiFiChannelandBandwidth_33(self, flask_username):
        """
            Swap WiFi Channel and Bandwidth and check if it was changed
        :return : A dict with the result of the test
        """
        channel_2g_exp = "9"
        channel_5g_exp = "36"
        try:
            def enablingWiFi2G():
                self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
                time.sleep(1)
                self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').click()
                time.sleep(1)
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(3)
                self._driver.switch_to_alert().accept()

            def enablingWiFi5G():
                self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
                time.sleep(1)
                self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').click()
                time.sleep(1)
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(3)
                self._driver.switch_to_alert().accept()

            # Entering on Advanced Interface
            time.sleep(1)
            self._driver.get('http://' + self._address_ip + '/padrao')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input').send_keys("support")
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/input').send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)

            # Entering on 2.4GHz WiFi Settings
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[1]').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrm')
            select = Select(self._driver.find_element_by_id('adm_bandwidth'))
            select.select_by_value('2')
            self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[5]/input[2]').click()
            time.sleep(3)

            # Entering on 5GHz WiFi Settings
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrm')
            select = Select(self._driver.find_element_by_id('adm_bandwidth'))
            select.select_by_value('2')
            self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[6]/input[2]').click()
            time.sleep(3)

            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(1)
                
            #Entering on 2.4GHz advanced settings
            enablingWiFi2G()
            time.sleep(3)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(3)
            self._driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a").click()
            self._driver.implicitly_wait(10)
            select = Select(self._driver.find_element_by_id('selChannel'))
            select.select_by_value(channel_2g_exp)
            self._driver.find_element_by_id('btnAdvSave').click()
            time.sleep(3)

            #Entering on 5GHz advanced settings
            enablingWiFi5G()
            time.sleep(3)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(3)
            self._driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a").click()
            self._driver.implicitly_wait(10)
            select = Select(self._driver.find_element_by_id('selChannel'))
            select.select_by_value(channel_5g_exp)
            time.sleep(2)
            try:
                self._driver.find_element_by_id('btnAdvSave').click()
                time.sleep(5)
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                time.sleep(2)
                button = self._driver.find_element_by_id('btnChannelAccept')
                self._driver.execute_script("arguments[0].click();", button)
                time.sleep(3)
            except Exception as e:
                print("exceção",e)
                self._driver.find_element_by_id('btnAdvSave').click()
                time.sleep(5)
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                time.sleep(2)
                button = self._driver.find_element_by_id('btnChannelAccept')
                self._driver.execute_script("arguments[0].click();", button)
                time.sleep(3)
            
            # Entering on Status
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/td[2]/a').click()
            time.sleep(1)
            channel_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[1]/div/ul/li[8]').text
            channel_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[1]/div/ul/li[8]').text
            print(channel_2g, channel_5g)

            if channel_2g != channel_2g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O canal do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}}'.format(channel_2g_exp, channel_2g)})
            elif channel_5g != channel_5g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O canal do WiFI 5GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}}'.format(channel_5g_exp, channel_5g)})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result


    # 41
    def testNetInf_41(self, flask_username):
        """
            Perform Net Inf tests in the web GUI user interface on all access classes available for 
            the device under test (MEDIAROOM)
        :return : A dict with the result of the test
        """
        # Entering on WiFi 2.4GHz settings and sign in
        self._driver.get('http://' + self._address_ip + '/')
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[6]/a').click()
        time.sleep(1)
        user_input = self._driver.find_element_by_id('txtUser')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_id('txtPass')
        pass_input.send_keys(self._password)
        self._driver.find_element_by_id('btnLogin').click()
        time.sleep(3)


    # 44
    def acsURL_44(self, flask_username):
        """
            Validate the device's ACS URL to know which Platform the device is targeting. (WAN disconnected)
        :return : A dict with the result of the test
        """
        try:
            # Entering on Advanced Interface
            self._driver.get('http://' + self._address_ip + '/padrao')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input').send_keys("support")
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/input').send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)

            # Entering on TR-069 Settings
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[1]').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrm')
            acs_url = str(self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[2]/input').get_attribute('value'))
            acs_username = str(self._driver.find_element_by_xpath('/html/body/div/fieldset/form/fieldset/div[2]/input').get_attribute('value'))
            port_7015 = bool(re.search(":7015/", acs_url))
            time.sleep(2)

            if port_7015 is not True:
                self._driver.quit()
                self._dict_result.update({"obs": 'A porta 7015 não está na URL ACS'})
            elif acs_username == 'telefonica':
                self._driver.quit()
                self._dict_result.update({"obs": 'O username não é válido ("telefonica")'})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result


    # 46
    def performWiFiSetup_46(self, flask_username):
        """
            Make WiFi configurations using special characters (Ex.: !@#$%&<>), following the rules below:
                1) 2.4/5GHz SSID cannot be set to "¨"\n
                2) 2.4/5GHz SSID First and last character cannot be space\n
                3) 2.4/5GHz SSID cannot be set to double space character\n
                4) 2.4/5 GHz password cannot be set to "¨"\n
                5) 2.4/5GHz password cannot be set as space character\n
        :return : A dict with the result of the test
        """
        # SSID and Password for basic interface
        ssid_2g_exp = '!@# $%&<> <><@#$'
        pass_2g_exp = '!@2a#$%&<>!@#<>$%&'
        ssid_5g_exp = '<>#%$ !#@$ &&$%<>'
        pass_5g_exp = '&%$b#@4!<>!@#&$#!<>'

        # SSID and Password for advanced interface
        ssid_2g_adv_exp = '#@! %$%# <><>!!'
        pass_2g_adv_exp = '<>!a@6#$%&#@<>!@$<>!'
        ssid_5g_adv_exp = '?><>@#$ &&&%!@ <>'
        pass_5g_adv_exp = '<>!@#$%&!@#12as$$$#@'

        try:
            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            user_input = self._driver.find_element_by_id('txtUser')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)
                
            # Making changes on 2.4GHz WiFi Settings
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').click()
            time.sleep(3)
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(ssid_2g_exp)
            time.sleep(1)
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys(pass_2g_exp)
            time.sleep(1)
            if len(pass_2g_exp) < 15:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(3)
                self._driver.switch_to_alert().accept()
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(3)

            # Making changes on 5GHz WiFi Settings
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').click()
            time.sleep(3)
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys(ssid_5g_exp)
            time.sleep(1)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys(pass_5g_exp)
            time.sleep(1)
            if len(pass_5g_exp) < 15:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(3)
                self._driver.switch_to_alert().accept()
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(3)
            
            # Entering on Status
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a').click()
            time.sleep(1) 

            # Checking SSID and password for 2.4GHz WiFi
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_2g_exp != ssid_2g:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}}'.format(ssid_2g_exp, ssid_2g)})
            elif pass_2g_exp != pass_2g:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}}'.format(pass_2g_exp, pass_2g)})
            
            # Checking SSID and password for 5GHz WiFi
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(1)
            ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_5g_exp != ssid_5g:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}}'.format(ssid_5g_exp, ssid_5g)})
            elif pass_5g_exp != pass_5g:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 5GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}}'.format(pass_5g_exp, pass_5g)})

            # Entering on Advanced Interface
            time.sleep(1)
            self._driver.get('http://' + self._address_ip + '/padrao')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input').send_keys("support")
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/input').send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)

            # Entering on 2.4GHz WiFi Settings
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[1]').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrm')
            self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/a').click()
            time.sleep(1)
            ssid_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/div[3]/input')
            ssid_adv_2g_input.clear()
            ssid_adv_2g_input.send_keys(ssid_2g_adv_exp)
            time.sleep(1)
            pass_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/fieldset[1]/div/div[4]/div[1]/input')
            pass_adv_2g_input.clear()
            pass_adv_2g_input.send_keys(pass_2g_adv_exp)
            self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/div[6]/input[5]').click()

            # Entering on 5GHz WiFi Settings
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrm')
            self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/a').click()
            time.sleep(1)
            ssid_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/div[3]/input')
            ssid_adv_2g_input.clear()
            ssid_adv_2g_input.send_keys(ssid_5g_adv_exp)
            time.sleep(1)
            pass_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/fieldset[1]/div/div[4]/div[1]/input')
            pass_adv_2g_input.clear()
            pass_adv_2g_input.send_keys(pass_5g_adv_exp)
            self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/div[6]/input[5]').click()
            time.sleep(3)
            self._driver._switch_to.default_content()
            time.sleep(1)

            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(3)

            # Checking SSID and password for 2.4GHz WiFi
            ssid_2g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_2g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_2g_adv_exp != ssid_2g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}}'.format(ssid_2g_adv_exp, ssid_2g_adv)})
            elif pass_2g_adv_exp != pass_2g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 2.4GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}}'.format(pass_2g_adv_exp, pass_2g_adv)})
            
            # Checking SSID and password for 5GHz WiFi
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(1)
            ssid_5g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_5g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_5g_adv_exp != ssid_5g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}}'.format(ssid_5g_adv_exp, ssid_5g_adv)})
            elif pass_5g_adv_exp != pass_5g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 5GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}}'.format(pass_2g_adv_exp, pass_2g_adv)})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result


    # 49
    def accessWebGui_49(self, flask_username):
        """
            Use the address http://1.1.1.1/ to access a Web Gui of the device under test
        :return : A dict with the result of the test
        """
        # Entering on http://1.1.1.1/ address
        try:
            self._driver.get('http://1.1.1.1/')
            time.sleep(2)
            try:
                if self._driver.find_element_by_xpath('/html/body/div[1]/div[1]/a') is not None:
                    if self._driver.find_element_by_xpath('/html/body/div[1]/div[1]/a').get_attribute('href') == 'https://www.vivo.com.br/':
                        self._driver.quit()
                        self._dict_result.update({"obs": 'A Web Gui do aparelho foi acessada}'})
                elif self._driver.current_url == 'http://' + self._address_ip + '/':
                    self._driver.quit()
                    self._dict_result.update({"obs": 'A Web Gui do aparelho foi acessada}'})
            except NoSuchElementException:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result


    # 68
    def connectFakeWizard_68(self, flask_username):

        site1 = "http://{address_ip}/wancfg.cmd?action=view".format(address_ip=self._address_ip)
        
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('site1 = ' + site1)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL ' + site1 + ' == ')
            self._driver.get(site1)
            time.sleep(5)
            print('\n\n == Aguardando redirecionamento de página == ')
            if self._driver.find_element_by_xpath('/html/body/h4'):
                result = self._driver.find_element_by_xpath('/html/body/h4').text
                print(result)
            time.sleep(1)
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        except NoSuchElementException as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result

    
    # 69
    def changeAdminPassword_69(self, flask_username, new_password):

        def open_change_password(driver):
            driver.switch_to.default_content()
            time.sleep(5)
            #driver.switch_to.frame("menufrm")
            driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
            time.sleep(1)
            link = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/a').click()
            time.sleep(1)

        def admin_authentication(driver, user, old_password):
            driver.switch_to.default_content()
            time.sleep(1)
            #driver.switch_to.frame("basefrm")
            user_input = driver.find_element_by_xpath('//*[@id="txtUser"]')
            user_input.send_keys(user)
            pass_input = driver.find_element_by_xpath('//*[@id="txtPass"]')
            pass_input.send_keys(old_password)
            login_button = driver.find_element_by_xpath('//*[@id="btnLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(1)

        def changing_password(driver, old_password, new_password):
            driver.switch_to.default_content()
            time.sleep(1)
            #driver.switch_to.frame("basefrm")
            time.sleep(1)
            gerenc_senha_old_valor = driver.find_element_by_xpath('//*[@id="txtOldPass"]').send_keys(str(old_password))
            time.sleep(1)
            gerenc_senha_new_valor = driver.find_element_by_xpath('//*[@id="txtNewPass"]').send_keys(str(new_password))
            time.sleep(1)
            gerenc_senha_new_valor2 = driver.find_element_by_xpath('//*[@id="txtConfirm"]').send_keys(str(new_password))
            time.sleep(1)
            config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnSave"]').click()  ### SAVE BUTTON
            time.sleep(8)  ### Tempo para recarregar a página após salvar as configs

        def change_password_back(driver, user, old_password, new_password):
            open_change_password(driver)
            changing_password(driver, new_password, old_password)

        self._driver.execute_script("window.alert = function() {};")
        
        print('\n\n == Abrindo URL == ')
        self._driver.get('http://' + self._address_ip + '/')


        if re.match(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$", new_password):
            print('SenhaAdmin de Entrada cumpre requisitos...')
            
            try:
                print(' == Solicitando troca de senha == ')
                open_change_password(self._driver)

                ########################################################################################
                print(' == Autenticando == ')
                admin_authentication(self._driver, self._username, self._password)
                time.sleep(5)

                #########################################################################################
                print(' == Troca de senha == ')
                changing_password(self._driver, self._password, new_password)

                
                time.sleep(5)
                self._driver.get('http://' + self._address_ip + '/')


                change_password_back(self._driver, self._username, self._password, new_password)

                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

            except Exception as exception:
                print(exception)
                self._dict_result.update({"obs": str(exception)})

            finally:
                print(' == Fim do teste == ')
                return self._dict_result

