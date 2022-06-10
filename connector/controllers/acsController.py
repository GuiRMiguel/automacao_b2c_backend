from flask_restful import Resource, reqparse
from flask import jsonify, request
from probes import acsProbe
from daos.mongo_dao import MongoConnSigleton

mongo_conn = MongoConnSigleton()

class acs(Resource):
    # def get(self, method):
        # if method == 'connectWifi':

    def post(self, method):

        obj = acsProbe.acs()
        print(method)

        #EAFP Approach
        try:
            username = request.json['username']
            password = request.json['password']
        except KeyError:
            pass

        if method == 'GPV_OneObjct':
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.GPV_OneObjct(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)

        
        elif method == 'initialInformations':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.initialInformations(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)
        

        elif method == 'wifi2GHzInformations':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.wifi2GHzInformations(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == 'wifi5GHzInformations':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.wifi5GHzInformations(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == 'setDHCP':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.setDHCP(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == 'set2GHzWiFi':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.set2GHzWiFi(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == 'set5GHzWiFi':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.set5GHzWiFi(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)
        
        elif method == 'indexWifi24ghz':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']

            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.indexWifi24ghz(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)

        elif method == 'indexWifi5ghz':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']


            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.indexWifi5ghz(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == 'checkIPv6Telefonica':
            # Parameters
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            acsPort = request.json['portaACS']
            password = request.json['password']
            ip = request.json['ip']


            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.checkIPv6Telefonica(GPV_Param, IPACS, acsUsername, acsPassword, acsPort, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == 'connectionRequestPort':
            serialnumber = request.json['serialnumber']
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            password = request.json['password']
            ip = request.json['ip']


            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            result = obj.connectionRequestPort(serialnumber, GPV_Param, IPACS, acsUsername, acsPassword, modelo, password, ip)
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == 'SPV':
            serialnumber = request.json['serialnumber']
            SPV_Param = request.json['SPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            
            ans = obj.SPV(serialnumber, IPACS, acsUsername, acsPassword, SPV_Param)

        elif method == 'execCusFuncPingDiagnostics':
            serialnumber = request.json['serialnumber']
            destAddress = request.json['destAddress']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            
            ans = obj.execCusFuncPingDiagnostics(serialnumber, IPACS, acsUsername, acsPassword, destAddress)

        elif method == 'execCusFuncHGUDiagnostics': ### NECESSITA VERIFICAR SAIDA ... AINDA NAO TESTAR
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            
            ans = obj.execCusFuncHGUDiagnostics(serialnumber, IPACS, acsUsername, acsPassword)

        elif method == 'execIssueConnectionRequest':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.execIssueConnectionRequest(serialnumber, IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass)

        elif method == 'execCheckDeviceAvailability':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.execCheckDeviceAvailability(serialnumber, IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass)

        elif method == 'getDeviceInfoACS':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            
            ans = obj.getDeviceInfoACS(serialnumber, IPACS, acsUsername, acsPassword)

        elif method == 'execRebootACS':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            deviceGUID = request.json['deviceGUID']
            
            ans = obj.execRebootACS(serialnumber, IPACS, acsUsername, acsPassword, deviceGUID)

        elif method == 'execGetWifiStatus':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.execGetWifiStatus(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber)

        elif method == 'execGetParameterAttributes':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            objeto = request.json['objeto']
            
            ans = obj.execGetParameterAttributes(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber, objeto)

        elif method == 'getLANHosts':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.getLANHosts(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber)

        elif method == 'getPPPoECredentials':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.getPPPoECredentials(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber)

        elif method == 'setPPPoECredentials':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            PPPoEUsername = request.json['PPPoEUsername']
            PPPoEPassword = request.json['PPPoEPassword']
            
            ans = obj.setPPPoECredentials(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber,PPPoEUsername,PPPoEPassword)

        elif method == 'execGetPortMapping':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.execGetPortMapping(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber)

        elif method == 'execAddPortMapping':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            enable = request.json['enable']
            internalClient = request.json['internalClient']
            internalPort = request.json['internalPort']
            externalPort = request.json['externalPort']
            portMapName = request.json['portMapName']
            protocolMapping = request.json['protocolMapping']
            
            ans = obj.execAddPortMapping(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber, enable, internalClient, internalPort, externalPort, portMapName, protocolMapping)

        elif method == 'execSetVoIP':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            DirectoryNumber = request.json['DirectoryNumber']
            AuthUserName = request.json['AuthUserName']
            ProxyServer = request.json['ProxyServer']
            RegistrarServer = request.json['RegistrarServer']
            UserAgentDomain = request.json['UserAgentDomain']
            OutboundProxy = request.json['OutboundProxy']
            phyReferenceList = request.json['phyReferenceList']
            
            ans = obj.execSetVoIP(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber, DirectoryNumber, AuthUserName, ProxyServer, RegistrarServer, UserAgentDomain, OutboundProxy,phyReferenceList)

        elif method == 'execSetWifi':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            WIFI_SETTINGS = request.json['WIFI_SETTINGS']
            
            ans = obj.execSetWifi(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber, WIFI_SETTINGS)

        elif method == 'execCancelVoIP':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            parameter = request.json['parameter']
            
            ans = obj.execCancelVoIP(serialnumber, IPACS, acsUsername, acsPassword, parameter)

        elif method == 'execDownloadDiagnostics':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            ip = request.json['ip']
            filesize = request.json['filesize']
            
            ans = obj.execDownloadDiagnostics(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber, ip, filesize)
        elif method == 'execGetDHCP':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.execGetDHCP(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber)

        elif method == 'execSetDHCP':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            DHCP_SETTINGS = request.json['DHCP_SETTINGS']
            
            ans = obj.execSetDHCP(IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass, serialnumber, DHCP_SETTINGS)

        elif method == 'execResetFactory':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            
            ans = obj.execResetFactory(serialnumber, IPACS, acsUsername, acsPassword,OUI,protocol,ProductClass)

        elif method == 'execFirmwareUpdate':
            serialnumber = request.json['serialnumber']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            OUI = request.json['OUI']
            protocol = request.json['protocol']
            ProductClass = request.json['ProductClass']
            firmwareName = request.json['firmwareName']
            
            ans = obj.execFirmwareUpdate(serialnumber, IPACS, acsUsername, acsPassword, OUI, protocol, ProductClass, firmwareName)

        elif method == 'GPV':
            serialnumber = request.json['serialnumber']
            GPV_Param = request.json['GPV_Param']
            IPACS = request.json['IPACS']
            acsUsername = request.json['acsUsername']
            acsPassword = request.json['acsPassword']
            
            ans = obj.GPV(serialnumber, GPV_Param, IPACS, acsUsername, acsPassword)

        else:
            return {"name_teste": "Doesnt Exist", "response": "none"}

        return jsonify(ans)