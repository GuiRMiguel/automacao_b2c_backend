# -*- coding: utf-8 -*-
#
import time

from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
import sys
from zeep import xsd
import zeep
import ast
import json

import logging.config


### DEBUG PARA VERIFICAR COMUNICAÇÃO SOAP ###
# logging.config.dictConfig({
#     'version': 1,
#     'formatters': {
#         'verbose': {
#             'format': '%(name)s: %(message)s'
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'zeep.transports': {
#             'level': 'DEBUG',
#             'propagate': True,
#             'handlers': ['console'],
#         },
#     }
# })
#
#
class SDO:
    def __init__(self, iphdm, porthdm, username, password):
        self.ip = iphdm
        self.port = porthdm
        self.username = username
        self.password = password
        self.connectionError = ''
        self.msgConnection = ''
        self.isOnline = ''
        self.msgTagExecution_PingDiag = ''
        self.msgErrorDetail_PingDiag = ''
        self.msgErrorLog_PingDiag = ''
        self.msgTagExecution_SPV = ''
        self.msgErrorDetail_SPV = ''
        self.msgErrorLog_SPV = ''
        self.msgTagExecution_SPV_ERROR = ''
        self.msgTagExecution_GPV = ''
        self.msgErrorDetail_GPV = ''
        self.msgErrorLog_GPV = ''
        self.msgTagExecution_GPV_ERROR = ''
        self.msgTagExecution_012 = ''
        self.msgErrorDetail_022 = ''
        self.msgErrorLog_022 = ''
        try:
            transport = Transport(timeout=2)
            SDO = "http://" + self.ip + ":" + self.port + "/SynchDeviceOpsImpl/SynchDeviceOperationsNBIService?wsdl"
            self.client = Client(SDO, wsse=(UsernameToken(self.username, self.password)), transport=transport)
            self.connectionError = 'False'
            self.msgTagExecution = 'EXECUTED'
            self.msgErrorLog = 'NONE'
            self.msgErrorDetail = 'MSG_003-WSDL INFORMADO COM SUCESSO SDO'
        except:
            e = sys.exc_info()[1]
            print(e)
            self.msgTagExecution = 'ERROR'
            self.msgErrorLog = str(e)
            self.msgErrorDetail = 'MSG_003-ERRO AO INFORMAR WSDL SDO'
#
    def issueConnectionRequest(self, OUI, productClass, protocol, seriaNumber):
        nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                       'serialNumber': seriaNumber}
        parameter = int(3500)
        try:
            connect = self.client.service.issueConnectionRequest(arg0=nbiDeviceId, arg1=parameter)
            self.isOnline = str(connect['success'])
            self.msgTagExecution_01 = 'EXECUTED'
            self.msgErrorLog_01 = 'ONLINE'
            self.msgErrorDetail_01 = 'MSG_002-SUCESSO DISPOSITIVO ONLINE'
            return self.isOnline
        except:
            e = sys.exc_info()[1]
            print(e)
            self.isOnline = 'False'
            self.msgTagExecution_01 = 'ERROR'
            self.msgErrorLog_01 = str(e)
            self.msgErrorDetail_01 = 'ERROR_007-ERROR DISPOSITIVO OFFLINE'
            return e
#
    def getParameterValue(self, OUI, productClass, protocol, serialNumber, object):
        try:
            #object = 'InternetGatewayDevice.ManagementServer.PeriodicInformInterval'
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol, 'serialNumber': serialNumber}
            timeout = 30000
            nBIOptions = {'disableCaptureConstraint': 'true', 'executionTimeoutSeconds': '120',
                          'expirationTimeoutSeconds': '60',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555', 'policyClass': 'policytest', 'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false', 'updateCachedDataRecord': 'true'}
            #getParameterValue = self.client.service.getParameterValues(arg0=nbiDeviceId, arg1=object, arg2=nBIOptions, arg3=timeout)
            # Exemplo de Request getParameterValues no SOAPUI - testado e validado
            """
            <soap:Body>
                <syn:getParameterValues>
                    <!--Optional:-->
                    <arg0>
        
                        <OUI>b046fc</OUI>
                        <productClass>GPT-2541GNAC-N1</productClass>
                        <protocol>DEVICE_PROTOCOL_DSLFTR069v1</protocol>
                        <serialNumber>A433D7E31BAA</serialNumber>
                    </arg0>
        
                    <arg1>
                        <parameterNames>InternetGatewayDevice.ManagementServer.PeriodicInformInterval</parameterNames>
                        <parameterNames>InternetGatewayDevice.ManagementServer.CWMPRetryMinimumWaitInterval</parameterNames>
                    </arg1>
        
                    <arg2>
                        <disableCaptureConstraint>true</disableCaptureConstraint>
                        <executionTimeoutSeconds>55</executionTimeoutSeconds>
                        <expirationTimeoutSeconds>60</expirationTimeoutSeconds>
                        <failOnConnectionRequestFailure>true</failOnConnectionRequestFailure>
                        <NBISingleDeviceOperationCallBackInfo>
                            <retry>false</retry>
                        </NBISingleDeviceOperationCallBackInfo>
                        <opaqueTransactionId>test5555</opaqueTransactionId>
                        <policyClass>policytest</policyClass>
                        <priority>100</priority>
                        <replaceDeviceCachedDataRecord>false</replaceDeviceCachedDataRecord>
                        <updateCachedDataRecord>true</updateCachedDataRecord>
                    </arg2>
                    <arg3>30000</arg3>
                </syn:getParameterValues>
            </soap:Body
            """
            # print('object = ', object)
            # print('type of object = ', type(object))
            # teste = self.client.get_type('ns0:getParameterValues')
            # print('get_type "getParameterValues" = ', teste)
            # teste = self.client.get_type('ns0:getParameterValuesDTO')
            # print('get_type "getParameterValuesDTO" = ', teste)
            # getParameterValue = self.client.service.getParameterValues(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), object), arg2=nBIOptions, arg3=timeout)
            getParameterValue = self.client.service.getParameterValues(arg0=nbiDeviceId, arg1=object, arg2=nBIOptions, arg3=timeout)
            self.msgTagExecution_GPV = 'EXECUTED'
            get_ParameterValue = list()
            for i in getParameterValue:
                input_dict = zeep.helpers.serialize_object(i)
                output_dict = json.loads(json.dumps(input_dict))
                get_ParameterValue.append(output_dict)
            return get_ParameterValue
        except TypeError:
            print("'NoneType' object is not iterable")
        except:
            e = sys.exc_info()[1]
            self.msgTagExecution_GPV_ERROR = 'ERROR'
            self.msgErrorLog_GPV = str(e)
            self.msgErrorDetail_GPV = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR GPV'

    def setParameterValue(self, OUI, productClass, protocol, serialNumber, input):
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol, 'serialNumber': serialNumber}
            parameter = {
                'parameterKey': '?',
                'parameterValueStructs':input
            }
            timeout = 50000
            nBIOptions = {'disableCaptureConstraint': 'true', 'executionTimeoutSeconds': '300',
                          'expirationTimeoutSeconds': '240',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555', 'policyClass': 'policytest', 'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false', 'updateCachedDataRecord': 'true'}
            self.parameterValue = self.client.service.setParameterValues(arg0=nbiDeviceId, arg1=parameter, arg2=nBIOptions, arg3=timeout)
            # print('\n\n\n', self.parameterValue, '\n\n\n')
            # print(type(self.parameterValue))
            self.msgTagExecution_SPV = 'EXECUTED'
            return self.parameterValue

        except:
            e = sys.exc_info()[1]
            self.msgTagExecution_SPV_ERROR = 'ERROR'
            self.msgErrorLog_SPV = str(e)
            self.msgErrorDetail_SPV = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR SPV'


    def pingDiagnostics(self, OUI, productClass, protocol, serialNumber, objeto):
        #Custom function Ping Diagnostics -> FunctionCode = 9530
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol, 'serialNumber': serialNumber}
            numberExecuteFunction = 9530
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            #parameter = str({"destAddress":"www.google.com.br", "qtdRequisitions":"2"})
            parameter = str({"destAddress": objeto, "qtdRequisitions": "4"})
            #print(parameter)
            ansPingDiag = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), parameter),
                                                         arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            #print(ansPingDiag)
            ansPingDiag = ast.literal_eval(ansPingDiag)
            # print('---------------------------------------------------------------')
            # print('                      PING RESULTS      ')
            # print('---------------------------------------------------------------')
            global varList
            varList = []
            for key, value in ansPingDiag.items():
                temp = [key, value]
                varList.append(temp)
            #for i in varList:
                #print(i)
            #print('-=' * 32)
            self.msgTagExecution_PingDiag = 'EXECUTED'
            return varList
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            #print('PRINT DO EXCEPT = ' + e)
            self.msgTagExecution_PingDiag_ERROR = 'ERROR'
            self.msgErrorLog_PingDiag = str(e)
            self.msgErrorDetail_PingDiag = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR PingDiag'

    def checkDeviceAvailability(self, OUI, productClass, protocol, serialNumber):
        nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                       'serialNumber': serialNumber}
        nBIOptions = {'disableCaptureConstraint': 'true',
                      'executionTimeoutSeconds': '180',
                      'expirationTimeoutSeconds': '180',
                      'failOnConnectionRequestFailure': 'true',
                      'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                      'opaqueTransactionId': 'teste555',
                      'policyClass': 'policytest',
                      'priority': '100',
                      'replaceDeviceCachedDataRecord': 'false',
                      'updateCachedDataRecord': 'true'}
        timeout = 30000
        parameter = int(3500)
        try:
            connect = self.client.service.checkOnline(arg0=nbiDeviceId, arg1=nBIOptions, arg2=timeout)
            # print(connect)
            self.isOnline = str(connect['success'])
            self.msgTagExecution_01 = 'EXECUTED'
            self.msgErrorLog_01 = 'ONLINE'
            self.msgErrorDetail_01 = 'MSG_002-SUCESSO DISPOSITIVO ONLINE'
            return connect
        except:
            e = sys.exc_info()[1]
            # print('ERRO = ',e)
            # for i in str(e):
            #     print(i)
            self.isOnline = 'False'
            self.msgTagExecution_01 = 'ERROR'
            self.msgErrorLog_01 = str(e)
            self.msgErrorDetail_01 = 'ERROR_007-ERROR DISPOSITIVO OFFLINE'
            return str(e)




    def getHGU_DIAGNOSTICS_CUSTOM(self, OUI, productClass, protocol, serialNumber):
        # Custom function Ping Diagnostics -> FunctionCode = 9530
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 12000
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            #print(timeout)
            HGU_DIAG = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), '{}'),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            print(HGU_DIAG)
            self.msgTagExecution_PingDiag = 'EXECUTED'
            return HGU_DIAG
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            self.msgTagExecution_PingDiag_ERROR = 'ERROR'
            self.msgErrorLog_PingDiag = str(e)
            self.msgErrorDetail_PingDiag = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR PingDiag'

    def changeVoIPPassword(self, OUI, productClass, protocol, serialNumber, change_password, phyRefList):
        # Custom function changeVoIPPassword -> FunctionCode = 10003
        # {"AuthPassword":"95305",
        #         "phyReferenceList":"1"}
        input = str({"AuthPassword": change_password, "phyReferenceList": phyRefList})
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 10003
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            #print(timeout)
            changeVoIPPassword = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), input), arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            print(changeVoIPPassword)
            self.msgTagExecution_PingDiag = 'EXECUTED'
            return changeVoIPPassword
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            self.msgTagExecution_PingDiag_ERROR = 'ERROR'
            self.msgErrorLog_PingDiag = str(e)
            self.msgErrorDetail_PingDiag = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR PingDiag'
            return e



    def setVoip(self, OUI, productClass, protocol, serialNumber, DirectoryNumber, AuthUserName, AuthPassword, ProxyServer, RegistrarServer, UserAgentDomain, OutboundProxy, phyReferenceList):
        # Custom function changeVoIPPassword -> FunctionCode = 10003
        # {"AuthPassword":"95305",
        #         "phyReferenceList":"1"}
        input = str({
            "DirectoryNumber": DirectoryNumber,
            "AuthUserName": AuthUserName,
            "AuthPassword": AuthPassword,
            "ProxyServer": ProxyServer,
            "RegistrarServer": RegistrarServer,
            "UserAgentDomain": UserAgentDomain,
            "OutboundProxy": OutboundProxy,
            "phyReferenceList": phyReferenceList
        })
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9500
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            #print(timeout)
            setvoip = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), input), arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            print(setvoip)
            self.msgTagExecution_SetVoIP = 'EXECUTED'
            return setvoip
        except TypeError as e:
            print(e)
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            self.msgTagExecution_SetVoIP_ERROR = 'ERROR'
            self.msgErrorLog_SetVoIP = str(e)
            self.msgErrorDetail_SetVoIP = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR SetVoIP'
            return e


    def cancelVoip(self, OUI, productClass, protocol, serialNumber, DirectoryNumber):
        # Custom function cancelVoIP -> FunctionCode = 9540
        input = str({
            "directoryNumber": DirectoryNumber
        })
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9540
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            #print(timeout)
            cancelVoip = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), input), arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            print(cancelVoip)
            self.msgTagExecution_cancelVoip = 'EXECUTED'
            return cancelVoip
        except TypeError as e:
            print(e)
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            self.msgTagExecution_cancelVoip_ERROR = 'ERROR'
            self.msgErrorLog_cancelVoip = str(e)
            self.msgErrorDetail_cancelVoip = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR cancelVoip'
            return e


    def runDownloadDiagnostics(self, OUI, productClass, protocol, serialNumber, file_size):
        # Custom function Download Diagnostics -> FunctionCode = 9110
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9110
            download_url = 'http://201.95.254.137/download/' + str(file_size)
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '600',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 300000
            #print(timeout)
            download_diagnostics = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), download_url),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            # print(download_diagnostics)
            self.msgTagExecution_download_diagnostics = 'EXECUTED'
            return download_diagnostics
        except TypeError as e:
            print(e)
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            self.msgTagExecution_download_diagnostics_ERROR = 'ERROR'
            self.msgErrorLog_download_diagnostics = str(e)
            self.msgErrorDetail_download_diagnostics = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR download_diagnostics'


    def runUploadDiagnostics(self, OUI, productClass, protocol, serialNumber, file_size):
        # Custom function Upload Diagnostics -> FunctionCode = 9120
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9120
            upload_url = 'http://201.95.254.137/upload_automacao/' + str(file_size)
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '600',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 300000
            #print(timeout)
            upload_diagnostics = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), upload_url),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            # print(upload_diagnostics)
            self.msgTagExecution_upload_diagnostics = 'EXECUTED'
            return upload_diagnostics
        except TypeError as e:
            print(e)
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            self.msgTagExecution_upload_diagnostics_ERROR = 'ERROR'
            self.msgErrorLog_upload_diagnostics = str(e)
            self.msgErrorDetail_upload_diagnostics = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR download_diagnostics'