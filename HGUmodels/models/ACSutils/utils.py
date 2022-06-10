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
        print(dados_entrada)
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
        #TODO: criar chamada no SDO

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
                            reboot = nbiRH.reboot(deviceGUID)
                            if nbiRH.msgTagExecution_03 == 'EXECUTED':
                                print(' -- SeT VoIP OK --')
                                dict_result = {"Resultado_Probe": "OK", "obs": "Teste OK", "result": "passed"}
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                            else:
                                print(' -- SeT VoIP NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- SeT VoIP NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                dict_result = {'obs': ' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- '}
                                print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                            
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            dict_result = {'obs': ' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- '}
                            print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        dict_result = {'obs': ' -- WEBSERVICES NOK --'}
                        print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    dict_result = {'obs': ' -- CONECTIVIDADE COM ACS NOK --'}
                    print('\n\n >>> Finalizando SeT VoIP ACS - Tempo de Execução:', total_time, '\n\n')

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
