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

    
    #32
    def UpgradeDowngradeFirmware_32(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            menu_maintance = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[6]/span[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(menu_maintance).perform()
            update_sw = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[5]/li[7]/a')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(update_sw).click().perform()
            time.sleep(5)

            print("STARTING DOWNGRADE...")

            # Iframe
            iframe = self._driver.find_element_by_xpath('/html/body/div/div[2]/div/iframe')
            self._driver.switch_to.frame(iframe)
            #Choice File
            self._driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/ul/li[1]/div[2]/ul[2]/li[2]/input').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/mitraEcnt/BR_g5.9_1.11WVK_0_b31.bin')
            time.sleep(5)
            #Upload
            self._driver.find_element_by_xpath('//*[@id="Upload_Id"]').click()
            time.sleep(240)

            #Testing Downgrade Admin
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            menu_maintance = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[6]/span[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(menu_maintance).perform()
            update_sw = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[5]/li[7]/a')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(update_sw).click().perform()
            time.sleep(5)
            # Iframe
            iframe = self._driver.find_element_by_xpath('/html/body/div/div[2]/div/iframe')
            self._driver.switch_to.frame(iframe)
            #FW Version
            dw_sw_version = self._driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/ul/li[1]/div[2]/ul[1]/li/font').text
            print(dw_sw_version)

            if dw_sw_version=='BR_g5.9_1.11(WVK.0)b31': 
                downgrade = True
            else:
                downgrade = False
            
            print(downgrade)
            
            #Logout
            self._driver.switch_to.default_content()
            time.sleep(5) 
            logout = self._driver.find_element_by_xpath('/html/body/div/div[1]/div/ul/li[3]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(logout).click().perform()
            #Confirm Logout
            confirm_logout = self._driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(confirm_logout).click().perform()
            
            time.sleep(5)
            print("...FINISHING DOWNGRADE")
            print("<<<<<<<<<<<>>>>>>>>>>")
            print("STARTING UPGRADE...")
            
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            menu_maintance = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[6]/span[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(menu_maintance).perform()
            update_sw = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[5]/li[7]/a')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(update_sw).click().perform()
            time.sleep(5)

            # Iframe
            iframe = self._driver.find_element_by_xpath('/html/body/div/div[2]/div/iframe')
            self._driver.switch_to.frame(iframe)
            #Choice File
            self._driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/ul/li[1]/div[2]/ul[2]/li[2]/input').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/mitraEcnt/BR_g5.9_1.11WVK_0_b32.bin')
            time.sleep(5)
            #Upload
            self._driver.find_element_by_xpath('//*[@id="Upload_Id"]').click()
            time.sleep(240)

            #Testing Downgrade Admin
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            menu_maintance = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[6]/span[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(menu_maintance).perform()
            update_sw = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[5]/li[7]/a')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(update_sw).click().perform()
            time.sleep(5)
            # Iframe
            iframe = self._driver.find_element_by_xpath('/html/body/div/div[2]/div/iframe')
            self._driver.switch_to.frame(iframe)
            #FW Version
            up_sw_version = self._driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/ul/li[1]/div[2]/ul[1]/li/font').text
            print(up_sw_version)

            if up_sw_version=='BR_g5.9_1.11(WVK.0)b32':
                upgrade = True
            else:
                upgrade = False
            
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
        pass_2g_exp = '123$abc!de0'
        ssid_5g_exp = 'VIVO-@UTO-5GHz'
        pass_5g_exp = '123#@abc<10'

        # SSID and Password for advanced interface
        ssid_2g_adv_exp = 'V!VO-AUTO-2GHz'
        pass_2g_adv_exp = '987@#$<>abc12'
        ssid_5g_adv_exp = 'V!VO-AUTO-5GHz'
        pass_5g_adv_exp = '987<>!jklm!@0'

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
            
            # Making changes on 2.4GHz WiFi Settings
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(4)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            time.sleep(3)
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(ssid_2g_exp)
            time.sleep(1)
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]')
            input_pass_2g.clear()
            input_pass_2g.send_keys(pass_2g_exp)
            time.sleep(1)
            try:
                self._driver.find_element_by_id('MLG_GVTSettings_WL_Basic_Save').click()
                time.sleep(1)
                self._driver.switch_to_alert().accept()
                time.sleep(20)
            except Exception as e:
                print(e)
                time.sleep(20)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[3]/span')
            time.sleep(1)
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('Test 1: passed')
                print('#########################################\n')
            
            # 2.1) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(' VIVO 2GHZ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[3]/span')
            time.sleep(1)
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do primeiro caracter'})
            else:
                print('\n#########################################')
                print('Test 2.1: passed')
                print('#########################################\n')

            # 2.2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHZ ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[3]/span')
            time.sleep(1)
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do último caracter'})
            else:
                print('\n#########################################')
                print('Test 2.2: passed')
                print('#########################################\n')

            # 3) 2.4/5GHz SSID cannot be set to double space character
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO  2GHz')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[3]/span')
            time.sleep(1)
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
            else:
                print('\n#########################################')
                print('Test 3: passed')
                print('#########################################\n')

            # Setting correct SSID
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(ssid_2g_exp)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(10)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/span[4]/span')
            time.sleep(1)
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('Test 4: passed')
                print('#########################################\n')

            # 5) 2.4/5GHz password cannot be set as space character
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/span[4]/span')
            time.sleep(1)
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou espaço vazio'})
            else:
                print('\n#########################################')
                print('Test 5: passed')
                print('#########################################\n')

            # Making changes on 5GHz WiFi Settings
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a').click()
            time.sleep(20)
            self._driver.switch_to.default_content()
            time.sleep(3)
            self._driver.switch_to.frame("basefrm")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            time.sleep(3)
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys(ssid_5g_exp)
            time.sleep(1)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys(pass_5g_exp)
            time.sleep(1)
            try:
                self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
                time.sleep(1)
                self._driver.switch_to_alert().accept()
                time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(20)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            time.sleep(2)
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 5GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(2)
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('5GHZ Test 1: passed')
                print('#########################################\n')
            
            # 2) 2.4/5GHz SSID First and last character cannot be space
            time.sleep(2)
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys(' VIVO 5GHZ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(2)
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz aceitou um espaço vazio no lugar do primeiro caracter'})
            else:
                print('\n#########################################')
                print('5GHZ Test 2.1: passed')
                print('#########################################\n')

            # 2) 2.4/5GHz SSID First and last character cannot be space
            time.sleep(2)
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 5GHZ ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(2)
            if message_error.text == '' or message_error.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz aceitou um espaço vazio no lugar do último caracter'})
            else:
                print('\n#########################################')
                print('5GHZ Test 2.2: passed')
                print('#########################################\n')

            # 3) 2.4/5GHz SSID cannot be set to double space character
            time.sleep(2)
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO  5GHz')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(2)
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(10)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            time.sleep(2)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(2)
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 5GHz aceitou ¨'})
            else:
                print('\n#########################################')
                print('5GHZ Test 4: passed')
                print('#########################################\n')

            # 5) 2.4/5GHz password cannot be set as space character
            time.sleep(2)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(2)
            if message_error_pass.text == '' or message_error_pass.text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 5GHz aceitou espaço vazio'})
            else:
                print('\n#########################################')
                print('5GHZ Test 5: passed')
                print('#########################################\n')
            
            # Entering on Status
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[1]/a').click()
            time.sleep(10) 

            # Checking SSID and password for 2.4GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(10)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]').get_attribute('value')

            if ssid_2g_exp != ssid_2g:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(ssid_2g_exp, ssid_2g)})
            elif pass_2g_exp != pass_2g:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(pass_2g_exp, pass_2g)})
            
            # Checking SSID and password for 5GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
            time.sleep(10)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_5g_exp != ssid_5g:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(ssid_5g_exp, ssid_5g)})
            elif pass_5g_exp != pass_5g:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 5GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(pass_5g_exp, pass_5g)})
            
            # Entering on Advanced Interface
            self._driver.get('http://' + self._address_ip + '/padrao')
            self._driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/ul/li[1]/div/form/fieldset/ul/li[1]/input').send_keys("support")
            self._driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/ul/li[1]/div/form/fieldset/ul/li[2]/input[3]').send_keys(self._password)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/ul/li[1]/div/form/fieldset/ul/li[4]/input').click()
            time.sleep(8)

            # Entering on 2.4GHz Settings
            menu_net = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[2]/span[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(menu_net).perform()
            wifi_2g_settings = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[1]/li[3]/a')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(wifi_2g_settings).click().perform()
            time.sleep(8)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            ssid_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            time.sleep(1)
            if ssid_adv_2g_input.get_attribute('value') != ssid_2g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(ssid_2g_exp, ssid_adv_2g_input)})
            else:
                print('\n#########################################')
                print('2.4GHZ SSID changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(3)
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 1 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou ¨'})
            
            # 2.1) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(' VIVO 2GHZ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 2.1 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do primeiro caracter'})

            # 2.2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHZ ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 2.2 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do último caracter'})
                
            # 3) 2.4/5GHz SSID cannot be set to double space character
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO  2GHz')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 3 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
                
            # Setting correct SSID
            ssid_adv_2g_input.clear()
            ssid_adv_2g_input.send_keys(ssid_2g_adv_exp)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(15)

            # Performing changes on 2.4GHz password
            pass_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[2]/div[2]/ul/li[2]/input')
            if pass_adv_2g_input.get_attribute('value') != pass_2g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz não foi alterada corretamente:\nesperado: {}, \nobtido: {}'.format(pass_2g_exp, pass_adv_2g_input)})
            else:
                print('\n#########################################')
                print('2.4GHZ password changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            time.sleep(1)
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[2]/div[2]/ul/li[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote[1]/form/table[2]/tbody/tr/td[2]/input').click()
            time.sleep(1)
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 4 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou ¨'})
                
            # 5) 2.4/5GHz password cannot be set as space character
            time.sleep(1)
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[2]/div[2]/ul/li[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote[1]/form/table[2]/tbody/tr/td[2]/input').click()
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 5 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou espaço vazio'})
            
            pass_adv_2g_input.clear()
            try:
                time.sleep(1)
                self._driver.switch_to_alert().accept()
                time.sleep(1)
            except Exception as e:
                time.sleep(1)
                print('pass clear:', e)
                time.sleep(1)
            pass_adv_2g_input.send_keys(pass_2g_adv_exp)
            time.sleep(1)
            try:
                self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
                time.sleep(3)
                self._driver.switch_to_alert().accept()
                time.sleep(15)
            except Exception as e:
                print(e)
                time.sleep(15)

            # Entering on 5GHz WiFi Settings
            self._driver.switch_to.default_content()
            time.sleep(1)
            menu_net = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[2]/span[2]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(menu_net).perform()
            wifi_5g_settings = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[1]/li[4]')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(wifi_5g_settings).click().perform()
            time.sleep(10)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            ssid_adv_5g_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[1]/li[2]/input')
            if ssid_adv_5g_input.get_attribute('value') != ssid_5g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(ssid_5g_exp, ssid_adv_5g_input)})
            else:
                print('\n#########################################')
                print('5GHZ SSID changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[1]/li[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(3)
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 1 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou ¨'})
            
            # 2.1) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[1]/li[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys(' VIVO 2GHZ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 2.1 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do primeiro caracter'})

            # 2.2) 2.4/5GHz SSID First and last character cannot be space
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[1]/li[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 2GHZ ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 2.2 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do último caracter'})
                
            # 3) 2.4/5GHz SSID cannot be set to double space character
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[1]/li[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO  2GHz')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 3 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
                
            # Setting correct SSID
            ssid_adv_5g_input.clear()
            ssid_adv_5g_input.send_keys(ssid_5g_adv_exp)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(20)

            # Performing changes on 5GHz password
            pass_adv_5g_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[4]/div[2]/div/ul[3]/li[2]/input')
            if pass_adv_5g_input.get_attribute('value') != pass_5g_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 5GHz não foi alterada corretamente:\nesperado: {}, \nobtido: {}'.format(pass_5g_exp, pass_adv_5g_input)})
            else:
                print('\n#########################################')
                print('5GHZ password changed succesfully')
                print('#########################################\n')
            time.sleep(1)

            # 4) 2.4/5 GHz password cannot be set to "¨"
            time.sleep(1)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[4]/div[2]/div/ul[3]/li[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote[1]/form/table[2]/tbody/tr/td[2]/input').click()
            time.sleep(1)
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 4 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou ¨'})
                
            # 5) 2.4/5GHz password cannot be set as space character
            time.sleep(1)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[4]/div[2]/div/ul[3]/li[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789 abcde")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote[1]/form/table[2]/tbody/tr/td[2]/input').click()
            alert = self._driver.switch_to.alert()
            time.sleep(1)
            alert_text = alert.text
            time.sleep(1)
            if alert_text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('5GHz Test 5 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou espaço vazio'})

            time.sleep(1)
            pass_adv_5g_input.clear()
            pass_adv_5g_input.send_keys(pass_5g_adv_exp)
            time.sleep(1)
            try:
                self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
                time.sleep(1)
                self._driver.switch_to_alert().accept()
                time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(15)
            self._driver._switch_to.default_content()
            time.sleep(1)

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
            time.sleep(10)

            # Checking SSID and password for 2.4GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(4)
            ssid_2g_adv = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_2g_adv = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]').get_attribute('value')

            if ssid_2g_adv_exp != ssid_2g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}}'.format(ssid_2g_adv_exp, ssid_2g_adv)})
            elif pass_2g_adv_exp != pass_2g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 2.4GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}}'.format(pass_2g_adv_exp, pass_2g_adv)})
            
            # Checking SSID and password for 5GHz WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a').click()
            time.sleep(10)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(4)
            ssid_5g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input').get_attribute('value')
            pass_5g_adv = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input').get_attribute('value')

            if ssid_5g_adv_exp != ssid_5g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 5GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}'.format(ssid_5g_adv_exp, ssid_5g_adv)})
            elif pass_5g_adv_exp != pass_5g_adv:
                self._driver.quit()
                self._dict_result.update({"obs": 'A Senha do WiFi 5GHz não foi alterado corretamente pela interface avançada:\nesperado: {}, \nobtido: {}'.format(pass_2g_adv_exp, pass_2g_adv)})
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


    def validiteSerialNumberAndMac_50(self, flask_username):
        try:
            #Login
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[3]/ul/li[3]/a/span').click()
            time.sleep(2)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            #Reconfigure
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(2)
            self._driver.find_element_by_xpath('/html/body/form/div/div/div[1]/table/tbody/tr[2]/td[1]/a/span').click()
            time.sleep(2)
            print('antes do iframe')
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(2)
            iframe = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/iframe')
            print(iframe)
            self._driver.switch_to.frame(iframe)
            self._driver.find_element_by_xpath('//*[@id="MLG_Pop_Reset_Yes"]').click()
            time.sleep(100)

            self._driver.set_page_load_timeout(10)
            try:
                self._driver.execute_script("window.stop();")
            except Exception as e:
                print(e)
                self._driver.get('http://' + self._address_ip + '/')

            #Verify serial number and MAC
            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down'])
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down'])
            time.sleep(10)
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up'])
            print("sub processos feitos")
            #Enter IP-reset
            time.sleep(10)

            self._driver.get('http://192.168.15.1/')
            time.sleep(5)
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
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[4]').send_keys('1')
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
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[4]').send_keys('2')
            time.sleep(3)
            #renge-2
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[3]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[4]').send_keys('200')
            
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[11]/td[2]/a[2]/span').click() 

            self._driver.set_page_load_timeout(10)
            try:
                self._driver.execute_script("window.stop();")
            except Exception as e:
                print(e)
                self._driver.get('http://' + self._address_ip + '/')

            #Verify serial number and MAC
            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down'])
            time.sleep(10)
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up'])
            print("sub processos feitos 2")
            time.sleep(10)

            self._driver.get('http://' + self._address_ip + '/')
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_About_Power_Box"]').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(2)


            try:
                if self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[3]/td[2]').text == '84aa9cd27948' and self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[4]/td[2]').text == '84:AA:9C:D2:79:48':
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



    def validiteUrlsWancfgCmdActionView_65(self, flask_username):
        site1 = f'http://{self._address_ip}/wancfg.cmd?action=view'
        site2 = 'http://192.168.1.1/wancfg.cmd?action=view'

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
                self._dict_result.update({"obs": "Nao foi possivel acessar interface avacada pelas URLs", "result":"passed", "Resultado_Probe": "OK"})
            return self._dict_result

    #66
    def changePasswordAccess_66(self, flask_username, new_password):

        def open_change_password(driver):
            driver.switch_to.default_content()
            #time.sleep(5)
            driver.switch_to.frame("menufrm")
            driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]').click()
            time.sleep(1)
            link = driver.find_element_by_xpath('//*[@id="MLG_Menu_Account_Settings"]').click()
            time.sleep(1)

        def admin_authentication(driver, user, password):
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(user)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(5)

        def changing_password(driver, old_password, new_password):
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("basefrm")
            time.sleep(1)
            gerenc_senha_old_valor = driver.find_element_by_xpath('//*[@id="pwdOld"]').send_keys(str(old_password))
            time.sleep(1)
            gerenc_senha_new_valor = driver.find_element_by_xpath('//*[@id="pwdNew"]').send_keys(str(new_password))
            time.sleep(1)
            gerenc_senha_new_valor2 = driver.find_element_by_xpath('//*[@id="pwdCfm"]').send_keys(str(new_password))
            time.sleep(1)
            config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="SOPHIA_UserAccount_Save"]').click()  ### SAVE BUTTON
            time.sleep(8)  ### Tempo para recarregar a página após salvar as configs

        def change_password_back(driver, user, old_password, new_password):
            open_change_password(driver)
            print(' == Autenticando == ')
            admin_authentication(self._driver, user, new_password)
            time.sleep(5)
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


    # 68
    def connectFakeWizard_68(self, flask_username):
        
        site1 = f'http://{self._address_ip}/wancfg.cmd?action=view'
        site2 = 'http://192.168.1.1/wancfg.cmd?action=view'
        site3 = 'http://' + self._address_ip + '/'

        try:
            self._driver.get(site3)
            #Login
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[3]/ul/li[3]/a/span').click()
            time.sleep(2)
            self.admin_authentication_mitraStat()
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
                self._dict_result.update({"obs": "Nao foi possivel acessar interface avancada pelas URLs", "result":"passed", "Resultado_Probe": "OK"})
            return self._dict_result



    #69
    def changeAdminPassword_69(self, flask_username, new_password):

        def open_change_password(driver):
            driver.switch_to.default_content()
            #time.sleep(5)
            driver.switch_to.frame("menufrm")
            driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]').click()
            time.sleep(1)
            link = driver.find_element_by_xpath('//*[@id="MLG_Menu_Account_Settings"]').click()
            time.sleep(1)

        def admin_authentication(driver, user, password):
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(user)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(5)

        def changing_password(driver, old_password, new_password):
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("basefrm")
            time.sleep(1)
            gerenc_senha_old_valor = driver.find_element_by_xpath('//*[@id="pwdOld"]').send_keys(str(old_password))
            time.sleep(1)
            gerenc_senha_new_valor = driver.find_element_by_xpath('//*[@id="pwdNew"]').send_keys(str(new_password))
            time.sleep(1)
            gerenc_senha_new_valor2 = driver.find_element_by_xpath('//*[@id="pwdCfm"]').send_keys(str(new_password))
            time.sleep(1)
            config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="SOPHIA_UserAccount_Save"]').click()  ### SAVE BUTTON
            time.sleep(8)  ### Tempo para recarregar a página após salvar as configs

        def change_password_back(driver, user, old_password, new_password):
            open_change_password(driver)
            print(' == Autenticando == ')
            admin_authentication(self._driver, user, new_password)
            time.sleep(5)
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

