import Setup.ACS.webSDO
import Setup.ACS.webRemoteHDM
import Setup.ACS.webServiceImpl
import os
import sys
import time
import datetime
import requests
import threading
import json
from json import JSONEncoder
from HGUmodels.models.SSHutils import infoDevices_utils

dict_result = dict

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class ACS():
    def teste(**kwargs):
        print(f'\nkwargs = {kwargs}')
        for chave, valor in kwargs.items():
            print(chave, valor)

    def checkDeviceAvailability(**dados_entrada):

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')


        print('\n\n >>> Iniciando Função CheckDeviceAvailability ACS -',start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print("\nNBI - RH:")
                        print(nbiRH.ip)
                        print("\nNBI - SDO:")
                        print(nbiSDO.ip)
                        print("\nNBI - SI")
                        print(nbiSI.ip)
                        
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(dados_entrada['serialnumber'])
                        
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])

                            print(' -- Executando ACS [CheckDeviceAvailability] --')
                            connectionRequest = nbiSDO.checkDeviceAvailability(OUI, productClass, protocol, dados_entrada['serialnumber'])
                            print('conexao:  ')
                            print(connectionRequest)
                            if connectionRequest.startswith('org/apache/xml/serializer/TreeWalker'):
                                print(' -- CheckDeviceAvailability NOK -- ERRO: org/apache/xml/serializer/TreeWalker')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- CheckDeviceAvailability NOK --')
                                print(' -- ATENÇÃO! ERRO TRANSPORT! -- ')
                                dict_result = {'obs': ' -- ATENÇÃO! ERRO TRANSPORT! -- '}
                                print('\n\n >>> Finalizando CheckDeviceAvailability ACS - Tempo de Execução:',total_time, '\n\n')
                            elif connectionRequest.startswith('status=6,'):
                                print(' -- CheckDeviceAvailability NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- CheckDeviceAvailability NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                dict_result = {"obs": "ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST!"}

                                print('\n\n >>> Finalizando CheckDeviceAvailability ACS - Tempo de Execução:',total_time, '\n\n')
                            else:
                                print(' -- CheckDeviceAvailability OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                print('\n\n >>> Finalizando CheckDeviceAvailability ACS - Tempo de Execução:',total_time, '\n\n')
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': " -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- "}
                            print('\n\n >>> Finalizando CheckDeviceAvailability ACS - Tempo de Execução:',total_time, '\n\n')
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando CheckDeviceAvailability ACS - Tempo de Execução:',total_time, '\n\n')
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    dict_result = {'obs': ' -- CONECTIVIDADE COM ACS NOK --'}
                    print('\n\n >>> Finalizando CheckDeviceAvailability ACS - Tempo de Execução:',total_time, '\n\n')

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            dict_result = {'obs': " -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- "}
            print('\n\n >>> Finalizando CheckDeviceAvailability ACS - Tempo de Execução:',total_time, '\n\n')
        return dict_result

    def setParameterValues(**dados_entrada):
        # print(f'\ndados_entrada = {dados_entrada}')
        # for chave, valor in dados_entrada.items():
        #     print(chave, valor)

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função SetParameterValues ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])

                            print(' -- Executando ACS [SetParameterValues] --')
                            spv = nbiSDO.setParameterValue(OUI, productClass, protocol, dados_entrada['serialnumber'], dados_entrada['SPV_Param'])
                            if spv == 0:
                                print(' -- SetParameterValues OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print('\n\n >>> Finalizando SetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                                return spv
                            else:
                                print(' -- SetParameterValues NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- SetParameterValues NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                print('\n\n >>> Finalizando SetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                                dict_result = {"obs": "ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST!"}
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            print('\n\n >>> Finalizando SetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                            dict_result = {"obs": "ATENÇÃO! REVEJA PARAMETROS DE ENTRADA!"}
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        print('\n\n >>> Finalizando SetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                        dict_result = {"obs": "WEBSERVICES NOK"}
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    print('\n\n >>> Finalizando SetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                    dict_result = {"obs": "CONECTIVIDADE COM ACS NOK"}

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            print('\n\n >>> Finalizando SetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
            dict_result = {"obs": "ATENÇÃO! REVEJA PARAMETROS DE ENTRADA!"}
        return dict_result

    def getParameterValues(**dados_entrada):
        #print(dados_entrada)
        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função GetParameterValues ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')

        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMACOES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])

                            print(' -- Executando ACS [GetParameterValues] --')
                            gpv = nbiSDO.getParameterValue(OUI, productClass, protocol, dados_entrada['serialnumber'], dados_entrada['GPV_Param'])
                            if gpv != None:
                                GPV_1 = json.dumps(gpv, cls=MyEncoder)
                                print(' -- GetParameterValues OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                                return gpv
                            else:
                                print(' -- GetParameterValues NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- GetParameterValues NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                                dict_result = {"obs": "ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST!"} 
                           
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                            dict_result = {"obs": "ATENÇÃO! REVEJA PARAMETROS DE ENTRADA!"}
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                        dict_result = {"obs": "WEBSERVICES NOK"}

                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                    dict_result = {"obs": "CONECTIVIDADE COM ACS NOK"}


            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
            dict_result = {"obs": "ATENÇÃO! REVEJA PARAMETROS DE ENTRADA!"}
        
        return dict_result

    def reboot(**dados_entrada):
        # print(f'\ndados_entrada = {dados_entrada}')
        # for chave, valor in dados_entrada.items():
        #     print(chave, valor)

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função Reboot ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])
                            deviceGUID = str(nbiRH.device["GUID"])

                            print(' -- Executando ACS [Reboot] --')
                            reboot = nbiRH.reboot(deviceGUID)
                            if nbiRH.msgTagExecution_03 == 'EXECUTED':
                                print(' -- Reboot OK --')
                                dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print('\n\n >>> Finalizando Reboot ACS - Tempo de Execução:', total_time, '\n\n')
                            else:
                                print(' -- Reboot NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- Reboot NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                dict_result = {'obs': ' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- '}
                                print('\n\n >>> Finalizando Reboot ACS - Tempo de Execução:', total_time, '\n\n')
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
                            print('\n\n >>> Finalizando Reboot ACS - Tempo de Execução:', total_time, '\n\n')
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando Reboot ACS - Tempo de Execução:', total_time, '\n\n')
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    dict_result = {'obs': ' -- CONECTIVIDADE COM ACS NOK --'}
                    print('\n\n >>> Finalizando Reboot ACS - Tempo de Execução:', total_time, '\n\n')

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
            print('\n\n >>> Finalizando Reboot ACS - Tempo de Execução:', total_time, '\n\n')
        return dict_result

    def setVoIP(**dados_entrada):

        # print(f'\ndados_entrada = {dados_entrada}')
        # for chave, valor in dados_entrada.items():
        #     print(chave, valor)

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função SeT VoIP ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])
                            deviceGUID = str(nbiRH.device["GUID"])

                            print(' -- Executando ACS [SeT VoIP] --')
                            setvoip = nbiSDO.setVoip(OUI, productClass, protocol, dados_entrada['serialnumber'], dados_entrada['set_voip']['DirectoryNumber'], dados_entrada['set_voip']['AuthUserName'], dados_entrada['set_voip']['AuthPassword'], dados_entrada['set_voip']['ProxyServer'], dados_entrada['set_voip']['RegistrarServer'], dados_entrada['set_voip']['UserAgentDomain'], dados_entrada['set_voip']['OutboundProxy'], dados_entrada['set_voip']['phyReferenceList'])
                            if nbiSDO.msgTagExecution_SetVoIP == 'EXECUTED':
                                print(' -- SeT VoIP OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                                return dict_result
                            else:
                                print(' -- SeT VoIP NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- SeT VoIP NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                dict_result = {'obs': ' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- '}
                                print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                                return dict_result
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
                            print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                            return dict_result
                    except Exception as e:
                        print(e)
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                        return dict_result
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    dict_result = {'obs': ' -- CONECTIVIDADE COM ACS NOK --'}
                    print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                    return dict_result

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
            print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
            return dict_result

    def cancelVoIP(**dados_entrada):

        # print(f'\ndados_entrada = {dados_entrada}')
        # for chave, valor in dados_entrada.items():
        #     print(chave, valor)

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função Cancel VoIP ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])
                            deviceGUID = str(nbiRH.device["GUID"])

                            print(' -- Executando ACS [Cancel VoIP] --')
                            cancelvoip = nbiSDO.cancelVoip(OUI, productClass, protocol, dados_entrada['serialnumber'], dados_entrada['set_voip']['DirectoryNumber'])
                            if nbiSDO.msgTagExecution_cancelVoip == 'EXECUTED':
                                print(' -- Cancel VoIP OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                print('\n\n >>> Finalizando Cancel VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                                return dict_result
                            else:
                                print(' -- Cancel VoIP NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- SeT VoIP NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                dict_result = {'obs': ' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- '}
                                print('\n\n >>> Finalizando Cancel VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                                return dict_result
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
                            print('\n\n >>> Finalizando Cancel VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                            return dict_result
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando Cancel VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                        return dict_result
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    dict_result = {'obs': ' -- CONECTIVIDADE COM ACS NOK --'}
                    print('\n\n >>> Finalizando Cancel VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                    return dict_result

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
            print('\n\n >>> Finalizando Cancel VoIP ACS - Tempo de Execução:', total_time, '\n\n')
            return dict_result

    def runDownloadDiagnostics(**dados_entrada):

        # print(f'\ndados_entrada = {dados_entrada}')
        # for chave, valor in dados_entrada.items():
        #     print(chave, valor)

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função Download Diagnostics ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])
                            deviceGUID = str(nbiRH.device["GUID"])

                            print(' -- Analisando Velocidade do Link --')
                            """
                            * Dispositivos disponíveis:
                            *    ASKEY = ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'RTF8115VW', 'RTF8117VW']
                            *    MITRA = ['GPT-2541GNAC-N1', 'GPT-2541GNAC-N2', 'GPT-2741GNAC-N1', 'GPT-2741GNAC-N2', 'GPT-2731GN2A4P', 'GPT-2731GN2A4P-N2, 'GPT-2741GNAC-N1-SV', 'GPT-2741GNAC-N2-SV']
                            *
                            *   VENDOR          ||                  MODEL                                    ||                           SUPPORTED SPEED(Down/Up [Mbps])
                            *   ASKEY                     RTF3505VW-N1 | RTF3505VW-N2                                                              50/25
                            *   ASKEY                     RTF3507VW-N1 | RTF3507VW-N2                                                             50/25
                            *   ASKEY                     RTF8115VW | RTF8117VW  |  RTF8115VW-SV                                                  50/25, 100/50, 200/100, 300/150, 600/300, 1000/500 
                            *   MITRASTAR                 GPT-2541GNAC-N1 | GPT-2541GNAC-N2                                                        50/25
                            *   MITRASTAR                 GPT-2731GN2A4P | GPT-2731GN2A4P-N2                                                    50/25, 100/50, 200/100, 300/150, 600/300, 1000/500 
                            *   MITRASTAR                 GPT-2741GNAC-N1 | GPT-2741GNAC-N2  |  GPT-2741GNAC-N1-SV  |  GPT-2741GNAC-N2-SV       50/25, 100/50, 200/100, 300/150, 600/300, 1000/500 
                            *
                            """
                            if dados_entrada['velocidade_link'] == 50:
                                file_size = 187
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'Mb --')
                            elif dados_entrada['velocidade_link'] == 100 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 375
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'Mb --')
                            elif dados_entrada['velocidade_link'] == 200 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 750
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'Mb --')
                            elif dados_entrada['velocidade_link'] == 300 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 1125
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'Mb --')
                            elif dados_entrada['velocidade_link'] == 600 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 2250
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'Mb --')
                            elif dados_entrada['velocidade_link'] == 1000 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 3750
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'Mb --')
                            else:
                                file_size = {'obs': ' -- ERRO! Velocidade de Link não suportada pelo dispositivo --'}
                                print(' -- ERRO! Velocidade de Link não suportada pelo dispositivo --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print('\n\n >>> Finalizando Download Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                                return file_size
                            print(' -- Executando ACS [Download Diagnostics] --')
                            download_diagnostics = nbiSDO.runDownloadDiagnostics(OUI, productClass, protocol, dados_entrada['serialnumber'], file_size)
                            for i in download_diagnostics:
                                # print(i['name'])
                                if i['name'] == 'InternetGatewayDevice.DownloadDiagnostics.TotalBytesReceived':
                                    total_bytes = int(i['value'])
                                    # print(total_bytes)
                                elif i['name'] == 'InternetGatewayDevice.DownloadDiagnostics.EOMTime':
                                    eom_time = i['value']
                                    # print(i['value'])
                                    eom_time = eom_time.split('T')
                                    horas = eom_time[1][:2]
                                    # print(horas)
                                    minutos = eom_time[1][3:5]
                                    # print(minutos)
                                    segundos = eom_time[1][6:8]
                                    # print(segundos)
                                    eom_time = (int(horas)*3600) + (int(minutos)*60) + int(segundos)
                                    # print(eom_time)
                                elif i['name'] == 'InternetGatewayDevice.DownloadDiagnostics.BOMTime':
                                    bom_time = i['value']
                                    # print(bom_time)
                                    bom_time = bom_time.split('T')
                                    horas = bom_time[1][:2]
                                    # print(horas)
                                    minutos = bom_time[1][3:5]
                                    # print(minutos)
                                    segundos = bom_time[1][6:8]
                                    # print(segundos)
                                    bom_time = (int(horas) * 3600) + (int(minutos) * 60) + int(segundos)
                                    # print(bom_time)
                            tempo = eom_time - bom_time
                            # print(total_bytes)
                            # print(eom_time)
                            # print(bom_time)
                            velocidade = round((8*total_bytes)/((eom_time-bom_time)*1024*1024), 2)
                            print(' -- Velocidade -- ', velocidade, 'Mbps')
                            #Todo: Comparar o valor de entrada "velocidade_link" com o resultado obtido.... valor obtido deve ser maior que 80% da entrada
                            if nbiSDO.msgTagExecution_download_diagnostics == 'EXECUTED':
                                print(' -- Download Diagnostics OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                print('\n\n >>> Finalizando Download Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                                return dict_result
                            else:
                                print(' -- Cancel VoIP NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- SeT VoIP NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                dict_result = {'obs': ' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- '}
                                print('\n\n >>> Finalizando Download Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
                            print('\n\n >>> Finalizando Download Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                            return dict_result
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando Download Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                        return dict_result
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    dict_result = {'obs': ' -- CONECTIVIDADE COM ACS NOK --'}
                    print('\n\n >>> Finalizando Download Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                    return dict_result

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
            print('\n\n >>> Finalizando Download Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
            return dict_result 

    def runUploadDiagnostics(**dados_entrada):

        # print(f'\ndados_entrada = {dados_entrada}')
        # for chave, valor in dados_entrada.items():
        #     print(chave, valor)

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função Upload Diagnostics ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])
                            deviceGUID = str(nbiRH.device["GUID"])

                            print(' -- Analisando Velocidade do Link --')
                            """
                            * Dispositivos disponíveis:
                            *    ASKEY = ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'RTF8115VW', 'RTF8117VW']
                            *    MITRA = ['GPT-2541GNAC-N1', 'GPT-2541GNAC-N2', 'GPT-2741GNAC-N1', 'GPT-2741GNAC-N2', 'GPT-2731GN2A4P', 'GPT-2731GN2A4P-N2, 'GPT-2741GNAC-N1-SV', 'GPT-2741GNAC-N2-SV']
                            *
                            *   VENDOR          ||                  MODEL                                    ||                           SUPPORTED SPEED(Down/Up [Mbps])
                            *   ASKEY                     RTF3505VW-N1 | RTF3505VW-N2                                                              50/25
                            *   ASKEY                     RTF3507VW-N1 | RTF3507VW-N2                                                             50/25
                            *   ASKEY                     RTF8115VW | RTF8117VW  |  RTF8115VW-SV                                                  50/25, 100/50, 200/100, 300/150, 600/300, 1000/500 
                            *   MITRASTAR                 GPT-2541GNAC-N1 | GPT-2541GNAC-N2                                                        50/25
                            *   MITRASTAR                 GPT-2731GN2A4P | GPT-2731GN2A4P-N2                                                    50/25, 100/50, 200/100, 300/150, 600/300, 1000/500 
                            *   MITRASTAR                 GPT-2741GNAC-N1 | GPT-2741GNAC-N2  |  GPT-2741GNAC-N1-SV  |  GPT-2741GNAC-N2-SV       50/25, 100/50, 200/100, 300/150, 600/300, 1000/500 
                            *
                            """
                            if dados_entrada['velocidade_link'] == 50:
                                # file_size = 97517568
                                file_size = 975178
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'bytes --')
                            elif dados_entrada['velocidade_link'] == 100 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 196083712
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'bytes --')
                            elif dados_entrada['velocidade_link'] == 200 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 393216000
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'bytes --')
                            elif dados_entrada['velocidade_link'] == 300 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 589299712
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'bytes --')
                            elif dados_entrada['velocidade_link'] == 600 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 1179648000
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'bytes --')
                            elif dados_entrada['velocidade_link'] == 1000 and productClass not in ['RTF3505VW-N1', 'RTF3505VW-N2', 'RTF3507VW-N1', 'RTF3507VW-N2', 'GPT-2541GNAC-N1', 'GPT-2541GNAC-N2']:
                                file_size = 1966080000
                                print(' -- Velocidade do Link OK - Tamanho do Arquivo = ' + str(file_size) + 'bytes --')
                            else:
                                file_size = {'obs': ' -- ERRO! Velocidade de Link não suportada pelo dispositivo --'}
                                print(' -- ERRO! Velocidade de Link não suportada pelo dispositivo --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print('\n\n >>> Finalizando Upload Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                                return file_size
                            print(' -- Executando ACS [Upload Diagnostics] --')
                            upload_diagnostics = nbiSDO.runUploadDiagnostics(OUI, productClass, protocol, dados_entrada['serialnumber'], file_size)
                            for i in upload_diagnostics:
                                print(i['name'])
                                print(i['value'])
                                if i['name'] == 'InternetGatewayDevice.UploadDiagnostics.TotalBytesSent':
                                    total_bytes = int(i['value'])
                                    print(total_bytes)
                                elif i['name'] == 'InternetGatewayDevice.UploadDiagnostics.EOMTime':
                                    eom_time = i['value']
                                    # print(i['value'])
                                    eom_time = eom_time.split('T')
                                    horas = eom_time[1][:2]
                                    print(horas)
                                    minutos = eom_time[1][3:5]
                                    # print(minutos)
                                    segundos = eom_time[1][6:8]
                                    # print(segundos)
                                    eom_time = (int(horas) * 3600) + (int(minutos) * 60) + int(segundos)
                                    # print(eom_time)
                                elif i['name'] == 'InternetGatewayDevice.UploadDiagnostics.BOMTime':
                                    bom_time = i['value'].strftime("%Y%m%d%H%M%S")
                                    bom_time = i['value']
                                    # print(bom_time)
                                    bom_time = bom_time.split('T')
                                    horas = bom_time[1][:2]
                                    # print(horas)
                                    minutos = bom_time[1][3:5]
                                    # print(minutos)
                                    segundos = bom_time[1][6:8]
                                    # print(segundos)
                                    bom_time = (int(horas) * 3600) + (int(minutos) * 60) + int(segundos)
                                    # print(bom_time)
                                tempo = eom_time - bom_time
                                # print(total_bytes)
                                # print(eom_time)
                                # print(bom_time)
                                velocidade = round((8 * total_bytes) / ((eom_time - bom_time) * 1024 * 1024), 2)
                                print(' -- Velocidade -- ', velocidade, 'Mbps')
                                # Todo: Comparar o valor de entrada "velocidade_link" com o resultado obtido.... valor obtido deve ser maior que 20% da entrada
                            if nbiSDO.msgTagExecution_download_diagnostics == 'EXECUTED':
                                print(' -- Upload Diagnostics OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                print('\n\n >>> Finalizando Upload Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                                return dict_result
                            else:
                                print(' -- Upload Diagnostics NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- Upload Diagnostics NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                dict_result = {'obs': ' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- '}
                                print('\n\n >>> Finalizando Upload Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                                return dict_result
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
                            print('\n\n >>> Finalizando Upload Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                            return dict_result
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando Upload Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                        return dict_result
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    dict_result = {'obs': ' -- CONECTIVIDADE COM ACS NOK --'}
                    print('\n\n >>> Finalizando Upload Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
                    return dict_result

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
            print('\n\n >>> Finalizando Upload Diagnostics ACS - Tempo de Execução:', total_time, '\n\n')
            return dict_result

    def firmwareUpdate(**dados_entrada):
        # print(f'\ndados_entrada = {dados_entrada}')
        # for chave, valor in dados_entrada.items():
        #     print(chave, valor)

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função Firmware Update ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        if dados_entrada.get('serialnumber') and dados_entrada.get('IPACS') and dados_entrada.get('portaACS') and dados_entrada.get('IPACS') and dados_entrada.get('acsUsername') and dados_entrada.get('acsPassword'):
            print(' -- INFORMAÇÔES DE ENTRADA OK --')
            #
            ###Testando Conectividade ACS-NOKIA###
            #
            try:
                url = 'http://' + dados_entrada['IPACS'] + ':' + dados_entrada['portaACS'] + '/hdm'
                connTest = requests.post(url, timeout=4)
                print(' -- Validação de Conectividade com ACS --')
                if connTest.status_code == 200:
                    print(' -- CONECTIVIDADE COM ACS OK -- IP: ', dados_entrada['IPACS'])
                    print(' -- Validação de WebServices ACS --')
                    try:
                        nbiRH = Setup.ACS.webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = Setup.ACS.webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = Setup.ACS.webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        print(' -- WebServices OK --')
                        print(' -- Executando ACS [FindDeviceBySerial] --')
                        nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        if nbiRH.msgTagExecution_02 == 'EXECUTED':
                            print(' -- FindDeviceBySerial OK --')
                            OUI = str(nbiRH.device["OUI"])
                            productClass = str(nbiRH.device["productClass"])
                            protocol = str(nbiRH.device["protocol"])
                            subscriberId = str(nbiRH.device["subscriberId"])
                            lastContactTime = str(nbiRH.device["lastContactTime"])
                            softwareVersion = str(nbiRH.device["softwareVersion"])
                            deviceGUID = str(nbiRH.device["GUID"])

                            print(' -- Executando ACS [Firmware Update] --')
                            fw_update = nbiRH.firmwareUpdate(OUI, productClass, protocol, dados_entrada['serialnumber'], dados_entrada['firmware_file'])
                            print(' -- Aguardando execução do comando (6min) --')
                            time.sleep(360) # Time para execução do comando acima
                            print(' -- Executando ACS [Busca Serial após FW update] --')
                            nbiRH.findDeviceBySerial(dados_entrada['serialnumber'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                            if nbiRH.msgTagExecution_02 == 'EXECUTED':
                                print(' -- FindDeviceBySerial OK --')
                                OUI = str(nbiRH.device["OUI"])
                                productClass = str(nbiRH.device["productClass"])
                                protocol = str(nbiRH.device["protocol"])
                                subscriberId = str(nbiRH.device["subscriberId"])
                                lastContactTime = str(nbiRH.device["lastContactTime"])
                                softwareVersion_novo = str(nbiRH.device["softwareVersion"])
                                deviceGUID = str(nbiRH.device["GUID"])
                                print(softwareVersion_novo)
                                print(' -- Firmware Update OK --')
                                print(' -- Executando SSH para verificar a versão do Firmware -- ')
                                ssh_results = infoDevices_utils.getInfoHgu(dados_entrada['password'], dados_entrada['ip'])
                                if ssh_results['firmware'] == dados_entrada['firmware_file']:
                                    final_time = time.time()
                                    total_time = (final_time - ts)
                                    print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')
                                    dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                    return dict_result
                                else:
                                    final_time = time.time()
                                    total_time = (final_time - ts)
                                    print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')
                                    dict_result = {'obs': 'Não foi possível fazer o upgrade da versão do firmware'}
                                    return dict_result
                                # Todo: Fazer comparação entre versão que estava antes e versão que será atualizada
                            else:
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- FindDeviceBySerial NOK --')
                                print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                                print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')
                                print(' -- Firmware Update NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- Reboot NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')
                                dict_result = {'obs': ' -- FindDeviceBySerial NOK --'}
                                return
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
                            print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')
                            return dict_result
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')
                        return dict_result
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
            print('\n\n >>> Finalizando Firmware Update ACS - Tempo de Execução:', total_time, '\n\n')
            return dict_result
