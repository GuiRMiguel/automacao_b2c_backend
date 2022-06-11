#from asyncio import exceptions
from ..ACSutils import utils
from audioop import lin2lin
from gc import collect
from http import client
from re import sub
import re
import time
from datetime import datetime
from ..AskeyECNT import HGU_AskeyECNT
from json import JSONEncoder
import json
from cgi import print_form
import re
import time
#from typing import final
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
from ..AskeyBROADCOM import HGU_AskeyBROADCOM
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchFrameException, NoSuchElementException
from selenium.webdriver.support.select import Select
from HGUmodels.config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton
from collections import namedtuple
from HGUmodels.utils import chunks

from selenium.common.exceptions import UnexpectedAlertPresentException, InvalidSelectorException


import paramiko
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException
import socket   


file = open('/home/automacao/Projects/automacao_b2c_backend/Default_Settings.json')
default_settings = json.load(file)



mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

from HGUmodels.main_session import MainSession
session = MainSession()

class HGU_AskeyBROADCOM_settingsProbe(HGU_AskeyBROADCOM):

   # 4
    def initialInformations_4(self, dados):
        # TODO: This function needs refactoring, zeep library not working, test crashing
        try:
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.DeviceInfo.ManufacturerOUI",
                "InternetGatewayDevice.DeviceInfo.Manufacturer",
                "InternetGatewayDevice.DeviceInfo.ModelName",
                "InternetGatewayDevice.DeviceInfo.ProductClass",
                "InternetGatewayDevice.DeviceInfo.SerialNumber",
                "InternetGatewayDevice.DeviceInfo.SoftwareVersion",
                "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress",

                "InternetGatewayDevice.ManagementServer.URL",
                "InternetGatewayDevice.ManagementServer.PeriodicInformEnable",
                "InternetGatewayDevice.ManagementServer.PeriodicInformInterval"
            ]}}
            dados.update(dados_gpv)
            dados_entrada = dados

            # GET
            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            parameter = default_settings['Default_Settings']

            for value_parameter in gpv_get:
                print('\nvalue parameter:', value_parameter['value'])
                if value_parameter['name'] == 'InternetGatewayDevice.DeviceInfo.ManufacturerOUI':
                    print('parameter:', parameter['ACS_aux']
                        ['Devices']['Askey_Broadcom']['oui'][0])
                    if value_parameter['value'] != parameter['ACS_aux']['Devices']['Askey_Broadcom']['oui'][0]:
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.DeviceInfo.Manufacturer":
                    print('parameter:', parameter['ACS_aux']
                        ['Devices']['Askey_Broadcom']['manufacturer'])
                    if value_parameter['value'] not in parameter['ACS_aux']['Devices']['Askey_Broadcom']['manufacturer']:
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.DeviceInfo.ModelName":
                    print('parameter:', parameter['ACS_aux']
                        ['Devices']['Askey_Broadcom']['modelos'])
                    if value_parameter['value'] not in parameter['ACS_aux']['Devices']['Askey_Broadcom']['modelos']:
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.DeviceInfo.ProductClass":
                    print('parameter:', parameter['ACS_aux']
                        ['Devices']['Askey_Broadcom']['modelos'])
                    if value_parameter['value'] not in parameter['ACS_aux']['Devices']['Askey_Broadcom']['modelos']:
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.ManagementServer.URL":
                    print('parameter:', parameter['CWMP (TR-069)']
                        ['Parameter']['ACS URL Management']['Value'])
                    if value_parameter['value'] != parameter['CWMP (TR-069)']['Parameter']['ACS URL Management']['Value']:
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.ManagementServer.PeriodicInformEnable":
                    print('parameter:', parameter['CWMP (TR-069)']
                        ['Parameter']['ManagementServer.EnableCWMP']['Value'])
                    if value_parameter['value'] != parameter['CWMP (TR-069)']['Parameter']['ManagementServer.EnableCWMP']['Value']:
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.ManagementServer.PeriodicInformInterval":
                    print('parameter:', parameter['CWMP (TR-069)']
                        ['Parameter']['Periodic inform Interval']['Value'])
                    if value_parameter['value'] != parameter['CWMP (TR-069)']['Parameter']['Periodic inform Interval']['Value']:
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.DeviceInfo.SerialNumber":
                        if value_parameter['value'] != dados_entrada['serialnumber']:
                            dict_result = {
                                "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}

                elif value_parameter['name'] == "InternetGatewayDevice.DeviceInfo.SoftwareVersion":
                        if value_parameter['value'] != dados_entrada['fmw_version']:
                            dict_result = {
                                "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    
                elif value_parameter['name'] == "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.ExternalIPAddress":
                        if value_parameter['value'] != dados_entrada['ip']:
                            dict_result = {
                                "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}


                else:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} não encontrado"}
        except Exception as e:
            dict_result = {
                            "obs": e}
        self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result
    
    # 5
    def wifi2GHzInformations_5(self, dados):
        # TODO: This function needs refactoring, zeep library not working, test crashing
        try:
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Enable",
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Status",
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID",
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.BeaconType",
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Standard",
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Channel",
            ]}}
            dados.update(dados_gpv)
            dados_entrada = dados

            # GET
            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            parameter = default_settings['Default_Settings']

            for value_parameter in gpv_get:
                print('\nvalue parameter:', value_parameter['value'])
                if value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Enable":
                    print('parameter:', parameter['Wifi 2.4']['Parameter']
                        ['Main Wireless network’s Enabled']['Value'])
                    print('1')
                    if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Main Wireless network’s Enabled']['Value'] and str(value_parameter['value']) != '1':
                        
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Status":
                    print('parameter:', parameter['Wifi 2.4']
                        ['Parameter']['Default Status']['Value'])
                    print('2')
                    if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Status']['Value'] and str(value_parameter['value']) != 'Up':
                        
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID":
                    print('parameter:', parameter['Wifi 2.4']['Parameter']
                        ["Main Wireless network’s SSID"]['Value'])
                    print('3')
                    if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']["Main Wireless network’s SSID"]['Value'] and str(value_parameter['value']) != 'automacao_24':
                        
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.BeaconType":
                    print('parameter:', parameter['Wifi 2.4']
                        ['Parameter']['Default Security type']['Value'])
                    print('4')
                    if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Security type']['Value'] and str(value_parameter['value']) != '11i':
                        
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Standard":
                    print('parameter:', parameter['Wifi 2.4']
                        ['Parameter']['Default Mode']['Value'])
                    print('5')
                    if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Mode']['Value'] and str(value_parameter['value']) != 'n':
                        
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Channel":
                    print('parameter:', parameter['Wifi 2.4']
                        ['Parameter']['Default Channel']['Value'])
                    print('6')
                    if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Channel']['Value']:
                        
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                else:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} não encontrado"}
        except Exception as e:
            dict_result = {'obs': f'{e}'}

        self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result
        
    # 6
    def wifi5GHzInformations_6(self, dados):
        dados_gpv = {'GPV_Param': {'parameterNames': [
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Enable",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Status",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.SSID",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.BeaconType",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Standard",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Channel"
        ]}}
        dados.update(dados_gpv)
        dados_entrada = dados

        # GET
        gpv_get = utils.ACS.getParameterValues(**dados_entrada)
        parameter = default_settings['Default_Settings']

        for value_parameter in gpv_get:
            print('\nvalue parameter:', value_parameter['value'])
            if value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Enable":
                print('parameter:', parameter['Wifi 2.4']['Parameter']
                      ['Main Wireless network’s Enabled']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Main Wireless network’s Enabled']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Status":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Status']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Status']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID":
                print('parameter:', parameter['Wifi 2.4']['Parameter']
                      ["Main Wireless network’s SSID"]['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']["Main Wireless network’s SSID"]['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.BeaconType":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Security type']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Security type']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Standard":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Mode']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Mode']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Channel":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Channel']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Channel']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            else:
                dict_result = {
                    "obs": f"Objeto {value_parameter['name']} não encontrado"}

        self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result
  
          
    # 10
    def setDHCP_10(self, dados):
        # TODO: This function needs refactoring, zeep library not working, test crashing
        try:
            dados_spv = {'SPV_Param': [
                {
                    "name": "InternetGatewayDevice.LANDevice.1.LANHostConfigManagement.MinAddress",
                    "type": "string",
                    "value": "192.168.15.6"
                }, {
                    "name": "InternetGatewayDevice.LANDevice.1.LANHostConfigManagement.MaxAddress",
                    "type": "string",
                    "value": "192.168.15.150"
                }]}
            dados.update(dados_spv)
            dados_entrada = dados

            # SET
            spv_set = utils.ACS.setParameterValues(**dados_entrada)

            # GET
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.LANDevice.1.LANHostConfigManagement.MinAddress",
                "InternetGatewayDevice.LANDevice.1.LANHostConfigManagement.MaxAddress"
            ]}}
            dados.update(dados_gpv)
            dados_entrada = dados

            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            if gpv_get[0]['value'] != "192.168.15.6":
                dict_result = {
                    "obs": f"Objeto {gpv_get[0]['name']} não encontrado"}
            elif gpv_get[1]['value'] != "192.168.15.150":
                dict_result = {
                    "obs": f"Objeto {gpv_get[1]['name']} não encontrado"}
            else:
                dict_result = {"Resultado_Probe": "OK",
                            "obs": "Teste OK", "result": "passed"}
        except Exception as e:
            dict_result = {'obs': f'{e}'}
        self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result

    # 12
    def set2GHzWiFi_12(self, dados):
        # TODO: This function needs refactoring, zeep library not working, test crashing
        try:
            dados_spv = {'SPV_Param': [
                {
                    "name": "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID",
                    "type": "string",
                    "value": "automacao_24"
                },
                {
                    "name": "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.PreSharedKey.1.KeyPassphrase",
                    "type": "string",
                    "value": "vivo@12345678"
                }]}
            dados.update(dados_spv)
            dados_entrada = dados

            # SET
            spv_set = utils.ACS.setParameterValues(**dados_entrada)

            # GET
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID",
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.PreSharedKey.1.KeyPassphrase"
            ]}}
            dados.update(dados_gpv)
            dados_entrada = dados

            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            if gpv_get[0]['value'] != 'automacao_24':
                dict_result = {
                    "obs": f"Objeto {gpv_get[0]['name']} não encontrado"}
            elif gpv_get[1]['value'] == "vivo@12345678" or gpv_get[1]['value'] is None:
                dict_result = {"Resultado_Probe": "OK",
                            "obs": "Teste OK", "result": "passed"}
            else:
                dict_result = {
                    "obs": f"Objeto {gpv_get[1]['name']} não encontrado"}
        except Exception as e:
            dict_result = {'obs': f'{e}'}
        self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result

    # 13
    def set5GHzWiFi_13(self, dados):
        # TODO: This function needs refactoring, zeep library not working, test crashing
        try:
            dados_spv = {'SPV_Param': [
                {
                    "name": "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.SSID",
                    "type": "string",
                    "value": "automacao_24"
                },
                {
                    "name": "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.PreSharedKey.1.KeyPassphrase",
                    "type": "string",
                    "value": "vivo@12345678"
                }]}
            dados.update(dados_spv)
            dados_entrada = dados

            # SET
            spv_set = utils.ACS.setParameterValues(**dados_entrada)

            # GET
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.SSID",
                "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.PreSharedKey.1.KeyPassphrase"
            ]}}
            dados.update(dados_gpv)
            dados_entrada = dados
            print(dados_entrada)

            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            if gpv_get[0]['value'] != 'automacao_24':
                dict_result = {
                    "obs": f"Objeto {gpv_get[0]['name']} não encontrado"}
            elif gpv_get[1]['value'] == "vivo@12345678" or gpv_get[1]['value'] is None:
                dict_result = {"Resultado_Probe": "OK",
                            "obs": "Teste OK", "result": "passed"}
            else:
                dict_result = {
                    "obs": f"Objeto {gpv_get[1]['name']} não encontrado"}
            self._dict_result.update(dict_result)
        except Exception as e:
            dict_result = {
                "obs": f'{e}'}
            self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result

    # 15
    def setPeriodicInterval_15(self, dados):
        try:
            dados_spv = {'SPV_Param': [
                {
                    "name" : "InternetGatewayDevice.ManagementServer.PeriodicInformInterval",
                    "type": "unsignedInt",
                    "value" : "600"
                    }]}
            dados.update(dados_spv)
            dados_entrada = dados

            # SET
            spv_set = utils.ACS.setParameterValues(**dados_entrada)

            # GET
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.ManagementServer.PeriodicInformInterval"
                ]}}
            dados.update(dados_gpv)
            dados_entrada = dados
            print(dados_entrada)

            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            if gpv_get[0]['value'] != '600':
                dict_result = {
                    "obs": f"Objeto {gpv_get[0]['name']} obteve um valor diferente do esperado."}
            else:
                dict_result = {"Resultado_Probe": "OK",
                            "obs": "Teste OK", "result": "passed"}
            self._dict_result.update(dict_result)
        except Exception as e:
            dict_result = {
                "obs": f'{e}'}
            self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result

    # 17
    def setAccessClass_17(self, dados):
        try:
            dados_spv = {'SPV_Param': [
                {
                "name" : "InternetGatewayDevice.X_VIVO_COM_BR.AccessClass",
                "type"  : "string",
                "value" : "service04"
                }]}
            dados.update(dados_spv)
            dados_entrada = dados

            # SET
            spv_set = utils.ACS.setParameterValues(**dados_entrada)

            # GET
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.X_VIVO_COM_BR.AccessClass"
                ]}}
            dados.update(dados_gpv)
            dados_entrada = dados
            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            print(gpv_get)

            if gpv_get[0]['value'] != 'service04':
                dict_result = {
                    "obs": f"Objeto {gpv_get[0]['name']} obteve um valor diferente do esperado. (esperado: service04; obtido: {gpv_get[0]['value']})"}
            else:
                dict_result = {"Resultado_Probe": "OK",
                            "obs": "Teste OK", "result": "passed"}
            self._dict_result.update(dict_result)
        except Exception as e:
            dict_result = {
                "obs": f'{e}'}
            self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result

    # 43
    def checkIPv6Telefonica_43(self, dados):
        try:
            # GET
            dados_gpv = {'GPV_Param': {'parameterNames': [
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Enable",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Status",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Alias",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.DestIPPrefix",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.ForwardingPolicy",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.NextHop",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Interface",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Origin",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.ForwardingMetric",
                "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.ExpirationTime",
                ]}}
            dados.update(dados_gpv)
            dados_entrada = dados

            gpv_get = utils.ACS.getParameterValues(**dados_entrada)
            if type(gpv_get) != list:
                self._dict_result.update(gpv_get)
                print('\n', self._dict_result, '\n')
                return self._dict_result

            for value_parameter in gpv_get:
                if value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Enable":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Status":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Alias":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.DestIPPrefix":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.ForwardingPolicy":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.NextHop":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Interface":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.Origin":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}

                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.ForwardingMetric":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                
                elif value_parameter['name'] == "InternetGatewayDevice.Layer3Forwarding.X_VIVO_COM_BR_IPv6Forwarding.1.ExpirationTime":
                    if value_parameter['value'] is None and value_parameter['value'] == '':
                        dict_result = {
                            "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}

                    else:
                        dict_result = {"Resultado_Probe": "OK",
                                    "obs": "Teste OK", "result": "passed"}

                else:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} não encontrado"}
                self._dict_result.update(dict_result)
        except Exception as e:
                dict_result = {
                            "obs": e
                            }
                self._dict_result.update(dict_result)

        print('\n', self._dict_result, '\n')
        return self._dict_result

     # 39
    def indexWifi24ghz_39(self, dados):
     
        dados_gpv = {'GPV_Param': {'parameterNames': [
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Enable",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Status",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.BeaconType",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Standard",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Channel",
            #"InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.X_BROADCOM_COM_WlanAdapter.WlBaseCfg.WlCountry",
             "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.X_TELEFONICA-ES_Bandwidth",
             "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.PreSharedKey.1.KeyPassphrase",
             "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.WPAEncryptionModes",
             "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.WPS.Enable"
       
        ]}}
        dados.update(dados_gpv)
        dados_entrada = dados

        # GET
        gpv_get = utils.ACS.getParameterValues(**dados_entrada)
        parameter = default_settings['Default_Settings']
        print(gpv_get)
        for value_parameter in gpv_get:
            print('\nvalue parameter:', value_parameter['value'])
            if value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Enable":
                print('parameter:', parameter['Wifi 2.4']['Parameter']
                      ['Main Wireless network’s Enabled']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Main Wireless network’s Enabled']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Status":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Status']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Status']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.SSID":
                print('parameter:', parameter['Wifi 2.4']['Parameter']
                      ["Main Wireless network’s SSID"]['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']["Main Wireless network’s SSID"]['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.BeaconType":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Security type']['Value'])
                if value_parameter['value'] == '11i' and parameter['Wifi 5']['Parameter']['Default Security type']['Value'] == "WPA2 -PSK":
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Standard":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Mode']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Mode']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.Channel":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Channel']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Channel']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}
            #New
            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.X_BROADCOM_COM_WlanAdapter.WlBaseCfg.WlCountry":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Channels in use - frequency plan']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Channels in use - frequency plan']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.X_TELEFONICA-ES_Bandwidth":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default Channel width']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default Channel width']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.PreSharedKey.1.KeyPassphrase":
                print(value_parameter['value'])
                if value_parameter['value'] != None:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.WPAEncryptionModes":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['Default cipher mode']['Value'])
                if value_parameter['value'] != parameter['Wifi 2.4']['Parameter']['Default cipher mode']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.WPS.Enable":
                print('parameter:', parameter['Wifi 2.4']
                      ['Parameter']['WPS default status']['Value'])
                print("Verificar valor 1")
                if value_parameter['value'] != '1':
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}


            else:
                dict_result = {
                    "obs": f"Objeto {value_parameter['name']} não encontrado"}

        self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result

    # 40
    def indexWifi5ghz_40(self, dados):
        dados_gpv = {'GPV_Param': {'parameterNames': [
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Enable",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Status",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.SSID",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.BeaconType",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Standard",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Channel",

            #"InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_BROADCOM_COM_WlanAdapter.WlBaseCfg.WlCountry",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_TELEFONICA-ES_Bandwidth",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.PreSharedKey.1.KeyPassphrase",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.WPAEncryptionModes",
            "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.WPS.Enable"
        ]}}
        dados.update(dados_gpv)
        dados_entrada = dados

        # GET
        gpv_get = utils.ACS.getParameterValues(**dados_entrada)
        parameter = default_settings['Default_Settings']

        for value_parameter in gpv_get:
            print('\nvalue parameter:', value_parameter['value'])
            if value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Enable":
                print('parameter:', parameter['Wifi 5']['Parameter']
                      ['Main Wireless network’s Enabled']['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']['Main Wireless network’s Enabled']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Status":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['Default Status']['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']['Default Status']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.SSID":
                print('parameter:', parameter['Wifi 5']['Parameter']
                      ["Main Wireless network’s SSID"]['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']["Main Wireless network’s SSID"]['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.BeaconType":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['Default Security type']['Value'])
                if value_parameter['value'] == '11i' and parameter['Wifi 5']['Parameter']['Default Security type']['Value'] == "WPA2 -PSK":
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Standard":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['Default Mode']['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']['Default Mode']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Channel":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['Default Channel']['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']['Default Channel']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}
            
            #New
            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_BROADCOM_COM_WlanAdapter.WlBaseCfg.WlCountry":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['Channels in use - frequency plan']['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']['Channels in use - frequency plan']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_TELEFONICA-ES_Bandwidth":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['Default Channel width']['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']['Default Channel width']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.PreSharedKey.1.KeyPassphrase":
                print(value_parameter['value'])
                if value_parameter['value'] != None:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.WPAEncryptionModes":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['Default cipher mode']['Value'])
                if value_parameter['value'] != parameter['Wifi 5']['Parameter']['Default cipher mode']['Value']:
                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}

            elif value_parameter['name'] == "InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.WPS.Enable":
                print('parameter:', parameter['Wifi 5']
                      ['Parameter']['WPS default status']['Value'])
                print("Verificar valor 1")
                if value_parameter['value'] != '1':
                                    dict_result = {
                        "obs": f"Objeto {value_parameter['name']} obteve um valor diferente"}
                else:
                    dict_result = {"Resultado_Probe": "OK",
                                   "obs": "Teste OK", "result": "passed"}


            else:
                dict_result = {
                    "obs": f"Objeto {value_parameter['name']} não encontrado"}

        self._dict_result.update(dict_result)
        print('\n', self._dict_result, '\n')
        return self._dict_result


    #48
    def rebootDevice_48(self, dados):
        try:
            dados_entrada = dados
            reboot_device = utils.ACS.reboot(**dados_entrada)

            self._dict_result.update(reboot_device)
        except Exception as e:
            self._dict_result.update({"obs": f"{e}"})
        finally:
            print('\n', self._dict_result, '\n')
            return self._dict_result


    def accessWizard_401(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            self.login_admin()

            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            time.sleep(3)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[2]/a').click()
            time.sleep(3)
            self._driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[3]/td[2]/input[1]').click()
    
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
            dict_saida = {"Resultado_Probe": "OK"}

        except (NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"obs": "Nao foi possivel realizar o login com sucesso"})
            dict_saida = {"Resultado_Probe": "NOK"}

        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'accessWizard_401', dict_saida)

            return self._dict_result


    def accessPadrao_403(self):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            
            self._driver.switch_to.frame('logofrm')
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/img')            
            
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs":'Login executado com sucesso'})
            
        except NoSuchFrameException as exception:
            self._dict_result.update({'obs': 'Login nao executado com sucesso'})
        finally:
            self._driver.quit()
            return self._dict_result


    def accessRemoteHttp_405(self, flask_username):
        final_dict = {}
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menufrm')
            #click managment
            self._driver.find_element_by_xpath('//*[@id="folder66"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            #click access control
            self._driver.find_element_by_xpath('//*[@id="folder76"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            #click trust domain
            self._driver.find_element_by_xpath('//*[@id="item79"]/table/tbody/tr/td/a').click()
            time.sleep(5)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            ip_address = self._driver.find_element_by_xpath('/html/body/blockquote/form/table/tbody/tr[1]/td[2]/input').text
            table_flat = self._driver.find_elements_by_xpath('//*[@id="tblRmgt"]//td')
            
            value_table_flat = []
            for cell in table_flat:
                try:
                    input = cell.find_element_by_xpath('input')
                    value_table_flat.append(
                        input.get_attribute('checked') 
                        if input.get_attribute('checked') 
                        else input.get_attribute('value') 
                    )
                except Exception as e:
                    value_table_flat.append(cell.text)
            value_table_flat = value_table_flat[2:-2]
            table = chunks(value_table_flat, 5)[:-2]

            header = table[0][1:]
            table = table[1:]
            
            
            for row in table:
                key = row[0].replace(':','')
                sub_dict = {header[idx]: ('Habilitado' 
                                          if value == 'true' 
                                          else 'Desabilitado' 
                                          if value=='on' else value) for idx, value in enumerate(row[1:])}
                final_dict.update({key: sub_dict})
    
            final_dict.update({'IP_Address': ip_address})
            self._driver.quit()

            if final_dict['HTTP'].get('WAN') == 'Desabilitado':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'WAN esta Desabilitado'})
            else:
                self._dict_result.update({'obs': 'WAN esta Habilitado'})
            print(final_dict)
        except Exception as exception:
            self._dict_result.update({'obs': exception})
        finally:
            self.update_global_result_memory(flask_username, 'accessRemoteHttp_405', final_dict)
        return self._dict_result


    def accessRemoteSSH_407(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessRemoteHttp_405')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 405 primeiro"})
        else:
            wan = result['SSH'].get('WAN')
            if wan == 'Desabilitado':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', "obs":"WAN esta Desabilitado"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno WAN esta {wan}"})
        
        return self._dict_result


    def accessRemoteTrustedIP_408(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessRemoteHttp_405')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 405 primeiro'})
        else:
            ip = result['IP_Address']
            if ip == '':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'IP Address esta vazio'})
            else:
                self._dict_result.update({'obs': f'Teste incorreto, retorno IP Address {ip}'})

        return self._dict_result


    def NTPServer_409(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {self._address_ip} \n{'#' * 50}")
            ssh.connect(hostname=self._address_ip, username=self._username, password=self._password, timeout=2)
            print("Authentication successfuly, connect to HGU")
            teste = ssh.invoke_shell()
            teste.send('sntp show \n')
            time.sleep(2)
            output = teste.recv(65000)
            out_str = output.decode('utf-8')
            ssh.close()
            str_list = out_str.splitlines()
            for i in str_list:
                if i.startswith('NTP Server1'):
                    split_ntp = i.split(':')
                    ntp_server = split_ntp[1]
                    ntp_server = ntp_server.strip()
            if (ntp_server == 'pool.ntp.br'):
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': f'NTP Server OK: {ntp_server}'})
            else:
                self._dict_result.update({'obs': f'NTP Server {ntp_server}'})
            
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            self._dict_result.update({'obs': 'Falha_Autenticacao'})
        except socket.timeout:
            print("Unable to establish SSH connection: Timeout de conexão")
            self._dict_result.update({'obs': 'Timeout_Connection'})
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            self._dict_result.update({'obs': str(sshException)})
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            self._dict_result.update({'obs': str(badHostKeyException)})
        finally:
            return self._dict_result


    def timeZone_410(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {self._address_ip} \n{'#' * 50}")
            ssh.connect(hostname=self._address_ip, username=self._username, password=self._password, timeout=2)
            print("Authentication successfuly, connect to HGU")
            teste = ssh.invoke_shell()
            teste.send('sntp show \n')
            time.sleep(2)
            output = teste.recv(65000)
            out_str = output.decode('utf-8')
            ssh.close()
            str_list = out_str.splitlines()
            for i in str_list:
                if i.startswith('Timezone'):
                    split_time = i.split(':')
                    time_zone = split_time[1]
                    time_zone = time_zone.strip()
            if (time_zone == '(GMT-3:00) Brasilia'):
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': f'Timezone OK: {time_zone}'})
            else:
                self._dict_result.update({'obs': f'Timezone {time_zone}'})

        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            self._dict_result.update({"obs": 'Falha_Autenticacao'})
        except socket.timeout:
            print("Unable to establish SSH connection: Timeout de conexão")
            self._dict_result.update({"obs": 'Timeout_Connection'})
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            self._dict_result.update({"obs":  str(sshException)})
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            self._dict_result.update({"obs": str(badHostKeyException)})
        finally:
            return self._dict_result


    def checkACSSettings_411(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')

            self.login_support()

            self._driver.switch_to.frame('menufrm')
            time.sleep(1)

            # Management
            self._driver.find_element_by_xpath('//*[@id="folder66"]/table/tbody/tr/td/a').click()
            time.sleep(1)
            # Tr-069
            self._driver.find_element_by_xpath('//*[@id="folder75"]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')

            # Pegando os valores
            header_inform = self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr//td')
            time.sleep(1)
            values_inform = self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr/td//input')
            time.sleep(1)
            values_form = self._driver.find_elements_by_xpath('/html/body/blockquote/form//input')
            dict_saida411 = {}
            for v in values_form:
                name = v.get_attribute('name')
                value = v.get_attribute('value')
                if name == 'debug':
                    name = 'cwmp'
                dict_saida411.update({name: value})

            # Tratando o inform para retornar o valor correto
            count = 1
            for v in values_inform:
                count += 1
                if v.get_attribute('checked'): 
                    break
                
            count2 = 0
            for v in header_inform:
                count2 += 1
                if count2 == count:
                    dict_saida411.update({'inform': v.text})
                    break
            
            # Tratando o cwmp para retornar o valor correto
            header_cwmp = self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[4]/tbody/tr//td')
            values_cwmp = self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[4]/tbody/tr/td//input')

            count3 = 1
            for v in values_cwmp:
                count3 += 1
                if v.get_attribute('checked'): 
                    break

            count4 = 0
            for v in header_cwmp:
                count4 += 1
                if count4 == count3:
                    dict_saida411.update({'cwmp': v.text})
                    break
            
            print(dict_saida411)
            
            # Resposta
            url = dict_saida411['acsURL']
            if url == 'http://acs.telesp.net.br:7005/cwmpWeb/WGCPEMgt':
                self._dict_result.update({"obs": "ACS URL OK", "Resultado_Probe": "OK", 'result':'passed'})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno ACS URL: {url}"})

        except Exception as e:
            self._dict_result.update({'obs': e})

        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkACSSettings_411', dict_saida411)
        return self._dict_result


    def validarDefaultUserACS_412(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        
        else:
            value = result['acsUser']
            if value == 'acsclient':
                self._dict_result.update({"obs": "Usuario: acsclient", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Usuario: {value}"})
        return self._dict_result
    

    def validarDefaultPasswordACS_413(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['acsPwd']
            if value == 'telefonica':
                self._dict_result.update({"obs": "Senha: telefonica", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Senha: {value}"})
        return self._dict_result
    

    def GPV_OneObjct_414(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
        self._dict_result.update({"obs": TEST_NOT_IMPLEMENTED_WARNING})
        return self._dict_result

    
    def periodicInformEnable_415(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['inform']
            if value == 'Enable':
                self._dict_result.update({"obs": "Informe: Habilitado ", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Informe: {value}"})
        return self._dict_result


    def periodicInformInterval_416(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['informInterval']
            if value == '68400':
                self._dict_result.update({"obs": "Informe Interval: 68400", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Informe Interval: {value}"})
        return self._dict_result


    def connectionRequestPort_417(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
        self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
        return self._dict_result


    # depende do 411, mas precisa modificar no dict
    def enableCwmp_418(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['cwmp']
            if value == 'Enable':
                self._dict_result.update({"obs": "CWMP: Habilitado", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno CWMP: {value}"})
        return self._dict_result


    def userConnectionRequest_419(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['connReqUser']
            if value == 'userid':
                self._dict_result.update({"obs": "Connection Request Username OK", "result":'passed'})
            else:
                self._dict_result.update({"obs": f" Teste incorreto, retorno Connection Request Username: {value}", "result":'failed'})
        return self._dict_result


    def checkWanInterface_420(self, flask_username):

        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder1"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="folder3"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            table_flat = self._driver.find_elements_by_xpath('/html/body/blockquote/form/center[1]/table/tbody//td')
            
            
            value_table_flat = [div.text for div in table_flat]

            table = chunks(value_table_flat, 13)
    
            header = table[0]
            table = table[1:]
            
            final_dict = {}
            for row in table:
                key = row[0].replace(':','')
                sub_dict = {header[idx]: value for idx, value in enumerate(row)}
                final_dict.update({key: sub_dict})

            cpe_config = config_collection.find_one()
            if final_dict['ppp0.1'].get('VlanMuxId') == '10' and final_dict['ppp0.1'].get('Type') == 'PPPoE' and cpe_config['REDE'] == 'VIVO_1':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'Type: PPPoE | VLAN: 10', "result":"passed"})
            else:
                self._dict_result.update({'obs': f"Teste incorreto, retorno: Type:{final_dict['ppp0.1'].get('VlanMuxId')}, VLAN:{final_dict['ppp0.1'].get('VlanMuxId')}, REDE:{cpe_config['REDE']}"})
            print(final_dict)
        except IndexError as exception:
            self._dict_result.update({'obs': exception})
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkWanInterface_420', final_dict)
        return self._dict_result

    
    def prioridadePPPoE_421(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Type')
                cpe_config = config_collection.find_one()
                if iface_type == 'PPPoE' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    if sub_dict.get('Vlan8021p') == '0':
                        self._dict_result.update({"obs": 'Type: PPPoE | Priority: 0', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno: Type:{iface_type}, Priority:{sub_dict.get('Vlan8021p')}"})
                        break
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: Type:{iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result

    
    def tipoRedeInet_422(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('VlanMuxId')
                cpe_config = config_collection.find_one()
                if iface_type == '10' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    if sub_dict.get('Type') == 'PPPoE':
                        self._dict_result.update({"obs": 'VLAN: 10 | Type:PPPoE', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno: VLAN:{iface_type}, TYPE:{sub_dict.get('Type')}"})
                        break
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: VLAN:{iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def checkNatSettings_423(self, flask_username):
        self._driver.quit()
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            status = result['ppp0.1'].get('NAT')
            print(status)
            if status == 'Enabled':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'interface ppp0.1 NAT: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({'obs': f'Teste incorreto, retorno interface NAT Status: {status}'})
            
        return self._dict_result


    def checkMulticastSettings_424(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menufrm')

            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="item14"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            tabela = self._driver.find_elements_by_xpath('/html/body/blockquote/form/center/table/tbody//tr')
            tabela_dados = [[y.text for y in x.find_elements_by_tag_name('td')] for x in tabela]
            self._driver.quit()
            
            dict_saida_424 = {}
            for n, linha in enumerate(tabela_dados):
                if n == 0: keys = linha 
                else: dict_saida_424[linha[0]] = {keys[i]: valor for i, valor in enumerate(linha) if i > 0}
            print(dict_saida_424)

            try: 
                igmp_inet = dict_saida_424['ppp0.1']['Igmp Proxy']
                if igmp_inet == 'Disabled':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: ppp0.1 | IGMP: Desabilitado", "result":"passed"})
                else:
                    self._dict_result.update({"obs": "Interface: ppp0.1 | IGMP: Habilitado"})
            except Exception:
                self._dict_result.update({"obs": "Interface ppp0.1 nao existe"})

        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            
            self.update_global_result_memory(flask_username, 'checkMulticastSettings_424', dict_saida_424)
            return self._dict_result


    def getFullConfig_425(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/')
        self.login_admin()
        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> GPON'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > GPON
        ### ------------------------------------------ ###
        self._driver.switch_to.frame('mainFrame')
        gpon = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/th/span').text
        print(gpon)
        divOptical = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div[1]').text
        divOptical = divOptical.split("\n")
        print(divOptical)
        divOptRx = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div[2]').text
        divOptRx = divOptRx.split("\n")
        print(divOptRx)
        divOptTx = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div[3]').text
        divOptTx = divOptTx.split("\n")
        print(divOptTx)
        print('\n#############################################'
                '\n MENU >> STATUS >> INTERNET'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > INTERNET
        ### ------------------------------------------ ###
        internet = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/th/span').text
        print(internet)
        divPpp = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[1]/div').text
        divPpp = divPpp.split("\n")
        print(divPpp)
        detalhes_internet = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/a')
        print(detalhes_internet.text)
        detalhes_internet.click()
        detalhes_IPv4_head = self._driver.find_element_by_link_text('IPv4').text
        print(detalhes_IPv4_head)
        detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[1]/ul')
        time.sleep(1)
        items_key_internet_ipv4 = detalhes_IPv4.find_elements_by_tag_name("li")
        detalhes_IPv4_nome = []
        for i in items_key_internet_ipv4:
            teste = i.text
            detalhes_IPv4_nome.append(teste)
        print(detalhes_IPv4_nome)
        detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[2]/ul')
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
        detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[1]/ul')
        time.sleep(1)
        items_key = detalhes_IPv6.find_elements_by_tag_name("li")
        detalhes_IPv6_nome = []
        for item in items_key:
            teste = item.text
            detalhes_IPv6_nome.append(teste)
        print(detalhes_IPv6_nome)
        detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[2]/ul')
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
        wifi_24 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/th/span').text
        print(wifi_24)
        wifi_24_name = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[1]/div').text
        wifi_24_name = wifi_24_name.replace('\n',' ').split(' ')
        print(wifi_24_name)
        wifi_24_detalhes = self._driver.find_element_by_xpath('//html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/a')
        wifi_24_detalhes.click()
        wifi_24_detalhes_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[1]/div/ul')
        items_key = wifi_24_detalhes_info.find_elements_by_tag_name("li")
        wifi_24_valor = []
        for item in items_key:
            teste = item.text
            wifi_24_valor.append(teste)
        print(wifi_24_valor)
        wifi_24_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[2]/textarea').get_attribute('value').strip('\n')
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
        wifi_5_detalhes_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[1]/div/ul')
        items_key = wifi_5_detalhes_info.find_elements_by_tag_name("li")
        wifi_5_valor = []
        for item in items_key:
            teste = item.text
            wifi_5_valor.append(teste)
        print(wifi_5_valor)
        wifi_5_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[2]/textarea').get_attribute('value').strip('\n')
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

        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> TV'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > TV
        ### ------------------------------------------ ###
        tv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/th/span').text
        print(tv)
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/td[2]/a').click()
        tv_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[12]/td[1]/div/ul')
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
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[13]/td[2]/a').click()
        telefone_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[14]/td[2]/textarea').get_attribute('value')
        telefone_stations = telefone_stations.split('\n')
        print(telefone_stations)
        time.sleep(2)
        print('\n#############################################'
        '\n MENU >> CONFIGURAÇÕES >> INTERNET'
        '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > INTERNET
        ### ------------------------------------------ ###
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[1]/a').click()
        config_internet = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/h3').text
        print(config_internet)
        config_internet_usuario = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]').text.strip(': ')
        print(config_internet_usuario)
        config_internet_usuario_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input').get_property('value')
        print(config_internet_usuario_valor)
        config_internet_senha = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[1]').text.strip(': ')
        print(config_internet_senha)
        config_internet_senha_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/input').get_property('value')
        print(config_internet_senha_valor)
        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> REDE LOCAL'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > REDE LOCAL
        ### ------------------------------------------ ###
        config_redelocal = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a')
        config_redelocal.click()
        time.sleep(1)
        config_redelocal_dhcp = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/thead/tr/th').text
        print(config_redelocal_dhcp)
        config_redelocal_servidordhcp = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[2]/td[1]').text.strip(': ')
        print(config_redelocal_servidordhcp)
        config_redelocal_servidordhcp_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
        if config_redelocal_servidordhcp_valor == 'true':
            config_redelocal_servidordhcp_valor = 'Habilitado'
        else:
            config_redelocal_servidordhcp_valor = 'Desabilitado'
        print(config_redelocal_servidordhcp_valor)
        config_redelocal_iphgu = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[1]').text.strip(': ')
        print(config_redelocal_iphgu)
        config_redelocal_iphgu_valor01 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').get_property('value')
        config_redelocal_iphgu_valor02 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').get_property('value')
        config_redelocal_iphgu_valor03 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').get_property('value')
        config_redelocal_iphgu_valor04 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[4]').get_property('value')
        config_redelocal_iphgu_valor = config_redelocal_iphgu_valor01 + '.' + config_redelocal_iphgu_valor02 + '.' + config_redelocal_iphgu_valor03 + '.' + config_redelocal_iphgu_valor04
        print(config_redelocal_iphgu_valor)

        config_redelocal_mask = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[1]').text.strip(': ')
        print(config_redelocal_mask)
        config_redelocal_mask_valor01 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[1]').get_property('value')
        config_redelocal_mask_valor02 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[2]').get_property('value')
        config_redelocal_mask_valor03 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[3]').get_property('value')
        config_redelocal_mask_valor04 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[4]').get_property('value')
        config_redelocal_mask_valor = config_redelocal_mask_valor01 + '.' + config_redelocal_mask_valor02 + '.' + config_redelocal_mask_valor03 + '.' + config_redelocal_mask_valor04
        print(config_redelocal_mask_valor)

        config_redelocal_pool = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[1]').text.strip(': ')
        print(config_redelocal_pool)
        config_redelocal_pool_valor_ini01 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]').get_property('value')
        config_redelocal_pool_valor_ini02 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]').get_property('value')
        config_redelocal_pool_valor_ini03 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[3]').get_property('value')
        config_redelocal_pool_valor_ini04 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[4]').get_property('value')
        config_redelocal_pool_ini_valor = config_redelocal_pool_valor_ini01 + '.' + config_redelocal_pool_valor_ini02 + '.' + config_redelocal_pool_valor_ini03 + '.' + config_redelocal_pool_valor_ini04
        config_redelocal_pool_valor_fin01 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[1]').get_property('value')
        config_redelocal_pool_valor_fin02 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[2]').get_property('value')
        config_redelocal_pool_valor_fin03 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[3]').get_property('value')
        config_redelocal_pool_valor_fin04 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[4]').get_property('value')
        config_redelocal_pool_fin_valor = config_redelocal_pool_valor_fin01 + '.' + config_redelocal_pool_valor_fin02 + '.' + config_redelocal_pool_valor_fin03 + '.' + config_redelocal_pool_valor_fin04
        print(config_redelocal_pool_ini_valor)
        print(config_redelocal_pool_fin_valor)

        config_redelocal_dns = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[7]/td[1]').text.strip(': ')
        print(config_redelocal_dns)
        config_redelocal_dns_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[7]/td[2]/input[1]').get_attribute('checked')
        if config_redelocal_dns_valor == 'true':
            config_redelocal_dns_valor = 'Habilitado'
        else:
            config_redelocal_dns_valor = 'Desabilitado'
        print(config_redelocal_dns_valor)

        config_redelocal_concessao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[10]/td[1]').text.strip(': ')
        print(config_redelocal_concessao)
        config_redelocal_concessao_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[10]/td[2]/input').get_property('value')
        print(config_redelocal_concessao_valor)

        config_redelocal_tabela_concessao = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[4]')
        for i in config_redelocal_tabela_concessao:
            ths = i.find_elements_by_tag_name('th')
            print([th.text for th in ths])
            tds = i.find_elements_by_tag_name('td')
            print([td.text for td in tds])

        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> WIFI 2.4GHz '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > WIFI 2.4GHz
        ### ------------------------------------------ ###
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
        config_wifi24 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/h3').text
        print(config_wifi24)
        time.sleep(2)
        config_wifi24_basico = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/thead/tr/th').text.strip(': ')
        print(config_wifi24_basico)
        config_wifi24_basico_redeprivada = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[1]').text.strip(': ')
        print(config_wifi24_basico_redeprivada)
        config_wifi24_basico_redeprivada_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_basico_redeprivada_valor == 'true':
            config_wifi24_basico_redeprivada_valor = 'Habilitado' 
            config_original_wifi24 = 0
        else:
            config_wifi24_basico_redeprivada_valor = 'Desabilitado'
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').click()
            time.sleep(1)
            config_original_wifi24 = 1
        print(config_wifi24_basico_redeprivada_valor)
        
        config_wifi24_basico_anuncio = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[1]').text.strip(': ')
        print(config_wifi24_basico_anuncio)
        config_wifi24_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_basico_anuncio_valor == 'true':
            config_wifi24_basico_anuncio_valor = 'Habilitado'
        else:
            config_wifi24_basico_anuncio_valor = 'Desabilitado'
        print(config_wifi24_basico_anuncio_valor)

        config_wifi24_basico_ssid = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[1]').text.strip(': ')
        print(config_wifi24_basico_ssid)
        config_wifi24_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_property('value')
        print(config_wifi24_basico_ssid_valor)

        config_wifi24_basico_ssid_senha = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[1]').text.strip(': ')
        print(config_wifi24_basico_ssid_senha)
        config_wifi24_basico_ssid_senha_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_property('value')
        print(config_wifi24_basico_ssid_senha_valor)
        config_wifi24_basico_seguranca = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[1]').text.strip(': ')
        print(config_wifi24_basico_seguranca)
        config_wifi24_basico_seguranca_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[2]/select')).first_selected_option.text
        print(config_wifi24_basico_seguranca_valor)

        config_wifi24_basico_wps = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[1]').text.strip(': ')
        print(config_wifi24_basico_wps)
        config_wifi24_basico_wps_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_basico_wps_valor == 'true':
            config_wifi24_basico_wps_valor = 'Habilitado'
        else:
            config_wifi24_basico_wps_valor = 'Desabilitado'
        print(config_wifi24_basico_wps_valor)

        config_wifi24_avancado = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a')
        config_wifi24_avancado.click()
        time.sleep(1)
        config_wifi24_avancado = config_wifi24_avancado.text
        print(config_wifi24_avancado)

        config_wifi24_avancado_modooperacao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[1]').text.strip(': ')
        print(config_wifi24_avancado_modooperacao)
        config_wifi24_avancado_modooperacao_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(config_wifi24_avancado_modooperacao_valor)

        config_wifi24_avancado_canal = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[1]').text
        print(config_wifi24_avancado_canal)
        config_wifi24_avancado_canal_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[2]/select')).first_selected_option.text
        print(config_wifi24_avancado_canal_valor)

        config_wifi24_avancado_largurabanda = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[1]').text.strip(': ')
        print(config_wifi24_avancado_largurabanda)
        config_wifi24_avancado_largurabanda_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[2]/select')).first_selected_option.text
        print(config_wifi24_avancado_largurabanda_valor)

        config_wifi24_avancado_wmm = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[4]/td[1]').text.strip(': ')
        print(config_wifi24_avancado_wmm)
        config_wifi24_avancado_wmm_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[4]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_avancado_wmm_valor == 'true' :
            config_wifi24_avancado_wmm_valor = 'Habilitado' 
        else:
            config_wifi24_avancado_wmm_valor = 'Desabilitado'
        print(config_wifi24_avancado_wmm_valor)

        config_wifi24_avancado_mac = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[6]/td[1]').text
        print(config_wifi24_avancado_mac)
        config_wifi24_avancado_mac_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[6]/td[2]').text
        print(config_wifi24_avancado_mac_valor)

        if config_original_wifi24 == 1:
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[2]').click()
            config_original_wifi24 = 0

        time.sleep(3)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> WIFI 5GHz '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > WIFI 5GHz
        ### ------------------------------------------ ###
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
        time.sleep(2)
        config_wifi5 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/h3').text
        print(config_wifi5)
        config_wifi5_basico = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/thead/tr/th').text
        print(config_wifi5_basico)
        config_wifi5_basico_redeprivada = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[1]').text.strip(': ')
        print(config_wifi5_basico_redeprivada)
        config_wifi5_basico_redeprivada_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_basico_redeprivada_valor == 'true':
            config_wifi5_basico_redeprivada_valor = 'Habilitado'
            config_original_wifi5 = 0
        else:
            config_wifi5_basico_redeprivada_valor = 'Desabilitado'
            # Habilitar o wi-fi para coletar as informacoes, o wifi voltara para configuracao original apos a coleta dos dados:
            config_wifi5_basico_habilitar = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]')
            config_wifi5_basico_habilitar.click()
            time.sleep(1)
            config_original_wifi5 = 1
        print(config_wifi5_basico_redeprivada_valor)

        config_wifi5_basico_anuncio = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[1]').text.strip(': ')
        print(config_wifi5_basico_anuncio)
        config_wifi5_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_basico_anuncio_valor == 'true':
            config_wifi5_basico_anuncio_valor = 'Habilitado'
        else:
            config_wifi5_basico_anuncio_valor = 'Desabilitado'
        print(config_wifi5_basico_anuncio_valor)

        config_wifi5_basico_ssid = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[1]').text.strip(': ')
        print(config_wifi5_basico_ssid)
        config_wifi5_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_property('value')
        print(config_wifi5_basico_ssid_valor)

        config_wifi5_basico_ssid_senha = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[1]').text.strip(': ')
        print(config_wifi5_basico_ssid_senha)
        config_wifi5_basico_ssid_senha_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_property('value')
        print(config_wifi5_basico_ssid_senha_valor)
        config_wifi5_basico_seguranca = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[1]').text.strip(': ')
        print(config_wifi5_basico_seguranca)
        config_wifi5_basico_seguranca_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[2]/select')).first_selected_option.text
        print(config_wifi5_basico_seguranca_valor)

        config_wifi5_basico_wps = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[1]').text
        print(config_wifi5_basico_wps)
        config_wifi5_basico_wps_valor = self._driver.find_element_by_xpath('//html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_basico_wps_valor == 'true':
            config_wifi5_basico_wps_valor = 'Habilitado'
        else:
            config_wifi5_basico_wps_valor = 'Desabilitado'
        print(config_wifi5_basico_wps_valor)

        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a').click()
        time.sleep(2)
        js = "$('tbody').contents().filter(function(){return this.nodeType === 8;}).replaceWith(function(){return this.data;})" # habilita elemento comentado
        self._driver.execute_script(js)

        config_wifi5_avancado = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/thead/tr/th').text
        print(config_wifi5_avancado)

        config_wifi5_avancado_modooperacao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[1]').text.strip(': ')
        print(config_wifi5_avancado_modooperacao)
        config_wifi5_avancado_modooperacao_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(config_wifi5_avancado_modooperacao_valor)

        config_wifi5_avancado_canal = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[1]').text.strip(': ')
        print(config_wifi5_avancado_canal)
        config_wifi5_avancado_canal_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[2]/select')).first_selected_option.text
        print(config_wifi5_avancado_canal_valor)

        config_wifi5_avancado_largurabanda = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[1]').text.strip(': ')
        print(config_wifi5_avancado_largurabanda)
        config_wifi5_avancado_largurabanda_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[2]/select')).first_selected_option.text
        print(config_wifi5_avancado_largurabanda_valor)
    
        config_wifi5_avancado_wmm = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[5]/td[1]').text.strip(": ")
        print(config_wifi5_avancado_wmm)
        config_wifi5_avancado_wmm_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[5]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_avancado_wmm_valor == 'true' :
            config_wifi5_avancado_wmm_valor = 'Habilitado' 
        else:
            config_wifi5_avancado_wmm_valor = 'Desabilitado'
        print(config_wifi5_avancado_wmm_valor)

        config_wifi5_avancado_mac = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[6]/td[1]').text.strip(': ')
        print(config_wifi5_avancado_mac)
        config_wifi5_avancado_mac_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[6]/td[2]').text
        print(config_wifi5_avancado_mac_valor)
        
        if config_original_wifi5 == 1:
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[2]').click()
            config_original_wifi5 = 0
        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> FIREWALL '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > FIREWALL
        ### ------------------------------------------ ###
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[6]/a').click()
        time.sleep(2)
        config_firewall = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/h3').text
        print(config_firewall)
    
        config_firewall_politicapadrao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/thead[1]/tr/th').text
        print(config_firewall_politicapadrao)
        config_firewall_politicapadrao_status = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[1]/tr/td[1]').text.strip(': ')
        print(config_firewall_politicapadrao_status)
        config_firewall_politicapadrao_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[1]/tr/td[2]/input[1]').get_attribute('checked')
        if config_firewall_politicapadrao_valor == 'true':
            config_firewall_politicapadrao_valor = 'Aceita'
        else:
            config_firewall_politicapadrao_valor = 'Rejeita'
        print(config_firewall_politicapadrao_valor)

        config_firewall_pingwan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/thead[2]/tr/th').text.strip(': ')
        print(config_firewall_pingwan)
        config_firewall_pingwan_status = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[2]/tr/td[1]').text.strip(': ')
        print(config_firewall_pingwan_status)
        config_firewall_pingwan_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[2]/tr/td[2]/input[1]').get_attribute('checked')
        if config_firewall_pingwan_valor == 'true':
            config_firewall_pingwan_valor = 'Aceita'
        else:
            config_firewall_pingwan_valor = 'Rejeita'
        print(config_firewall_pingwan_valor)



        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> MODO DA WAN '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > MODO DA WAN
        ### ------------------------------------------ ###
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[7]/a').click()
        time.sleep(2)
        config_modowan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/h3').text
        print(config_modowan)

        config_modowan_bridge = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/thead/tr/th').text
        print(config_modowan_bridge)

        config_modowan_bridge_modo = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[1]').text.strip(': ')
        print(config_modowan_bridge_modo)
        config_modowan_bridge_modo_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(config_modowan_bridge_modo_valor)

        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> GERENCIAMENTO >> IDIOMA '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > IDIOMA
        ### ------------------------------------------ ###
        
        gerenciamento = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a')
        gerenciamento.click()
        time.sleep(1)
        gerenciamento = gerenciamento.text
        print(gerenciamento)   
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[1]/a').click()
        time.sleep(5)
        gerenciamento_idioma = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/h3').text
        print(gerenciamento_idioma)
    
        gerenciamento_idioma_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td/input[1]').get_attribute('checked')
        if gerenciamento_idioma_valor == 'true':
            gerenciamento_idioma_valor = 'Português'
        else:
            gerenciamento_idioma_valor = 'Inglês'
        print(gerenciamento_idioma_valor)

        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> SOBRE O DISPOSITIVO  '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > SOBRE O DISPOSITIVO
        ### ------------------------------------------ ###

        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[4]/a').click()
        time.sleep(2)
        sobre = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/h3').text
        print(sobre)

        info_dispositivo = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/thead/tr/th').text
        print(info_dispositivo)
        info_dispositivo_fabricante = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[1]/strong').text.strip(': ')
        print(info_dispositivo_fabricante)
        info_dispositivo_fabricante_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]').text
        print(info_dispositivo_fabricante_valor)

        info_dispositivo_firmware = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[1]/strong').text
        print(info_dispositivo_firmware)
        info_dispositivo_firmware_valor = self._driver.find_element_by_xpath('//html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[2]').text
        print(info_dispositivo_firmware_valor)

        info_dispositivo_serial = self._driver.find_element_by_xpath('//html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[1]/strong').text
        print(info_dispositivo_serial)
        info_dispositivo_serial_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]').text
        print(info_dispositivo_serial_valor)

        info_dispositivo_macwan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[1]/strong').text
        print(info_dispositivo_macwan)
        info_dispositivo_macwan_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]').text
        print(info_dispositivo_macwan_valor)

        info_dispositivo_modelo = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[3]/strong').text.strip(': ')
        print(info_dispositivo_modelo)
        iinfo_dispositivo_modelo_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[4]').text
        print(iinfo_dispositivo_modelo_valor)

        info_dispositivo_hardware = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[3]/strong').text
        print(info_dispositivo_hardware)
        info_dispositivo_hardware_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[4]').text
        print(info_dispositivo_hardware_valor)

        info_dispositivo_serialgpon = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[3]/strong').text.strip(': ')
        print(info_dispositivo_serialgpon)
        info_dispositivo_serialgpon_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[4]').text
        print(info_dispositivo_serialgpon_valor)

        info_dispositivo_maclan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[3]/strong').text.strip(': ')
        print(info_dispositivo_maclan)
        info_dispositivo_maclan_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[4]').text
        print(info_dispositivo_maclan_valor)


        #print('\n\n\n == Criando JSON de saída... == ')
        dict_saida425 = {
                        "Status":
                            {
                            gpon:
                                {
                                    divOptical[0]:divOptical[1],
                                    divOptRx[0]:divOptRx[1],
                                    divOptTx[0]:divOptTx[1]
                                },
                            internet:
                                {
                                    divPpp[0]: divPpp[1],
                                    detalhes_IPv4_head:
                                        {
                                            detalhes_IPv4_nome[0]: detalhes_IPv4_valor[0],
                                            detalhes_IPv4_nome[1]: detalhes_IPv4_valor[1],
                                            detalhes_IPv4_nome[2]: detalhes_IPv4_valor[2],
                                            detalhes_IPv4_nome[3]: detalhes_IPv4_valor[3],
                                            detalhes_IPv4_nome[4]: detalhes_IPv4_valor[4]
                                        },
                                    detalhes_IPv6_head:
                                        {
                                            detalhes_IPv6_nome[0]: detalhes_IPv6_valor[0],
                                            detalhes_IPv6_nome[1]: detalhes_IPv6_valor[1],
                                            detalhes_IPv6_nome[2]: detalhes_IPv6_valor[2],
                                            detalhes_IPv6_nome[3]: detalhes_IPv6_valor[3],
                                            detalhes_IPv6_nome[4]: detalhes_IPv6_valor[4],
                                            detalhes_IPv6_nome[5]: detalhes_IPv6_valor[5]
                                        }
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
                            rede_local:
                                {
                                    rede_local_name[0]: rede_local_name[1],
                                    rede_local_name[2]: rede_local_name[3],
                                    rede_local_name[4]: rede_local_name[5],
                                    "Estações Conectadas:": rede_local_stations
                                },
                            tv:
                                {
                                    tv_valor[0]: tv_valor[1],
                                    tv_valor[2]: tv_valor[3],
                                    "Estações Conectadas:": tv_stations
                                },
                            telefone:
                                {
                                    telefone_info_rede[0]: telefone_info_rede[1],
                                    telefone_info_status[0]: telefone_info_status[1],
                                    "Estações Conectadas:": telefone_stations
                                }
                            },
                        "Configurações":
                            {
                                "Internet":
                                    {
                                        config_internet_usuario: config_internet_usuario_valor,
                                        config_internet_senha: config_internet_senha_valor
                                    },
                                rede_local:
                                    {
                                        config_redelocal_dhcp:config_redelocal_servidordhcp_valor,
                                        config_redelocal_iphgu:config_redelocal_iphgu_valor,
                                        config_redelocal_mask:config_redelocal_mask_valor,
                                        config_redelocal_pool:
                                            {
                                                "inicio:":config_redelocal_pool_ini_valor,
                                                "fim:":config_redelocal_pool_fin_valor
                                            },
                                        config_redelocal_dns:config_redelocal_dns_valor,
                                        config_redelocal_concessao:config_redelocal_concessao_valor
                                    },
                                'Rede Wifi 2.4Ghz':
                                    {
                                        config_wifi24_basico:
                                            {
                                                config_wifi24_basico_redeprivada:config_wifi24_basico_redeprivada_valor,
                                                config_wifi24_basico_anuncio:config_wifi24_basico_anuncio_valor,
                                                config_wifi24_basico_ssid:config_wifi24_basico_ssid_valor,
                                                config_wifi24_basico_ssid_senha:config_wifi24_basico_ssid_senha_valor,
                                                config_wifi24_basico_seguranca:config_wifi24_basico_seguranca_valor,
                                                config_wifi24_basico_wps:config_wifi24_basico_wps_valor
                                            },
                                        config_wifi24_avancado:
                                            {
                                                config_wifi24_avancado_modooperacao:config_wifi24_avancado_modooperacao_valor,
                                                config_wifi24_avancado_canal:config_wifi24_avancado_canal_valor,
                                                config_wifi24_avancado_largurabanda:config_wifi24_avancado_largurabanda_valor,
                                                config_wifi24_avancado_mac:config_wifi24_avancado_mac_valor
                                            }
                                    },
                                'Rede Wifi 5Ghz':
                                    {
                                        config_wifi5_basico:
                                            {
                                                config_wifi5_basico_redeprivada: config_wifi5_basico_redeprivada_valor,
                                                config_wifi5_basico_anuncio: config_wifi5_basico_anuncio_valor,
                                                config_wifi5_basico_ssid: config_wifi5_basico_ssid_valor,
                                                config_wifi5_basico_ssid_senha: config_wifi5_basico_ssid_senha_valor,
                                                config_wifi5_basico_seguranca: config_wifi5_basico_seguranca_valor,
                                                config_wifi5_basico_wps: config_wifi5_basico_wps_valor
                                            },
                                        config_wifi5_avancado:
                                            {
                                                config_wifi5_avancado_modooperacao: config_wifi5_avancado_modooperacao_valor,
                                                config_wifi5_avancado_canal: config_wifi5_avancado_canal_valor,
                                                config_wifi5_avancado_largurabanda: config_wifi5_avancado_largurabanda_valor,
                                                config_wifi5_avancado_wmm: config_wifi5_avancado_wmm_valor,
                                                config_wifi5_avancado_wmm: config_wifi5_avancado_wmm_valor,
                                                config_wifi5_avancado_mac: config_wifi5_avancado_mac_valor
                                            }
                                    },
                                "Firewall":
                                    {
                                        config_firewall_politicapadrao:
                                            {
                                                config_firewall_politicapadrao_status:config_firewall_politicapadrao_valor
                                            },
                                        config_firewall_pingwan:
                                            {
                                                config_firewall_pingwan_status:config_firewall_pingwan_valor
                                            }
                                    },
                                "Modo da Wan":
                                    {
                                        config_modowan_bridge:
                                            {
                                                config_modowan_bridge_modo:config_modowan_bridge_modo_valor
                                            }
                                    }
                            },
                        gerenciamento:
                            {
                                gerenciamento_idioma:gerenciamento_idioma_valor
                            },
                        sobre:
                            {
                                info_dispositivo:
                                    {
                                        info_dispositivo_fabricante:info_dispositivo_fabricante_valor,
                                        info_dispositivo_firmware:info_dispositivo_firmware_valor,
                                        info_dispositivo_serial:info_dispositivo_serial_valor,
                                        info_dispositivo_macwan:info_dispositivo_macwan_valor,
                                        info_dispositivo_modelo:iinfo_dispositivo_modelo_valor,
                                        info_dispositivo_hardware:info_dispositivo_hardware_valor,
                                        info_dispositivo_serialgpon:info_dispositivo_serialgpon_valor,
                                        info_dispositivo_maclan:info_dispositivo_maclan_valor
                                    }
                            }
                        }

        self._driver.quit()

        print(dict_saida425)
        user = dict_saida425['Configurações']['Internet'].get('Usuário')
        if user == 'cliente@cliente':
            self._dict_result.update({"Resultado_Probe": "OK", "obs": "Usuario: cliente@cliente", "result":"passed"})
        else:
            self._dict_result.update({"obs": f"Teste incorreto, retorno Usuario: {user}"})

        self.update_global_result_memory(flask_username, 'getFullConfig_425', dict_saida425)
        return self._dict_result


    def verificarSenhaPppDefaultFibra_426(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            senha = result['Configurações']['Internet'].get('Senha')
            if senha == 'cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'senha:cliente', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno senha: {senha}'})
            
        return self._dict_result    


    def checkWanInterface_x_427(self, flask_username, interface):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            time.sleep(5)
            self.login_support()
            time.sleep(5)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="item14"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/blockquote/form/center/table/tbody/tr[5]/td[15]/input').click()
            time.sleep(1)
            # Pegando o Dual Stack
            network_protocol = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[2]/select').get_attribute('value')

            
            final_dict = {'network_protocol': network_protocol, 'Addressing Type': 'Nao existe'}

            # Resposta do teste 
            if network_protocol == 'IPv4&IPv6':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Adm.State: Dual Stack", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno {network_protocol}"})
            print(final_dict)
        except IndexError as exception:
            self._dict_result.update({'obs': exception})
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkWanInterface_x_427', final_dict)
        return self._dict_result


    def validarDHCPv6Wan_428(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        print(result)
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            ans_428 = result['Addressing Type']
            if 'SLAAC' == ans_428:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Addressing Type igual a MSFT_IPTV and TEF_IPTV", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Addressing Type: {ans_428}"})
        return self._dict_result


    def checkLANSettings_429(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="folder15"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="item17"]/table/tbody/tr/td/a').click()
            time.sleep(1)

            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            # form_elements = self._driver.find_elements_by_xpath('/html/body/blockquote//form')
            # print(form_elements)
            # names = [values.text for values in form_elements]
            # print(names)
            # attributes = [values.get_attribute('value') for values in form_elements]
            # print('attr aqui ',attributes)
            prefix_element = self._driver.find_elements_by_xpath('/html/body/blockquote/form/div[2]/table[2]/tbody/tr//td')
            prefix = [values.text.strip().replace(":", "") for values in prefix_element]

            final_dict = {prefix[0]: prefix[1]}

            if prefix[1] == 'ip2':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix: ip2", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno do Prefix:{prefix[1]}"})
    
        except IndexError as exception:
            self._dict_result.update({'obs': exception})
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkLANSettings_429', final_dict)
            print(final_dict)
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_431(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Type')
                if iface_type == 'PPPoE' and cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if sub_dict.get('VlanMuxId') == '8,35':
                        self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VID: 8,35', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: PPPoE, VID: {sub_dict.get('VlanMuxId')}"})
                        break
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_432(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('VlanMuxId')
                if iface_type == '8,35' and cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if sub_dict.get('Type') == 'PPPoE':
                        self._dict_result.update({"obs": 'VID: 8,35 Encapsulamento: PPPoE', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs":  f"Teste incorreto, retorno VID: {iface_type}, Encapsulamento: {sub_dict.get('Type')}"})
                        break
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_433(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                status = result['ppp0.1'].get('NAT')
                if status == 'Enabled':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'interface ppp0.1 NAT: Habilitado', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno interface NAT Status: {status}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result        
               
 
    def vivo_1_usernamePppDefault_435(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 425 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            usuario = result['Configurações']['Internet']['Usuário']
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if usuario == 'cliente@cliente':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Usuário: cliente@cliente', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno: Usuário: {usuario}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_passwordPppDefault_436(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        cpe_config = config_collection.find_one()
        if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
            senha = result['Configurações']['Internet'].get('Senha')
            if senha == 'cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Senha: cliente', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno senha:{senha}'})
        else:
            self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        return self._dict_result


    def checkWanInterface_x_437(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                network_protocol = result['network_protocol']
                if network_protocol == 'IPv4&IPv6':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Adm.State: Dual Stack", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno {network_protocol}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})               
        return self._dict_result


    def validarDHCPv6Wan_438(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        print(result)
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                ans_438 = result['Addressing Type']
                if 'SLAAC' == ans_438:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Addressing Type igual a MSFT_IPTV and TEF_IPTV", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Addressing Type: {ans_438}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result

    def checkLANSettings_439(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                prefix = result['Prefix']
                if prefix == 'ip2':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix: ip2", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno do Prefix:{prefix}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_441(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            for _, sub_dict in result.items():
                cpe_config = config_collection.find_one()
                if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if sub_dict.get('Type') == 'PPPoE':
                        iface_type = sub_dict.get('VlanMuxId')
                        if iface_type == '8,35':
                            self._dict_result.update({"obs": 'Encapsulamento PPPoE, VID: 0,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VID: 0,35'})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {sub_dict.get('Type')}"})
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_442(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            for _, sub_dict in result.items():
                cpe_config = config_collection.find_one()
                iface_type = sub_dict.get('VlanMuxId')
                if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if iface_type == '8,35':
                        if sub_dict.get('Type') == 'PPPoE':
                            self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VID: 8,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {sub_dict.get('Type')}"})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno VID: {iface_type}"})
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_443(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                status = result['ppp0.1'].get('NAT')
                if status == 'Enabled':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'interface ppp0.1 NAT: Habilitado', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno interface NAT Status: {status}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result     

        
    def vivo_2_usernamePppDefault_445(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        try:
            result = session.get_result_from_test(flask_username, 'getFullConfig_425')
            cpe_config = config_collection.find_one()
            usuario = result['Configurações']['Internet']['Usuário']
            #print('\n #445 usuario:', usuario)
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if usuario == 'cliente@cliente':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Usuário: cliente@cliente', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno Usuário: {usuario}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        except Exception:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        finally:
            return self._dict_result


    def vivo_2_passwordPppDefault_446(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
            
        cpe_config = config_collection.find_one()
        if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
            senha = result['Configurações']['Internet'].get('Senha')
            if senha == 'cliente@cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Senha: cliente@cliente', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Senha: {senha}'})
        else:
            self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        return self._dict_result


    def validarDualStack_447(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':    
                network_protocol = result['network_protocol']
                if network_protocol == 'IPv4&IPv6':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Adm.State: Dual Stack", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno {network_protocol}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def validarDHCPv6Wan_448(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':  
                ans_448 = result['Addressing Type']
                if 'SLAAC' == ans_448:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Addressing Type igual a MSFT_IPTV and TEF_IPTV", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Addressing Type: {ans_448}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result
    

    def prefixDelegationInet_449(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':   
                prefix = result['Prefix']
                if prefix == 'ip2':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix: ip2", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno do Prefix:{prefix}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result



    def vivo_1_vlanIdIptvVivo1_450(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
            
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'veip0.3':
                        if sub_dict.get('VlanMuxId') == '20':
                            self._dict_result.update({"obs": 'Name: veip0.3 | VLAN: 20', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: veip0.3| VLAN {sub_dict.get("VlanMuxId")}'})
                            break
                    else:
                        self._dict_result.update({"obs":  f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})

        return self._dict_result


    def vivo_1_prioridadeIptv_451(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        print(result)
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            for _, sub_dict in result.items():
                cpe_config = config_collection.find_one()
                if cpe_config['REDE'] == 'VIVO_1': 
                    if sub_dict.get('Description') == 'Vod_ip_interface':
                        priority = sub_dict.get('Vlan8021p')
                        if priority == '3':
                            self._dict_result.update({"obs": 'Description: Vod_ip_interface,  Prioridade: 3', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Description: Vod_ip_interface, Prioridade: {priority}"})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Description: {sub_dict.get('Description')}"})
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_validarNatIptv_452(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Vod_ip_interface':
                        if sub_dict.get('NAT') == 'Enabled':
                            self._dict_result.update({"obs": 'Interface: Vod_ip_interface | NAT: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Vod_ip_interface | NAT: {sub_dict.get("NAT")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_igmpIptv_453(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                try: 
                    igmp_inet = result['ppp0.1']['Igmp Proxy']
                    if igmp_inet == 'Enabled':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: ppp0.1 | IGMP: Desabilitado", "result":"passed"})
                    else:
                        self._dict_result.update({"obs": "Interface: ppp0.1 | IGMP: Habilitado"})
                except Exception:
                    self._dict_result.update({"obs": "Interface ppp0.1 nao existe"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result    


    def vlanIdVodVivo2_454(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Vod_ip_interface':
                        vid = sub_dict.get('VlanMuxId')
                        if vid == '602':
                            self._dict_result.update({"obs": 'Description: Vod_ip_interface, VLAN: 602', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Description: Vod_ip_interface, VID: {vid}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo2_validarNatIPTV_455(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict.get('Vlan8021p')
                    if iface_type == '3':
                        if sub_dict.get('VlanMuxId') == '602':
                            iface_name = sub_dict.get('Description')
                            break

                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == iface_name:
                        if sub_dict.get('NAT') == 'Enabled':
                            self._dict_result.update({"obs": 'Interface: Vod_ip_interface | NAT: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Vod_ip_interface | NAT: {sub_dict.get("NAT")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name 1: {iface_type}, Name 2: {iface_name} '})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo_2_igmpVoD_456(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                try: 
                    igmp_inet = result['ppp0.1']['Igmp Proxy'] # Verificar o equivalente a interface IP5! seria o veip0.4 (multicast)?
                    if igmp_inet == 'Enabled':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: ppp0.1 | IGMP: Desabilitado", "result":"passed"})
                    else:
                        self._dict_result.update({"obs": "Interface: ppp0.1 | IGMP: Habilitado"})
                except Exception:
                    self._dict_result.update({"obs": "Interface ppp0.1 nao existe"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result  


    def vlanIdMulticastVivo2_457(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": f'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Multicast_ip_interface':
                        if sub_dict.get('VlanMuxId') == '4000':
                            self._dict_result.update({"obs": 'Name: Multicast_ip_interface | VID: 4000', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: Multicast_ip_interface | VID: {sub_dict.get("VlanMuxId")} '})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def natMulticastVivo2_458(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Description')
                if iface_type == 'Vod_ip_interface':
                    if sub_dict.get('NAT') == 'Disable':
                        self._dict_result.update({"obs": 'Interface: Vod_ip_interface | Adm.State: Desabilitado', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Vod_ip_interface | Adm.State: Habilitado '})
                        break
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
        return self._dict_result


    def checkIGMPVivo2_459(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            try: 
                igmp_inet = result['veip0.3']['Igmp Proxy'] # Verificar o equivalente a interface IP5! seria o veip0.4 (multicast)?
                if igmp_inet == 'Enabled':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: veip0.3 | IGMP: Habilitado", "result":"passed"})
                else:
                    self._dict_result.update({"obs": "Interface: veip0.3 | IGMP: Desabilitado"})
            except Exception:
                    self._dict_result.update({"obs": "Interface veip0.3 nao existe"})
        return self._dict_result    


    def vivo1_vlanIdVoip_460(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": f'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Voip_ip_interface':
                        if sub_dict.get('VlanMuxId') == '30':
                            obs_result = 'Name: VoIP | VID: 30'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result = f'Teste incorreto, retorno Name: VoIP, VID: {sub_dict.get("VlanMuxId")}'
                            break
                    else:
                        obs_result = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"
            
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Voip_ip_interface':
                        if sub_dict.get('VlanMuxId') == '601':
                            obs_result2 = 'Name: VoIP | VID: 601'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Name: VoIP, VID: {sub_dict.get("VlanMuxId")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"

            self._dict_result.update({"obs": f"Teste 460_1: {obs_result}, Teste 460_2: {obs_result2}" })
        return self._dict_result


    def vivo2_prioridadeVoip_461(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": f'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Voip_ip_interface':
                        if sub_dict.get('Vlan8021p') == '5':
                            obs_result = 'Name: VoIP | Priority: 5'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result = f'Teste incorreto, retorno Name: VoIP | Priority: {sub_dict.get("Vlan8021p")}'
                            break
                    else:
                        obs_result = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"

            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Voip_ip_interface':
                        if sub_dict.get('Vlan8021p') == '601':
                            obs_result2 = 'Name: VoIP | Priority: 601'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Name: VoIP | Priority: {sub_dict.get("Vlan8021p")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
        
            self._dict_result.update({"obs": f"Teste 461_1: {obs_result}, Teste 461_2: {obs_result2}" })
        return self._dict_result


    def vivo1_validarNatVoip_462(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict.get('Vlan8021p')
                    if iface_type == '5':
                        if sub_dict.get('VlanMuxId') == '30':
                            iface_name = sub_dict.get('Interface')
                            obs_result1 = f"Name: {iface_name}"
                            break
                        else:
                            obs_result1 = (f'Teste incorreto, retorno Priority: 5 | VLAN: {sub_dict.get("VlanMuxId")}')
                            self._dict_result.update({"result":"failed", "Resultado_Probe": "NOK"})

                            break
                    else:
                        obs_result1 = (f'Teste incorreto, retorno Priority: {iface_type}')
            
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == iface_name:
                        if sub_dict.get('NAT') == 'Enabled':
                            obs_result1 = 'Adm.State: Habilitado'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result1 = f'Teste incorreto, retorno Adm.State: {sub_dict.get("NAT")}'
                            self._dict_result.update({"result":"failed", "Resultado_Probe": "NOK"})

                            break
                    else:
                        obs_result1 = f'Teste incorreto, retorno {iface_type} diferente de {iface_name}'

            else:
                obs_result1 = f"REDE:{cpe_config['REDE']}"
                self._dict_result.update({"result":"failed", "Resultado_Probe": "NOK"})

        #2
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict.get('Vlan8021p')
                    if iface_type == '5':
                        if sub_dict.get('VlanMuxId') == '601':
                            iface_name = sub_dict.get('Interface')
                            obs_result2 = f"Name: {iface_name}"
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Priority: 5, VLAN: {sub_dict.get("VlanMuxId")}'
                            self._dict_result.update({"result":"failed", "Resultado_Probe": "NOK"})

                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Priority: {iface_type}'
                    
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == iface_name:
                        if sub_dict.get('NAT') == 'Enabled':
                            obs_result2 = 'Adm.State: Habilitado'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Adm.State: {sub_dict.get("NAT")}'
                            self._dict_result.update({"result":"failed", "Resultado_Probe": "NOK"})
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno {iface_type} diferente de {iface_name}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
                self._dict_result.update({"result":"failed", "Resultado_Probe": "NOK"})
        
        self._dict_result.update({"obs": f"Teste 462_1: {obs_result1}, Teste 462_2: {obs_result2}" })
        return self._dict_result


    def vivo_1_igmpVoip_463(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                try: 
                    igmp_inet = result['veip0.2']['Igmp Proxy'] # Verificar o equivalente a interface IP5! seria o veip0.4 (multicast)?
                    if igmp_inet == 'Enabled':
                        obs_result = 'Interface: veip0.2 | IGMP: Habilitado'
                        self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                    else:
                        obs_result =  'Teste incorreto, retorno Interface: veip0.2 | IGMP: Desabilitado'
                except Exception:
                        obs_result = 'Interface veip0.2 nao existe'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"
            
            if cpe_config['REDE'] == 'VIVO_2':
                try: 
                    igmp_inet = result['veip0.2']['Igmp Proxy'] # Verificar o equivalente a interface IP5! seria o veip0.4 (multicast)?
                    if igmp_inet == 'Enabled':
                        obs_result2 = 'Interface: veip0.2 | IGMP: Habilitado'
                        self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                    else:
                        obs_result2 =  'Teste incorreto, retorno Interface: veip0.2 | IGMP: Desabilitado'
                except Exception:
                        obs_result2 = 'Interface veip0.2 nao existe'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
            self._dict_result.update({"obs": f"463_1: {obs_result}, 463_2: {obs_result2}"})
        return self._dict_result


    def checkLANDHCPSettings_x_464(self, flask_username, port='4'):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="folder15"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            final_dict = {}

            # IGMP /html/body/blockquote/form/table[2]/tbody/tr/td
            igmp_is_checked = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td//input')]
            igmp_is_checked = 'Habilitado' if igmp_is_checked[0] == 'true' else 'Desabilitado'

            # Pegando a chave e o valor para o gateway e subnet
            ip_elements = [value.text.strip().replace(":", "") for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr//td')]
            ip_values = [value.get_attribute('value') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr/td//input')]
            final_dict.update({ip_elements[0]: ip_values[0], ip_elements[2]: ip_values[1]})

            # Para o teste 465
            lista = [value.text.strip().replace(":", "") for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/div[3]/table[2]/tbody/tr//td')]
            ip_start_end = [value for value in lista if value != '' and value != 'DHCP options']
            ip_start_end_values = [value.get_attribute('value') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/div[3]/table[2]/tbody/tr/td//input')]


            # Infos da tabela 
            tabela_name = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/div[3]/table[4]/tbody/tr[2]/td/table/tbody/tr[1]//td')]
            tabela_values = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/div[3]/table[4]/tbody/tr[2]/td/table/tbody/tr[2]//td')]
            tabela_user_id = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/div[3]/table[4]/tbody/tr[2]/td/table/tbody/tr[3]//td')]
            tabela_values2 = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/div[3]/table[4]/tbody/tr[2]/td/table/tbody/tr[4] //td')]

            self._driver.quit()

            # Colocando no dict infos do teste 465
            for v in range(0, len(ip_start_end)):
                final_dict.update({ip_start_end[v]: ip_start_end_values[v]})

            # Colocando no dict infos do teste 467
            tabela_1 = {}
            tabela_2 = {}
            for v in range(0, len(tabela_name)):
                tabela_1.update({tabela_name[v]: tabela_values[v]})
                tabela_2.update({tabela_name[v]: tabela_values2[v]})

            final_dict.update({'tabela_values1': tabela_1, 'tabela_values2': tabela_2})
            final_dict.update({tabela_user_id[0]: tabela_user_id[1], 'igmp': igmp_is_checked})

            print(final_dict)

            if final_dict['IP Address'] == '192.168.17.1':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": f"Gateway: 192.168.17.1", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Gateway: {final_dict['IP Address']}"})

        
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self.update_global_result_memory(flask_username, 'checkLANDHCPSettings_x_464', final_dict)
        return self._dict_result


    def poolDhcpLan_465(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            start_addr = result['Start IP Address']
            end_addr = result['End IP Address']
            if start_addr == '192.168.15.2' and end_addr == '192.168.15.200':
                self._dict_result.update({"obs": 'IP Address Range OK', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": 'IP Address Range NOK'})
        return self._dict_result


    def leaseTime_466(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            ans_466 = result['Leased Time (second)']
            if '14400' == ans_466:
                self._dict_result.update({"obs": 'Lease Time: 14400', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Lease Time: {ans_466}'})      
        return self._dict_result


    
    def vendorIdIptvEnable_467(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            vendorID_check = result['Vendor Information']
            user_id = result['User Class ID']
            cpe_config = config_collection.find_one()
            
            #1
            if vendorID_check == 'Enabled':
                obs_result1 = f'VendorID esta Habilitado'
                self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result1 = f"Teste incorreto, retorno VendorID: {vendorID_check}"

            #2
            if cpe_config['REDE'] == 'VIVO_1':
                vendorID = result['tabela_values1'].get('Vendor Class ID') + ',' +result['tabela_values2'].get('Vendor Class ID')
                print(vendorID)
                if vendorID == 'MSFT_IPTV,TEF_IPTV':
                    obs_result2 = f'Valor VendorID: {vendorID}'
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                    obs_result2 = f"Teste incorreto, retorno Valor VendorID: {vendorID}"
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result2 = f"REDE:{cpe_config['REDE']}"
            
            #3
            if cpe_config['REDE'] == 'VIVO_2':
                if user_id == 'GVT-STB,RSTIH89-500_HD,DSTIH78_GVT,VM1110,DSTIH79_GVT,VM1110_HD_HYBRID,DSITH79_GVT_HD':
                    obs_result3 = f'Valor VendorID: {vendorID}'
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                    obs_result3 = f"Teste incorreto, retorno Valor VendorID: {vendorID}"
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result3 = f"REDE:{cpe_config['REDE']}"

            self._dict_result.update({"obs": f"467_1: {obs_result1} | 467_2: {obs_result2} | 467_3: {obs_result3}"})
            
        return self._dict_result


    def poolDhcpIptv_468(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 464 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 467 primeiro'})
        else:
            ip_inicio = result['tabela_values1']['Start IP']
            ip_fim = result['tabela_values1']['End IP']
            if ip_inicio == '192.168.17.230' and ip_fim == '192.168.17.254':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'IP Address Range: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno IP Address Range: {ip_inicio} | {ip_fim}'})         
        return self._dict_result

    
    def igmpSnoopingLAN_469(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 464 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            igmp_check = result['igmp']
            if igmp_check == 'Habilitado':
                self._dict_result.update({"obs": 'IGMP Snooping: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno IGMP Snooping: {igmp_check}'})
       
        return self._dict_result



    def verificarWifi24SsidDefault_470(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_ssid = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['SSID']
            ssid = re.findall("^VIVOFIBRA-\w{4}", result_ssid)
            if ssid:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'SSID: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'SSID: {result_ssid}'})
        return self._dict_result


    def verificarWifi24Habilitado_471(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            rede_pv = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['Rede Wi-Fi Privada']
            if rede_pv == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Rede Wi-Fi Privada: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Rede Wi-Fi Privada: {rede_pv}'})
        return self._dict_result


    def verificarWifi24Padrao_472(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            modo_ope = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado']['Modo de Operação']
            if modo_ope == '802.11g/n':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11g/n', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Operação: {modo_ope}'})
        return self._dict_result


    def frequencyPlan_473(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(1) 
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[46]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[47]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[51]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        bandwidth24G = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[2]/table/tbody/tr[1]/td[1]').text
        bandwidth24G_value = Select(self._driver.find_element_by_xpath('/html/body/blockquote/form/div[2]/table/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(bandwidth24G, '=', bandwidth24G_value)
        channel24G = self._driver.find_element_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr[2]/td[1]').text
        channel24G_values = self._driver.find_element_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr[2]/td[2]/select')
        channel24G_list = [x.text for x in channel24G_values.find_elements_by_tag_name("option")]
        print(channel24G, '=', channel24G_list)
        self._driver.quit()

        cpe_config = config_collection.find_one()

        if bandwidth24G_value == '20MHz':
            ref_list = cpe_config["REF_CHANNEL_2_4_20MHz"]              
            if channel24G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

        else:
            ref_list = cpe_config["REF_CHANNEL_2_4_40MHz"]    
            if channel24G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

        return self._dict_result          


    def verificarWifi24AutoChannel_474(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            canal = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado'].get('Canal:')
            if canal == 'Automático':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Canal: Automático', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Canal: {canal}'})
            
        return self._dict_result


    def verificarWifi24LarguraBanda_475(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            larg_banda_canal = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado']['Largura de Banda do Canal']
            if larg_banda_canal == '20 MHz':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Largura de Banda do Canal: 20 MHz', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Largura de Banda do Canal: {larg_banda_canal}'})
            
        return self._dict_result


    def verificarWifi24Seguranca_476(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            seguranca = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['Modo de Segurança']
            if seguranca == 'WPA2':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Segurança: WPA2', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Segurança: {seguranca}'})          
        return self._dict_result


    def verificarWifi24PasswordDefault_477(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(1) 
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[46]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[47]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[49]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')

        passphrase_value = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[3]/table/tbody/tr/td[2]/input').get_attribute('value')
        #print(passphrase,"=", passphrase_value)
        self._driver.quit()
        
        password = re.findall("^\w{8}", passphrase_value)

        if password:
            self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Passprhase: OK', "result":"passed"})
        else:
            self._dict_result.update({"obs": 'Teste incorreto, retorno Passphrase: NOK'})          
      
        return self._dict_result


    def cipherModeDefault_478(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(1) 
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[46]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[47]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[49]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')

        encryption = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[4]/table/tbody/tr/td[1]').text
        encryption_value = Select(self._driver.find_element_by_xpath('/html/body/blockquote/form/div[4]/table/tbody/tr/td[2]/select')).first_selected_option.text
        print(encryption,"=", encryption_value)
        self._driver.quit()

        if encryption_value == "AES":
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Encryption: AES', "result":"passed"})
        else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Encryption: {encryption_value}'})          
      
        return self._dict_result


    def verificarWifi24WPS_479(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            wps = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['WPS']
            if wps == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'WPS: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno WPS: {wps}'})          
        return self._dict_result


    def verificarWifi5SsidDefault_480(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_ssid = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas']['SSID']
            ssid = re.findall("^VIVOFIBRA-\w{4}.*-5G$", result_ssid)
            if ssid:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'SSID: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno SSID: {result_ssid}'})
            
        return self._dict_result


    def verificarWifi5Habilitado_481(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            rede_pv = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('Rede Wi-Fi Privada')
            if rede_pv == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Rede Wi-Fi Privada: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Rede Wi-Fi Privada: {rede_pv}'})        
        return self._dict_result


    def verificarWifi5Padrao_482(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            modo_ope = result['Configurações']['Rede Wifi 5Ghz']['Configurações Avançadas'].get('Modo de Operação')
            if modo_ope == '802.11n/ac':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11n/ac', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Modo de Operação: {modo_ope}'})           
        return self._dict_result


    def frequencyPlan5GHz_483(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(1) 
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[46]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[54]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[58]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        bandwidth5G = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[2]/table/tbody/tr[1]/td[1]').text
        bandwidth5G_value = Select(self._driver.find_element_by_xpath('/html/body/blockquote/form/div[2]/table/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(bandwidth5G, ' = ', bandwidth5G_value)

        channel5G = self._driver.find_element_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr[2]/td[1]').text
        channel5G_values = self._driver.find_element_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr[2]/td[2]/select')
        channel5G_list = [x.text for x in channel5G_values.find_elements_by_tag_name("option")]
        print(channel5G, ' = ', channel5G_list)
        self._driver.quit()

        cpe_config = config_collection.find_one()
  
        if bandwidth5G_value == '20MHz':
            ref_list = cpe_config["REF_CHANNEL_5_20MHz"]              
            print('\n reference = ',ref_list) 
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
       
        if bandwidth5G_value == '40MHz':
            ref_list = ref_list = cpe_config["REF_CHANNEL_5_40MHz"]      
            print('\n reference = ',ref_list) 
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
         
        if bandwidth5G_value == '80MHz':
            ref_list = ref_list = cpe_config["REF_CHANNEL_5_80MHz"]   
            print('\n reference = ',ref_list) 
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

        return self._dict_result   


    def verificarWifi5AutoChannel_484(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            canal = result['Configurações']['Rede Wifi 5Ghz']['Configurações Avançadas'].get('Canal')
            if canal == 'Automático':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Canal: Automático', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Canal: {canal}'})         
        return self._dict_result


    def verificarWifi5LarguraBanda_485(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            larg_banda_canal = result['Configurações']['Rede Wifi 5Ghz']['Configurações Avançadas'].get('Largura de Banda do Canal')
            if larg_banda_canal == '80 MHz':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Largura de Banda do Canal: 80 MHz', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Largura de Banda do Canal: {larg_banda_canal}'})
            
        return self._dict_result


    def verificarWifi5Seguranca_486(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            seguranca = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('Modo de Segurança')
            if seguranca == 'WPA2':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Segurança: WPA2', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Modo de Segurança: {seguranca}'})          
        return self._dict_result


    def verificarWifi5PasswordDefault_487(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_senha = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('Senha')
            senha = re.findall("^\w{8}", result_senha)
            if senha:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Senha: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno Senha: NOK'})          
        return self._dict_result


    def cipherModeDefault5GHz_488(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(1) 
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[46]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[54]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[56]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')

        encryption = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[4]/table/tbody/tr/td[1]').text
        encryption_value = Select(self._driver.find_element_by_xpath('/html/body/blockquote/form/div[4]/table/tbody/tr/td[2]/select')).first_selected_option.text
        print(encryption,"=", encryption_value)
        self._driver.quit()
     
        if encryption_value == "AES":
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Encryption: AES', "result":"passed"})
        else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Encryption: {encryption_value}'})          
      
        return self._dict_result


    def verificarWifi5WPS_489(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            wps = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('WPS:')
            if wps == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'WPS: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno WPS: {wps}'})          
        return self._dict_result


    def checkVoIPSettings_490(self, flask_username):
        
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(3)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder60"]/table/tbody/tr/td/a').click()


            self._driver.switch_to.default_content()

            self._driver.switch_to.frame('basefrm')
            final_dict = {}            

            # Basic

            table_values = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/ul/div[2]/div/div[5]/table/tbody/tr//td')]
            ptime = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/ul/div[2]/div/div[5]/table/tbody/tr[10]/td[2]/select//option') if value.get_attribute('checked')]
            codec_1 = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/ul/div[2]/div/div[5]/table/tbody/tr[11]/td[2]/select//option') if value.get_attribute('checked')]
            codec_2 = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/ul/div[2]/div/div[5]/table/tbody/tr[12]/td[2]/select//option') if value.get_attribute('checked')]
            codec_3 = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/ul/div[2]/div/div[5]/table/tbody/tr[13]/td[2]/select//option') if value.get_attribute('checked')]
            
            len_table = int(len(table_values) / 2)
            n = 0
            for v in range(0,len_table):
                final_dict.update({table_values[n]: table_values[(n+1)]})
                n += 2
            
            final_dict.update({'Preferred ptime': ptime[0]})
            final_dict.update({'Preferred codec 1': codec_1[0]})
            final_dict.update({'Preferred codec 2': codec_2[0]})
            final_dict.update({'Preferred codec 3': codec_3[0]})


            # Advanced

            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="item62"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)

            # T38
            t38_checkbox = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/ul/div[2]/div/table[1]/tbody/tr/td[1]/input')]
            t38_checkbox = 'Habilitado' if t38_checkbox[0] == 'true' else 'Desabilitado'
            # DTMF
            dtmf = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/ul/div[2]/div/div[6]/table/tbody/tr/td[2]/select//option') if value.get_attribute('selected') == 'true']

            self._driver.quit()

            final_dict.update({'t38': t38_checkbox, 'dtmf': dtmf[0]})
            print('DICT: ',final_dict)
            cpe_config = config_collection.find_one()

            # 490_1        
            if cpe_config['REDE'] == 'VIVO_1':
                if final_dict['t38'] == 'Desabilitado':
                    obs_result1 =  f"Fax T38: Desabilitado"
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    obs_result1 = f"Teste incorreto, retorno Fax T38: {final_dict['t38'] }"
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
            else: 
                obs_result1 = f"REDE:{cpe_config['REDE']}"
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})

            # 490_2
            if cpe_config['REDE'] == 'VIVO_2':
                if final_dict['t38'] == 'Desabilitado':

                    obs_result2 =  f"Fax T38: Desabilitado"
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    obs_result2 = f"Teste incorreto, retorno Fax T38: {final_dict['t38']}"
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})

            else: 
                obs_result2 = f"REDE:{cpe_config['REDE']}"
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})

            self._dict_result.update({"obs": f"490_1: {obs_result1} | 490_2: {obs_result2}"})
        except Exception as e:
            self._dict_result.update({"obs": e})          

        finally:
            self.update_global_result_memory(flask_username, 'checkVoIPSettings_490', final_dict)
        return self._dict_result


    def verificarDtmfMethod_491(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            dtmf = result['dtmf']
            if dtmf == 'RFC2833':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "DTMF Method: RFC2833", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno DTMF Method: {dtmf}"})
        return self._dict_result
    

    def prioridadeCodec_0_493(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            codec = result['Preferred codec 1']
            if codec == 'G.711ALaw':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Order: 1 = G.711ALaw", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Order: 0 = {codec} "})
        return self._dict_result


    def prioridadeCodec_1_494(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            codec = result['Preferred codec 2']
            if codec == 'G.729':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Order: 2 = G.729", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Order: 2 = {codec} "})
        return self._dict_result




    def checkUPnP_497(self, flask_username):
        
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(3)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="folder34"]/table/tbody/tr/td/a').click()

            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')

            upnp = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/b/table/tbody/tr/td[1]/input')]
            
            self._driver.quit()

            print(upnp)
            if upnp[0] == 'true':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'UPnP: Habilitado', "result":"passed"})

            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno UPnP: {upnp}'})

        except Exception as e:
            self._dict_result.update({"obs": e})

        return self._dict_result


    def linkLocalType_498(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            linkLocal = result['Status']['Internet']['IPv6']['Endereço IPv6 Link-Local - LAN:']
            print(linkLocal)
            try:
                if linkLocal.split('/')[-1] == '64':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "LAN link local: 64", "result":"passed"})
            except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno LAN link local: {linkLocal}"})

        return self._dict_result


    def lanGlobalType_499(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            linkGlobal = result['Status']['Internet']['IPv6']['Endereço IPv6 Global - WAN:']
            if linkGlobal.split('/')[-1] == '64':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "WAN global identifier: 64", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno WAN global identifier: {linkGlobal}"})
        return self._dict_result


    def prefixDelegationfromInet_500(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            delegate = result['Prefix']
            if 'ip2' == delegate:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: ip2", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Prefix Delegation WAN: {delegate}"})
            
        return self._dict_result



    