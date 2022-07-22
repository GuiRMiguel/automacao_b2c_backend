import re
import time
import subprocess
from datetime import datetime
from ..MItraStarECNT import HGU_MItraStarECNT
from json import JSONEncoder
import paramiko
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from paramiko.ssh_exception import SSHException
import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config
from HGUmodels.models.Atuadoresutils.utils import atuadores


session = MainSession()

mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()


class HGU_MItraStarECNT_functionalProbe(HGU_MItraStarECNT):

    # 1
    def sequentialSwitchFiftyTimes_1(self, dados_entrada) -> dict:
        """
            Turn off the device switch 50 times with an interval of 2 seconds sequential. 
            After PPPoE synchronization and authentication, validate if it is online 
            in the ACS (Online in the CSC or respond to the HDM check device).
        :return : A dict with the result of the test
        """

        # Desabling other devices
        pwd = '4ut0m4c40'
        cmd = 'ls'
        subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

        subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
        subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
        subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
        subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
        subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
        subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
        time.sleep(15)

        ip_device = '172.18.192.1'
        number_of_cicles = 50
        timeInSeconds = 10
        timeDeactivate = 500
        timeActivate = 2500
        sleepHGU = 60
        sleepEthernet = 5
        try:
            ligaDesliga = atuadores.arduinoReguaLigaDesliga(self, dados_entrada['ip_arduino'], dados_entrada['rele'], timeDeactivate, timeActivate, number_of_cicles)
            if ligaDesliga[0] == 0:
                time.sleep(sleepHGU)
                hguResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', ip_device], stderr=subprocess.STDOUT, universal_newlines=True)
                hguLostPackets = int(hguResponse.split(',')[2].split('%')[0].strip())
                if hguLostPackets == 0:
                    time.sleep(sleepEthernet)
                    googleResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                    googleLostPackets = int(googleResponse.split(',')[2].split('%')[0].strip())
                    if googleLostPackets == 0:
                        self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
                    else:
                        self._dict_result.update({'obs': 'Conexão com a internet falhou'})
                else:
                    self._dict_result.update({'obs': 'HGU não retornou a conexão'})
            elif ligaDesliga[0] == -1:
                self._dict_result.update(ligaDesliga[1])

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            return self._dict_result
        
        except Exception as e:

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            print('Exception: ', e)
            self._dict_result.update({'obs': f'{e}'})
            return self._dict_result

    # 2
    def twoSecondsSwitchTwentyTimes_2(self, dados_entrada) -> dict:
        """
            Turn off the device switch 20 times with an interval of 2 seconds. 
            After PPPoE synchronization and authentication, validate if it is online 
            in the ACS (Online in the CSC or respond to the HDM check device).
        :return : A dict with the result of the test
        """

        # Desabling other devices
        pwd = '4ut0m4c40'
        cmd = 'ls'
        subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

        subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
        subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
        subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
        subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
        subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
        subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
        time.sleep(15)

        ip_device = '172.18.192.1'
        number_of_cicles = 20
        timeInSeconds = 10
        timeDeactivate = 500
        timeActivate = 2500
        sleepHGU = 60
        sleepEthernet = 5
        try:
            ligaDesliga = atuadores.arduinoReguaLigaDesliga(self, dados_entrada['ip_arduino'], dados_entrada['rele'], timeDeactivate, timeActivate, number_of_cicles)
            if ligaDesliga[0] == 0:
                time.sleep(sleepHGU)
                hguResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', ip_device], stderr=subprocess.STDOUT, universal_newlines=True)
                hguLostPackets = int(hguResponse.split(',')[2].split('%')[0].strip())
                if hguLostPackets == 0:
                    time.sleep(sleepEthernet)
                    googleResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                    googleLostPackets = int(googleResponse.split(',')[2].split('%')[0].strip())
                    if googleLostPackets == 0:
                        self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
                    else:
                        self._dict_result.update({'obs': 'Conexão com a internet falhou'})
                else:
                    self._dict_result.update({'obs': 'HGU não retornou a conexão'})
            elif ligaDesliga[0] == -1:
                self._dict_result.update(ligaDesliga[1])

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            return self._dict_result
        
        except Exception as e:

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            print('Exception: ', e)
            self._dict_result.update({'obs': f'{e}'})
            return self._dict_result

    # 3
    def ONTSwitchFiftyTimes_3(self, dados_entrada) -> dict:
        """
            Turn off the ONT switch 50 times sequentially
        :return : A dict with the result of the test
        """

        # Desabling other devices
        pwd = '4ut0m4c40'
        cmd = 'ls'
        subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

        subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
        subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
        subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
        subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
        subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
        subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
        time.sleep(15)

        ip_device = '172.18.192.1'
        number_of_cicles = 50
        timeInSeconds = 10
        timeDeactivate = 500
        timeActivate = 2500
        sleepHGU = 60
        sleepEthernet = 5
        try:
            ligaDesliga = atuadores.arduinoReguaLigaDesliga(self, dados_entrada['ip_arduino'], dados_entrada['rele'], timeDeactivate, timeActivate, number_of_cicles)
            if ligaDesliga[0] == 0:
                time.sleep(sleepHGU)
                hguResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', ip_device], stderr=subprocess.STDOUT, universal_newlines=True)
                hguLostPackets = int(hguResponse.split(',')[2].split('%')[0].strip())
                if hguLostPackets == 0:
                    time.sleep(sleepEthernet)
                    googleResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                    googleLostPackets = int(googleResponse.split(',')[2].split('%')[0].strip())
                    if googleLostPackets == 0:
                        self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
                    else:
                        self._dict_result.update({'obs': 'Conexão com a internet falhou'})
                else:
                    self._dict_result.update({'obs': 'HGU não retornou a conexão'})
            elif ligaDesliga[0] == -1:
                self._dict_result.update(ligaDesliga[1])
            
            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            return self._dict_result
        
        except Exception as e:

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            print('Exception: ', e)
            self._dict_result.update({'obs': f'{e}'})
            return self._dict_result


    # 4
    def twoSecondsSwitchTwentyTimesONT_4(self, dados_entrada) -> dict:
        """
            Turn off the ONT switch 20 times with an interval of 2 seconds
        :return : A dict with the result of the test
        """

        # Desabling other devices
        pwd = '4ut0m4c40'
        cmd = 'ls'
        subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

        subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
        subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
        subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
        subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
        subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
        subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
        time.sleep(15)
        
        ip_device = '172.18.192.1'
        number_of_cicles = 20
        timeInSeconds = 10
        timeDeactivate = 500
        timeActivate = 2500
        sleepHGU = 60
        sleepEthernet = 5
        try:
            ligaDesliga = atuadores.arduinoReguaLigaDesliga(self, dados_entrada['ip_arduino'], dados_entrada['rele'], timeDeactivate, timeActivate, number_of_cicles)
            if ligaDesliga[0] == 0:
                time.sleep(sleepHGU)
                hguResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', ip_device], stderr=subprocess.STDOUT, universal_newlines=True)
                hguLostPackets = int(hguResponse.split(',')[2].split('%')[0].strip())
                if hguLostPackets == 0:
                    time.sleep(sleepEthernet)
                    googleResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                    googleLostPackets = int(googleResponse.split(',')[2].split('%')[0].strip())
                    if googleLostPackets == 0:
                        self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
                    else:
                        self._dict_result.update({'obs': 'Conexão com a internet falhou'})
                else:
                    self._dict_result.update({'obs': 'HGU não retornou a conexão'})
            elif ligaDesliga[0] == -1:
                self._dict_result.update(ligaDesliga[1])
            
            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            return self._dict_result
        
        except Exception as e:

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            print('Exception: ', e)
            self._dict_result.update({'obs': f'{e}'})
            return self._dict_result


    # 5
    def STBSwitchFiftyTimes_5(self, dados_entrada) -> dict:
        """
            Turn off the STB switch 50 times sequentially
        :return : A dict with the result of the test
        """
        # Desabling other devices
        pwd = '4ut0m4c40'
        cmd = 'ls'
        subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

        subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
        subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
        subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
        subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
        subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
        subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
        time.sleep(15)

        ip_device = '172.18.192.1'
        number_of_cicles = 50
        timeInSeconds = 10
        timeDeactivate = 500
        timeActivate = 2500
        sleepHGU = 60
        sleepEthernet = 5
        try:
            ligaDesliga = atuadores.arduinoReguaLigaDesliga(self, dados_entrada['ip_arduino'], dados_entrada['rele'], timeDeactivate, timeActivate, number_of_cicles)
            if ligaDesliga[0] == 0:
                time.sleep(sleepHGU)
                hguResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', ip_device], stderr=subprocess.STDOUT, universal_newlines=True)
                hguLostPackets = int(hguResponse.split(',')[2].split('%')[0].strip())
                if hguLostPackets == 0:
                    time.sleep(sleepEthernet)
                    googleResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                    googleLostPackets = int(googleResponse.split(',')[2].split('%')[0].strip())
                    if googleLostPackets == 0:
                        self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
                    else:
                        self._dict_result.update({'obs': 'Conexão com a internet falhou'})
                else:
                    self._dict_result.update({'obs': 'HGU não retornou a conexão'})
            elif ligaDesliga[0] == -1:
                self._dict_result.update(ligaDesliga[1])
            
            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            return self._dict_result
        
        except Exception as e:

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            print('Exception: ', e)
            self._dict_result.update({'obs': f'{e}'})
            return self._dict_result


    # 6
    def twoSecondsSwitchTwentyTimesSTB_6(self, dados_entrada) -> dict:
        """
            Turn off the STB switch 20 times sequentially
        :return : A dict with the result of the test
        """
        # Desabling other devices
        pwd = '4ut0m4c40'
        cmd = 'ls'
        subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

        subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
        subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
        subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
        subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
        subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
        subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
        subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
        time.sleep(15)

        ip_device = '172.18.192.1'
        number_of_cicles = 20
        timeInSeconds = 10
        timeDeactivate = 500
        timeActivate = 2500
        sleepHGU = 60
        sleepEthernet = 5
        try:
            ligaDesliga = atuadores.arduinoReguaLigaDesliga(self, dados_entrada['ip_arduino'], dados_entrada['rele'], timeDeactivate, timeActivate, number_of_cicles)
            if ligaDesliga[0] == 0:
                time.sleep(sleepHGU)
                hguResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', ip_device], stderr=subprocess.STDOUT, universal_newlines=True)
                hguLostPackets = int(hguResponse.split(',')[2].split('%')[0].strip())
                if hguLostPackets == 0:
                    time.sleep(sleepEthernet)
                    googleResponse = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                    googleLostPackets = int(googleResponse.split(',')[2].split('%')[0].strip())
                    if googleLostPackets == 0:
                        self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
                    else:
                        self._dict_result.update({'obs': 'Conexão com a internet falhou'})
                else:
                    self._dict_result.update({'obs': 'HGU não retornou a conexão'})
            elif ligaDesliga[0] == -1:
                self._dict_result.update(ligaDesliga[1])
            
            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            return self._dict_result
        
        except Exception as e:

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            print('Exception: ', e)
            self._dict_result.update({'obs': f'{e}'})
            return self._dict_result


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

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
            time.sleep(15)

            try:
                try:
                    self._driver.set_page_load_timeout(15)
                    try:
                        self._driver.get(speed_test)
                        self._driver.execute_script("window.stop();")
                    except Exception as e:
                        print(e)
                        self._driver.get(speed_test)
                        self._driver.execute_script("window.stop();")
                    self._driver.get(speed_test)
                except Exception as e:
                    print(e)
                    self._driver.set_page_load_timeout(30)
                    self._driver.get(speed_test)
                time.sleep(5)
                self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
                time.sleep(60)
                print('\n\n#####################################################################')
                try:
                    time.sleep(1)
                    self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/a/svg/use').click()
                    time.sleep(3)
                except Exception as e:
                    print(e)
                download_speed = float(self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
                print(' -- Download Speed   -   ', download_speed)
                upload_speed = float(self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
                print(' -- Upload Speed     -   ', upload_speed)
                print('#####################################################################\n\n')
            except Exception as e:
                print(e)
            
            # Verificar a velocidade contratada
            down_speed_exp = 100
            up_speed_exp = 100

            if download_speed < 0.8*down_speed_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A velocidade de Download está abaixo do esperado'})
            elif upload_speed < 0.8*up_speed_exp:
                self._driver.quit()
                self._dict_result.update({"obs": 'A velocidade de Upload está abaixo do esperado'})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        
            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) # Old 15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) # Old 16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) # Old 17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) # Old 18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # MitraStar BROADCOM
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # MitraStar ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # Askey ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # Askey BROADCOM


        except Exception as exception:
            print(exception)
            self._driver.quit()
            if 'download_speed' in str(e):
                self._dict_result.update({"obs": 'Página speedtest.net não carregou corretamente'})
            else:
                self._dict_result.update({"obs": str(exception)})

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

        finally:
            return self._dict_result


    # 18
    def checkSpeed2GHz_18(self, flask_username):
        """
            Check the transmission speed on the WiFi 2.4 GHz
        :return : A dict with the result of the test
        """
        speed_test = "https://www.speedtest.net/"
        try:
            # Entering on WiFi 5GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(8)

            # Entering on WiFi 2.4GHz settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(5)

            # Desabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)
            ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            pass_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]')
            wifiSSID = ssid_2g.get_attribute('value')
            wifiPassword = pass_2g.get_attribute('value')
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(8)

            # Enabling WiFi
            subprocess.run(["nmcli", "dev", "wifi", "con", f"{wifiSSID}", "password", f"{wifiPassword}"])
            time.sleep(20)

            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # xx WiFi
            time.sleep(15)

            # Executing a Speed Test
            try:
                try:
                    self._driver.set_page_load_timeout(15)
                    self._driver.get(speed_test)
                    self._driver.execute_script("window.stop();")
                    self._driver.get(speed_test)
                    self._driver.execute_script("window.stop();")
                    self._driver.get(speed_test)
                except Exception as e:
                    print(e)
                    self._driver.set_page_load_timeout(30)
                    self._driver.get(speed_test)
                time.sleep(5)
                self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
                time.sleep(60)
                download_speed = float(self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
                upload_speed = float(self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
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
        
            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi


        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
            
            #  Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

        finally:
            self._driver.quit()
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
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)
            ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            wifiSSID = ssid_5g.get_attribute('value')
            wifiPassword = pass_5g.get_attribute('value')
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(8)

            # Entering on WiFi 2.4GHz settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(5)

            # Desabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(8)

            # Enabling WiFi
            subprocess.run(["nmcli", "dev", "wifi", "con", f"{wifiSSID}", "password", f"{wifiPassword}"])
            time.sleep(20)

            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # xx WiFi
            time.sleep(15)

            # Executing a Speed Test
            try:
                try:
                    self._driver.set_page_load_timeout(15)
                    self._driver.get(speed_test)
                    self._driver.execute_script("window.stop();")
                    self._driver.get(speed_test)
                    self._driver.execute_script("window.stop();")
                    self._driver.get(speed_test)
                except Exception as e:
                    print(e)
                    self._driver.set_page_load_timeout(30)
                    self._driver.get(speed_test)
                time.sleep(5)
                self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
                time.sleep(60)
                download_speed = float(self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
                upload_speed = float(self._driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
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
        
            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi


        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})

            #  Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

        finally:
            return self._dict_result


    # 23
    def uninterruptedPing_23(self, flask_username):
        """
            Generate ping (IPv4 and IPv6) from machines connected via WiFi (2.4 and 5GHz) to the 
            IP of the box and external (Two different sites) ex. google for 6 hours
        :return : A dict with the result of the test
        """

        timeInSeconds = 10
        try:
            # Entering on WiFi 5GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)
            ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            wifiSSID = ssid_5g.get_attribute('value')
            wifiPassword = pass_5g.get_attribute('value')
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(8)

            # Enabling WiFi
            subprocess.run(["nmcli", "dev", "wifi", "con", f"{wifiSSID}", "password", f"{wifiPassword}"])
            time.sleep(20)

            # Entering on WiFi 2.4GHz settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(5)

            # Desabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(8)

            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # xx WiFi
            time.sleep(15)

            # Executing the ping test 5GHz    
            print('INICIANDO PING NO 5GHz')     
            try:
                response5GHz = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                lostPackets5GHz = int(response5GHz.split(',')[2].split('%')[0].strip())
            except subprocess.CalledProcessError:
                lostPackets5GHz = -1

            if lostPackets5GHz > 0:
                self._driver.quit()
                self._dict_result.update({"obs": '% pacotes foram perdidos no 5GHz' % lostPackets5GHz})
            elif lostPackets5GHz < 0:
                self._driver.quit()
                self._dict_result.update({"obs": 'Except do subprocess do ping 5GHz'})
            
            # Entering on WiFi 5GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)

            # Disabling WiFi
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(8)

            # Entering on WiFi 2.4GHz settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(5)

            # Enabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)
            ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            pass_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]')
            wifiSSID = ssid_2g.get_attribute('value')
            wifiPassword = pass_2g.get_attribute('value')
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(10)

            # Enabling WiFi
            subprocess.run(["nmcli", "dev", "wifi", "con", f"{wifiSSID}", "password", f"{wifiPassword}"])
            time.sleep(20)

            # Executing the ping test 2GHz     
            print('INICIANDO PING NO 2.4GHz')      
            try:
                response2GHz = subprocess.check_output(['ping', '-w', str(timeInSeconds), '-q', 'google.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                lostPackets2GHz = int(response2GHz.split(',')[2].split('%')[0].strip())
            except subprocess.CalledProcessError:
                lostPackets2GHz = -1


            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            if lostPackets2GHz > 0:
                self._driver.quit()
                self._dict_result.update({"obs": '% pacotes foram perdidos no 2.4GHz' % lostPackets2GHz})
            elif lostPackets2GHz < 0:
                self._driver.quit()
                self._dict_result.update({"obs": 'Except do subprocess do ping 2.4GHz'})
            else:
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})


        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            self._driver.quit()
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

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
            time.sleep(15)


            
            # Desabling Firewall
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)
            subprocess.run(['sudo', 'systemctl', 'stop', 'firewalld'])
            subprocess.run(['sudo', 'ufw', 'disable'])

            # Making a request
            self._driver.get('http://ipv6-test.com/')
            time.sleep(3)
            try:
                icmpv6_status = self._driver.find_element_by_xpath('//*[@id="v6_conn"]/tbody/tr[9]/td[1]/span')
                self._driver.implicitly_wait(10)
                icmpv6_status = icmpv6_status.text

                if icmpv6_status != 'Reachable':
                    self._driver.quit()
                    self._dict_result.update({'result': 'NOK' ,"obs": 'O ICMP não está acessível'})
                else:
                    self._driver.quit()
                    self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

            except Exception as e:
                print(e)
                self._driver.quit()
                self._dict_result.update({"obs": 'O ICMP não está acessível'})
            time.sleep(3)


            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

            # Enabling Firewall
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)
            subprocess.run(['sudo', 'systemctl', 'enable', 'firewalld'])
            subprocess.run(['sudo', 'systemctl', 'start', 'firewalld'])

        except Exception as exception:
            print(exception)

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi
            
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})

        finally:
            return self._dict_result


    # 25
    def testStreaming_25(self, flask_username) -> dict:
        """
            Play video connected to WiFi 2.4 and 5GHz for 1 hour (NetFlix and YouTube).
            Test with different equipment (PlayStation, Notebook, Cellular, etc...)
        :return : A dict with the result of the test
        """
        timePlaying = 3600
        wifiSSID = "VIVO automacao Mitra ECNT"
        wifiPassword = "vivo12345678910"
        try:
            # Entering on WiFi 5GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)
            ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            ssid_5g.clear()
            ssid_5g.send_keys(wifiSSID)
            pass_5g.clear()
            pass_5g.send_keys(wifiPassword)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(8)

            # Entering on WiFi 2.4GHz settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(5)

            # Desabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(8)

            # Enabling WiFi
            subprocess.run(["nmcli", "dev", "wifi", "con", f"{wifiSSID}", "password", f"{wifiPassword}"])
            time.sleep(20)

            # Desabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # xx WiFi
            time.sleep(15)

            # Making a request
            self._driver.get('https://www.youtube.com/watch?v=dV_0KOMeejA&ab_channel=SamukaBoss')
            time.sleep(3)
            # self._driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player').click()
            # time.sleep(3)
            time.sleep(timePlaying)
            self._driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player').click()
            time.sleep(5)
            progress_bar = self._driver.find_element_by_class_name('ytp-progress-bar')
            time_spent = int(progress_bar.get_attribute('aria-valuenow'))
            time.sleep(2)
            print('\n###################################')
            print('-- Expected time: ', timePlaying, " --")
            print('-- Time spent: ', time_spent, " --")
            print('###################################')
            if time_spent < timePlaying:
                self._driver.quit()
                self._dict_result.update({"obs": 'Ocorreu algum erro na reprodução do vídeo'})
                return self._dict_result

            # Entering on WiFi 5GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
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

            # Disabling WiFi
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            self._driver.implicitly_wait(10)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(8)

            # Entering on WiFi 2.4GHz settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(5)

            # Enabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)
            ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            pass_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]')
            ssid_2g.clear()
            ssid_2g.send_keys(wifiSSID)
            pass_2g.clear()
            pass_2g.send_keys(wifiPassword)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(10)

            # Making a request
            self._driver.get('https://www.youtube.com/watch?v=dV_0KOMeejA&ab_channel=SamukaBoss')
            time.sleep(3)
            # self._driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player').click()
            # time.sleep(3)
            time.sleep(timePlaying)
            self._driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player').click()
            time.sleep(3)
            progress_bar = self._driver.find_element_by_class_name('ytp-progress-bar')
            time_spent = int(progress_bar.get_attribute('aria-valuenow'))
            time.sleep(2)
            print('\n###################################')
            print('-- Expected time: ', timePlaying, " --")
            print('-- Time spent: ', time_spent, " --")
            print('###################################')
            if time_spent < timePlaying:
                self._driver.quit()
                self._dict_result.update({"obs": 'Ocorreu algum erro na reprodução do vídeo'})
                return self._dict_result
            else:
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

            # Enabling other devices
            pwd = '4ut0m4c40'
            cmd = 'ls'
            subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'up']) #15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'up']) #16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'up']) #17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'up']) #18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'up']) # xx WiFi
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'up']) # xx WiFi

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

            subprocess.run(['sudo', 'ifconfig', 'ens192', 'down']) # Old 15
            subprocess.run(['sudo', 'ifconfig', 'ens256', 'down']) # Old 16
            subprocess.run(['sudo', 'ifconfig', 'ens193', 'down']) # Old 17
            subprocess.run(['sudo', 'ifconfig', 'ens257', 'down']) # Old 18
            subprocess.run(['sudo', 'ifconfig', 'ens160', 'down']) # MitraStar BROADCOM
            subprocess.run(['sudo', 'ifconfig', 'ens161', 'up'])   # MitraStar ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens224', 'down']) # Askey ECNT
            subprocess.run(['sudo', 'ifconfig', 'ens225', 'down']) # Askey BROADCOM
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


    # 29
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
            user_input.send_keys('admin')
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(5)
            
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


    # 30
    def useDMZ_30(self, flask_username):
        """
            Turn on DMZ
        :return : A dict with the result of the test
        """

        try:          
            # Entering on Config menu
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[2]/a/span').click()
            time.sleep(5)
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

            # Entering on Local Network
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/ul/li[3]/a').click()
            time.sleep(5)

            # Turn on DMZ
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[2]/div/table/tbody/tr[2]/td[2]/input[1]').click()
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            # Get IP Input
            ipInput = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[2]/div/table/tbody/tr[3]/td[2]/input')
            
            # Get IP Data
            ipSelected = ''
            try:
                ipsResponse = subprocess.check_output(['hostname', '-I'], stderr=subprocess.STDOUT, universal_newlines=True).split(' ')

                for ipItem in ipsResponse:
                    if "192.168.17" in ipItem:
                        ipSelected = ipItem
    
            except subprocess.CalledProcessError:
                lostPackets5GHz = -1
            
            ipInput.clear()
            ipInput.send_keys(ipSelected)

            try:
                # Confirm changes
                self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[2]/div/table/tbody/tr[4]/td/a[2]').click()
                time.sleep(4)
                self._driver.switch_to.frame(self._driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/iframe'))
                time.sleep(3)
                self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[4]/td/a[1]').click()
                time.sleep(60)
                print('\n-- Send command --\n')
                time.sleep(60)
                self._driver.get('http://' + self._address_ip + '/')
                time.sleep(3)
            except Exception as e:
                print(e)
                self._driver.get('http://' + self._address_ip + '/')

            publicIp = subprocess.check_output(['wget', '-qO-', 'http://ipecho.net/plain'], stderr=subprocess.STDOUT, universal_newlines=True)

            sshClient = paramiko.SSHClient()
            sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # ----------------------------------------- #
            # ----------------------------------------- #
            # -- Atualizar o IP, username e password -- #
            # ----------------------------------------- #
            # ----------------------------------------- #
            
            sshClient.connect('192.168.17.27', port=22, username='automacao', password='4ut0m4c40', timeout=3)

            stdin, stdout, stderr = sshClient.exec_command('telnet ' + str(publicIp) + ' 11002')

            endtime = time.time() + 30
            while not stdout.channel.eof_received:
                time.sleep(1)
                if time.time() > endtime:
                    stdout.channel.close()
                    break
            
            output = str(stdout.read())

            if output.find('Trying'):
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'It was not possible to connect'})

        except Exception as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            self._driver.quit()
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
            self._driver.implicitly_wait(20)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(30)
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
            time.sleep(30)

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

    
    # 32
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
            time.sleep(15)

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
            time.sleep(10)
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
                time.sleep(30)
            except Exception as e:
                print(e)
                time.sleep(30)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[1]')
            time.sleep(1)
            message_error_text = message_error.text
            time.sleep(1)
            if message_error_text == '' or message_error_text is None:
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
            message_error = self._driver.find_element_by_id('MLG_GVTSettings_WL_Error_SSID_Space_Char')
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
            message_error = self._driver.find_element_by_id('MLG_GVTSettings_WL_Error_SSID_Space_Char')
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
            message_error = self._driver.find_element_by_id('MLG_GVTSettings_WL_Error_SSID_Space_Char')
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

            # 4) 2.4/5 GHz password cannot be set to "¨"
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_pass_2g.clear()
            input_pass_2g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/span[3]')
            time.sleep(1)
            message_error_pass_text = message_error_pass.text
            time.sleep(1)
            if message_error_pass_text == '' or message_error_pass_text is None:
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
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/span[4]')
            time.sleep(1)
            message_error_pass_text = message_error_pass.text
            time.sleep(1)
            if message_error_pass_text == '' or message_error_pass_text is None:
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
            time.sleep(30)
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
                time.sleep(30)
            except Exception as e:
                print(e)
                time.sleep(30)

            # 1) 2.4/5GHz SSID cannot be set to "¨"
            time.sleep(2)
            input_ssid_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_ssid_5g.clear()
            input_ssid_5g.send_keys('VIVO 5GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[3]')
            time.sleep(1)
            message_error_text = message_error.text
            time.sleep(1)
            if message_error_text == '' or message_error_text is None:
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
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(1)
            message_error_text = message_error.text
            time.sleep(1)
            if message_error_text == '' or message_error_text is None:
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
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(1)
            message_error_text = message_error.text
            time.sleep(1)
            if message_error_text == '' or message_error_text is None:
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
            message_error = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/span[4]')
            time.sleep(1)
            message_error_text = message_error.text
            time.sleep(1)
            if message_error_text == '' or message_error_text is None:
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
            time.sleep(2)
            input_pass_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_pass_5g.clear()
            input_pass_5g.send_keys("123456789abcde¨")
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[7]/td/a[2]').click()
            time.sleep(3)
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/span[5]')
            time.sleep(1)
            message_error_pass_text = message_error_pass.text
            time.sleep(1)
            if message_error_pass_text == '' or message_error_pass_text is None:
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
            message_error_pass = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/span[4]')
            time.sleep(1)
            message_error_pass_text = message_error_pass.text
            time.sleep(1)
            if message_error_pass_text == '' or message_error_pass_text is None:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 5GHz aceitou espaço vazio'})
            else:
                print('\n#########################################')
                print('5GHZ Test 5: passed')
                print('#########################################\n')
            
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
            ssid_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input').get_attribute('value')
            time.sleep(1)
            
            # 1) 2.4/5GHz SSID cannot be set to "¨"
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHz ¨')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 1 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou ¨'})
            
            # 2.1) 2.4/5GHz SSID First and last character cannot be space
            time.sleep(2)
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(' VIVO 2GHZ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 2.1 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do primeiro caracter'})

            # 2.2) 2.4/5GHz SSID First and last character cannot be space
            time.sleep(2)
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO 2GHZ ')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 2.2 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou um espaço vazio no lugar do último caracter'})
                
            # 3) 2.4/5GHz SSID cannot be set to double space character
            time.sleep(2)
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')
            input_ssid_2g.clear()
            input_ssid_2g.send_keys('VIVO  2GHz')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 3 ADVANCED: passed')
                print('#########################################\n')
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz aceitou dois espaços vazios'})
            
            # Setting correct SSID
            time.sleep(1)
            input_ssid_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[2]/li[2]/input')          
            input_ssid_2g.clear()
            input_ssid_2g.send_keys(ssid_2g_adv_exp)
            time.sleep(1)

            # Performing changes on 2.4GHz password
            pass_adv_2g_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[2]/div[2]/ul/li[2]/input')
            print(pass_adv_2g_input.get_attribute('value'), pass_2g_exp)
            if pass_adv_2g_input.get_attribute('value') != pass_2g_exp:
                print('password')
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz não foi alterada corretamente:\nesperado: {}, \nobtido: {}'.format(pass_2g_exp, pass_adv_2g_input)})
            elif ssid_adv_2g_input != ssid_2g_exp:
                print('ssid')
                self._driver.quit()
                self._dict_result.update({"obs": 'O SSID do WiFi 2.4GHz não foi alterado corretamente:\nesperado: {}, \nobtido: {}'.format(ssid_2g_exp, ssid_adv_2g_input)})
            else:
                print('\n#########################################')
                print('2.4GHZ SSID changed succesfully')
                print('#########################################\n')
                print('\n#########################################')
                print('2.4GHZ password changed succesfully')
                print('#########################################\n')
            time.sleep(1)
            
            # 4) 2.4/5 GHz password cannot be set to "¨"
            time.sleep(1)            
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[2]/div[2]/ul/li[2]/input')           
            input_pass_2g.clear()
            try:
                input_pass_2g.send_keys("123456789abcde¨")
                self._driver.switch_to_alert().accept()
            except Exception as e:
                print(e)
                input_pass_2g.send_keys("123456789abcde¨")
                time.sleep(3)
            time.sleep(1)
            print('test 4')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 4 ADVANCED: passed')
                print('#########################################\n')
                try:
                    self._driver.switch_to_alert().accept()
                except Exception as e:
                    print(e)
            else:
                self._driver.quit()
                self._dict_result.update({"obs": 'A senha do WiFi 2.4GHz aceitou ¨'})
                
            # 5) 2.4/5GHz password cannot be set as space character
            time.sleep(1)
            input_pass_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[2]/div[2]/ul/li[2]/input')
            input_pass_2g.clear()
            try:
                input_pass_2g.send_keys("123456789 abcde")
                self._driver.switch_to_alert().accept()
            except Exception as e:
                print(e)
                input_pass_2g.send_keys("123456789 abcde")
                time.sleep(3)
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
                self._driver.switch_to_alert().accept()
                time.sleep(2)
                print('\n#########################################')
                print('Test 5 ADVANCED: passed')
                print('#########################################\n')
                try:
                    self._driver.switch_to_alert().accept()
                except Exception as e:
                    print(e)
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
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
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
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
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
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
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
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[3]/div/input[1]').click()
            time.sleep(1)
            alert_text = self._driver.switch_to_alert().text
            print(alert_text)
            time.sleep(1)
            if self._driver.switch_to_alert().text != "Wi-Fi clients may lose their connectivity with the gateway. Please connect again after the change has been updated.":
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
                time.sleep(15)
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
            print(ssid_2g_adv, pass_2g_adv)

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
            print(ssid_5g_adv, pass_2g_adv)

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


    # 48
    def validiteDefaultModeAfterReset_48(self, flask_username):
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

            def verificationAcsOnline():
                self._driver.get('http://' + self._address_ip + '/')
                time.sleep(2)
                try:
                    self.admin_authentication_mitraStat()
                except Exception as e:
                    print(e)
                time.sleep(5)
                self._driver.switch_to.default_content()
                time.sleep(1)
                self._driver.switch_to.frame('menufrm')
                time.sleep(1)
                self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
                time.sleep(2)
                self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a').click()
                time.sleep(2)
                try:
                    self.admin_authentication_mitraStat()
                except Exception as e:
                    print(3)

                print('\n#############################################'
                        '\n MENU >> STATUS'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS
                ### ------------------------------------------ ###
                self._driver.switch_to.frame('menufrm')
                self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[1]/a/span').click()
                time.sleep(2)
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                time.sleep(2)
                print('\n#############################################'
                        '\n MENU >> STATUS >> GPON'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > GPON
                ### ------------------------------------------ ###
                gpon = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/th/span').text
                print(gpon)
                divOptical = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]/div[1]').text
                divOptical = divOptical.split("\n")
                print(divOptical)
                divOptRx = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]/div[2]').text
                divOptRx = divOptRx.split("\n")
                print(divOptRx)
                divOptTx = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]/div[3]').text
                divOptTx = divOptTx.split("\n")
                print(divOptTx)
                print('\n#############################################'
                        '\n MENU >> STATUS >> INTERNET'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > INTERNET
                ### ------------------------------------------ ###
                internet = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/th/span').text
                print(internet)
                divPpp = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/td[1]/div').text
                divPpp = divPpp.split("\n")
                print(divPpp)
                detalhes_internet = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/td[2]/a/span')
                print(detalhes_internet.text)
                detalhes_internet.click()
                detalhes_IPv4_head = self._driver.find_element_by_link_text('IPv4').text
                print(detalhes_IPv4_head)
                detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[2]/div[1]')
                time.sleep(1)
                items_key_internet_ipv4 = detalhes_IPv4.find_elements_by_tag_name("li")
                detalhes_IPv4_nome = []
                for i in items_key_internet_ipv4:
                    teste = i.text
                    detalhes_IPv4_nome.append(teste)
                print(detalhes_IPv4_nome)
                detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[2]/div[2]')
                items_key = detalhes_IPv4.find_elements_by_tag_name("li")
                detalhes_IPv4_valor = []
                for i in items_key:
                    teste = i.text
                    detalhes_IPv4_valor.append(teste)
                print(detalhes_IPv4_valor)
                time.sleep(2)
                detalhes_IPv6 = self._driver.find_element_by_link_text('IPv6')
                detalhes_IPv6.click()
                time.sleep(1)
                detalhes_IPv6_head = self._driver.find_element_by_link_text('IPv6').text
                print(detalhes_IPv6_head)
                detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[3]/div[1]')
                time.sleep(1)
                items_key = detalhes_IPv6.find_elements_by_tag_name("li")
                detalhes_IPv6_nome = []
                for item in items_key:
                    teste = item.text
                    detalhes_IPv6_nome.append(teste)
                print(detalhes_IPv6_nome)
                detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[3]/div[2]')
                items_key = detalhes_IPv6.find_elements_by_tag_name("li")
                detalhes_IPv6_valor = []
                for item in items_key:
                    teste = item.text
                    detalhes_IPv6_valor.append(teste)
                print(detalhes_IPv6_valor)
                time.sleep(2)
                print('\n#############################################'
                        '\n MENU >> STATUS >> WIFI 2.4GHz'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > WIFI 2.4GHz
                ### ------------------------------------------ ###
                wifi_24 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/th/span').text
                print(wifi_24)
                wifi_24_name = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/td[1]/div').text
                wifi_24_name = wifi_24_name.replace('\n',' ').split(' ')
                print(wifi_24_name)
                wifi_24_detalhes = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/td[2]/a/span')
                wifi_24_detalhes.click()
                wifi_24_detalhes_info = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[6]/td[1]/div')
                items_key = wifi_24_detalhes_info.find_elements_by_tag_name("li")
                wifi_24_valor = []
                for item in items_key:
                    teste = item.text
                    wifi_24_valor.append(teste)
                print(wifi_24_valor)
                wifi_24_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[6]/td[2]/div/textarea').get_attribute('value').strip('\n')
                print(wifi_24_detalhes_stations)
                time.sleep(2)
                print('\n#############################################'
                        '\n MENU >> STATUS >> WIFI 5GHz'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > WIFI 5GHz
                ### ------------------------------------------ ###
                wifi_5 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[7]/th/span').text
                print(wifi_5)
                wifi_5_name = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[7]/td[1]/div').text
                wifi_5_name = wifi_5_name.replace('\n', ' ').split(' ')
                print(wifi_5_name)
                wifi_5_detalhes = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[7]/td[2]/a')
                wifi_5_detalhes.click()
                wifi_5_detalhes_info = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[8]/td[1]/div')
                items_key = wifi_5_detalhes_info.find_elements_by_tag_name("li")
                wifi_5_valor = []
                for item in items_key:
                    teste = item.text
                    wifi_5_valor.append(teste)
                print(wifi_5_valor)
                wifi_5_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[8]/td[2]/div/textarea').get_attribute('value').strip('\n')
                wifi_5_detalhes_stations = wifi_5_detalhes_stations.split('\n')
                print(wifi_5_detalhes_stations)
                time.sleep(2)
                print('\n#############################################'
                        '\n MENU >> STATUS >> REDE LOCAL'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > REDE LOCAL
                ### ------------------------------------------ ###
                rede_local = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[11]/th/span').text
                print(rede_local)
                time.sleep(2)
                rede_local_name = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[11]/td[1]').text
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

        
                rede_local_detalhes = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[11]/td[2]/a')
                rede_local_detalhes.click()
                rede_local_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[12]/td[2]/div/textarea').get_attribute('value')
                rede_local_stations = rede_local_stations.split('\n')
        
                time.sleep(2)
                print('\n#############################################'
                        '\n MENU >> STATUS >> TV'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > TV
                ### ------------------------------------------ ###
                tv = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[13]/th/span').text
                print(tv)
                self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[13]/td[2]/a').click()
                tv_info = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[14]/td[1]/div')
                items_key = tv_info.find_elements_by_tag_name("li")
                tv_valor = []
                for item in items_key:
                    teste = item.text
                    # print(item.text)
                    tv_valor.append(teste)
                print(tv_valor)
                tv_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[14]/td[2]/div/textarea').get_attribute('value')
                tv_stations = tv_stations.split('\n')
                print(tv_stations)
                time.sleep(2)
                print('\n#############################################'
                        '\n MENU >> STATUS >> TELEFONE'
                        '\n#############################################\n')
                ### ------------------------------------------ ###
                ###         STATUS > TELEFONE
                ### ------------------------------------------ ###
                telefone = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[15]/th/span').text
                print(telefone)
                telefone_info_rede = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[15]/td[1]/div[1]').text
                telefone_info_rede = telefone_info_rede.split('\n')
                print(telefone_info_rede)
                telefone_info_status = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[15]/td[1]/div[2]').text
                telefone_info_status = telefone_info_status.split('\n')
                print(telefone_info_status)
                # telefone_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[14]/td[2]/textarea').get_attribute('value')
                # telefone_stations = telefone_stations.split('\n')
                # print(telefone_stations)
                # time.sleep(2)

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
            
            json_saida_upgrade = verificationAcsOnline()
            print(json_saida_upgrade)

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
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="MLG_Pop_Reset_Yes"]').click()
            time.sleep(300)

            self._driver.set_page_load_timeout(10)
            try:
                self._driver.execute_script("window.stop();")
            except Exception as e:
                print(e)
                self._driver.get('http://' + self._address_ip + '/')


            self._driver.get('http://' + self._address_ip + '/')
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_About_Power_Box"]').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(2)


            try:
                if self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[3]/td[2]').text == 'c03dd94800d8' and self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[4]/td[2]').text == '84:AA:9C:D2:79:48':
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

