# -*- coding: utf-8 -*-
#
import requests
import sys
from zeep import Client
from zeep import xsd
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
import logging.config

#
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
class NRH:
    def __init__(self, iphdm, porthdm, username, password):
        self.ip = iphdm
        self.port = porthdm
        self.username = username
        self.password = password
        self.serialNumber = ''
        self.GUID = ''
        self.msgTagExecution = ''
        self.msgErrorLog = ''
        self.msgErrosDetail = ''
        #
        try:
            transport = Transport(timeout=2)
            remoteHDM = "http://" + self.ip + ":" + self.port + "/remotehdm/NBIService?wsdl"
            self.client = Client(remoteHDM, wsse=(UsernameToken(self.username, self.password)), transport=transport)
            self.msgTagExecution = 'EXECUTED'
        except:
            e = sys.exc_info()[1]
            self.msgTagExecution = 'ERROR'
            self.msgErrorLog = str(e)
            self.msgErrorDetail = 'ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM - REMOTEHDM'

    #
    #
    #
    def createSingleFirmwareUpdateOperation(self, OUI, productClass, protocol, serialNumber, firmwareNameIn):
        deviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol, 'serialNumber': serialNumber}
        firmwareName = str(firmwareNameIn)
        timeout = int(300)
        try:
            self.firmwareAction = self.client.service.createSingleFirmwareUpdateOperation(nBIDeviceID=deviceId, string=firmwareName,
                                                                                          intVal=timeout)
            self.msgTagExecution_01 = 'EXECUTED'
            self.msgErrorLog_01 = 'FIRMWARE UPDATE EXECUTADO COM SUCESSO'
            self.msgErrorDetail_01 = 'MSG_004-SUCESSO AO EXECUTAR FIMRWARE UPDATE'
        except:
            e = sys.exc_info()[1]
            self.msgTagExecution_01 = 'ERROR'
            self.msgErrorLog_01 = str(e)
            self.msgErrorDetail_01 = 'ERROR_004-ERROR AO EXECUTAR FIMRWARE UPDATE'

    #
    #
    def findDeviceBySerial(self, serialNumber, username, password):
        try:
            wsdl = 'Setup/ACS/NBIService.wsdl'
            client = Client(wsdl, wsse=UsernameToken(username, password))
            NbiParameter = client.get_type("ns3:NBIParameter")
            dadosNbiPar = NbiParameter(name='serialNumber', value=xsd.AnyObject(xsd.String(), serialNumber))
            ArrayOfNBITemplate = client.get_type('ns3:ArrayOfNBITemplate')
            dadosArray = ArrayOfNBITemplate([dadosNbiPar])
            NbiTemplate = client.get_type('ns3:NBITemplate')
            dadosNbiTem = NbiTemplate(name="ct.find.devices.serialNumber", parameters=dadosArray)
            connService = client.service.findDevicesByTemplate(dadosNbiTem, 500, -1)
            self.device = {"OUI": connService[0]['deviceId']['OUI'],
                           "productClass": connService[0]['deviceId']['productClass'],
                           "serialNumber": connService[0]['deviceId']['serialNumber'],
                           "protocol": connService[0]['deviceId']['protocol'],
                           "softwareVersion": connService[0]['softwareVersion'],
                           "subscriberId": connService[0]['subscriberID'],
                           "GUID": connService[0]['deviceGUID'],
                           "firstContactTime": connService[0]['firstContactTime'],
                           "iPAddressWAN": connService[0]['IPAddress'],
                           "lastActivationTime": connService[0]['lastActivationTime'],
                           "lastContactTime": connService[0]['lastContactTime'],
                           "activated": connService[0]['activated']
                           }
            self.msgTagExecution_02 = 'EXECUTED'
            self.msgErrorLog_02 = 'SERIAL ENCONTRADO'
            self.msgErrorDetail_02 = 'MSG_006-SUCESSO AO EXECUTAR BUSCA DE INFORMACOES PELO SERIAL'
        except Exception as erro:
            print(erro)
            e = sys.exc_info()[1]
            self.msgTagExecution_02 = 'ERROR'
            self.msgErrorLog_02 = str(e)
            self.msgErrorDetail_02 = 'ERROR_005-ERROR AO EXECUTAR BUSCA DE INFORMACOES PELO SERIAL OU INEXISTENTE'

    #
    #
    #
    def reboot(self, deviceGUID):
        nBIOptions = {'disableCaptureConstraint': 'true', 'executionTimeoutSeconds': '500', 'expirationTimeoutSeconds': '120',
                      'failOnConnectionRequestFailure': 'true', 'policyClass': 'test555', 'priority': '100',
                      'updateCachedDataRecord': 'false'}
        try:
            reboot = self.client.service.createSingleDeviceOperationByDeviceGUID(longVal=deviceGUID, nBIFunction={'functionCode': '1'},
                                                                                 nBISingleDeviceOperationOptions=nBIOptions)
            self.msgTagExecution_03 = 'EXECUTED'
            self.msgErrorLog_03 = 'REBOOT EXECUTADO COM SUCESSO'
            self.msgErrorDetail_03 = 'MSG_006-remoteHDM-SUCESSO AO EXECUTAR REBOOT'
            return self.msgTagExecution_03
        except:
            e = sys.exc_info()[1]
            self.msgTagExecution_03 = 'ERROR'
            self.msgErrorLog_03 = str(e)
            self.msgErrorDetail_03 = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR REBOOT'
            return e
