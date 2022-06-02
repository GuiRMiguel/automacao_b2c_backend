import Setup.ACS.webSDO
import Setup.ACS.webRemoteHDM
from Setup.ACS import webRemoteHDM
from Setup.ACS import webServiceImpl
from Setup.ACS import webSDO
import os
import sys
import time
import datetime
import requests
import threading
import json
from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class ACS():
    def getParameterValues(**dados_entrada):

        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')

        print('\n\n >>> Iniciando Função GetParameterValues ACS -', start_time, '\n\n')

        print(' -- Validações de Entrada --')
        print(dados_entrada.get('serialnumber'))
        print(dados_entrada.get('IPACS'))
        print(dados_entrada.get('portaACS'))
        print(dados_entrada.get('acsUsername'))
        print(dados_entrada.get('acsPassword'))

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
                        nbiRH = webRemoteHDM.NRH(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSDO = webSDO.SDO(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
                        nbiSI = webServiceImpl.NSI(dados_entrada['IPACS'], dados_entrada['portaACS'], dados_entrada['acsUsername'], dados_entrada['acsPassword'])
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
                                print(GPV_1)
                                
                                print(' -- GetParameterValues OK --')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                            else:
                                print(' -- GetParameterValues NOK -- ERRO: Device OFFLINE')
                                final_time = time.time()
                                total_time = (final_time - ts)
                                print(' -- GetParameterValues NOK --')
                                print(' -- ATENÇÃO! DISPOSITIVO OFFLINE OU NÃO RESPONDENDO A CONNECTION REQUEST! -- ')
                                print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                           
                        else:
                            final_time = time.time()
                            total_time = (final_time - ts)
                            print(' -- FindDeviceBySerial NOK --')
                            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
                            print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                    except:
                        final_time = time.time()
                        total_time = (final_time - ts)
                        print(' -- WEBSERVICES NOK --')
                        print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
                else:
                    final_time = time.time()
                    total_time = (final_time - ts)
                    print(' -- CONECTIVIDADE COM ACS NOK --')
                    print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')

            except:
                e = sys.exc_info()[1]
        else:
            final_time = time.time()
            total_time = (final_time - ts)
            print(' -- Informações de Entrada NOK --')
            print(' -- ATENÇÃO! REVEJA PARAMETROS DE ENTRADA! -- ')
            print('\n\n >>> Finalizando GetParameterValues ACS - Tempo de Execução:', total_time, '\n\n')
