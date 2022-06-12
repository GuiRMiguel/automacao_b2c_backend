from pickle import FALSE, TRUE
import re
import time
import subprocess
from datetime import datetime
from ..AskeyBROADCOM import HGU_AskeyBROADCOM
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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from paramiko.ssh_exception import SSHException
import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config

session = MainSession()

mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()


class HGU_AskeyBROADCOM_functionalProbe(HGU_AskeyBROADCOM):


    # 17
    def checkSpeedEthernetCable_17(self, flask_username):
        """
            Check the transmission speed on the ethernet network cable
        :return : A dict with the result of the test
        """
        speed_test = "https://www.speedtest.net/"
        try:
            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # xx WiFi

            # Executing a Speed Test
            try:
                try:
                    self._driver.get(speed_test)
                    self._driver.set_load_page_timeout(10)
                    self._driver.execute_script("window.stop();")
                    self._driver.get(speed_test)
                except Exception as e:
                    print(e)
                    self._driver.get(speed_test)
                time.sleep(5)
                self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
                time.sleep(60)
                download_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
                upload_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text)
                print('#####################################################################')
                print('Download Speed   -   ', download_speed)
                print('Upload Speed     -   ', upload_speed)
                print('#####################################################################')
            except Exception as e:
                print(e)
            
            # Habling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'uo']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

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


    # 19
    def checkSpeed5GHz_19(self, flask_username):
        """
            Check the transmission speed on the ethernet network cable
        :return : A dict with the result of the test
        """
        speed_test = "https://www.speedtest.net/"
        try:
            # Entering on WiFi 5GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self.login_admin()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(1)
            
            # Enabling 5GHz WiFi
            self._driver.find_element_by_xpath('//*[@id="radWifiEn1"]').click()
            self._driver.implicitly_wait(10)
            pass_5g = str(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value'))
            if len(pass_5g) < 15:
                self._driver.find_element_by_id('btnBasSave').click()
                self._driver.switch_to_alert().accept()
                time.sleep(30)
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(30)

            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            
            # Disabling 2.4GHz WiFi
            self._driver.find_element_by_xpath('//*[@id="radWifiEn0"]').click()
            self._driver.implicitly_wait(10)
            pass_2g = str(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value'))
            if len(pass_2g) < 15:
                self._driver.find_element_by_id('btnBasSave').click()
                self._driver.switch_to_alert().accept()
                time.sleep(30)
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(30)

            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # xx WiFi
            time.sleep(5)

            # Executing a Speed Test
            try:
                try:
                    self._driver.get(speed_test)
                    self._driver.set_load_page_timeout(10)
                    self._driver.execute_script("window.stop();")
                    self._driver.get(speed_test)
                except Exception as e:
                    print(e)
                    self._driver.get(speed_test)
                time.sleep(5)
                self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
                time.sleep(90)
                download_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
                upload_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text)
                print('\n\n#####################################################################')
                print('Download Speed   -   ', download_speed)
                print('Upload Speed     -   ', upload_speed)
                print('#####################################################################\n\n')
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
        
            # Habling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'uo']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi


        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result



    # 24
    def testICMPv6_24(self, flask_username):
        """
            Perform ICMPv6 test at http://ipv6-test.com/
        :return : A dict with the result of the test
        """
        try:
            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down'])

            # Desabling Firewall
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)
            subprocess.run(['sudo', 'systemctl', 'stop', 'firewalld'])

            # Making a request
            self._driver.get('http://ipv6-test.com/')
            time.sleep(3)
            icmpv6_status = self._driver.find_element_by_xpath('//*[@id="v6_conn"]/tbody/tr[9]/td[1]/span')
            self._driver.implicitly_wait(10)
            icmpv6_status = icmpv6_status.text
            time.sleep(3)

            if icmpv6_status != 'Reachable':
                self._driver.quit()
                self._dict_result.update({"obs": 'O ICMP não está acessível'})
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
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down'])

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


    # 33 -> Check why the 2.4GHz and 5GHz WiFi channels aren't changing on status page
    def swapWiFiChannelandBandwidth_33(self, flask_username):
        """
            Swap WiFi Channel and Bandwidth and check if it was changed
        :return : A dict with the result of the test
        """
        channel_2g_exp = "11"
        channel_5g_exp = "36"
        try:
            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self.login_admin()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            
            # Desabling 2.4GHz WiFi
            self._driver.find_element_by_xpath('//*[@id="radWifiEn0"]').click()
            self._driver.implicitly_wait(10)
            pass_2g = str(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value'))
            if len(pass_2g) < 15:
                self._driver.find_element_by_id('btnBasSave').click()
                self._driver.switch_to_alert().accept()
                time.sleep(30)
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(30)

            # Performing changes on 2.4GHz WiFi
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a').click()
            time.sleep(15)
            select_bdw = Select(self._driver.find_element_by_id('selBandwidth'))
            self._driver.implicitly_wait(10)
            time.sleep(1)
            select_bdw.select_by_value('1')
            time.sleep(1)
            self._driver.find_element_by_id('btnAdvSave').click()
            time.sleep(30)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a').click()
            time.sleep(20)
            self._driver.implicitly_wait(10)
            select_channel = Select(self._driver.find_element_by_id('selChannel'))
            self._driver.implicitly_wait(10)
            select_channel.select_by_value(channel_2g_exp)
            time.sleep(1)
            self._driver.find_element_by_id('btnAdvSave').click()
            time.sleep(8)
            
            # Enabling 5GHz WiFi
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="radWifiEn1"]').click()
            pass_2g = str(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value'))
            if len(pass_2g) < 15:
                self._driver.find_element_by_id('btnBasSave').click()
                self._driver.switch_to_alert().accept()
                time.sleep(30)
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(30)

            # Performing changes on 5GHz WiFi
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a').click()
            time.sleep(15)
            select_channel = Select(self._driver.find_element_by_id('selChannel'))
            self._driver.implicitly_wait(10)
            select_channel.select_by_value(channel_5g_exp)
            time.sleep(1)
            try:
                self._driver.switch_to_alert().accept()
            except Exception as e:
                print(e)
            time.sleep(1)
            self._driver.find_element_by_id('btnAdvSave').click()
            time.sleep(1)
            try:
                self._driver.switch_to_alert().accept()
            except Exception as e:
                print(e)
            time.sleep(30)

            # Rebooting
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[3]/a').click()
            time.sleep(10)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/a/span').click()
            time.sleep(8)
            iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
            time.sleep(1)
            self._driver.switch_to.frame(iframe)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td/a[1]/span').click()
            time.sleep(10)
            try:
                self._driver.get('http://' + self._address_ip + '/')
            except Exception as e:
                print(e)
                time.sleep(180)

            # Entering on Status
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(8)

            self._driver.quit()
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
            
            """self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/td[2]/a').click()
            time.sleep(1)
            channel_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[1]/div/ul/li[8]').text
            channel_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[1]/div/ul/li[8]').text

            if channel_2g != channel_2g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O canal do WiFi 2.4GHz não foi alterado corretamente: esperado: {}, obtido: {}'.format(channel_2g_exp, channel_2g)})
            elif channel_5g != channel_5g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O canal do WiFI 5GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(channel_5g_exp, channel_5g)})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})"""
        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result


    # 44
    def acsURL_44(self, flask_username):
        """
            Validate the device's ACS URL to know which Platform the device is targeting. (WAN disconnected)
        :return : A dict with the result of the test
        """
        try:
            # Entering on Advanced Interface
            self._driver.get('http://' + self._address_ip + '/padrao')
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('loginfrm')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input').send_keys("support")
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/input').send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)

            # Entering on TR-069 Settings
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[68]/table/tbody/tr/td/a').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[77]/table/tbody/tr/td/a').click()
            time.sleep(3)

            # Looking for specific informations
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            acs_url = str(self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr[2]/td[2]/input').get_attribute('value'))
            acs_username = str(self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr[3]/td[2]/input').get_attribute('value'))
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
        ssid_2g_exp = 'VIVO-@UTO-2GHz'
        pass_2g_exp = '123$abc!de00123'
        ssid_5g_exp = 'VIVO-@UTO-5GHz'
        pass_5g_exp = '123#@abc<101234'

        # SSID and Password for advanced interface
        ssid_2g_adv_exp = 'V!VO-AUTO-2GHz'
        pass_2g_adv_exp = '987@#$<>abc1213'
        ssid_5g_adv_exp = 'V!VO-AUTO-5GHz'
        pass_5g_adv_exp = '987<>!jklm!@012'

        try:
            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self.login_admin()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(10)
                
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
                time.sleep(15)
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(15)
                
            # 1) 2.4/5GHz SSID cannot be set to "¨"
            time.sleep(20)
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('Test 1: passed')
                print('#########################################\n')
            
            # 2.1) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(' VIVO 2GHZ')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do primeiro caracter'})
            else:
                print('\n#########################################')
                print('Test 2.1: passed')
                print('#########################################\n')

            # 2.2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHZ ')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do último caracter'})
            else:
                print('\n#########################################')
                print('Test 2.2: passed')
                print('#########################################\n')

            # 3) 2.4/5GHz SSID cannot be set to double space character
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO  2GHz')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
            else:
                print('\n#########################################')
                print('Test 3: passed')
                print('#########################################\n')

            # Setting correct SSID
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(ssid_2g_exp)
            time.sleep(1)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/span')
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('Test 4: passed')
                print('#########################################\n')

            # 5) 2.4/5GHz password cannot be set as space character
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/span')
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou espaço vazio'})
            else:
                print('\n#########################################')
                print('Test 5: passed')
                print('#########################################\n')

            # Making changes on 5GHz WiFi Settings
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(10)
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
                time.sleep(15)
            else:
                self._driver.find_element_by_id('btnBasSave').click()
                time.sleep(15)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 5GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('5GHZ Test 1: passed')
                print('#########################################\n')
            
            # 2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys(' VIVO 5GHZ')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz aceitou um espaço vazio no lugar do primeiro caracter'})
            else:
                print('\n#########################################')
                print('5GHZ Test 2.1: passed')
                print('#########################################\n')

            # 2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 5GHZ ')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz aceitou um espaço vazio no lugar do último caracter'})
            else:
                print('\n#########################################')
                print('5GHZ Test 2.2: passed')
                print('#########################################\n')

            # 3) 2.4/5GHz SSID cannot be set to double space character
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO  5GHz')
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/span')
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
            else:
                print('\n#########################################')
                print('5GHZ Test 3: passed')
                print('#########################################\n')

            # Setting correct SSID
            input_ssid_5g.clear()
            input_ssid_5g.send_keys(ssid_5g_exp)
            time.sleep(1)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/span')
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 5GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('5GHZ Test 4: passed')
                print('#########################################\n')

            # 5) 2.4/5GHz password cannot be set as space character
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/span')
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 5GHz aceitou espaço vazio'})
            else:
                print('\n#########################################')
                print('5GHZ Test 5: passed')
                print('#########################################\n')
             
            # Entering on Advanced Interface
            self._driver.get('http://' + self._address_ip + '/padrao')
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('loginfrm')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input').send_keys("support")
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/input').send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)

            # Entering on 2.4GHz WiFi Settings
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[46]/table/tbody/tr/td/a').click()
            time.sleep(8)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[47]/table/tbody/tr/td/a').click()
            time.sleep(5)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[49]/table/tbody/tr/td/a').click()
            time.sleep(8)

            # Performing changes on 2.4GHz
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            # Changing password
            pass_adv_2g_input = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[3]/table/tbody/tr/td[2]/input')
            time.sleep(1)
            if pass_adv_2g_input.get_attribute('value') != pass_2g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz não foi alterada corretamente:\nesperado: {}, \nobtido: {}'.format(pass_2g_exp, pass_adv_2g_input)})
            else:
                print('\n#########################################')
                print('2.4GHZ password changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[3]/table/tbody/tr/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td[2]/input').click()
            time.sleep(1)
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 4 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou ¨'})
                
            # 5) 2.4/5GHz password cannot be set as space character
            time.sleep(1)
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[3]/table/tbody/tr/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td[2]/input').click()
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 5 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou espaço vazio'})
            
            time.sleep(1)
            pass_adv_2g_input.clear()
            time.sleep(1)
            pass_adv_2g_input.send_keys(pass_2g_adv_exp)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td[2]/input').click()
            time.sleep(15)
            # Changing SSID
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[47]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            ssid_adv_2g_input = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            if ssid_adv_2g_input.get_attribute('value') != ssid_2g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(ssid_2g_exp, ssid_adv_2g_input)})
            else:
                print('\n#########################################')
                print('2.4GHZ SSID changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            time.sleep(3)
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 1 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou ¨'})
            
            # 2.1) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(' VIVO 2GHZ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 2.1 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do primeiro caracter'})

            # 2.2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHZ ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 2.2 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do último caracter'})
                
            # 3) 2.4/5GHz SSID cannot be set to double space character
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO  2GHz')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            time.sleep(1)
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 3 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
                
            # Setting correct SSID
            ssid_adv_2g_input.clear()
            time.sleep(1)
            ssid_adv_2g_input.send_keys(ssid_2g_adv_exp)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            time.sleep(15)

            # Entering on 5GHz WiFi Settings
            self._driver.switch_to.default_content()
            time.sleep(5)
            self._driver.switch_to.frame('menufrm')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[54]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            ssid_adv_5g_input = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            if ssid_adv_5g_input.get_attribute('value') != ssid_5g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(ssid_5g_exp, ssid_adv_5g_input)})
            else:
                print('\n#########################################')
                print('5GHz SSID changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            time.sleep(3)
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 1 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou ¨'})
            
            # 2.1) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys(' VIVO 2GHZ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 2.1 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do primeiro caracter'})

            # 2.2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 2GHZ ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 2.2 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do último caracter'})
                
            # 3) 2.4/5GHz SSID cannot be set to double space character
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[5]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO  2GHz')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
            time.sleep(1)
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 3 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
                
            # Setting correct SSID
            ssid_adv_5g_input.clear()
            ssid_adv_5g_input.send_keys(ssid_5g_adv_exp)
            time.sleep(1)
            try:
                self._driver.find_element_by_xpath('/html/body/blockquote/form/div[6]/table/tbody/tr/td/input').click()
                self._driver.switch_to.alert.accept()
                time.sleep(15)
            except Exception as e:
                print(e)

            # Changing password
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[56]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            pass_adv_5g_input = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[3]/table/tbody/tr/td[2]/input')
            time.sleep(1)
            if pass_adv_5g_input.get_attribute('value') != pass_5g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz não foi alterada corretamente:\nesperado: {}, \nobtido: {}'.format(pass_5g_exp, pass_adv_5g_input)})
            else:
                print('\n#########################################')
                print('5GHZ password changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[3]/table/tbody/tr/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td[2]/input').click()
            time.sleep(1)
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHZ Test 4 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou ¨'})
                
            # 5) 2.4/5GHz password cannot be set as space character
            time.sleep(1)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[3]/table/tbody/tr/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td[2]/input').click()
            try:
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHZ Test 5 ADVANCED: passed')
                print('#########################################\n')
            except Exception as e:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou espaço vazio'})
            pass_adv_5g_input.clear()
            time.sleep(1)
            pass_adv_5g_input.send_keys(pass_5g_adv_exp)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td[2]/input').click()
            time.sleep(15)

            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(8)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/input')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="btnLogin"]')
            time.sleep(2)
            login_button.click()
            time.sleep(10)

            # Checking SSID and password for 2.4GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            ssid_2g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_2g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_2g_adv_exp != ssid_2g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}'.format(ssid_2g_adv_exp, ssid_2g_adv)})
            elif pass_2g_adv_exp != pass_2g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 2.4GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}'.format(pass_2g_adv_exp, pass_2g_adv)})
            
            # Checking SSID and password for 5GHz WiFi
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(10)
            ssid_5g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_5g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_5g_adv_exp != ssid_5g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}'.format(ssid_5g_adv_exp, ssid_5g_adv)})
            elif pass_5g_adv_exp != pass_5g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 5GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}'.format(pass_5g_adv_exp, pass_5g_adv)})
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

    #29
    def changeIPDhcpViaWizard_29(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
        
            self.login_admin()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="menu-loc-net"]/ul/li[1]/a').click()
            time.sleep(2)
            
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[1]/a').click() #DHCP
            time.sleep(2)
            #Changing IP
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').send_keys('16')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[4]').send_keys('3')
            time.sleep(2)
            #Changing address range
            #range-1
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[3]').send_keys('16')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[4]').send_keys('4')
            time.sleep(3)
            #renge-2
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[3]').send_keys('16')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[4]').send_keys('204')

            if self._driver.find_element_by_xpath('//*[@id="btnDhcpSave"]/span').click():
                varOk = 'ok'

            
            try:
                if varOk == 'ok':
                    self._dict_result.update({"obs": f"Alterar range de IP do DHCP.", "result":"passed", "Resultado_Probe": "OK"})
                else:
                    self._dict_result.update({"obs": f"Erro ao associar alterar range do IP no DHCP pelo usuario.", "result":"passed", "Resultado_Probe": "NOK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  
    
    
    #32
    def UpgradeDowngradeFirmware_32(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            #self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            #Management
            print(1)
            self._driver.find_element_by_xpath('//*[@id="folder67"]/table/tbody/tr/td/a').click()
            time.sleep(1)
            #Update Software
            print(2)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[82]/table/tbody/tr/td/a').click()
            time.sleep(1)
            print(3)
            #FW update SW
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('basefrm')

            print("STARTING DOWNGRADE...")

            #Upload File
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table/tbody/tr/td[2]/input').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/askeyBroadcom/BR_SV_g000_R3505VWN1001_s36')
            #Update SW
            self._driver.find_element_by_xpath('/html/body/blockquote/form/p/input').click()
            time.sleep(240)

            #Testing Downgrade 
            self._driver.get('http://' + self._address_ip + '/padrao')
            time.sleep(5)
            self.login_support()
            #Menu-Left
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            time.sleep(5)
            #FW Upgrade
            self._driver.find_element_by_xpath('//*[@id="folder1"]/table/tbody/tr/td/a').click()
            time.sleep(3)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('basefrm')
            dw_sw_version = self._driver.find_element_by_xpath('/html/body/blockquote/form/b/table/tbody/tr[4]/td[2]').text
            print(dw_sw_version)

            if dw_sw_version=='BR_SV_g000_R3505VWN1001_s36':
                downgrade = True
            else:
                downgrade = False


            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('logofrm')
            print("Logout")
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/a').click()
            time.sleep(5)

            print("downgrade")
            print(downgrade)
            print("...FINISHING DOWNGRADE")
            print("<<<<<<<<<<<>>>>>>>>>>")
            print("STARTING UPGRADE...")


            
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left

            iframe = self._driver.find_element_by_xpath('/html/frameset/frame[1]')
            self._driver.switch_to.frame(iframe)

            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            time.sleep(5)
            print("uai?")
            #Management
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[67]/table/tbody/tr/td/a').click()
            time.sleep(1)
            #Update Software
            print(2)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[81]/table/tbody/tr/td/a').click()
            time.sleep(1)
            print(3)
            #FW update SW
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('basefrm')
            
            #Upload File
            self._driver.find_element_by_xpath('/html/body/blockquote/form/table/tbody/tr/td[2]/input').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/askeyBroadcom/BR_SV_g000_R3505VWN1001_s37')
            #Update SW
            self._driver.find_element_by_xpath('/html/body/blockquote/form/p/input').click()
            time.sleep(240)

            #Testing upgrade
            self._driver.get('http://' + self._address_ip + '/padrao')
            time.sleep(5)
            self.login_support()
            #Menu-Left
            iframe = self._driver.find_element_by_xpath('/html/frameset/frame[1]')
            self._driver.switch_to.frame(iframe)

            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('//*[@id="folder1"]/table/tbody/tr/td/a').click()
            time.sleep(3)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('basefrm')
            up_sw_version = self._driver.find_element_by_xpath('/html/body/blockquote/form/b/table/tbody/tr[4]/td[2]').text
            print(up_sw_version)

            if up_sw_version=='BR_SV_g000_R3505VWN1001_s37':
                upgrade = True
            else: 
                upgrade = False
            
            
            time.sleep(3)

            print("upgrade:")
            print(upgrade)
            print("...FINISHING UPGRADE")

            try:
                if downgrade and upgrade:
                    self._dict_result.update({"obs": "Teste passou. Up/Down de FW ok.", "result":"passed", "Resultado_Probe": "OK"})

                else:
                    self._dict_result.update({"obs": f"Teste falhou.", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  


    def validiteConectStbTv_41(self, flask_username):
        try:
            #Login
            self._driver.get('http://' + self._address_ip + '/')
            self.login_admin()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[6]/a').click()
            time.sleep(2)
            # #NetInf
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[2]/a').click()
            time.sleep(3)
            #Iframe Message Attention
            iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
            self._driver.switch_to.frame(iframe)
            #Click OK
            self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td/a[1]/span').click()
            #Configure NetInf
            self._driver.switch_to.default_content()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[6]/a').click()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[2]/td[2]/input').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[2]/td[2]/input').send_keys('-50')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[3]/td[2]/input').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[3]/td[2]/input').send_keys('150')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[4]/td[2]/input').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[4]/td[2]/input').send_keys('1300')

            #Save Configure NetInf
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[1]/tbody/tr[5]/td/a[2]/span').click()
            time.sleep(5)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[2]/tbody/tr[3]/td[2]/a[2]/span').click()
            time.sleep(100)
            try:
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/table[2]/tbody/tr[1]/td[3]/strong/label').text != 'HPNA desprevenido':
                    self._dict_result.update({"obs": "Teste passou. Net Inf validada.", "result":"passed", "Resultado_Probe": "OK"})

                else:
                    self._dict_result.update({"obs": f"Teste falhou.", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  

    
    def validiteSerialNumberAndMac_50(self, flask_username):
        try:
            #Login
            self._driver.get('http://' + self._address_ip + '/')
            self.login_admin()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            #Config.
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').click() 
            time.sleep(1)
            #Reiniciar
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[3]/a').click()
            time.sleep(1)
            
            #Reconfigurar
            self._driver.find_element_by_xpath('//*[@id="btn-clicktocall"]/span').click()
            time.sleep(3)
            print('antes do iframe')
            iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
            self._driver.switch_to.frame(iframe)
            #print(iframe)
            self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td/a[1]/span').click()
            time.sleep(300)
            #Verify serial number and MAC
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[4]/a').click()
            time.sleep(3)
            try:
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]').text == '94EAEAD5EF47' and self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]').text == '94:EA:EA:D5:EF:47':
                    self._dict_result.update({"obs": "Teste passou. Numero de serie e MAC da WAN corretos.", "result":"passed", "Resultado_Probe": "OK"})

                else:
                    self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  
    

    def validiteUrlsWancfgCmd_64(self, flask_username):
        try:
            site1 = f'http://{self._address_ip}/wancfg.cmd'
            site2 = 'http://192.168.1.1/wancfg.cmd'

            try:
                self._driver.get('http://' + self._address_ip + '/')
                self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
                time.sleep(1)
                self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
                time.sleep(1)
                self._driver.get('http://' + self._address_ip + '/login.asp')
                self._driver.switch_to.default_content()
                user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(self._username)
                pass_input = self._driver.find_element_by_id('txtPass')
                pass_input.send_keys(self._password)
                login_button = self._driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(2)
            except:
                loginVivo = 'falhou'

            try:
                self._driver.get(site1)
                time.sleep(5)
                self._driver.switch_to.frame('mainFrame')
                time.sleep(5)
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
                elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
                resultado1 = 'ok'

            except:
                resultado1 = 'falhou'
            
            try:
                self._driver.get(site2)
                time.sleep(2)
                self._driver.switch_to.default_content()
                user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys('support')
                pass_input = self._driver.find_element_by_id('txtPass')
                pass_input.send_keys(self._password)
                login_button = self._driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
                resultado2 = 'ok'
            except:
                resultado2 = 'falhou'

            try:
                #self._driver.quit()
                if (resultado1 == 'ok' or resultado2 == 'ok') and loginVivo == 'ok':
                    self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}"})
                else:
                    self._dict_result.update({"obs": "Nao foi possivel acessar interface avacada pelas URLs", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  
    


    def validiteUrlsWancfgCmdActionView_65(self, flask_username):
        site1 = f'http://{self._address_ip}/wancfg.cmd'
        site2 = 'http://192.168.1.1/wancfg.cmd'

        try:
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.get('http://' + self._address_ip + '/login.asp')
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(2)
        except:
            loginVivo = 'falhou'

        try:
            self._driver.get(site1)
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(5)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado1 = 'ok'

        except:
            resultado1 = 'falhou'
        
        try:
            self._driver.get(site2)
            time.sleep(2)
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys('support')
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado2 = 'ok'
        except:
            resultado2 = 'falhou'

        finally:
            #self._driver.quit()
            if (resultado1 == 'ok' or resultado2 == 'ok') and loginVivo == 'ok':
               self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}"})
            else:
                self._dict_result.update({"obs": "Nao foi possivel acessar interface avancada pelas URLs", "result":"passed", "Resultado_Probe": "OK"})
            return self._dict_result



    def changePasswordAccess_66(self, flask_username, new_password):

        def open_change_password(driver):
            driver.switch_to.default_content()
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            #Management
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').click() 
            time.sleep(1)
            # Change Password
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/a').click()
            time.sleep(1)

        def admin_authentication(driver, user, password):
            driver.switch_to.default_content()
            #Login
            self._driver.switch_to.frame('mainFrame')
            self.check_before_login()
            time.sleep(2)
            user_input = self._driver.find_element_by_xpath('//*[@id="txtUser"]')
            user_input.send_keys(user)
            pass_input = self._driver.find_element_by_xpath('//*[@id="txtPass"]')
            pass_input.send_keys(password)
            login_button = self._driver.find_element_by_xpath('//*[@id="btnLogin"]')
            time.sleep(2)
            login_button.click()
            time.sleep(1)

        def changing_password(driver, old_password, new_password):
            driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
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
            print("ola back 1")
            open_change_password(driver)
            print("ola back 2")
            print(' == Autenticando == ')
            admin_authentication(self._driver, user, new_password)
            time.sleep(5)
            changing_password(driver, new_password, old_password)
            print("ola back 3")


        self._driver.execute_script("window.alert = function() {};")
        
        print('\n\n == Abrindo URL == ')
        self._driver.get('http://' + self._address_ip + '/')


        if re.match(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$", new_password):
            print('SenhaAdmin de Entrada cumpre requisitos...')
            
            try:
                print(' == Solicitando troca de senha == ')
                open_change_password(self._driver)
                time.sleep(3)
                ########################################################################################
                print(' == Autenticando == ')
                admin_authentication(self._driver, self._username, self._password)
                time.sleep(5)

                #########################################################################################
                print(' == Troca de senha == ')
                changing_password(self._driver, self._password, new_password)

                
                time.sleep(5)
                self._driver.get('http://' + self._address_ip + '/')

                print(' == Troca para senha antiga == ')
                change_password_back(self._driver, self._username, self._password, new_password)

                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

            except Exception as exception:
                print(exception)
                self._dict_result.update({"obs": str(exception)})

            finally:
                print(' == Fim do teste == ')
                return self._dict_result

   # 68
    def connectFakeWizard_68(self, flask_username):
        site1 = f'http://{self._address_ip}/wancfg.cmd?action=view'
        site2 = 'http://192.168.1.1/wancfg.cmd?action=view'
        site3 = 'http://' + self._address_ip + '/'
        
        try:
            self._driver.get(site3)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.get('http://' + self._address_ip + '/login.asp')
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(2)
            loginVivo = 'ok'
            print(loginVivo)
        except:
            loginVivo = 'falhou'

        try:
            self._driver.get(site1)
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(5)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado1 = 'ok'

        except:
            resultado1 = 'falhou'
        
        try:
            self._driver.get(site2)
            time.sleep(2)
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys('support')
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado2 = 'ok'
        except:
            resultado2 = 'falhou'

        finally:
            #self._driver.quit()
            if (resultado1 == 'ok' or resultado2 == 'ok') and loginVivo == 'ok':
               self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}"})
            else:
                self._dict_result.update({"obs": "Nao foi possivel acessar interface avacada pelas URLs", "result":"passed", "Resultado_Probe": "OK"})
            return self._dict_result


    #69
    def changeAdminPassword_69(self, flask_username, new_password):

        def open_change_password(driver):
            driver.switch_to.default_content()
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            #Management
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').click() 
            time.sleep(1)
            # Change Password
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/a').click()
            time.sleep(1)

        def admin_authentication(driver, user, password):
            driver.switch_to.default_content()
            #Login
            self._driver.switch_to.frame('mainFrame')
            self.check_before_login()
            time.sleep(2)
            user_input = self._driver.find_element_by_xpath('//*[@id="txtUser"]')
            user_input.send_keys(user)
            pass_input = self._driver.find_element_by_xpath('//*[@id="txtPass"]')
            pass_input.send_keys(password)
            login_button = self._driver.find_element_by_xpath('//*[@id="btnLogin"]')
            time.sleep(2)
            login_button.click()
            time.sleep(1)

        def changing_password(driver, old_password, new_password):
            driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
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
            print("ola back 1")
            open_change_password(driver)
            print("ola back 2")
            print(' == Autenticando == ')
            admin_authentication(self._driver, user, new_password)
            time.sleep(5)
            changing_password(driver, new_password, old_password)
            print("ola back 3")


        self._driver.execute_script("window.alert = function() {};")
        
        print('\n\n == Abrindo URL == ')
        self._driver.get('http://' + self._address_ip + '/')


        if re.match(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$", new_password):
            print('SenhaAdmin de Entrada cumpre requisitos...')
            
            try:
                print(' == Solicitando troca de senha == ')
                open_change_password(self._driver)
                time.sleep(3)
                ########################################################################################
                print(' == Autenticando == ')
                admin_authentication(self._driver, self._username, self._password)
                time.sleep(5)

                #########################################################################################
                print(' == Troca de senha == ')
                changing_password(self._driver, self._password, new_password)

                
                time.sleep(5)
                self._driver.get('http://' + self._address_ip + '/')

                print(' == Troca para senha antiga == ')
                change_password_back(self._driver, self._username, self._password, new_password)

                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

            except Exception as exception:
                print(exception)
                self._dict_result.update({"obs": str(exception)})

            finally:
                print(' == Fim do teste == ')
                return self._dict_result

