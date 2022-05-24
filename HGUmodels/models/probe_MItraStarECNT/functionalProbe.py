import re
import time
import subprocess
from datetime import datetime
from ..MItraStarECNT import HGU_MItraStarECNT
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


class HGU_MItraStarECNT_functionalProbe(HGU_MItraStarECNT):
    

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
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            
            # Desabling 2.4GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(4)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)

            # Desabling 5GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(10)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            self._driver.implicitly_wait(15)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            time.sleep(3)
            self._driver.find_element_by_xpath('//*[@id="MLG_GVTSettings_5G_Basic_Save"]').click()
            time.sleep(8)

            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down'])

            # Executing a Speed Test
            try:
                self._driver.get(speed_test)
                time.sleep(1)
                self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
                time.sleep(60)
                download_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
                upload_speed = float(self._driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text)
                print('#####################################################################')
                print('Download Speed   -   ', download_speed)
                print('Upload Speed     -   ', upload_speed)
                print('#####################################################################')
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
            except Exception as e:
                    print(e)
            
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
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down'])

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
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down'])
            time.sleep(10)

            # Making a request
            self._driver.get('https://web.whatsapp.com/')
            response = requests.get('https://web.whatsapp.com/').status_code
            time.sleep(3)

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

    #29
    def changeIPDhcpViaWizard_29(self, flask_username):
        try:
            # Entering on local lan settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            #self._driver.get('http://192.168.17.3/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[2]/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            
            #Click DHCP
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/ul/li[1]/a').click()
            time.sleep(2)
            #Changing IP
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[3]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[4]').send_keys('3')
            time.sleep(2)
            #Changing address range
            #range-1
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[3]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[4]').send_keys('4')
            time.sleep(3)
            #renge-2
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[3]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[4]').send_keys('204')
            
            try:
                self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[11]/td[2]/a[2]/span').click() 
                self._dict_result.update({"obs": f"Alterar range de IP do DHCP.", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
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
            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(5)

            # Enabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(8)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("menufrm")
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_id('MLG_Menu_Wireless5G').click()
            time.sleep(3)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(20)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(20)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(15)

            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(2)

            # Changing channel 2.4GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/ul/li[2]/a').click()
            time.sleep(2)
            select_channel = Select(self._driver.find_element_by_id('select_Channel'))
            time.sleep(1)
            select_channel.select_by_value(channel_2g_exp)
            time.sleep(1)
            select_bdw = Select(self._driver.find_element_by_id('select_Bandwidth'))
            time.sleep(1)
            select_bdw.select_by_value('1')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[8]/td/a[2]/span').click()
            time.sleep(8)

            # Entering on 5GHz WiFi Settings
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("menufrm")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a').click()
            self._driver.implicitly_wait(10)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/ul/li[2]/a/span').click()
            time.sleep(2)
            select_channel = Select(self._driver.find_element_by_id('select_Channel_5G'))
            time.sleep(1)
            select_channel.select_by_value(channel_5g_exp)
            time.sleep(1)
            select_bdw = Select(self._driver.find_element_by_id('select_Bandwidth_5G'))
            time.sleep(1)
            select_bdw.select_by_value('2040auto')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(8)

            # Entering on Status
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/td[2]/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[7]/td[2]/a/span').click()
            time.sleep
            channel_2g = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[6]/td[1]/div/ul/li[8]').text
            channel_5g = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[8]/td[1]/div/ul/li[8]').text
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


    # 44
    def acsURL_44(self, flask_username):
        """
            Validate the device's ACS URL to know which Platform the device is targeting. (WAN disconnected)
        :return : A dict with the result of the test
        """
        try:
            # Entering on Advanced Interface
            self._driver.get('http://' + self._address_ip + '/padrao')
            self._driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/ul/li[1]/div/form/fieldset/ul/li[1]/input').send_keys("support")
            self._driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/ul/li[1]/div/form/fieldset/ul/li[2]/input[3]').send_keys(self._password)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/ul/li[1]/div/form/fieldset/ul/li[4]/input').click()
            time.sleep(3)

            # Entering on TR-069 Settings
            menu_maintance = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[6]/span[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(menu_maintance).perform()
            tr069_settings = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[5]/li[3]/a')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(tr069_settings).click().perform()
            time.sleep(5)

            # Looking for specific informations
            iframe = self._driver.find_element_by_xpath('/html/body/div/div[2]/div/iframe')
            self._driver.switch_to.frame(iframe)
            acs_url = str(self._driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/ul/li[1]/div[2]/ul/li[2]/input').get_attribute('value'))
            acs_username = str(self._driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/ul/li[1]/div[3]/ul/li[2]/input').get_attribute('value'))
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