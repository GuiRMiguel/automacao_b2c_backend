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
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": "Nao foi possivel acessar a URL"})
        except NoSuchElementException as exception:
            print(exception)
            self._dict_result.update({"obs": str(exception)})
        finally:
            self._driver.quit()
            return self._dict_result
    



