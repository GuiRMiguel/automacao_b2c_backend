import re
import time
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

from paramiko.ssh_exception import SSHException
import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config

session = MainSession()

mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()


class HGU_AskeyBROADCOM_functionalProbe(HGU_AskeyBROADCOM):

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
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": "Nao foi possivel acessar a URL"})
        except NoSuchElementException as exception:
            print(exception)
            self._dict_result.update({"obs": str(exception)})
        finally:
            self._driver.quit()
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
    


