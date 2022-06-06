import time, datetime
import sys
import requests
from Setup.ACS import webRemoteHDM
from Setup.ACS import webServiceImpl
from Setup.ACS import webSDO
import pandas as pd
import zeep
import json
from json import JSONEncoder
from HGUmodels.factory import HGUModelFactory
from webdriver.webdriver import WebDriver

class acs:
    def __init__(self):
        self.ip = []
        self.username = []
        self.password = []
    
    # 4
    def initialInformations(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword, acsPort, model_name):

        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "GPV_OneObjct", 
            "Probe#": "XXXXXXX", 
            "Description": "Executa Get Parameter Value via ACS", 
            "obs": None}

        dados_entrada = {
            'serialnumber': serialnumber,
            'GPV_Param': GPV_Param,
            'IPACS': IPACS,
            'acsUsername': acsUsername,
            'acsPassword': acsPassword,
            'portaACS': acsPort
        }

        hgu = HGUModelFactory.getHGU(probe='settingsProbe', model_name=model_name, dict_result=dict_result)
        # print(serialnumber, GPV_Param, IPACS, acsUsername, acsPassword)
        return hgu.initialInformations_4(dados_entrada)

    #414
    def GPV_OneObjct(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword, acsPort, model_name):

        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "GPV_OneObjct", 
            "Probe#": "XXXXXXX", 
            "Description": "Executa Get Parameter Value via ACS", 
            "obs": None}

        dados_entrada = {
            'serialnumber': serialnumber,
            'GPV_Param': GPV_Param,
            'IPACS': IPACS,
            'acsUsername': acsUsername,
            'acsPassword': acsPassword,
            'portaACS': acsPort
        }

        hgu = HGUModelFactory.getHGU(probe='settingsProbe', model_name=model_name, dict_result=dict_result)
        # print(serialnumber, GPV_Param, IPACS, acsUsername, acsPassword)
        return hgu.GPV_OneObjct_414(dados_entrada)

    #417
    def connectionRequestPort(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword, model_name):

        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "GPV_OneObjct", 
            "Probe#": "XXXXXXX", 
            "Description": "Executa Get Parameter Value via ACS", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe', model_name=model_name, dict_result=dict_result)
        return hgu.connectionRequestPort_417(serialnumber, GPV_Param, IPACS, acsUsername, acsPassword)


    def execCusFuncPingDiagnostics(self, serialnumber, IPACS, acsUsername, acsPassword, destAddress):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('destAddress # = ' + str(destAddress))
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    #
                    ###BUSCANDO DADOS DO DISPOSITIVO###
                    #
                    tsa = time.time()
                    sta = datetime.datetime.fromtimestamp(tsa).strftime('%Y_%m_%d_%HH:%MM:%SS')
                    nbiRH.findDeviceBySerial(serialnumber, acsUsername, acsPassword)
                    if nbiRH.msgTagExecution_02 == 'EXECUTED':
                        OUI = str(nbiRH.device["OUI"])
                        productClass = str(nbiRH.device["productClass"])
                        protocol = str(nbiRH.device["protocol"])
                        subscriberId = str(nbiRH.device["subscriberId"])
                        lastContactTime = str(nbiRH.device["lastContactTime"])
                        softwareVersion = str(nbiRH.device["softwareVersion"])
                        externalIpAddress = str(nbiRH.device["iPAddressWAN"])
                        activated = str(nbiRH.device["activated"])
                        lastActivationTime = pd.Timestamp(str(nbiRH.device["lastActivationTime"])).tz_convert("UTC")
                        lastActivationTime = lastActivationTime.strftime("%d-%m-%Y %H:%M:%S")
                        print('-=-' * 40)
                        print('##MODELO##: ' + nbiRH.device["productClass"] + "\t\t" '##CURRENT FIRMWARE##: ' + nbiRH.device["softwareVersion"])
                        print('-=-' * 40 + '\n')

                        ########################################
                        ###     CUSTOM FUNCTIONS        ###
                        ########################################
                        result = []
                        print('Custom Function a ser executada: pingDiagnostics')
                        for k in destAddress:
                            objeto = k
                            print('o valor de IP agora é: ' + objeto)
                            #
                            CUSTOM = nbiSDO.pingDiagnostics(OUI, productClass, protocol, serialnumber, objeto)
                            #
                            print(CUSTOM)
                            result.append(CUSTOM)
                        print(result)
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execEnableTelnetWizard", "Probe#": "XXXXXXX", "Description": "Executa ping nos IPs determinados", "Resultado": result}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCusFuncPingDiagnostics", "Probe#": "XXXXXXX", "Description": "Executa ping nos IPs determinados", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execEnableTelnetWizard", "Probe#": "XXXXXXX", "Description": "Executa ping nos IPs determinados", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCusFuncPingDiagnostics", "Probe#": "XXXXXXX", "Description": "Executa ping nos IPs determinados", "Resultado": str(e)}

    def execCusFuncHGUDiagnostics(self, serialnumber, IPACS, acsUsername, acsPassword): ### NECESSITA VERIFICAR SAIDA ... AINDA NAO TESTAR
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    #
                    ###BUSCANDO DADOS DO DISPOSITIVO###
                    #
                    tsa = time.time()
                    sta = datetime.datetime.fromtimestamp(tsa).strftime('%Y_%m_%d_%HH:%MM:%SS')
                    nbiRH.findDeviceBySerial(serialnumber, acsUsername, acsPassword)
                    if nbiRH.msgTagExecution_02 == 'EXECUTED':
                        OUI = str(nbiRH.device["OUI"])
                        productClass = str(nbiRH.device["productClass"])
                        protocol = str(nbiRH.device["protocol"])
                        subscriberId = str(nbiRH.device["subscriberId"])
                        lastContactTime = str(nbiRH.device["lastContactTime"])
                        softwareVersion = str(nbiRH.device["softwareVersion"])
                        externalIpAddress = str(nbiRH.device["iPAddressWAN"])
                        activated = str(nbiRH.device["activated"])
                        lastActivationTime = pd.Timestamp(str(nbiRH.device["lastActivationTime"])).tz_convert("UTC")
                        lastActivationTime = lastActivationTime.strftime("%d-%m-%Y %H:%M:%S")
                        print('-=-' * 40)
                        print('##MODELO##: ' + nbiRH.device["productClass"] + "\t\t" '##CURRENT FIRMWARE##: ' + nbiRH.device["softwareVersion"])
                        print('-=-' * 40 + '\n')

                        ########################################
                        ###     CUSTOM FUNCTIONS        ###
                        ########################################
                        print('Custom Function a ser executada: pingDiagnostics')
                        #
                        CUSTOM = nbiSDO.getHGU_DIAGNOSTICS_CUSTOM(OUI, productClass, protocol, serialnumber)
                        #
                        print(CUSTOM)
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execCusFuncHGUDiagnostics", "Probe#": "XXXXXXX", "Description": "Executa HGU Diagnostics no HGU", "Resultado": CUSTOM}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCusFuncHGUDiagnostics", "Probe#": "XXXXXXX", "Description": "Executa HGU Diagnostics no HGU", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execCusFuncHGUDiagnostics", "Probe#": "XXXXXXX", "Description": "Executa HGU Diagnostics no HGU", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCusFuncHGUDiagnostics", "Probe#": "XXXXXXX", "Description": "Executa HGU Diagnostics no HGU", "Resultado": str(e)}

    def execIssueConnectionRequest(self, serialnumber, IPACS, acsUsername, acsPassword, OUI, protocol, ProductClass):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProductClass = ' + ProductClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    ########################################
                    ###     CUSTOM FUNCTIONS        ###
                    ########################################
                    print('Function a ser executada: issueConnectionRequest')
                    #
                    FUNCTION = nbiSDO.issueConnectionRequest(OUI, ProductClass, protocol, serialnumber)
                    #
                    print(FUNCTION)
                    if FUNCTION == True:
                        result = '200_OK'
                    else:
                        result = '400_NOK'
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execIssueConnectionRequest", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": result}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execIssueConnectionRequest", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execIssueConnectionRequest", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execIssueConnectionRequest", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": str(e)}

    def execCheckDeviceAvailability(self, serialnumber, IPACS, acsUsername, acsPassword, OUI, protocol, ProductClass):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProductClass = ' + ProductClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    ########################################
                    ###     CUSTOM FUNCTIONS        ###
                    ########################################
                    print('Function a ser executada: CheckDeviceAvailability')
                    #
                    FUNCTION = nbiSDO.checkOnline(OUI, ProductClass, protocol, serialnumber)
                    #
                    print(FUNCTION)
                    if FUNCTION == None:
                        result = '200_OK'
                    else:
                        result = '400_NOK'
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execCheckDeviceAvailability", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": result}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCheckDeviceAvailability", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execCheckDeviceAvailability", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCheckDeviceAvailability", "Probe#": "XXXXXXX", "Description": "Executa Connection Request no dispositivo", "Resultado": str(e)}

    def getDeviceInfoACS(self,serialnumber, IPACS, acsUsername, acsPassword):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    #
                    ###BUSCANDO DADOS DO DISPOSITIVO###
                    #
                    tsa = time.time()
                    sta = datetime.datetime.fromtimestamp(tsa).strftime('%Y_%m_%d_%HH:%MM:%SS')
                    result = nbiRH.findDeviceBySerial(serialnumber, acsUsername, acsPassword)
                    print(result)
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "getDeviceInfoACS", "Probe#": "XXXXXXX", "Description": "Verifica as informações do dispositivo via ACS", "Resultado": result}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "getDeviceInfoACS", "Probe#": "XXXXXXX", "Description": "Verifica as informações do dispositivo via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "getDeviceInfoACS", "Probe#": "XXXXXXX", "Description": "Verifica as informações do dispositivo via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "getDeviceInfoACS", "Probe#": "XXXXXXX", "Description": "Verifica as informações do dispositivo via ACS", "Resultado": str(e)}

    def execRebootACS(self,serialnumber, IPACS, acsUsername, acsPassword, deviceGUID):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('deviceGUID = ' + deviceGUID)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    #
                    ###Executar REBOOT
                    #
                    result = nbiRH.reboot(deviceGUID)
                    print(result)
                    if result == None:
                        result = '200_OK'
                    else:
                        result = '400_NOK'
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execRebootACS", "Probe#": "XXXXXXX", "Description": "Executa reboot via ACS", "Resultado": result}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execRebootACS", "Probe#": "XXXXXXX", "Description": "Executa reboot via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execRebootACS", "Probe#": "XXXXXXX", "Description": "Executa reboot via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execRebootACS", "Probe#": "XXXXXXX", "Description": "Executa reboot via ACS", "Resultado": str(e)}

    def execGetWifiStatus(self,IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###     CUSTOM FUNCTIONS        ###
                ########################################
                print('Custom Function a ser executada: getWifiStatus')
                #
                customFUNCTION = nbiSDO.getWifiStatus(OUI, ProcudctClass, protocol, serialnumber)
                #
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica as configurações de Wifi do dispositivo", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica as configurações de Wifi do dispositivo", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica as configurações de Wifi do dispositivo", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica as configurações de Wifi do dispositivo", "Resultado": str(e)}

    def execGetParameterAttributes(self,IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber, objeto):
        class MyEncoder(JSONEncoder):
            def default(self, o):
                return o.__dict__
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('objeto = ' + objeto)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###     FUNCTIONS        ###
                ########################################
                print('Function a ser executada: getParameterAttributes')
                #
                FUNCTION = nbiSDO.getParameterAttributes(OUI, ProcudctClass, protocol, serialnumber,objeto)
                #
                if FUNCTION != None:
                    FUNCTION = json.dumps(FUNCTION, cls=MyEncoder)
                    FUNCTION_1 = json.loads(FUNCTION)
                    json_saida = []
                    for key, value in enumerate(FUNCTION_1):
                        for chave, valor in value.items():
                            aux = {
                                "name": valor['accessList'],
                                "type": valor['name'],
                                "value": valor['notification']
                            }
                            json_saida.append(aux)
                    print(json_saida)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetParameterAttributes", "Probe#": "XXXXXXX", "Description": "Verifica os atributos do objeto no ACS", "Resultado": json_saida}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetParameterAttributes", "Probe#": "XXXXXXX", "Description": "Verifica os atributos do objeto no ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetParameterAttributes", "Probe#": "XXXXXXX", "Description": "Verifica os atributos do objeto no ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetParameterAttributes", "Probe#": "XXXXXXX", "Description": "Verifica os atributos do objeto no ACS", "Resultado": str(e)}

    def getLANHosts(self,IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: getLANHosts')
                #
                customFUNCTION = nbiSDO.getLANHosts(OUI, ProcudctClass, protocol, serialnumber)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "getLANHosts", "Probe#": "XXXXXXX", "Description": "Verifica dispositicos conectados na LAN do HGU", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "getLANHosts", "Probe#": "XXXXXXX", "Description": "Verifica dispositicos conectados na LAN do HGU", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "getLANHosts", "Probe#": "XXXXXXX", "Description": "Verifica dispositicos conectados na LAN do HGU", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "getLANHosts", "Probe#": "XXXXXXX", "Description": "Verifica dispositicos conectados na LAN do HGU", "Resultado": str(e)}

    def getPPPoECredentials(self,IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: getPPPoECredentials')
                #
                customFUNCTION = nbiSDO.getPPPoECredentials(OUI, ProcudctClass, protocol, serialnumber)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "getPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Verifica credenciais PPPoE via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "getPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Verifica credenciais PPPoE via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "getPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Verifica credenciais PPPoE via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "getPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Verifica credenciais PPPoE via ACS", "Resultado": str(e)}

    def setPPPoECredentials(self,IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber, PPPoEUsername, PPPoEPassword):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('PPPoEUsername = ' + PPPoEUsername)
        print('PPPoEPassword = ' + PPPoEPassword)
        print('-=-' * 20)
        acsPort = 7015

        credentials = {
            "username": PPPoEUsername,
            "password": PPPoEPassword
        }

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: setPPPoECredentials')
                #
                customFUNCTION = nbiSDO.setPPPoECredentials(OUI, ProcudctClass, protocol, serialnumber, credentials)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "setPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Altera credenciais PPPoE via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "setPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Altera credenciais PPPoE via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "setPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Altera credenciais PPPoE via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "setPPPoECredentials", "Probe#": "XXXXXXX", "Description": "Altera credenciais PPPoE via ACS", "Resultado": str(e)}

    def execSetWifi(self, IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber, WIFI_SETTINGS):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('WIFI_SETTINGS = ' + str(WIFI_SETTINGS))
        print('-=-' * 20)
        acsPort = 7015

        newDic = {
            key: WIFI_SETTINGS[key]
            for key in WIFI_SETTINGS
            if WIFI_SETTINGS[key] != ''
        }
        print('Novo WIFI_SETTINGS = ' + str(newDic))
        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: setWifi')
                #
                customFUNCTION = nbiSDO.setWifi(OUI, ProcudctClass, protocol, serialnumber, newDic)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execSetWifi", "Probe#": "XXXXXXX", "Description": "Altera configurações da rede Wifi (2.4GHz e 5GHz) via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execSetWifi", "Probe#": "XXXXXXX", "Description": "Altera configurações da rede Wifi (2.4GHz e 5GHz) via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execSetWifi", "Probe#": "XXXXXXX", "Description": "Altera configurações da rede Wifi (2.4GHz e 5GHz) via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execSetWifi", "Probe#": "XXXXXXX", "Description": "Altera configurações da rede Wifi (2.4GHz e 5GHz) via ACS", "Resultado": str(e)}

    def execGetPortMapping(self, IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: getPortMapping')
                #
                customFUNCTION = nbiSDO.getPortMapping(OUI, ProcudctClass, protocol, serialnumber)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": str(e)}

    def execAddPortMapping(self, IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber, enable, internalClient, internalPort, externalPort, portMapName, protocolMapping):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('enable = ' + enable)
        print('internalClient = ' + internalClient)
        print('internalPort = ' + internalPort)
        print('externalPort = ' + externalPort)
        print('portMapName = ' + portMapName)
        print('protocolMapping = ' + protocolMapping)
        print('-=-' * 20)
        acsPort = 7015

        options = {
            "enable": enable,
            "internalClient": internalClient,
            "internalPort": internalPort,
            "externalPort": externalPort,
            "portMapName": portMapName,
            "protocol": protocolMapping
        }

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: execAddPortMapping')
                #
                customFUNCTION = nbiSDO.addPortMapping(OUI, ProcudctClass, protocol, serialnumber, options)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execAddPortMapping", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execAddPortMapping", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execAddPortMapping", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execAddPortMapping", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": str(e)}

    def execSetVoIP(self, IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber, DirectoryNumber, AuthUserName, ProxyServer, RegistrarServer, UserAgentDomain, OutboundProxy, phyReferenceList):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('DirectoryNumber = ' + DirectoryNumber)
        print('AuthUserName = ' + AuthUserName)
        print('ProxyServer = ' + ProxyServer)
        print('RegistrarServer = ' + RegistrarServer)
        print('UserAgentDomain = ' + UserAgentDomain)
        print('OutboundProxy = ' + OutboundProxy)
        print('phyReferenceList = ' + phyReferenceList)
        print('-=-' * 20)
        acsPort = 7015

        parameters = {
            "DirectoryNumber": DirectoryNumber,
            "AuthUserName": AuthUserName,
            "ProxyServer": ProxyServer,
            "RegistrarServer": RegistrarServer,
            "UserAgentDomain": UserAgentDomain,
            "OutboundProxy": OutboundProxy,
            "phyReferenceList": phyReferenceList
        }

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: setVoIP')
                #
                customFUNCTION = nbiSDO.setVoIP(OUI, ProcudctClass, protocol, serialnumber, parameters)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execSetVoIP", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execSetVoIP", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execSetVoIP", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execSetVoIP", "Probe#": "XXXXXXX", "Description": "Cria mapeamentos de porta via ACS", "Resultado": str(e)}

    def SPV(self, serialnumber, IPACS, acsUsername, acsPassword, SPV_Param):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        objeto = SPV_Param
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('objeto = ' + str(objeto))
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')
                    #
                    ###BUSCANDO DADOS DO DISPOSITIVO###
                    #
                    tsa = time.time()
                    sta = datetime.datetime.fromtimestamp(tsa).strftime('%Y_%m_%d_%HH:%MM:%SS')
                    nbiRH.findDeviceBySerial(serialnumber, acsUsername, acsPassword)
                    if nbiRH.msgTagExecution_02 == 'EXECUTED':
                        OUI = str(nbiRH.device["OUI"])
                        productClass = str(nbiRH.device["productClass"])
                        protocol = str(nbiRH.device["protocol"])
                        subscriberId = str(nbiRH.device["subscriberId"])
                        lastContactTime = str(nbiRH.device["lastContactTime"])
                        softwareVersion = str(nbiRH.device["softwareVersion"])
                        externalIpAddress = str(nbiRH.device["iPAddressWAN"])
                        activated = str(nbiRH.device["activated"])
                        lastActivationTime = pd.Timestamp(str(nbiRH.device["lastActivationTime"])).tz_convert("UTC")
                        lastActivationTime = lastActivationTime.strftime("%d-%m-%Y %H:%M:%S")
                        print('-=-' * 40)
                        print('##MODELO##: ' + nbiRH.device["productClass"] + "\t\t" '##CURRENT FIRMWARE##: ' + nbiRH.device["softwareVersion"])
                        print('-=-' * 40 + '\n')
                        #
                        SPV = nbiSDO.setParameterValue(OUI, productClass, protocol, serialnumber, objeto)
                        #
                        if SPV == None:
                            print(type(SPV))
                            print(SPV)
                            result = '200_OK'
                            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "SPV", "Probe#": "XXXXXXX", "Description": "Executa Set Parameter Value via ACS", "Resultado": result}
            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "SPV", "Probe#": "XXXXXXX", "Description": "Executa Set Parameter Value via ACS", "Resultado": str(e)}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "SPV", "Probe#": "XXXXXXX", "Description": "Executa Set Parameter Value via ACS", "Resultado": str(e)}

    def execCancelVoIP(self, serialnumber, IPACS, acsUsername, acsPassword, parameter):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        objeto = parameter
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('objeto = ' + str(objeto))
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')
                    #
                    ###BUSCANDO DADOS DO DISPOSITIVO###
                    #
                    tsa = time.time()
                    sta = datetime.datetime.fromtimestamp(tsa).strftime('%Y_%m_%d_%HH:%MM:%SS')
                    nbiRH.findDeviceBySerial(serialnumber, acsUsername, acsPassword)
                    if nbiRH.msgTagExecution_02 == 'EXECUTED':
                        OUI = str(nbiRH.device["OUI"])
                        productClass = str(nbiRH.device["productClass"])
                        protocol = str(nbiRH.device["protocol"])
                        subscriberId = str(nbiRH.device["subscriberId"])
                        lastContactTime = str(nbiRH.device["lastContactTime"])
                        softwareVersion = str(nbiRH.device["softwareVersion"])
                        externalIpAddress = str(nbiRH.device["iPAddressWAN"])
                        activated = str(nbiRH.device["activated"])
                        lastActivationTime = pd.Timestamp(str(nbiRH.device["lastActivationTime"])).tz_convert("UTC")
                        lastActivationTime = lastActivationTime.strftime("%d-%m-%Y %H:%M:%S")
                        print('-=-' * 40)
                        print('##MODELO##: ' + nbiRH.device["productClass"] + "\t\t" '##CURRENT FIRMWARE##: ' + nbiRH.device["softwareVersion"])
                        print('-=-' * 40 + '\n')
                        #
                        cancelVoIP = nbiSDO.cancelVoIP(OUI, productClass, protocol, serialnumber, objeto)
                        #
                        if cancelVoIP == None:
                            print(type(cancelVoIP))
                            print(cancelVoIP)
                            result = '200_OK'
                            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execCancelVoIP", "Probe#": "XXXXXXX", "Description": "Executa Set Parameter Value via ACS", "Resultado": result}
            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCancelVoIP", "Probe#": "XXXXXXX", "Description": "Executa Set Parameter Value via ACS", "Resultado": str(e)}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execCancelVoIP", "Probe#": "XXXXXXX", "Description": "Executa Set Parameter Value via ACS", "Resultado": str(e)}

    def execDownloadDiagnostics(self, IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber, ip, filesize): ### VALIDAR SAIDA!!!!!!!!!!!!
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('ip = ' + ip)
        print('filesize = ' + filesize)
        print('-=-' * 20)
        acsPort = 7015

        downloadURL = 'http://' + ip + '/download/' + filesize

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: downloadDiagnostics')
                #
                customFUNCTION = nbiSDO.downloadDiagnostics(OUI, ProcudctClass, protocol, serialnumber, downloadURL)
                #
                print(customFUNCTION)
                time.sleep(2)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetPortMapping", "Probe#": "XXXXXXX", "Description": "Verifica mapeamentos de porta via ACS", "Resultado": str(e)}

    def execGetDHCP(self,IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: getDHCP')
                #
                customFUNCTION = nbiSDO.getDHCP(OUI, ProcudctClass, protocol, serialnumber)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetDHCP", "Probe#": "XXXXXXX", "Description": "Verifica informações de DHCP do HGU via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetDHCP", "Probe#": "XXXXXXX", "Description": "Verifica informações de DHCP do HGU via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execGetDHCP", "Probe#": "XXXXXXX", "Description": "Verifica informações de DHCP do HGU via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execGetDHCP", "Probe#": "XXXXXXX", "Description": "Verifica informações de DHCP do HGU via ACS", "Resultado": str(e)}

    def execSetDHCP(self, IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass, serialnumber, DHCP_SETTINGS):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('DHCP_SETTINGS = ' + str(DHCP_SETTINGS))
        print('-=-' * 20)
        acsPort = 7015

        # newDic = {
        #     key: DHCP_SETTINGS[key]
        #     for key in DHCP_SETTINGS
        #     if DHCP_SETTINGS[key] != ''
        # }
        # print('Novo DHCP_SETTINGS = ' + str(newDic))
        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                ########################################
                ###    CUSTOM FUNCTIONS        ###
                ########################################
                print('CUSTOM Function a ser executada: setDHCP')
                #
                customFUNCTION = nbiSDO.setDHCP(OUI, ProcudctClass, protocol, serialnumber, DHCP_SETTINGS)
                #
                print(customFUNCTION)

                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execSetDHCP", "Probe#": "XXXXXXX", "Description": "Altera informações de DHCP do HGU via ACS", "Resultado": customFUNCTION}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execSetDHCP", "Probe#": "XXXXXXX", "Description": "Altera informações de DHCP do HGU via ACS", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execSetDHCP", "Probe#": "XXXXXXX", "Description": "Altera informações de DHCP do HGU via ACS", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execSetDHCP", "Probe#": "XXXXXXX", "Description": "Altera informações de DHCP do HGU via ACS", "Resultado": str(e)}

    def execResetFactory(self, serialnumber, IPACS, acsUsername, acsPassword, OUI, protocol, ProcudctClass):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProcudctClass)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    ########################################
                    ###     CUSTOM FUNCTIONS        ###
                    ########################################
                    print('Function a ser executada: resetFactory')
                    #
                    FUNCTION = nbiSDO.resetFactory(OUI, ProcudctClass, protocol, serialnumber)
                    #
                    print(FUNCTION)
                    if FUNCTION == True:
                        result = '200_OK'
                    else:
                        result = '400_NOK'
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execResetFactory", "Probe#": "XXXXXXX", "Description": "Executa Reset Factory no dispositivo", "Resultado": result}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execResetFactory", "Probe#": "XXXXXXX", "Description": "Executa Reset Factory no dispositivo", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execResetFactory", "Probe#": "XXXXXXX", "Description": "Executa Reset Factory no dispositivo", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execResetFactory", "Probe#": "XXXXXXX", "Description": "Executa Reset Factory no dispositivo", "Resultado": str(e)}

    def execFirmwareUpdate(self, serialnumber, IPACS, acsUsername, acsPassword, OUI, protocol, ProductClass, firmwareName):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('OUI = ' + OUI)
        print('protocol = ' + protocol)
        print('ProcudctClass = ' + ProductClass)
        print('firmwareName = ' + firmwareName)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')

                    ########################################
                    ###     CUSTOM FUNCTIONS        ###
                    ########################################
                    print('Function a ser executada: firmwareUpdate')
                    #
                    FUNCTION = nbiRH.createSingleFirmwareUpdateOperation(OUI, ProductClass, protocol, serialnumber, firmwareName)
                    #
                    print(FUNCTION)
                    if FUNCTION == None:
                        result = '200_OK'
                    else:
                        result = '400_NOK'
                return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa Firmware Update no dispositivo", "Resultado": result}

            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa Firmware Update no dispositivo", "Resultado": str(e)}

            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "execFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa Firmware Update no dispositivo", "Resultado": result}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "execFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa Firmware Update no dispositivo", "Resultado": str(e)}

    def GPV(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
        class MyEncoder(JSONEncoder):
            def default(self, o):
                return o.__dict__
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('serialnumber = ' + serialnumber)
        print('IPACS = ' + IPACS)
        print('acsUsername = ' + acsUsername)
        print('acsPassword = ' + acsPassword)
        print('-=-' * 20)
        acsPort = 7015

        try:
            url = 'http://' + IPACS + ':' + str(acsPort) + '/hdm'
            connTest = requests.post(url, timeout=4)
            try:
                if connTest.status_code != 200:
                    sys.exit('ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: ' + IPACS + ':' + str(acsPort))
                else:
                    print('\n#############################################'
                          '\n CONECTIVIDADE COM ACS-HDM OK: ' + IPACS +
                          '\n#############################################\n')
                    #
                    ###INICIANDO WEBSERIVCES###
                    #
                    try:
                        nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                        nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                    except:
                        sys.exit('ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84) ')
                    #
                    ###BUSCANDO DADOS DO DISPOSITIVO###
                    #
                    tsa = time.time()
                    sta = datetime.datetime.fromtimestamp(tsa).strftime('%Y_%m_%d_%HH:%MM:%SS')
                    nbiRH.findDeviceBySerial(serialnumber, acsUsername, acsPassword)
                    if nbiRH.msgTagExecution_02 == 'EXECUTED':
                        OUI = str(nbiRH.device["OUI"])
                        productClass = str(nbiRH.device["productClass"])
                        protocol = str(nbiRH.device["protocol"])
                        subscriberId = str(nbiRH.device["subscriberId"])
                        lastContactTime = str(nbiRH.device["lastContactTime"])
                        softwareVersion = str(nbiRH.device["softwareVersion"])
                        externalIpAddress = str(nbiRH.device["iPAddressWAN"])
                        activated = str(nbiRH.device["activated"])
                        lastActivationTime = pd.Timestamp(str(nbiRH.device["lastActivationTime"])).tz_convert("UTC")
                        lastActivationTime = lastActivationTime.strftime("%d-%m-%Y %H:%M:%S")
                        print('-=-' * 40)
                        print('##MODELO##: ' + nbiRH.device["productClass"] + "\t\t" '##CURRENT FIRMWARE##: ' + nbiRH.device["softwareVersion"])
                        print('-=-' * 40 + '\n')
                        #
                        GPV = nbiSDO.getParameterValue(OUI, productClass, protocol, serialnumber, GPV_Param)
                        #
                        if GPV != None:
                            print(type(GPV))
                            print(GPV)
                            GPV = json.dumps(GPV, cls=MyEncoder)
                            GPV_1 = json.loads(GPV)
                            json_saida = []
                            for key, value in enumerate(GPV_1):
                                for chave, valor in value.items():
                                    aux = {
                                        "name":valor['name'],
                                        "type":valor['type'],
                                        "value":valor['value']
                                    }
                                    json_saida.append(aux)
                            print(json_saida)
                            return {"Resultado_Probe": "OK", "ControllerName": "acs", "ProbeName": "GPV_OneObjct", "Probe#": "XXXXXXX", "Description": "Executa Get Parameter Value via ACS", "Resultado": json_saida}
            except Exception as e:
                e = sys.exc_info()[1]
                print(e)
                sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
                return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "GPV_OneObjct", "Probe#": "XXXXXXX", "Description": "Executa Get Parameter Value via ACS", "Resultado": str(e)}
        except Exception as e:
            e = sys.exc_info()[1]
            print(e)
            sys.exit('ERROR_001 - ERRO AO VERIFICAR CONECTIVIDADE COM ACS-NOKIA: ' + IPACS + ':' + str(acsPort))
            return {"Resultado_Probe": "NOK", "ControllerName": "acs", "ProbeName": "GPV_OneObjct", "Probe#": "XXXXXXX", "Description": "Executa Get Parameter Value via ACS", "Resultado": str(e)}