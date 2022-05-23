from pickle import FALSE, TRUE
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

<<<<<<< HEAD
    #29
    def changeIPDhcpViaWizard_29(self, flask_username):
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[1]/a').click() #DHCP
            time.sleep(2)
            #Changing IP
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').send_keys('15')
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[3]').send_keys('15')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[4]').send_keys('4')
            time.sleep(3)
            #renge-2
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[1]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[2]').send_keys('168')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[3]').send_keys('15')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[4]').send_keys('204')

            self._driver.find_element_by_xpath('//*[@id="btnDhcpSave"]/span').click()

            time.sleep(1)
            try:
                time.sleep(2)
                if self._driver.get('http://192.168.15.3/') ==None:
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
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/a').click()
            time.sleep(1)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')

            print("STARTING DOWNGRADE...")

            #Upload File
            self._driver.find_element_by_id('fileUpgradeByHTTP').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/BR_g12.6_RTF_TEF001_V7.15_V015')
            #Upgrade
            self._driver.find_element_by_xpath('/html/body/div/fieldset/fieldset[2]/form/p[6]/input').click()
            time.sleep(240)
                
            #Testing Downgrade Admin
            self._driver.get('http://' + self._address_ip + '/padrao')
            time.sleep(5)
            self.login_support()
            #Menu-Left
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')
            dw_sw_version = self._driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]').text
            print(dw_sw_version)

            if dw_sw_version=='BR_SV_g12.6_RTF_TEF001_V7.15_V015':
                downgrade = TRUE
            else:
                downgrade = FALSE

            print("...FINISHING DOWNGRADE")
            print("<<<<<<<<<<<>>>>>>>>>>")
            print("STARTING UPGRADE...")
            
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/a').click()
            time.sleep(1)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')
            #Upload File
            self._driver.find_element_by_id('fileUpgradeByHTTP').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/BR_g12.6_RTF_TEF001_V7.20_V016')
            #Upgrade
            self._driver.find_element_by_xpath('/html/body/div/fieldset/fieldset[2]/form/p[6]/input').click()
            time.sleep(240)

            #Testing Downgrade Admin
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(4)
            #Menu-Left
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')
            up_sw_version = self._driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]').text
            print(up_sw_version)

            if up_sw_version=='BR_g12.6_RTF_TEF001_V7.20_V016':
                upgrade = TRUE
            else: 
                upgrade = FALSE
            time.sleep(3)
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[6]/a').click()
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
            #NetInf
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


    def validiteDefaultModeAfterReset_48(self, flask_username):
        try:
            print("LOGGING /padrao")
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/a').click()
            time.sleep(1)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')

            print("STARTING DOWNGRADE...")

            #Upload File
            self._driver.find_element_by_id('fileUpgradeByHTTP').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/BR_g12.6_RTF_TEF001_V7.15_V015')
            #Upgrade
            self._driver.find_element_by_xpath('/html/body/div/fieldset/fieldset[2]/form/p[6]/input').click()
            time.sleep(240)
                
            #Testing Downgrade Admin
            self._driver.get('http://' + self._address_ip + '/padrao')
            time.sleep(5)
            self.login_support()
            #Menu-Left
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')
            dw_sw_version = self._driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]').text
            print(dw_sw_version)

            if dw_sw_version=='BR_SV_g12.6_RTF_TEF001_V7.15_V015':
                downgrade = TRUE
            else:
                downgrade = FALSE

            print("...FINISHING DOWNGRADE")

            def verificationAcsOnline():

                print("STARTING VERIFICATION ASC ONLINE...")

                self._driver.get('http://' + self._address_ip + '/')
                link = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
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
                time.sleep(1)
                print('\n#############################################'
                    '\n MENU >> STATUS'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS
                ### ------------------------------------------ ###
                status = self._driver.find_element_by_link_text('Status')
                print(status.text)
                status.click()
                time.sleep(1)
                print('\n#############################################'
                    '\n MENU >> STATUS >> GPON'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > GPON
                ### ------------------------------------------ ###
                gpon = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
                print('linha #445   ' + gpon)
                divOptical = self._driver.find_element_by_id('divOptical').text
                divOptical = divOptical.split("\n")
                print(divOptical)
                divOptRx = self._driver.find_element_by_id('divOptRx').text
                divOptRx = divOptRx.split("\n")
                print(divOptRx)
                divOptTx = self._driver.find_element_by_id('divOptTx').text
                divOptTx = divOptTx.split("\n")
                print(divOptTx)
                print('\n#############################################'
                    '\n MENU >> STATUS >> INTERNET'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > INTERNET
                ### ------------------------------------------ ###
                internet = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[3]/th/span').text
                print(internet)
                divPpp = self._driver.find_element_by_id('divPpp').text
                divPpp = divPpp.split("\n")
                print(divPpp)
                detalhes_internet = self._driver.find_element_by_link_text('Detalhes')
                print(detalhes_internet.text)
                detalhes_internet.click()
                detalhes_IPv4_head = self._driver.find_element_by_link_text('IPv4').text
                print(detalhes_IPv4_head)
                detalhes_IPv4 = self._driver.find_element_by_id('tabip-02')
                detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[1]')
                time.sleep(1)
                items_key_internet_ipv4 = detalhes_IPv4.find_elements_by_tag_name("li")
                detalhes_IPv4_nome = []
                for i in items_key_internet_ipv4:
                    teste = i.text
                    #print(i.text)
                    detalhes_IPv4_nome.append(teste)
                print(detalhes_IPv4_nome)
                detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[2]')
                items_key = detalhes_IPv4.find_elements_by_tag_name("li")
                detalhes_IPv4_valor = []
                for i in items_key:
                    teste = i.text
                    #print(i.text)
                    detalhes_IPv4_valor.append(teste)
                print(detalhes_IPv4_valor)
                time.sleep(2)
                detalhes_IPv6 = self._driver.find_element_by_link_text('IPv6')
                detalhes_IPv6.click()
                time.sleep(1)
                detalhes_IPv6_head = self._driver.find_element_by_link_text('IPv6').text
                print(detalhes_IPv6_head)
                detalhes_IPv6 = self._driver.find_element_by_id('tabip-02')
                detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[1]')
                time.sleep(1)
                items_key = detalhes_IPv6.find_elements_by_tag_name("li")
                detalhes_IPv6_nome = []
                for item in items_key:
                    teste = item.text
                    #print(item.text)
                    detalhes_IPv6_nome.append(teste)
                print(detalhes_IPv6_nome)
                detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[2]')
                items_key = detalhes_IPv6.find_elements_by_tag_name("li")
                detalhes_IPv6_valor = []
                for item in items_key:
                    teste = item.text
                    # print(item.text)
                    detalhes_IPv6_valor.append(teste)
                print(detalhes_IPv6_valor)
                time.sleep(2)
                print('\n#############################################'
                    '\n MENU >> STATUS >> WIFI 2.4GHz'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > WIFI 2.4GHz
                ### ------------------------------------------ ###
                wifi_24 = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[5]/th/span').text
                print(wifi_24)
                wifi_24_name = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[1]/div').text
                wifi_24_name = wifi_24_name.replace('\n',' ').split(' ')
                print(wifi_24_name)
                wifi_24_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/a')
                wifi_24_detalhes.click()
                wifi_24_detalhes_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[1]/div')
                items_key = wifi_24_detalhes_info.find_elements_by_tag_name("li")
                wifi_24_valor = []
                for item in items_key:
                    teste = item.text
                    # print(item.text)
                    wifi_24_valor.append(teste)
                print(wifi_24_valor)
                wifi_24_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[2]/textarea').get_attribute('value')
                print(wifi_24_detalhes_stations)
                time.sleep(2)
                print('\n#############################################'
                    '\n MENU >> STATUS >> WIFI 5GHz'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > WIFI 5GHz
                ### ------------------------------------------ ###
                wifi_5 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/th/span').text
                print(wifi_5)
                wifi_5_name = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/td[1]/div').text
                wifi_5_name = wifi_5_name.replace('\n', ' ').split(' ')
                print(wifi_5_name)
                wifi_5_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/td[2]/a')
                wifi_5_detalhes.click()
                wifi_5_detalhes_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[1]/div')
                items_key = wifi_5_detalhes_info.find_elements_by_tag_name("li")
                wifi_5_valor = []
                for item in items_key:
                    teste = item.text
                    # print(item.text)
                    wifi_5_valor.append(teste)
                print(wifi_5_valor)
                wifi_5_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[2]/textarea').get_attribute('value')
                wifi_5_detalhes_stations = wifi_5_detalhes_stations.split('\n')
                print(wifi_5_detalhes_stations)
                time.sleep(2)
                print('\n#############################################'
                    '\n MENU >> STATUS >> REDE LOCAL'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > REDE LOCAL
                ### ------------------------------------------ ###
                rede_local = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[9]/th/span').text
                print(rede_local)
                time.sleep(2)
                rede_local_name = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[9]/td[1]').text
                rede_local_name = rede_local_name.replace(' ', '')
                rede_local_name = rede_local_name.split('\n')
                rede_local_name_ok = {"LAN1": "NULL", "LAN2": "NULL", "LAN3": "NULL", "LAN4": "NULL"}
                indexLAN = 0
                index = 0
                for i in rede_local_name:
                    if i.startswith('LAN') == True:
                        indexLAN = indexLAN + 1
                        pos = 'LAN' + str(indexLAN)
                    else:
                        rede_local_name_ok[pos] = rede_local_name[index]
                    index = index + 1
                print(rede_local_name_ok)

                rede_local_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[9]/td[2]/a')
                rede_local_detalhes.click()
                rede_local_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[10]/td[2]/textarea').get_attribute('value')
                rede_local_stations = rede_local_stations.split('\n')
                # print(rede_local_stations)
                time.sleep(2)
                print('\n#############################################'
                    '\n MENU >> STATUS >> TV'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > TV
                ### ------------------------------------------ ###
                tv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/th/span').text
                print(tv)
                tv_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/td[2]/a').click()
                tv_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[12]/td[1]/div')
                items_key = tv_info.find_elements_by_tag_name("li")
                tv_valor = []
                for item in items_key:
                    teste = item.text
                    # print(item.text)
                    tv_valor.append(teste)
                print(tv_valor)
                tv_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[12]/td[2]/textarea').get_attribute('value')
                tv_stations = tv_stations.split('\n')
                print(tv_stations)
                time.sleep(2)
                print('\n#############################################'
                    '\n MENU >> STATUS >> TELEFONE'
                    '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > TELEFONE
                ### ------------------------------------------ ###
                telefone = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[13]/th/span').text
                print(telefone)
                telefone_info_rede = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[13]/td[1]/div[1]').text
                telefone_info_rede = telefone_info_rede.split('\n')
                print(telefone_info_rede)
                telefone_info_status = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[13]/td[1]/div[2]').text
                telefone_info_status = telefone_info_status.split('\n')
                print(telefone_info_status)
                telefone_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/td[2]/a').click()
                telefone_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[14]/td[2]/textarea').get_attribute('value')
                telefone_stations = telefone_stations.split('\n')
                print(telefone_stations)
                time.sleep(2)
                            
                print('\n\n\n == Criando JSON de saída... == ')
                json_saida = {
                                "Status":
                                    {
                                    internet:
                                        {
                                            divPpp[0]: divPpp[1],
                                            detalhes_IPv4_head:
                                                {
                                                    detalhes_IPv4_nome[0]: detalhes_IPv4_valor[0]
                                                },
                                        },
                                    wifi_24:
                                        {
                                            wifi_24_valor[0]: wifi_24_valor[1],
                                            wifi_24_valor[2]: wifi_24_valor[3],
                                            wifi_24_valor[4]: wifi_24_valor[5],
                                            wifi_24_valor[6]: wifi_24_valor[7],
                                            "Estações Conectadas:": wifi_24_detalhes_stations
                                        },
                                    wifi_5:
                                        {
                                            wifi_5_valor[0]: wifi_5_valor[1],
                                            wifi_5_valor[2]: wifi_5_valor[3],
                                            wifi_5_valor[4]: wifi_5_valor[5],
                                            wifi_5_valor[6]: wifi_5_valor[7],
                                            "Estações Conectadas:": wifi_5_detalhes_stations
                                        },
                                    telefone:
                                        {
                                            telefone_info_rede[0]: telefone_info_rede[1],
                                            telefone_info_status[0]: telefone_info_status[1],
                                            "Estações Conectadas:": telefone_stations
                                        }
                                    }
                }
                print("...FINISHING ACS ONLINE")
                return json_saida

            json_saida_downgrade = verificationAcsOnline()
            print(json_saida_downgrade)
            print("<<<<<<<<<<<>>>>>>>>>>")
            print("STARTING UPGRADE...")
            
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            #Menu-Left
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/a').click()
            time.sleep(1)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')
            #Upload File
            self._driver.find_element_by_id('fileUpgradeByHTTP').send_keys('/home/automacao/Projects/automacao_b2c_backend/data/BR_g12.6_RTF_TEF001_V7.20_V016')
            #Upgrade
            self._driver.find_element_by_xpath('/html/body/div/fieldset/fieldset[2]/form/p[6]/input').click()
            time.sleep(240)

            #Testing Downgrade Admin
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(4)
            #Menu-Left
            self._driver.switch_to.frame('menuFrm')
            #FW Upgrade
            self._driver.find_element_by_xpath('/html/body/div[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')
            up_sw_version = self._driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]').text
            print(up_sw_version)

            if up_sw_version=='BR_g12.6_RTF_TEF001_V7.20_V016':
                upgrade = TRUE
            else: 
                upgrade = FALSE
            time.sleep(3)


            print("...FINISHING UPGRADE")

            json_saida_upgrade = verificationAcsOnline()
            print(json_saida_upgrade)
            try:
                if (downgrade and upgrade) and (json_saida_downgrade == json_saida_upgrade):
                    self._dict_result.update({"obs": "Teste passou. Dispositivo ativo e Online", "result":"passed", "Resultado_Probe": "OK"})

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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[3]/a').click()
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[4]/a').click()
            time.sleep(3)
            try:
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]').text == '7CDB984180E1' and self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]').text == '7C:DB:98:41:80:E1':
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
                self._dict_result.update({"obs": "Nao foi possivel acessar interface avacada pelas URLs", "result":"passed", "Resultado_Probe": "OK"})
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
                self._dict_result.update({"obs": "Nao foi possivel acessar interface avacada pelas URLs", "result":"passed", "Resultado_Probe": "OK"})
            return self._dict_result


    def changePasswordAccess_66(self, flask_username, new_password):

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


    def pingDifferNetwork_68(self, flask_username):
        site1 = f'http://{self._address_ip}/wancfg.cmd?action=view'
        site2 = 'http://192.168.1.1/wancfg.cmd?action=view'
=======
>>>>>>> b5ebdd1ecf993bcbb4883dff33cd037e8a156a32

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

            # Rebooting 
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/a').click()
            time.sleep(5)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrm')
            self._driver.find_element_by_id('btnReboot').click()
            time.sleep(3)
            self._driver.switch_to_alert().accept()
            time.sleep(5)
            try:
                self._driver.get('http://' + self._address_ip + '/')
            except Exception as e:
                print(e)
                time.sleep(240)
                self._driver.get('http://' + self._address_ip + '/padrao')
                time.sleep(4)

            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            time.sleep(1)
            user_input = self._driver.find_element_by_id('txtUser')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(3)
                
            # Entering on 2.4GHz WiFi settings
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

            # Entering on 5GHz WiFi settings
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

