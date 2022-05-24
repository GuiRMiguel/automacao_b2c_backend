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
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)
            
            # Desabling 5GHz WiFi
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="radWifiEn0"]').click()
            self._driver.find_element_by_id('btnBasSave').click()
            time.sleep(3)

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
    
    #TODO
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


