from ..ACSutils import utils
from audioop import lin2lin
from gc import collect
from http import client
from re import sub
import re
import time
from datetime import datetime
# from turtle import up
# from tkinter.messagebox import NO
from ..AskeyECNT import HGU_AskeyECNT
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

import paramiko
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException
import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config

session = MainSession()

mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

class HGU_AskeyECNT_settingsProbe(HGU_AskeyECNT):
    class MyEncoder(JSONEncoder):
            def default(self, o):
                return o.__dict__

    def initialInformations_4(self, flask_sername):
        """
        """
        self._driver.get('http://' + self._address_ip + '/')
        time.sleep(3)
        self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[4]/a').click()
        time.sleep(5)
        firmware_version = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[2]')




    def accessWizard_401(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            
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
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="menu-loc-net"]/ul/li[1]/a').click()
            self._driver.quit()
            

            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
            dict_saida = {"Resultado_Probe": "OK"}
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"obs": "Nao foi possivel realizar o login com sucesso"})
            dict_saida = {"Resultado_Probe": "NOK"}

        finally:
            self.update_global_result_memory(flask_username, 'accessWizard_401', dict_saida)
            return self._dict_result

    '''
    Teste 402 e igual ao 401
    ''' 

    def accessPadrao_403(self):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            user_input = self._driver.find_element_by_id('txtUser')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(2)
            self._driver.switch_to.frame('mainFrm')
            self._driver.find_element_by_xpath('//*[@id="tbGPONinfo"]')
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"obs": 'Nao foi possivel realizar o login com sucesso'})
        finally:
            self._driver.quit()
            return self._dict_result

    '''
    Teste 404 e igual ao 403
    ''' 

    def accessRemoteHttp_405(self, flask_username):

        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            
            self._driver.switch_to.frame('menuFrm')
            trustDomain = self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[3]').click()
            trustDomain = self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[3]').text
            time.sleep(1)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')

            trustDomain_ip_valor = self._driver.find_element_by_xpath('//*[@id="wan_src_ip"]').get_attribute('value')
            trustDomain_httpServices_port_valor = self._driver.find_element_by_xpath('//*[@id="TrustDomainForm"]/div[2]/input[4]').get_attribute('value')
            trustDomain_SSHServices_port_valor = self._driver.find_element_by_xpath('//*[@id="TrustDomainForm"]/div[3]/input[4]').get_attribute('value')
            
            Domain = namedtuple('Domin', 'xpath inputs')
            dict_domain = {
                'httpServices': Domain(xpath='//*[@id="TrustDomainForm"]/div[2]/input', inputs=[]), 
                'SSHServices' : Domain(xpath='//*[@id="TrustDomainForm"]/div[3]/input', inputs=[]), 
                'ICMPServices': Domain(xpath='//*[@id="TrustDomainForm"]/div[4]/input', inputs=[])
            }

            for domain in dict_domain.values():
                for input in self._driver.find_elements_by_xpath(domain.xpath):
                    teste = input.get_attribute('checked')
                    domain.inputs.append('Habilitado' if teste == 'true' else 'Desabilitado')
            json_saida405 = {
                trustDomain:
                    {
                        'trustDomain_ip': trustDomain_ip_valor,
                        'httpServices':
                            {
                                "LAN/WLAN": dict_domain['httpServices'].inputs[0],
                                "WAN": dict_domain['httpServices'].inputs[1],
                                "Trusted": dict_domain['httpServices'].inputs[2],
                                "Port": trustDomain_httpServices_port_valor
                            },
                        'SSHServices':
                            {
                                "LAN/WLAN": dict_domain['SSHServices'].inputs[0],
                                "WAN": dict_domain['SSHServices'].inputs[1],
                                "Trusted": dict_domain['SSHServices'].inputs[2],
                                "Port": trustDomain_SSHServices_port_valor
                            },
                        'ICMPServices':
                            {
                                "LAN/WLAN": dict_domain['ICMPServices'].inputs[0],
                                "WAN": dict_domain['ICMPServices'].inputs[1],
                                "Trusted": dict_domain['ICMPServices'].inputs[2],
                            }
                    }
            }
            if json_saida405['Trust Domain']['httpServices'].get('WAN') == 'Desabilitado':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'WAN esta Desabilitado'})
            else:
                self._dict_result.update({'obs': 'WAN esta Habilitado'})
            
        except IndexError as exception:
            self._dict_result.update({'obs': exception})
        finally:
            self._driver.quit()
            
            self.update_global_result_memory(flask_username, 'accessRemoteHttp_405', json_saida405)
            return self._dict_result

    
    '''
    Teste 406 e igual ao 407. 406 Teste de telnet. Nao disponivel
    ''' 

    
    def accessRemoteSSH_407(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessRemoteHttp_405')

        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 405 primeiro'})
        else:
            wan = result['Trust Domain']['SSHServices'].get('WAN')
            if wan == 'Desabilitado':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'WAN esta Desabilitado'})
            else:
                self._dict_result.update({'obs': 'WAN esta Habilitado'})

        return self._dict_result


    def accessRemoteTrustedIP_408(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessRemoteHttp_405')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 405 primeiro'})
        else:
            ip = result['Trust Domain'].get('trustDomain_ip')
            if ip == '':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'IP Address esta vazio'})
            else:
                self._dict_result.update({'obs': 'IP Address esta preenchido'})

        return self._dict_result


    def NTPServer_409(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {self._address_ip} \n{'#' * 50}")
            ssh.connect(hostname=self._address_ip, username=self._username, password=self._password, timeout=2)
            print("Authentication successfuly, connect to HGU")
            teste = ssh.invoke_shell()
            teste.send('rg\n')
            time.sleep(2)
            teste.send('time \n')
            time.sleep(2)
            teste.send('show \n')
            time.sleep(2)
            output = teste.recv(65000)
            out_str = output.decode('utf-8')
            str_list = out_str.splitlines()
            for i in str_list:
                if i.startswith('NTP server 1'):
                    split_ntp = i.split('=')
                    ntp_server = split_ntp[1]
                    ntp_server = ntp_server.strip()
                    print(ntp_server)

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
            teste.send('rg\n')
            time.sleep(2)
            teste.send('time \n')
            time.sleep(2)
            teste.send('show \n')
            time.sleep(2)
            output = teste.recv(65000)
            out_str = output.decode('utf-8')
            ssh.close()
            str_list = out_str.splitlines()
          
            for i in str_list:
                if i.startswith('timezone'):
                    split_time = i.split('=')
                    time_zone = split_time[1]
                    time_zone = time_zone.strip()
                    print(time_zone)
           
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
            
            #Manutencao >> TR069-Client
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[1]').click()
            self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[1]').text
            

            time.sleep(5)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')
            time.sleep(2)

            tr69_cwmp_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[1]/input[1]').get_attribute('checked')
            tr69_cwmp_valor = 'Habilitado' if tr69_cwmp_valor == 'true' else 'Desabilitado'

            tr69_acsURL_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[2]/input').get_attribute('value')

            tr69_acsUsername_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[3]/input').get_attribute('value')

            tr69_acsPassword_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[4]/input').get_attribute('value')

            tr69_acsPII_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[5]/input').get_attribute('value')

            tr69_acsPII_interval_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[6]/input').get_attribute('value')

            tr69_connection_request_URL_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/fieldset/div[1]/label[2]').get_attribute('value')

            tr69_connection_request_Username_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/fieldset/div[2]/input').get_attribute('value')

            tr69_connection_request_Password_valor = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/fieldset/div[3]/input').get_attribute('value')
            json_saida411 = {
                "tr69_setting":
                    {
                        "tr69_cwmp": tr69_cwmp_valor,
                        "tr69_acsURL": tr69_acsURL_valor,
                        "tr69_acsUsername": tr69_acsUsername_valor,
                        "tr69_acsPassword": tr69_acsPassword_valor,
                        "tr69_acsPII": tr69_acsPII_valor,
                        "tr69_acsPII_interval": tr69_acsPII_interval_valor,
                    },
                "tr69_connection_request":
                    {
                        "tr69_connection_request_URL": tr69_connection_request_URL_valor,
                        "tr69_connection_request_Username": tr69_connection_request_Username_valor,
                        "tr69_connection_request_Password": tr69_connection_request_Password_valor
                    }
            }

            self._driver.quit()
            acs_url = json_saida411['tr69_setting']['tr69_acsURL']
            if acs_url == 'http://acs.telesp.net.br:7005/cwmpWeb/WGCPEMgt':
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": "ACS URL esta correta"})
            else:
                self._dict_result.update({"obs": f'ACS URL incorreta, seu retorno: {acs_url}'})

        except IndexError as exception:
            self._dict_result.update({"obs":str(exception)})
        finally:
            self._driver.quit()
            
            self.update_global_result_memory(flask_username, 'checkACSSettings_411', json_saida411)
            return self._dict_result


    def validarDefaultUserACS_412(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result)==0:
            self._dict_result.update({"obs": 'Execute o teste 411 primeiro'})
        else:
            value = result['tr69_connection_request'].get('tr69_connection_request_Username')
            if value == 'acsclient':
                self._dict_result.update({"obs": "Username esta correto", "result":'passed'})
            else:
                self._dict_result.update({"obs": f"Username incorreto, retorno: {value}", "result":'failed'})
        return self._dict_result


    def validarDefaultPasswordACS_413(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result)==0:
            self._dict_result.update({"obs": 'Execute o teste 411 primeiro', "result":'failed'})
        else:
            value = result['tr69_setting'].get('tr69_acsPassword')
            if value == 'telefonica':
                self._dict_result.update({"obs": "Password esta correta", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Password incorreta, retorno: {value}"})
        return self._dict_result


    def GPV_OneObjct_414(self, dados):
        #TODO: This function needs refactoring, zeep library not working, test crashing
        
        dados_entrada = dados
        #print(dados_entrada)
        
        #CheckDA
        gpv_cda = utils.ACS.checkDeviceAvailability(**dados_entrada)
        #print(gpv_cda)

        #Set
        #gpv_apv = utils.ACS.setParameterValues(**dados_entrada)
        #print(gpv_apv)

        #GET
        # gpv_get = utils.ACS.getParameterValues(**dados_entrada)
        # #print(gpv_get)
        # self._dict_result.update(gpv_get)
        # return self._dict_result

        # #Reboot
        # gpv_rbt = utils.ACS.reboot(**dados_entrada)
        # print(gpv_rbt)

        #SetVoIP
        # gpv_avip = utils.ACS.setVoIP(**dados_entrada)
        # print(gpv_avip)



        


    def periodicInformEnable_415(self, flask_username):
         #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result)==0:
            self._dict_result.update({"obs": 'Execute o teste 411 primeiro'})
        else:
            value = result['tr69_setting'].get('tr69_acsPII')
            if value == '1':
                self._dict_result.update({"obs": "Periodic Infom esta habilitado", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": "Periodic Infom esta desabilitado", "result":'failed'})
        return self._dict_result
 
 
    def periodicInformInterval_416(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result)==0:
            self._dict_result.update({"obs": 'Execute o teste 411 primeiro', "result":'failed'})
        else:
            value = result['tr69_setting'].get('tr69_acsPII_interval')
            if value == '68400':
                self._dict_result.update({"obs": "Periodic Inform Interval OK", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Periodic Inform Interval esta incorreto, retorno: {value}"})
        return self._dict_result


    def connectionRequestPort_417(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
        d = self.GPV_OneObjct_414(serialnumber, GPV_Param, IPACS, acsUsername, acsPassword)
        
        gpv_probe = self._dict_result['Resultado_Probe']
    
        if gpv_probe == 'OK':
            gpv_result = self._dict_result['Resultado']
            for key in gpv_result:
                port_cr_value = key.get('value').strip('/').split(':')[2]
                if port_cr_value == '7547':
                    self._dict_result.update({"obs": None, "result":'passed', "Resultado_Probe": "OK"})
                    return self._dict_result
            self._dict_result.update({"obs": "port_cr_value != '7547'", "result":'failed'})
            return self._dict_result
        elif gpv_probe == 'NOK':
            self._dict_result.update({"obs": "Teste 414 GPV_OneObjct Falhou!", "result":'failed'})
            return self._dict_result


    def enableCwmp_418(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result)==0:
            self._dict_result.update({"obs": 'Execute o teste 411 primeiro', "result":'failed'})
        else:
            value = result['tr69_setting'].get('tr69_cwmp')
            if value == 'Habilitado':
                self._dict_result.update({"obs": "CWMP esta habilitado", "result":'passed', "Resultado_Probe": "OK" })
            else:
                self._dict_result.update({"obs": "CWMP esta desabilitado"})
        return self._dict_result


    def userConnectionRequest_419(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        #TODO: Verificar se o teste 419 é igual ao teste 412
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result)==0:
            self._dict_result.update({"obs": 'Execute o teste 411 primeiro', "result":'failed'})
        else:
            value = result['tr69_connection_request'].get('tr69_connection_request_Username')
            if value == 'userid':
                self._dict_result.update({"obs": "Connection Request Username OK", "result":'passed', "Resultado_Probe": "OK" })
            else:
                self._dict_result.update({"obs": f"Connection Request Username incorreta, retorno: {value}"})
        return self._dict_result


    def checkWanInterface_420(self, flask_username):

        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menuFrm')
            wanInterface = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            time.sleep(1)
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('mainFrm')

            header_list = [header.text for header in self._driver.find_elements_by_xpath('//*[@id="WanIPIntfList"]/table/thead/tr/th')]
            number_cols = len(header_list)

            table_flat = self._driver.find_elements_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr/td')

            table = chunks(table_flat, number_cols)

            dict_saida420 = {}
            for i, row in enumerate(table):
                # d = {col:row[j].text for (j,col) in enumerate(header_list[3:-1], start=3)}
                d = {col:row[j].text for (j,col) in enumerate(header_list)}
                dict_saida420.update({f'index_{i}':d})
                
            self._driver.quit()

            for k, item in dict_saida420.items():
                cpe_config = config_collection.find_one()
                if item['Type'] == 'PPPoE' and item['VLAN'] == '10' and cpe_config['REDE'] == 'VIVO_1': 
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Type: PPPoE | VLAN: 10", "result":"passed"})
                    break
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: Type:{item['Type']}, VLAN:{item['VLAN']}, REDE:{cpe_config['REDE']}"})

        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self._dict_result.update({'dict_saida': dict_saida420})
            self.update_global_result_memory(flask_username, 'checkWanInterface_420', dict_saida420)
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
                    if sub_dict.get('Priority') == '0':
                        self._dict_result.update({"obs": 'Type: PPPoE | Priority: 0', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno: Type:{iface_type}, Priority:{sub_dict.get('Priority')}"})
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
                iface_type = sub_dict.get('VLAN')
                cpe_config = config_collection.find_one()
                if iface_type == '10' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    if sub_dict.get('Type') == 'PPPoE':
                        self._dict_result.update({"obs": 'VLAN: 10 | Type:PPPoE, teste OK', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno: VLAN:{iface_type}, TYPE:{sub_dict.get('Type')}"})
                        break
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: VLAN:{iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result



    def checkNatSettings_423(self, flask_username):

        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menuFrm')
            wanInterface = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[1]').click()
            time.sleep(1)
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('mainFrm')

            header_list = [header.text for header in self._driver.find_elements_by_xpath('//*[@id="NATTable"]/table/thead/tr/th')]
            number_cols = len(header_list)
            table_flat = self._driver.find_elements_by_xpath('//*[@id="NATTable"]/table/tbody/tr/td')
            checkbox_inputs = self._driver.find_elements_by_xpath('//*[@id="NATTable"]/table/tbody/tr/td/input')

            table = chunks(table_flat, number_cols)
            dict_saida423 = {}

            for i, row in enumerate(table):
                d = {col: (('Habilitado' if checkbox_inputs[i].get_attribute('checked') == 'true' else 'Desabilitado') if j==1 else
                                                                                            row[j].text.split('\n')[0] if j==2 else
                                                                                            row[j].text)
                    for (j,col) in enumerate(header_list[:-1])}
                dict_saida423.update({f'index_{i}':d})



            
            for i, row in dict_saida423.items():
                cpe_config = config_collection.find_one()
                if row['Interface'] == 'ip2' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    if row['Adm.State'] == 'Habilitado':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: Ip2 | Adm.State: Habilitado", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": "Interface: Ip2 | Adm.State: desabilitado"})
                        break
                else:
                    self._dict_result.update({"obs": f"Interface Ip2 nao existe, , ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
            self._driver.quit()

        except Exception as exception:
            dict_saida423 = {}
            self._dict_result.update({"obs": exception})
        finally:
            
            self.update_global_result_memory(flask_username, 'checkNatSettings_423', dict_saida423)
            return self._dict_result


    def checkMulticastSettings_424(self, flask_username):

        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.frame('menuFrm')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[5]/a[1]').click()
            time.sleep(1)
            self._driver.switch_to.parent_frame()
            self._driver.switch_to.frame('mainFrm')

            header_list = [header.text for header in self._driver.find_elements_by_xpath('//*[@id="MulticastTable"]/table/thead/tr/th')]
            number_cols = len(header_list)
            table_flat = self._driver.find_elements_by_xpath('//*[@id="MulticastTable"]/table/tbody/tr/td')
            checkbox_inputs = self._driver.find_elements_by_xpath('//*[@id="MulticastTable"]/table/tbody/tr/td/input')
            table = chunks(table_flat, number_cols)
            dict_saida424 = {}
            for i, row in enumerate(table):
                d = {col: (('Habilitado' if checkbox_inputs[i].get_attribute('checked') == 'true' else 'Desabilitado') if j==1 else
                                                                                            row[j].text.split('\n')[0] if j==2 else
                                                                                            row[j].text)
                    for (j,col) in enumerate(header_list[:-1])}
                dict_saida424.update({f'index_{i}':d})

            self._driver.quit()
            for _, row in dict_saida424.items():
                if row['Interface'] == 'ip2':
                    if row['IGMP'] == 'Desabilitado':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: ip2 | IGMP: Desabilitado", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": "Interface: ip2 | IGMP: Habilitado"})
                        break
                else:
                    self._dict_result.update({"obs": "Interface Ip2 nao existe"})

        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self.update_global_result_memory(flask_username, 'checkMulticastSettings_424', dict_saida424)
            return self._dict_result



    def getFullConfig_425(self, flask_username):

            self._driver.get('http://' + self._address_ip + '/')
            link = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
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
            time.sleep(1)
            print('\n#############################################'
                  '\n MENU >> STATUS'
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         STATUS
            ### ------------------------------------------ ###
            status = self._driver.find_element_by_link_text('Status')
            print(status.text)
            status.click()
            time.sleep(1)
            print('\n#############################################'
                  '\n MENU >> STATUS >> GPON'
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         STATUS > GPON
            ### ------------------------------------------ ###
            gpon = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
            print('linha #445   ' + gpon)
            divOptical = self._driver.find_element_by_id('divOptical').text
            divOptical = divOptical.split("\n")
            print(divOptical)
            divOptRx = self._driver.find_element_by_id('divOptRx').text
            divOptRx = divOptRx.split("\n")
            print(divOptRx)
            divOptTx = self._driver.find_element_by_id('divOptTx').text
            divOptTx = divOptTx.split("\n")
            print(divOptTx)
            print('\n#############################################'
                  '\n MENU >> STATUS >> INTERNET'
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         STATUS > INTERNET
            ### ------------------------------------------ ###
            internet = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[3]/th/span').text
            print(internet)
            divPpp = self._driver.find_element_by_id('divPpp').text
            divPpp = divPpp.split("\n")
            print(divPpp)
            detalhes_internet = self._driver.find_element_by_link_text('Detalhes')
            print(detalhes_internet.text)
            detalhes_internet.click()
            detalhes_IPv4_head = self._driver.find_element_by_link_text('IPv4').text
            print(detalhes_IPv4_head)
            detalhes_IPv4 = self._driver.find_element_by_id('tabip-02')
            detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[1]')
            time.sleep(1)
            items_key_internet_ipv4 = detalhes_IPv4.find_elements_by_tag_name("li")
            detalhes_IPv4_nome = []
            for i in items_key_internet_ipv4:
                teste = i.text
                #print(i.text)
                detalhes_IPv4_nome.append(teste)
            print(detalhes_IPv4_nome)
            detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[2]')
            items_key = detalhes_IPv4.find_elements_by_tag_name("li")
            detalhes_IPv4_valor = []
            for i in items_key:
                teste = i.text
                #print(i.text)
                detalhes_IPv4_valor.append(teste)
            print(detalhes_IPv4_valor)
            time.sleep(2)
            detalhes_IPv6 = self._driver.find_element_by_link_text('IPv6')
            detalhes_IPv6.click()
            time.sleep(1)
            detalhes_IPv6_head = self._driver.find_element_by_link_text('IPv6').text
            print(detalhes_IPv6_head)
            detalhes_IPv6 = self._driver.find_element_by_id('tabip-02')
            detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[1]')
            time.sleep(1)
            items_key = detalhes_IPv6.find_elements_by_tag_name("li")
            detalhes_IPv6_nome = []
            for item in items_key:
                teste = item.text
                #print(item.text)
                detalhes_IPv6_nome.append(teste)
            print(detalhes_IPv6_nome)
            detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[2]')
            items_key = detalhes_IPv6.find_elements_by_tag_name("li")
            detalhes_IPv6_valor = []
            for item in items_key:
                teste = item.text
                # print(item.text)
                detalhes_IPv6_valor.append(teste)
            print(detalhes_IPv6_valor)
            time.sleep(2)
            print('\n#############################################'
                  '\n MENU >> STATUS >> WIFI 2.4GHz'
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         STATUS > WIFI 2.4GHz
            ### ------------------------------------------ ###
            wifi_24 = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[5]/th/span').text
            print(wifi_24)
            wifi_24_name = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[1]/div').text
            wifi_24_name = wifi_24_name.replace('\n',' ').split(' ')
            print(wifi_24_name)
            wifi_24_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/a')
            wifi_24_detalhes.click()
            wifi_24_detalhes_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[1]/div')
            items_key = wifi_24_detalhes_info.find_elements_by_tag_name("li")
            wifi_24_valor = []
            for item in items_key:
                teste = item.text
                # print(item.text)
                wifi_24_valor.append(teste)
            print(wifi_24_valor)
            wifi_24_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[2]/textarea').get_attribute('value')
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
            wifi_5_detalhes_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[1]/div')
            items_key = wifi_5_detalhes_info.find_elements_by_tag_name("li")
            wifi_5_valor = []
            for item in items_key:
                teste = item.text
                # print(item.text)
                wifi_5_valor.append(teste)
            print(wifi_5_valor)
            wifi_5_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[2]/textarea').get_attribute('value')
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

            # print('lista de entrada = ' + str(rede_local_name))
            # print('tamanho = '+ str(len(rede_local_name))+'\n')
            # a = 0
            # for i in rede_local_name:
            #     print('index = '+ str(a) +'  '+ str(i))
            #     if len(rede_local_name) < 8:
            #         rede_local_name[0] = i
            #     a = a+ 1
            # print(rede_local_name)
            rede_local_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[9]/td[2]/a')
            rede_local_detalhes.click()
            rede_local_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[10]/td[2]/textarea').get_attribute('value')
            rede_local_stations = rede_local_stations.split('\n')
            # print(rede_local_stations)
            time.sleep(2)
            print('\n#############################################'
                  '\n MENU >> STATUS >> TV'
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         STATUS > TV
            ### ------------------------------------------ ###
            tv = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/th/span').text
            print(tv)
            tv_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/td[2]/a').click()
            tv_info = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[12]/td[1]/div')
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
            telefone_detalhes = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[11]/td[2]/a').click()
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
            config = self._driver.find_element_by_link_text('Configurações').click()
            time.sleep(1)
            config_internet = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[1]/a')
            config_internet.click()
            config_internet = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[1]/a').text
            print(config_internet)
            config_internet_usuario = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]').text
            print(config_internet_usuario)
            config_internet_usuario_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input').get_property('value')
            print(config_internet_usuario_valor)
            config_internet_senha = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[1]').text
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
            connfig_redelocal = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').text
            print(config_redelocal)
            config_redelocal_dhcp = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/thead/tr/th').text
            print(config_redelocal_dhcp)
            config_redelocal_servidordhcp = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[2]/td[1]').text
            print(config_redelocal_servidordhcp)
            config_redelocal_servidordhcp_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
            if config_redelocal_servidordhcp_valor == 'true':
                config_redelocal_servidordhcp_valor = 'Habilitado'
            else:
                config_redelocal_servidordhcp_valor = 'Desabilitado'
            print(config_redelocal_servidordhcp_valor)
            config_redelocal_iphgu = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[1]').text
            print(config_redelocal_iphgu)
            config_redelocal_iphgu_valor01 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').get_property('value')
            config_redelocal_iphgu_valor02 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').get_property('value')
            config_redelocal_iphgu_valor03 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').get_property('value')
            config_redelocal_iphgu_valor04 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[4]').get_property('value')
            config_redelocal_iphgu_valor = config_redelocal_iphgu_valor01 + '.' + config_redelocal_iphgu_valor02 + '.' + config_redelocal_iphgu_valor03 + '.' + config_redelocal_iphgu_valor04
            print(config_redelocal_iphgu_valor)

            config_redelocal_mask = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[1]').text
            print(config_redelocal_mask)
            config_redelocal_mask_valor01 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[1]').get_property('value')
            config_redelocal_mask_valor02 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[2]').get_property('value')
            config_redelocal_mask_valor03 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[3]').get_property('value')
            config_redelocal_mask_valor04 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[4]/td[2]/input[4]').get_property('value')
            config_redelocal_mask_valor = config_redelocal_mask_valor01 + '.' + config_redelocal_mask_valor02 + '.' + config_redelocal_mask_valor03 + '.' + config_redelocal_mask_valor04
            print(config_redelocal_mask_valor)

            config_redelocal_pool = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[1]').text
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

            config_redelocal_dns = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[7]/td[1]').text
            print(config_redelocal_dns)
            config_redelocal_dns_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[7]/td[2]/input[1]').get_attribute('checked')
            if config_redelocal_dns_valor == 'true':
                config_redelocal_dns_valor = 'Habilitado'
            else:
                config_redelocal_dns_valor = 'Desabilitado'
            print(config_redelocal_dns_valor)

            config_redelocal_concessao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[10]/td[1]').text
            print(config_redelocal_concessao)
            config_redelocal_concessao_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[10]/td[2]/input').get_property('value')
            print(config_redelocal_concessao_valor)

            config_redelocal_tabela_concessao = self._driver.find_elements_by_id('tblDhcpLease')
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
            config_wifi24 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a')
            print(config_wifi24.text)
            config_wifi24.click()
            config_wifi24 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').text
            config_wifi24_basico = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[1]/a').text
            print(config_wifi24_basico)
            config_wifi24_basico_redeprivada = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[1]').text
            print(config_wifi24_basico_redeprivada)
            config_wifi24_basico_redeprivada_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').get_attribute('checked')
            
            if config_wifi24_basico_redeprivada_valor == 'true':
                config_wifi24_basico_redeprivada_valor = 'Habilitado' 
                config_original_wifi24 = 0
            else:
                config_wifi24_basico_redeprivada_valor = 'Desabilitado'
                # Habilita o wi-fi para coletar as informacoes, o wifi voltara para configuracao original apos a coleta dos dados:
                config_wifi24_basico_habilitar = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]')
                config_wifi24_basico_habilitar.click()
                time.sleep(1)
                config_original_wifi24 = 1
            print(config_wifi24_basico_redeprivada_valor)
            
            config_wifi24_basico_anuncio = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[1]').text
            print(config_wifi24_basico_anuncio)
            config_wifi24_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
            if config_wifi24_basico_anuncio_valor == 'true':
                config_wifi24_basico_anuncio_valor = 'Habilitado'
            else:
                config_wifi24_basico_anuncio_valor = 'Desabilitado'
            print(config_wifi24_basico_anuncio_valor)

            config_wifi24_basico_ssid = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[1]').text
            print(config_wifi24_basico_ssid)
            config_wifi24_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_property('value')
            print(config_wifi24_basico_ssid_valor)

            config_wifi24_basico_ssid_senha = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[1]').text
            print(config_wifi24_basico_ssid_senha)
            config_wifi24_basico_ssid_senha_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_property('value')
            print(config_wifi24_basico_ssid_senha_valor)
            config_wifi24_basico_seguranca = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[1]').text
            print(config_wifi24_basico_seguranca)
            config_wifi24_basico_seguranca_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[2]/select').get_property('value')
            if config_wifi24_basico_seguranca_valor == '34':
                config_wifi24_basico_seguranca_valor = 'WPA2'
            elif config_wifi24_basico_seguranca_valor == '44':
                config_wifi24_basico_seguranca_valor = 'WPA / WPA2'
            elif config_wifi24_basico_seguranca_valor == '02':
                config_wifi24_basico_seguranca_valor = 'WEP'
            elif config_wifi24_basico_seguranca_valor == '00':
                config_wifi24_basico_seguranca_valor = 'Nenhum'
            print(config_wifi24_basico_seguranca_valor)

            config_wifi24_basico_wps = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[1]').text
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
            config_wifi24_avancado = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a').text
            print(config_wifi24_avancado)
    
            config_wifi24_avancado_modooperacao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[1]').text
            print(config_wifi24_avancado_modooperacao)
            config_wifi24_avancado_modooperacao_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[2]/select').get_property('value')
            if config_wifi24_avancado_modooperacao_valor == '12':
                config_wifi24_avancado_modooperacao_valor = '802.11g/n'
            elif config_wifi24_avancado_modooperacao_valor == '2':
                config_wifi24_avancado_modooperacao_valor = '802.11b'
            elif config_wifi24_avancado_modooperacao_valor == '4':
                config_wifi24_avancado_modooperacao_valor = '802.11g'
            elif config_wifi24_avancado_modooperacao_valor == '6':
                config_wifi24_avancado_modooperacao_valor = '802.11b/g'
            elif config_wifi24_avancado_modooperacao_valor == '8':
                config_wifi24_avancado_modooperacao_valor = '802.11n'
            elif config_wifi24_avancado_modooperacao_valor == '14':
                config_wifi24_avancado_modooperacao_valor = '802.11b/g/n'
            print(config_wifi24_avancado_modooperacao_valor)

            config_wifi24_avancado_canal = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[1]').text
            print(config_wifi24_avancado_canal)
            config_wifi24_avancado_canal_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[2]/select').get_property('value')
            print(config_wifi24_avancado_canal_valor)

            #config_wifi24_avancado_largurabanda = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[1]').text
            config_wifi24_avancado_largurabanda = 'Largura de Banda do Canal:'
            print(config_wifi24_avancado_largurabanda)
            config_wifi24_avancado_largurabanda_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[2]/select').get_property('value')
            print(config_wifi24_avancado_largurabanda_valor)
            if config_wifi24_avancado_largurabanda_valor == '1':
                config_wifi24_avancado_largurabanda_valor = '20 MHz'
            elif config_wifi24_avancado_largurabanda_valor == '2':
                config_wifi24_avancado_largurabanda_valor = '40 MHz'
            elif config_wifi24_avancado_largurabanda_valor == '0':
                config_wifi24_avancado_largurabanda_valor = 'Automático'
            print(config_wifi24_avancado_largurabanda_valor)

            config_wifi24_avancado_wmm = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[5]/td[1]').text
            print(config_wifi24_avancado_wmm)
            config_wifi24_avancado_wmm_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[5]/td[2]/input[1]').get_attribute('checked')
            if config_wifi24_avancado_wmm_valor == 'true' :
                config_wifi24_avancado_wmm_valor = 'Habilitado' 
            else:
                config_wifi24_avancado_wmm_valor = 'Desabilitado'
            print(config_wifi24_avancado_wmm_valor)


            config_wifi24_avancado_mac = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[7]/td[1]').text
            print(config_wifi24_avancado_mac)
            config_wifi24_avancado_mac_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[7]/td[2]').text
            print(config_wifi24_avancado_mac_valor)
        
            if config_original_wifi24 == 1:
                config_wifi24_voltar = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[1]/a')
                config_wifi24_voltar.click()
                time.sleep(1)
                config_wifi24_basico_desabilitar = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[2]')
                config_wifi24_basico_desabilitar.click()
                config_original_wifi24 = 0

            time.sleep(1)
            print('\n#############################################'
                  '\n MENU >> CONFIGURAÇÕES >> WIFI 5GHz '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         CONFIGURAÇÕES > WIFI 5GHz
            ### ------------------------------------------ ###
            config_wifi5 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a')
            print(config_wifi5.text)
            config_wifi5.click()
            config_wifi5 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').text
            time.sleep(2)
            config_wifi5_basico = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[1]/a').text
            print(config_wifi5_basico)
            config_wifi5_basico_redeprivada = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[1]').text
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


            config_wifi5_basico_anuncio = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[1]').text
            print(config_wifi5_basico_anuncio)
            config_wifi5_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
            if config_wifi5_basico_anuncio_valor == 'true':
                config_wifi5_basico_anuncio_valor = 'Habilitado'
            else:
                config_wifi5_basico_anuncio_valor = 'Desabilitado'

            print(config_wifi5_basico_anuncio_valor)

            config_wifi5_basico_ssid = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[1]').text
            print(config_wifi5_basico_ssid)
            config_wifi5_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input').get_property('value')
            print(config_wifi5_basico_ssid_valor)

            config_wifi5_basico_ssid_senha = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[1]').text
            print(config_wifi5_basico_ssid_senha)
            config_wifi5_basico_ssid_senha_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input').get_property('value')
            print(config_wifi5_basico_ssid_senha_valor)
            config_wifi5_basico_seguranca = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[1]').text
            print(config_wifi5_basico_seguranca)
            config_wifi5_basico_seguranca_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[5]/td[2]/select').get_property('value')
            if config_wifi5_basico_seguranca_valor == '34':
                config_wifi5_basico_seguranca_valor = 'WPA2'
            elif config_wifi5_basico_seguranca_valor == '44':
                config_wifi5_basico_seguranca_valor = 'WPA / WPA2'
            elif config_wifi5_basico_seguranca_valor == '02':
                config_wifi5_basico_seguranca_valor = 'WEP'
            elif config_wifi5_basico_seguranca_valor == '00':
                config_wifi5_basico_seguranca_valor = 'Nenhum'
            print(config_wifi5_basico_seguranca_valor)

            config_wifi5_basico_wps = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[1]').text
            print(config_wifi5_basico_wps)
            config_wifi5_basico_wps_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[2]/input[1]').get_attribute('checked')
            if config_wifi5_basico_wps_valor == 'true':
                config_wifi5_basico_wps_valor = 'Habilitado'
            else:
                config_wifi5_basico_wps_valor = 'Desabilitado'
            print(config_wifi5_basico_wps_valor)

            config_wifi5_avancado = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a')
            config_wifi5_avancado.click()
            time.sleep(1)
            config_wifi5_avancado = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[2]/a').text
            print(config_wifi5_avancado)
    
            config_wifi5_avancado_modooperacao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[1]').text
            print(config_wifi5_avancado_modooperacao)
            config_wifi5_avancado_modooperacao_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[1]/td[2]/select').get_property('value')
            if config_wifi5_avancado_modooperacao_valor == '25':
                config_wifi5_avancado_modooperacao_valor = '802.11n/ac'
            print(config_wifi5_avancado_modooperacao_valor)

            config_wifi5_avancado_canal = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[1]').text
            print(config_wifi5_avancado_canal)
            config_wifi5_avancado_canal_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[2]/td[2]/select').get_property('value')
            print(config_wifi5_avancado_canal_valor)

            #config_wifi5_avancado_largurabanda = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[1]').text
            config_wifi5_avancado_largurabanda = 'Largura de Banda do Canal:' #selenium nao pega informacoes de texto de elementos ocultos
            print(config_wifi5_avancado_largurabanda)
            config_wifi5_avancado_largurabanda_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[3]/td[2]/select').get_property('value')
            if config_wifi5_avancado_largurabanda_valor == '1':
                config_wifi5_avancado_largurabanda_valor = '20 MHz'
            elif config_wifi5_avancado_largurabanda_valor == '2':
                config_wifi5_avancado_largurabanda_valor = '40 MHz'
            elif config_wifi5_avancado_largurabanda_valor == '0':
                config_wifi5_avancado_largurabanda_valor = 'Automático'
            elif config_wifi5_avancado_largurabanda_valor == '3':
                config_wifi5_avancado_largurabanda_valor = '80 Mhz'
            print(config_wifi5_avancado_largurabanda_valor)

            config_wifi5_avancado_wmm = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[5]/td[1]').text
            print(config_wifi5_avancado_wmm)
            config_wifi5_avancado_wmm_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[5]/td[2]/input[1]').get_attribute('checked')
            if config_wifi5_avancado_wmm_valor == 'true' :
                config_wifi5_avancado_wmm_valor = 'Habilitado' 
            else:
                config_wifi5_avancado_wmm_valor = 'Desabilitado'
            print(config_wifi5_avancado_wmm_valor)

            config_wifi5_avancado_mac = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[7]/td[1]').text
            print(config_wifi5_avancado_mac)
            config_wifi5_avancado_mac_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[4]/form/table/tbody/tr[7]/td[2]').text
            print(config_wifi5_avancado_mac_valor)

            if config_original_wifi5 == 1:
                config_wifi5_voltar = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/ul/li[1]/a')
                config_wifi5_voltar.click()
                time.sleep(1)
                config_wifi5_basico_desabilitar = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[2]')
                config_wifi5_basico_desabilitar.click()
                config_original_wifi5 = 0
            
            time.sleep(1)
            print('\n#############################################'
                  '\n MENU >> CONFIGURAÇÕES >> FIREWALL '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         CONFIGURAÇÕES > FIREWALL
            ### ------------------------------------------ ###
            config_firewall = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[6]/a')
            print(config_firewall.text)
            config_firewall.click()
            config_firewall = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[6]/a').text
            time.sleep(3)
            config_firewall_politicapadrao = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/thead[1]/tr/th').text
            print(config_firewall_politicapadrao)
            config_firewall_politicapadrao_status = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[1]/tr/td[1]').text
            print(config_firewall_politicapadrao_status)
            config_firewall_politicapadrao_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[1]/tr/td[2]/input[1]').get_attribute('checked')
            if config_firewall_politicapadrao_valor == 'true':
                config_firewall_politicapadrao_valor = 'Habilitado'
            else:
                config_firewall_politicapadrao_valor = 'Desabilitado'
            print(config_firewall_politicapadrao_valor)

            config_firewall_pingwan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/thead[2]/tr/th').text
            print(config_firewall_pingwan)
            config_firewall_pingwan_status = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[2]/tr/td[1]').text
            print(config_firewall_pingwan_status)
            config_firewall_pingwan_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[2]/tbody[2]/tr/td[2]/input[1]').get_attribute('checked')
            if config_firewall_pingwan_valor == 'true':
                config_firewall_pingwan_valor = 'Habilitado'
            else:
                config_firewall_pingwan_valor = 'Desabilitado'
            print(config_firewall_pingwan_valor)



            time.sleep(1)
            print('\n#############################################'
                  '\n MENU >> CONFIGURAÇÕES >> MODO DA WAN '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         CONFIGURAÇÕES > MODO DA WAN
            ### ------------------------------------------ ###
            config_modowan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[7]/a')
            print(config_modowan.text)
            config_modowan.click()
            config_modowan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[7]/a').text
            time.sleep(1)
            config_modowan_bridge = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/thead/tr/th').text
            print(config_modowan_bridge)

            config_modowan_bridge_modo = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[1]').text
            print(config_modowan_bridge_modo)
            config_modowan_bridge_modo_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[2]/select').get_property('value')
            if config_modowan_bridge_modo_valor == '1':
                config_modowan_bridge_modo_valor = 'Roteador (Padrão)'
            elif config_modowan_bridge_modo_valor == '0':
                config_modowan_bridge_modo_valor = 'Bridge'
            print(config_modowan_bridge_modo_valor)

            time.sleep(1)
            print('\n#############################################'
                  '\n MENU >> GERENCIAMENTO >> IDIOMA '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         CONFIGURAÇÕES > IDIOMA
            ### ------------------------------------------ ###
            gerenciamento = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a')
            print(gerenciamento.text)
            gerenciamento.click()
            gerenciamento = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a').text
            time.sleep(2)
            gerenciamento_idioma = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[1]/a')
            print(gerenciamento_idioma.text)
            gerenciamento_idioma.click()
            gerenciamento_idioma = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/ul/li[1]/a').text
            time.sleep(2)
            gerenciamento_idioma = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/thead/tr/th').text
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
            sobre = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[4]/a')
            print(sobre.text)
            sobre.click()
            time.sleep(2)
            sobre = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[4]/a').text
            info_dispositivo = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/thead/tr/th').text
            print(info_dispositivo)
            info_dispositivo_fabricante = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[1]/strong').text
            print(info_dispositivo_fabricante)
            info_dispositivo_fabricante_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]').text
            print(info_dispositivo_fabricante_valor)

            info_dispositivo_firmware = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[1]/strong').text
            print(info_dispositivo_firmware)
            info_dispositivo_firmware_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[2]').text
            print(info_dispositivo_firmware_valor)

            info_dispositivo_serial = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[1]/strong').text
            print(info_dispositivo_serial)
            info_dispositivo_serial_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]').text
            print(info_dispositivo_serial_valor)

            info_dispositivo_fabricante = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[1]/strong').text
            print(info_dispositivo_fabricante)
            info_dispositivo_fabricante_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]').text
            print(info_dispositivo_fabricante_valor)

            info_dispositivo_macwan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[1]/strong').text
            print(info_dispositivo_macwan)
            info_dispositivo_macwan_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]').text
            print(info_dispositivo_macwan_valor)

            info_dispositivo_modelo = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[3]/strong').text
            print(info_dispositivo_modelo)
            iinfo_dispositivo_modelo_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[4]').text
            print(iinfo_dispositivo_modelo_valor)

            info_dispositivo_fabricante = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[1]/strong').text
            print(info_dispositivo_fabricante)
            info_dispositivo_fabricante_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]').text
            print(info_dispositivo_fabricante_valor)

            info_dispositivo_hardware = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[3]/strong').text
            print(info_dispositivo_hardware)
            info_dispositivo_hardware_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[4]').text
            print(info_dispositivo_hardware_valor)

            info_dispositivo_serialgpon = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[3]/strong').text
            print(info_dispositivo_serialgpon)
            info_dispositivo_serialgpon_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[4]').text
            print(info_dispositivo_serialgpon_valor)

            info_dispositivo_maclan = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[3]/strong').text
            print(info_dispositivo_maclan)
            info_dispositivo_maclan_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[4]').text
            print(info_dispositivo_maclan_valor)




            print('\n\n\n == Criando JSON de saída... == ')
            json_saida425 = {
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
                                        rede_local_name[4]: rede_local_name[5], ### NECESSARIO REVISAR CODIGO
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
            print(json_saida425)
            user = json_saida425['Configurações']['Internet'].get('Usuário:')
            if user == 'cliente@cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Usuario: cliente@cliente", "result":"passed"})

            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Usuario: {user}"})

            
            self.update_global_result_memory(flask_username, 'getFullConfig_425', json_saida425)
            return self._dict_result


    def verificarSenhaPppDefaultFibra_426(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')

        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            senha = result['Configurações']['Internet'].get('Senha:')
            if senha == 'cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'senha:cliente', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno senha: {senha}'})
            
        return self._dict_result




    def checkWanInterface_x_427(self, flask_username, interface):
        
        
        usuario = self._username
        senha = self._password
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            user_input = self._driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = self._driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            self._driver.switch_to.frame('menuFrm')
            wanInterface = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wanInterface = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wanInterface)
            time.sleep(1)
            if interface == '1':
                self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
                self._driver.switch_to.frame('mainFrm')
                index = self._driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[' +str(interface)+ ']/td[2]/a').click()
                wanInterface_AdminState = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/label').text
                print(wanInterface_AdminState)
                wanInterface_AdminState_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/input[1]').get_attribute('checked')
                if wanInterface_AdminState_valor == 'true':
                    wanInterface_AdminState_valor = 'Habilitado'
                else:
                    wanInterface_AdminState_valor = 'Desabilitado'
                print(wanInterface_AdminState_valor)

                wanInterface_VLANPrior = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/legend').text
                print(wanInterface_VLANPrior)
                wanInterface_VLANPrior_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[1]/input[1]').get_attribute('checked')
                if wanInterface_VLANPrior_valor == 'true':
                    wanInterface_VLANPrior_valor = 'Tagged'
                else:
                    wanInterface_VLANPrior_valor = 'UnTagged'
                print(wanInterface_VLANPrior_valor)
                wanInterface_VLANPrior_VLANID = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/label').text
                print(wanInterface_VLANPrior_VLANID)
                wanInterface_VLANPrior_VLANID_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').get_attribute('value')
                print(wanInterface_VLANPrior_VLANID_valor)
                wanInterface_VLANPrior_priority = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[3]/label').text
                print(wanInterface_VLANPrior_priority)
                wanInterface_VLANPrior_priority_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[3]/select').get_attribute('value')
                print(wanInterface_VLANPrior_priority_valor)

                wanInterface_Addressing = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/legend').text
                print(wanInterface_Addressing)
                wanInterface_Addressing_type = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/label').text
                print(wanInterface_Addressing_type)
                if self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[1]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'PPPoE'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[2]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'DHCP'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[3]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'Estático'
                print(wanInterface_Addressing_type_valor)
                wanInterface_Addressing_PPPoE = self._driver.find_element_by_xpath('//*[@id="pppoe"]/legend').text
                print(wanInterface_Addressing_PPPoE)
                wanInterface_Addressing_PPPoE_user = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[1]/label').text
                print(wanInterface_Addressing_PPPoE_user)
                wanInterface_Addressing_PPPoE_user_valor = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[1]/input').get_attribute('value')
                print(wanInterface_Addressing_PPPoE_user_valor)
                wanInterface_Addressing_PPPoE_passwd = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[2]/label').text
                print(wanInterface_Addressing_PPPoE_passwd)
                wanInterface_Addressing_PPPoE_passwd_valor = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[2]/input').get_attribute('value')
                print(wanInterface_Addressing_PPPoE_passwd_valor)
                wanInterface_Addressing_PPPoE_ServiceName = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[3]/label').text
                print(wanInterface_Addressing_PPPoE_ServiceName)
                wanInterface_Addressing_PPPoE_ServiceName_valor = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[3]/input').get_attribute('value')
                print(wanInterface_Addressing_PPPoE_ServiceName_valor)
                wanInterface_Addressing_PPPoE_ACName = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[4]/label').text
                print(wanInterface_Addressing_PPPoE_ACName)
                wanInterface_Addressing_PPPoE_ACName_valor = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[4]/input').get_attribute('value')
                print(wanInterface_Addressing_PPPoE_ACName_valor)
                wanInterface_Addressing_PPPoE_IdlTimeout = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[6]/label').text
                print(wanInterface_Addressing_PPPoE_IdlTimeout)
                wanInterface_Addressing_PPPoE_IdlTimeout_valor = self._driver.find_element_by_xpath('//*[@id="pppoe"]/div[6]/input').get_attribute('value')
                print(wanInterface_Addressing_PPPoE_IdlTimeout_valor)

                wanInterface_Addressing_DNS = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/legend').text
                print(wanInterface_Addressing_DNS)
                wanInterface_Addressing_DNS_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[1]/input').get_attribute('checked')
                if wanInterface_Addressing_DNS_valor == 'true':
                    wanInterface_Addressing_DNS_valor = 'DNS Override'
                print(wanInterface_Addressing_DNS_valor)
                wanInterface_Addressing_DNS_Primary = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/label').text
                print(wanInterface_Addressing_DNS_Primary)
                wanInterface_Addressing_DNS_Primary_valor = (self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[1]').get_attribute('value') +
                '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[2]').get_attribute('value') +
                '.' +self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[3]').get_attribute('value') +
                '.' +self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[4]').get_attribute('value') )
                print(wanInterface_Addressing_DNS_Primary_valor)
                wanInterface_Addressing_DNS_Secondary = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/label').text
                print(wanInterface_Addressing_DNS_Secondary)
                wanInterface_Addressing_DNS_Secondary_valor = (self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[1]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[2]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[3]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[4]').get_attribute('value'))
                print(wanInterface_Addressing_DNS_Secondary_valor)

                wanInterface_Addressing_IPv6 = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/legend').text
                print(wanInterface_Addressing_IPv6)
                wanInterface_Addressing_IPv6_AdmState = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/label').text
                print(wanInterface_Addressing_IPv6_AdmState)
                if self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[1]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Dual Stack'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[2]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Somente IPv6'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[3]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Desabilitado'
                print(wanInterface_Addressing_IPv6_AdmState_valor)
                wanInterface_Addressing_IPv6_Unnumbered = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[2]/label').text
                print(wanInterface_Addressing_IPv6_Unnumbered)
                wanInterface_Addressing_IPv6_Unnumbered_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[2]/input[1]').get_attribute('checked')
                if wanInterface_Addressing_IPv6_Unnumbered_valor == 'true':
                    wanInterface_Addressing_IPv6_Unnumbered_valor = 'Habilitado'
                else:
                    wanInterface_Addressing_IPv6_Unnumbered_valor = 'Desabilitado'
                print(wanInterface_Addressing_IPv6_Unnumbered_valor)
                wanInterface_Addressing_IPv6_AddrType = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[3]/label').text
                print(wanInterface_Addressing_IPv6_AddrType)
                wanInterface_Addressing_IPv6_AddrType_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[3]/input[1]').get_attribute('checked')
                if wanInterface_Addressing_IPv6_AddrType_valor == 'true':
                    wanInterface_Addressing_IPv6_AddrType_valor = 'SLAAC'
                else:
                    wanInterface_Addressing_IPv6_AddrType_valor = 'DHCP'
                print(wanInterface_Addressing_IPv6_AddrType_valor)
                time.sleep(1)
                interface = int(interface) - 1
                json_saida427 = {
                    "Interface #" + str(interface):
                        {
                            wanInterface_AdminState:wanInterface_AdminState_valor
                        },
                    wanInterface_VLANPrior:
                        {
                            wanInterface_VLANPrior:wanInterface_VLANPrior_valor,
                            wanInterface_VLANPrior_VLANID:wanInterface_VLANPrior_VLANID_valor,
                            wanInterface_VLANPrior_priority:wanInterface_VLANPrior_priority_valor
                        },
                    wanInterface_Addressing:
                        {
                            wanInterface_Addressing_type:wanInterface_Addressing_type_valor,
                            wanInterface_Addressing_PPPoE:
                                {
                                    wanInterface_Addressing_PPPoE_user:wanInterface_Addressing_PPPoE_user_valor,
                                    wanInterface_Addressing_PPPoE_passwd:wanInterface_Addressing_PPPoE_passwd_valor,
                                    wanInterface_Addressing_PPPoE_ServiceName:wanInterface_Addressing_PPPoE_ServiceName_valor,
                                    wanInterface_Addressing_PPPoE_IdlTimeout:wanInterface_Addressing_PPPoE_IdlTimeout_valor
                                }
                        },
                    wanInterface_Addressing_DNS:
                        {
                            wanInterface_Addressing_DNS:wanInterface_Addressing_DNS_valor,
                            wanInterface_Addressing_DNS_Primary:wanInterface_Addressing_DNS_Primary_valor,
                            wanInterface_Addressing_DNS_Secondary:wanInterface_Addressing_DNS_Secondary_valor
                        },
                    wanInterface_Addressing_IPv6:
                        {
                            wanInterface_Addressing_IPv6_AdmState:wanInterface_Addressing_IPv6_AdmState_valor,
                            wanInterface_Addressing_IPv6_Unnumbered:wanInterface_Addressing_IPv6_Unnumbered_valor,
                            wanInterface_Addressing_IPv6_AddrType:wanInterface_Addressing_IPv6_AddrType_valor
                        }
                }
                self._driver.quit()
                if json_saida427['IPv6'].get('Adm.State') == 'Dual Stack':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Adm.State: Dual Stack", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno {json_saida427['IPv6'].get('Adm.State')}"})

                
                self.update_global_result_memory(flask_username, 'checkWanInterface_x_427', json_saida427)
                return self._dict_result


            elif interface == '2':
                self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
                self._driver.switch_to.frame('mainFrm')
                index = self._driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[' + str(interface) + ']/td[2]/a').click()
                wanInterface_AdminState = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/label').text
                print(wanInterface_AdminState)
                wanInterface_AdminState_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/input[1]').get_attribute('checked')
                if wanInterface_AdminState_valor == 'true':
                    wanInterface_AdminState_valor = 'Habilitado'
                else:
                    wanInterface_AdminState_valor = 'Desabilitado'
                print(wanInterface_AdminState_valor)

                wanInterface_VLANPrior = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/legend').text
                print(wanInterface_VLANPrior)
                wanInterface_VLANPrior_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[1]/input[1]').get_attribute('checked')
                if wanInterface_VLANPrior_valor == 'true':
                    wanInterface_VLANPrior_valor = 'Tagged'
                else:
                    wanInterface_VLANPrior_valor = 'UnTagged'
                print(wanInterface_VLANPrior_valor)
                wanInterface_VLANPrior_VLANID = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/label').text
                print(wanInterface_VLANPrior_VLANID)
                wanInterface_VLANPrior_VLANID_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').get_attribute('value')
                print(wanInterface_VLANPrior_VLANID_valor)
                wanInterface_VLANPrior_priority = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[3]/label').text
                print(wanInterface_VLANPrior_priority)
                wanInterface_VLANPrior_priority_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[3]/select').get_attribute('value')
                print(wanInterface_VLANPrior_priority_valor)

                wanInterface_Addressing = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/legend').text
                print(wanInterface_Addressing)
                wanInterface_Addressing_type = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/label').text
                print(wanInterface_Addressing_type)
                if self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[1]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'PPPoE'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[2]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'DHCP'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[3]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'Estático'
                print(wanInterface_Addressing_type_valor)
                wanInterface_Addressing_DHCPSet = self._driver.find_element_by_xpath('//*[@id="ipoe"]/legend').text
                print(wanInterface_Addressing_DHCPSet)
                wanInterface_Addressing_DHCPSet_VendorID = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[1]/label').text
                print(wanInterface_Addressing_DHCPSet_VendorID)
                wanInterface_Addressing_DHCPSet_VendorID_valor = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[1]/input').get_attribute('value')
                print(wanInterface_Addressing_DHCPSet_VendorID_valor)
                wanInterface_Addressing_DHCPSet_Client = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[2]/label').text
                print(wanInterface_Addressing_DHCPSet_Client)
                wanInterface_Addressing_DHCPSet_Client_valor = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[2]/input').get_attribute('value')
                print(wanInterface_Addressing_DHCPSet_Client_valor)
                wanInterface_Addressing_DHCPSet_UserClassID = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[3]/label').text
                print(wanInterface_Addressing_DHCPSet_UserClassID)
                wanInterface_Addressing_DHCPSet_UserClassID_valor = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[3]/input').get_attribute('value')
                print(wanInterface_Addressing_DHCPSet_UserClassID_valor)

                wanInterface_DNS = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/legend').text
                print(wanInterface_DNS)
                wanInterface_Addressing_DNS_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[1]/input').get_attribute('checked')
                if wanInterface_Addressing_DNS_valor == 'true':
                    wanInterface_Addressing_DNS_valor = 'DNS Override'
                print(wanInterface_Addressing_DNS_valor)
                wanInterface_Addressing_DNS_Primary = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/label').text
                print(wanInterface_Addressing_DNS_Primary)
                wanInterface_Addressing_DNS_Primary_valor = (self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[1]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[2]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[3]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[4]').get_attribute('value'))
                print(wanInterface_Addressing_DNS_Primary_valor)
                wanInterface_Addressing_DNS_Secondary = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/label').text
                print(wanInterface_Addressing_DNS_Secondary)
                wanInterface_Addressing_DNS_Secondary_valor = (self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[1]').get_attribute('value') +
                                                               '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[2]').get_attribute('value') +
                                                               '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[3]').get_attribute('value') +
                                                               '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[4]').get_attribute('value'))
                print(wanInterface_Addressing_DNS_Secondary_valor)

                wanInterface_Addressing_IPv6 = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/legend').text
                print(wanInterface_Addressing_IPv6)
                wanInterface_Addressing_IPv6_AdmState = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/label').text
                print(wanInterface_Addressing_IPv6_AdmState)
                if self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[1]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Dual Stack'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[2]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Somente IPv6'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[3]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Desabilitado'
                print(wanInterface_Addressing_IPv6_AdmState_valor)
                wanInterface_Addressing_IPv6_Unnumbered = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[2]/label').text
                print(wanInterface_Addressing_IPv6_Unnumbered)
                wanInterface_Addressing_IPv6_Unnumbered_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[2]/input[1]').get_attribute('checked')
                if wanInterface_Addressing_IPv6_Unnumbered_valor == 'true':
                    wanInterface_Addressing_IPv6_Unnumbered_valor = 'Habilitado'
                else:
                    wanInterface_Addressing_IPv6_Unnumbered_valor = 'Desabilitado'
                print(wanInterface_Addressing_IPv6_Unnumbered_valor)
                wanInterface_Addressing_IPv6_AddrType = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[3]/label').text
                print(wanInterface_Addressing_IPv6_AddrType)
                wanInterface_Addressing_IPv6_AddrType_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[3]/input[1]').get_attribute('checked')
                if wanInterface_Addressing_IPv6_AddrType_valor == 'true':
                    wanInterface_Addressing_IPv6_AddrType_valor = 'SLAAC'
                else:
                    wanInterface_Addressing_IPv6_AddrType_valor = 'DHCP'
                print(wanInterface_Addressing_IPv6_AddrType_valor)

                interface = int(interface) - 1

                json_saida427 = {
                    "Interface #" + str(interface):
                        {
                            wanInterface_AdminState: wanInterface_AdminState_valor
                        },
                    wanInterface_VLANPrior:
                        {
                            wanInterface_VLANPrior: wanInterface_VLANPrior_valor,
                            wanInterface_VLANPrior_VLANID: wanInterface_VLANPrior_VLANID_valor,
                            wanInterface_VLANPrior_priority: wanInterface_VLANPrior_priority_valor
                        },
                    wanInterface_Addressing:
                        {
                            wanInterface_Addressing_type: wanInterface_Addressing_type_valor,
                            wanInterface_Addressing_DHCPSet:
                                {
                                    wanInterface_Addressing_DHCPSet_VendorID: wanInterface_Addressing_DHCPSet_VendorID_valor,
                                    wanInterface_Addressing_DHCPSet_Client: wanInterface_Addressing_DHCPSet_Client_valor,
                                    wanInterface_Addressing_DHCPSet_UserClassID: wanInterface_Addressing_DHCPSet_UserClassID_valor
                                }
                        },
                    wanInterface_DNS:
                        {
                            'DNS Override': wanInterface_Addressing_DNS_valor,
                            wanInterface_Addressing_DNS_Primary: wanInterface_Addressing_DNS_Primary_valor,
                            wanInterface_Addressing_DNS_Secondary: wanInterface_Addressing_DNS_Secondary_valor
                        },
                    wanInterface_Addressing_IPv6:
                        {
                            wanInterface_Addressing_IPv6_AdmState: wanInterface_Addressing_IPv6_AdmState_valor,
                            wanInterface_Addressing_IPv6_Unnumbered: wanInterface_Addressing_IPv6_Unnumbered_valor,
                            wanInterface_Addressing_IPv6_AddrType: wanInterface_Addressing_IPv6_AddrType_valor
                        }
                }
                self._driver.quit()
                self._dict_result.update({"Resultado_Probe": "OK", "obs": json_saida427, "result":"passed"})
                self.update_global_result_memory(flask_username, 'checkWanInterface_x_427', json_saida427)
                return self._dict_result

            elif interface == '3':
                self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
                self._driver.switch_to.frame('mainFrm')
                index = self._driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[' + str(interface) + ']/td[2]/a').click()
                wanInterface_AdminState = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/label').text
                print(wanInterface_AdminState)
                wanInterface_AdminState_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/input[1]').get_attribute('checked')
                if wanInterface_AdminState_valor == 'true':
                    wanInterface_AdminState_valor = 'Habilitado'
                else:
                    wanInterface_AdminState_valor = 'Desabilitado'
                print(wanInterface_AdminState_valor)

                wanInterface_VLANPrior = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/legend').text
                print(wanInterface_VLANPrior)
                wanInterface_VLANPrior_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[1]/input[1]').get_attribute('checked')
                if wanInterface_VLANPrior_valor == 'true':
                    wanInterface_VLANPrior_valor = 'Tagged'
                else:
                    wanInterface_VLANPrior_valor = 'UnTagged'
                print(wanInterface_VLANPrior_valor)
                wanInterface_VLANPrior_VLANID = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/label').text
                print(wanInterface_VLANPrior_VLANID)
                wanInterface_VLANPrior_VLANID_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').get_attribute('value')
                print(wanInterface_VLANPrior_VLANID_valor)
                wanInterface_VLANPrior_priority = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[3]/label').text
                print(wanInterface_VLANPrior_priority)
                wanInterface_VLANPrior_priority_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[3]/select').get_attribute('value')
                print(wanInterface_VLANPrior_priority_valor)

                wanInterface_Addressing = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/legend').text
                print(wanInterface_Addressing)
                wanInterface_Addressing_type = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/label').text
                print(wanInterface_Addressing_type)
                if self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[1]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'PPPoE'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[2]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'DHCP'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[2]/div/input[3]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_type_valor = 'Estático'
                print(wanInterface_Addressing_type_valor)
                wanInterface_Addressing_DHCPSet = self._driver.find_element_by_xpath('//*[@id="ipoe"]/legend').text
                print(wanInterface_Addressing_DHCPSet)
                wanInterface_Addressing_DHCPSet_VendorID = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[1]/label').text
                print(wanInterface_Addressing_DHCPSet_VendorID)
                wanInterface_Addressing_DHCPSet_VendorID_valor = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[1]/input').get_attribute('value')
                print(wanInterface_Addressing_DHCPSet_VendorID_valor)
                wanInterface_Addressing_DHCPSet_Client = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[2]/label').text
                print(wanInterface_Addressing_DHCPSet_Client)
                wanInterface_Addressing_DHCPSet_Client_valor = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[2]/input').get_attribute('value')
                print(wanInterface_Addressing_DHCPSet_Client_valor)
                wanInterface_Addressing_DHCPSet_UserClassID = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[3]/label').text
                print(wanInterface_Addressing_DHCPSet_UserClassID)
                wanInterface_Addressing_DHCPSet_UserClassID_valor = self._driver.find_element_by_xpath('//*[@id="ipoe"]/div[3]/input').get_attribute('value')
                print(wanInterface_Addressing_DHCPSet_UserClassID_valor)

                wanInterface_DNS = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/legend').text
                print(wanInterface_DNS)
                wanInterface_Addressing_DNS_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[1]/input').get_attribute('checked')
                if wanInterface_Addressing_DNS_valor == 'true':
                    wanInterface_Addressing_DNS_valor = 'DNS Override'
                print(wanInterface_Addressing_DNS_valor)
                wanInterface_Addressing_DNS_Primary = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/label').text
                print(wanInterface_Addressing_DNS_Primary)
                wanInterface_Addressing_DNS_Primary_valor = (self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[1]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[2]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[3]').get_attribute('value') +
                                                             '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[4]').get_attribute('value'))
                print(wanInterface_Addressing_DNS_Primary_valor)
                wanInterface_Addressing_DNS_Secondary = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/label').text
                print(wanInterface_Addressing_DNS_Secondary)
                wanInterface_Addressing_DNS_Secondary_valor = (self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[1]').get_attribute('value') +
                                                               '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[2]').get_attribute('value') +
                                                               '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[3]').get_attribute('value') +
                                                               '.' + self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[4]').get_attribute('value'))
                print(wanInterface_Addressing_DNS_Secondary_valor)

                wanInterface_Addressing_IPv6 = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/legend').text
                print(wanInterface_Addressing_IPv6)
                wanInterface_Addressing_IPv6_AdmState = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/label').text
                print(wanInterface_Addressing_IPv6_AdmState)
                if self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[1]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Dual Stack'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[2]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Somente IPv6'
                elif self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[3]').get_attribute('checked') == 'true':
                    wanInterface_Addressing_IPv6_AdmState_valor = 'Desabilitado'
                print(wanInterface_Addressing_IPv6_AdmState_valor)
                wanInterface_Addressing_IPv6_Unnumbered = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[2]/label').text
                print(wanInterface_Addressing_IPv6_Unnumbered)
                wanInterface_Addressing_IPv6_Unnumbered_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[2]/input[1]').get_attribute('checked')
                if wanInterface_Addressing_IPv6_Unnumbered_valor == 'true':
                    wanInterface_Addressing_IPv6_Unnumbered_valor = 'Habilitado'
                else:
                    wanInterface_Addressing_IPv6_Unnumbered_valor = 'Desabilitado'
                print(wanInterface_Addressing_IPv6_Unnumbered_valor)
                wanInterface_Addressing_IPv6_AddrType = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[3]/label').text
                print(wanInterface_Addressing_IPv6_AddrType)
                wanInterface_Addressing_IPv6_AddrType_valor = self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[3]/input[1]').get_attribute('checked')
                if wanInterface_Addressing_IPv6_AddrType_valor == 'true':
                    wanInterface_Addressing_IPv6_AddrType_valor = 'SLAAC'
                else:
                    wanInterface_Addressing_IPv6_AddrType_valor = 'DHCP'
                print(wanInterface_Addressing_IPv6_AddrType_valor)

                interface = int(interface) - 1

                json_saida427 = {
                    "Interface #" + str(interface):
                        {
                            wanInterface_AdminState: wanInterface_AdminState_valor
                        },
                    wanInterface_VLANPrior:
                        {
                            wanInterface_VLANPrior: wanInterface_VLANPrior_valor,
                            wanInterface_VLANPrior_VLANID: wanInterface_VLANPrior_VLANID_valor,
                            wanInterface_VLANPrior_priority: wanInterface_VLANPrior_priority_valor
                        },
                    wanInterface_Addressing:
                        {
                            wanInterface_Addressing_type: wanInterface_Addressing_type_valor,
                            wanInterface_Addressing_DHCPSet:
                                {
                                    wanInterface_Addressing_DHCPSet_VendorID: wanInterface_Addressing_DHCPSet_VendorID_valor,
                                    wanInterface_Addressing_DHCPSet_Client: wanInterface_Addressing_DHCPSet_Client_valor,
                                    wanInterface_Addressing_DHCPSet_UserClassID: wanInterface_Addressing_DHCPSet_UserClassID_valor
                                }
                        },
                    wanInterface_DNS:
                        {
                            "DNS Override": wanInterface_Addressing_DNS_valor,
                            wanInterface_Addressing_DNS_Primary: wanInterface_Addressing_DNS_Primary_valor,
                            wanInterface_Addressing_DNS_Secondary: wanInterface_Addressing_DNS_Secondary_valor
                        },
                    wanInterface_Addressing_IPv6:
                        {
                            wanInterface_Addressing_IPv6_AdmState: wanInterface_Addressing_IPv6_AdmState_valor,
                            wanInterface_Addressing_IPv6_Unnumbered: wanInterface_Addressing_IPv6_Unnumbered_valor,
                            wanInterface_Addressing_IPv6_AddrType: wanInterface_Addressing_IPv6_AddrType_valor
                        }
                }
                self._driver.quit()
                if json_saida427['IPv6'].get('Adm.State') == 'Dual Stack':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Adm.State: Dual Stack", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno {json_saida427['IPv6'].get('Adm.State')}"})

                self.update_global_result_memory(flask_username, 'checkWanInterface_x_427', json_saida427)
                return self._dict_result


        except Exception as e:
                self._dict_result.update({ "obs": e})
                return self._dict_result


    def validarDHCPv6Wan_428(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')

        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            ans_428 = result['IPv6'].get('Addressing Type')
            if 'SLAAC' == ans_428:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Addressing Type igual a SLAAC", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Addressing Type diferente de SLAAC, retorno {ans_428}"})
        return self._dict_result


    def checkLANSettings_429(self, flask_username):
        usuario = self._username
        senha = self._password
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            user_input = self._driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = self._driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            self._driver.switch_to.frame('menuFrm')
            print('\n#############################################'
                  '\n MENU >> LAN SETTINGS  '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         LAN SETTINGS > IP INTERFACE
            ### ------------------------------------------ ###
            lanSettings = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/p[1]/b').text
            print(lanSettings)
            lanSettings_ipInterfc = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[1]').click()
            time.sleep(1)
            lanSettings_ipInterfc = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[1]').text
            print(lanSettings_ipInterfc)
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('mainFrm')
            lanSettings_ipInterfc_ipv4 = self._driver.find_element_by_xpath('/html/body/h1').text
            print(lanSettings_ipInterfc_ipv4)
            lanSettings_ipInterfc_ipv4_ipInterfc = self._driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
            print(lanSettings_ipInterfc_ipv4_ipInterfc)
            lanSettings_ipInterfc_ipv4_ipInterfc_adminState = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[1]/label').text
            print(lanSettings_ipInterfc_ipv4_ipInterfc_adminState)
            lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[1]/input[1]').get_attribute('checked')
            if lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor == 'true':
                lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor = 'Habilitado'
            else:
                lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor = 'Desabilitado'
            print(lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor)

            lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[2]/label').text
            print(lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping)
            lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[2]/input[1]').get_attribute('checked')
            if lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor == 'true':
                lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor = 'Habilitado'
            else:
                lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor = 'Desabilitado'
            print(lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor)

            lanSettings_ipInterfc_ipv4_ipv4_addr = self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            lanSettings_ipInterfc_ipv4_ipv4_addr = self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
            print(lanSettings_ipInterfc_ipv4_ipv4_addr)
            lanSettings_ipInterfc_ipv4_ipv4_addr_head = []
            for head in range(1, len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))):
                teste = self._driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th[' + str(head) + ']').text
                lanSettings_ipInterfc_ipv4_ipv4_addr_head.append(teste)
            print(lanSettings_ipInterfc_ipv4_ipv4_addr_head)
            countlinhas = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
            countcols = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[1]/td'))
            lanSettings_ipInterfc_ipv4_ipv4_addr_table = []
            print(teste)
            for col in range(1, countcols):
                teste = self._driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td[' + str(col) + ']').text
                lanSettings_ipInterfc_ipv4_ipv4_addr_table.append(teste)
            print(lanSettings_ipInterfc_ipv4_ipv4_addr_table)

            ### ------------------------------------------ ###
            ###         LAN SETTINGS > IPv6
            ### ------------------------------------------ ###
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('menuFrm')
            lanSettings_ipv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[3]').click()
            lanSettings_ipv6 = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[3]').text
            print(lanSettings_ipv6)
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('mainFrm')
            lanSettings_ipv6_Status = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[1]/label[1]').text
            print(lanSettings_ipv6_Status)
            lanSettings_ipv6_Status_valor = self._driver.find_element_by_xpath('//*[@id="ipv6_opr_status"]').text
            print(lanSettings_ipv6_Status_valor)
            lanSettings_ipv6_Global = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[2]/label[1]').text
            print(lanSettings_ipv6_Global)
            lanSettings_ipv6_Global_valor = self._driver.find_element_by_xpath('//*[@id="g_ipv6addr_all"]').text
            print(lanSettings_ipv6_Global_valor)
            lanSettings_ipv6_AdmState = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[3]/label').text
            print(lanSettings_ipv6_AdmState)
            lanSettings_ipv6_AdmState_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[3]/input[1]').get_attribute('checked')
            if lanSettings_ipv6_AdmState_valor == 'true':
                lanSettings_ipv6_AdmState_valor = 'Habilitado'
            else:
                lanSettings_ipv6_AdmState_valor = 'Desabilitado'
            print(lanSettings_ipv6_AdmState_valor)

            lanSettings_ipv6_RADVD = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/legend').text
            print(lanSettings_ipv6_RADVD)
            lanSettings_ipv6_RADVD_AdmState = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[1]/label').text
            print(lanSettings_ipv6_RADVD_AdmState)
            lanSettings_ipv6_RADVD_AdmState_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[1]/input[1]').get_attribute('checked')
            if lanSettings_ipv6_RADVD_AdmState_valor == 'true':
                lanSettings_ipv6_RADVD_AdmState_valor = 'Habilitado'
            else:
                lanSettings_ipv6_RADVD_AdmState_valor = 'Desabilitado'
            print(lanSettings_ipv6_RADVD_AdmState_valor)
            lanSettings_ipv6_RADVD_PrfxDeleg = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[2]/label').text
            print(lanSettings_ipv6_RADVD_PrfxDeleg)
            lanSettings_ipv6_RADVD_PrfxDeleg_valor = self._driver.find_element_by_xpath('//*[@id="IPIntfId"]').get_attribute('value')
            if lanSettings_ipv6_RADVD_PrfxDeleg_valor == '2':
                lanSettings_ipv6_RADVD_PrfxDeleg_valor = 'ip2'
            print(lanSettings_ipv6_RADVD_PrfxDeleg_valor)
            lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[3]/input').get_attribute('checked')
            if lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor == 'true':
                lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor = 'Habilitado'
            else:
                lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor = 'Desabilitado'
            print(lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor)
            lanSettings_ipv6_RADVD_Prefix = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[4]/label').text
            print(lanSettings_ipv6_RADVD_Prefix)
            lanSettings_ipv6_RADVD_Prefix_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[4]/input').get_attribute('value')
            print(lanSettings_ipv6_RADVD_Prefix_valor)
            lanSettings_ipv6_RADVD_Preferred = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[5]/label').text
            print(lanSettings_ipv6_RADVD_Preferred)
            lanSettings_ipv6_RADVD_Preferred_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[5]/input').get_attribute('value')
            print(lanSettings_ipv6_RADVD_Preferred_valor)
            lanSettings_ipv6_RADVD_Valid = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[6]/label').text
            print(lanSettings_ipv6_RADVD_Valid)
            lanSettings_ipv6_RADVD_Valid_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[6]/input').get_attribute('value')
            print(lanSettings_ipv6_RADVD_Valid_valor)

            lanSettings_ipv6_DHCPv6 = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/legend').text
            print(lanSettings_ipv6_DHCPv6)
            lanSettings_ipv6_DHCPv6_Mode = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/label').text
            print(lanSettings_ipv6_DHCPv6_Mode)
            if self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[1]').get_attribute('checked') == 'true':
                lanSettings_ipv6_DHCPv6_Mode_valor = 'Desabilitado'
            if self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[2]').get_attribute('checked') == 'true':
                lanSettings_ipv6_DHCPv6_Mode_valor = 'Stateless'
            if self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[3]').get_attribute('checked') == 'true':
                lanSettings_ipv6_DHCPv6_Mode_valor = 'Stateful'
            print(lanSettings_ipv6_DHCPv6_Mode_valor)
            lanSettings_ipv6_DHCPv6_Start = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[2]/label').text
            print(lanSettings_ipv6_DHCPv6_Start)
            lanSettings_ipv6_DHCPv6_Start_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[2]/input').get_attribute('value')
            print(lanSettings_ipv6_DHCPv6_Start_valor)
            lanSettings_ipv6_DHCPv6_End = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[3]/label').text
            print(lanSettings_ipv6_DHCPv6_End)
            lanSettings_ipv6_DHCPv6_End_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[3]/input').get_attribute('value')
            print(lanSettings_ipv6_DHCPv6_End_valor)
            lanSettings_ipv6_DHCPv6_Lease = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[4]/label').text
            print(lanSettings_ipv6_DHCPv6_Lease)
            lanSettings_ipv6_DHCPv6_Lease_valor = self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[4]/input').get_attribute('value')
            print(lanSettings_ipv6_DHCPv6_Lease_valor)

            json_saida429 = {
                lanSettings:
                    {
                        lanSettings_ipInterfc:
                            {
                                lanSettings_ipInterfc_ipv4_ipInterfc_adminState: lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor,
                                lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping: lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor
                            },
                        lanSettings_ipInterfc_ipv4_ipv4_addr:
                            {
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[2]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[2],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[3]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[3],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[4]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[4],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[5]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[5],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[6]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[6]
                            },
                        lanSettings_ipv6:
                            {
                                lanSettings_ipv6_Status: lanSettings_ipv6_Status_valor,
                                lanSettings_ipv6_AdmState: lanSettings_ipv6_RADVD_AdmState_valor,
                                lanSettings_ipv6_Global: lanSettings_ipv6_Global_valor,
                                lanSettings_ipv6_RADVD:
                                    {
                                        lanSettings_ipv6_RADVD_AdmState: lanSettings_ipv6_RADVD_AdmState_valor,
                                        lanSettings_ipv6_RADVD_PrfxDeleg: lanSettings_ipv6_RADVD_PrfxDeleg_valor,
                                        "ULA Prefix": lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor,
                                        lanSettings_ipv6_RADVD_Prefix: lanSettings_ipv6_RADVD_Prefix_valor,
                                        lanSettings_ipv6_RADVD_Preferred: lanSettings_ipv6_RADVD_Preferred_valor,
                                        lanSettings_ipv6_RADVD_Valid: lanSettings_ipv6_RADVD_Valid_valor
                                    },
                                lanSettings_ipv6_DHCPv6:
                                    {
                                        lanSettings_ipv6_DHCPv6_Mode: lanSettings_ipv6_DHCPv6_Mode_valor,
                                        lanSettings_ipv6_DHCPv6_Start: lanSettings_ipv6_DHCPv6_Start_valor,
                                        lanSettings_ipv6_DHCPv6_End: lanSettings_ipv6_DHCPv6_End_valor,
                                        lanSettings_ipv6_DHCPv6_Lease: lanSettings_ipv6_DHCPv6_Lease_valor
                                    }
                            }

                    }
            }

            self._driver.quit()
            for _,row in json_saida429.items():
                prefix_wan = row['IPv6']['RADVD'].get('Prefix Delegation WAN')
                if prefix_wan == 'ip2':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: ip2", "result":"passed"})
                    break
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno do Prefix Delegation WAN:{prefix_wan}"})


            
            self.update_global_result_memory(flask_username, 'checkLANSettings_429', json_saida429)
            return self._dict_result

        except Exception as exception:
            print(exception)
            self._dict_result.update({"obs": exception})
            return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_431(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Type')
                    if iface_type == 'PPPoe':
                        if sub_dict.get('VLAN') == '8,35':
                            self._dict_result.update({"obs": 'Type: PPPoE, VLAN: 8,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Type: PPPoE | VLAN: {sub_dict.get('VLAN')}"})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Type:{iface_type}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result

    
    def vivo_1_ADSL_vlanIdPPPoE_432(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('VLAN')
                    if iface_type == '8,35':
                        if sub_dict.get('Type') == 'PPPoE':
                            self._dict_result.update({"obs": 'VLAN: 8,35 | Type: PPPoE ', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno VLAN: 8,35 | Type: {sub_dict.get('TYPE')} "})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno VLAN:{iface_type}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_433(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'ip2':
                        if sub_dict.get('Adm.State') == 'Habilitado':
                            self._dict_result.update({"obs": 'Interface: ip2 | Adm.State: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Interface: ip2 | Adm.State:{sub_dict.get("Adm.State")} '})
                            break
                else:
                    self._dict_result.update({"obs": 'Teste incorreto, retorno Interface:{iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})

        return self._dict_result


    def vivo_1_usernamePppDefault_435(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        cpe_config = config_collection.find_one()
        if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
            usuario = result['Configurações']['Internet'].get('Usuário:')
            if usuario == 'cliente@cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Usuário: cliente@cliente', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno: Usuário: {usuario}'})
        else:
            self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        return self._dict_result


    def vivo_1_passwordPppDefault_436(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        cpe_config = config_collection.find_one()
        if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
            senha = result['Configurações']['Internet'].get('Senha:')
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
                for idx, sub_dict in result.items():
                    if idx == ('IPv6'):
                        if sub_dict.get('Adm.State') == 'Dual Stack':
                            self._dict_result.update({"obs": 'IPv6: Adm.State: Dual Stack', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno IPv6: Adm.State: {sub_dict.get('Adm.State')}"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno IPv6: {idx}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})               
        return self._dict_result


    def validarDHCPv6Wan_438(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                ans_438 = result['IPv6'].get('Addressing Type')
                if 'SLAAC' == ans_438:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Addressing Type igual a SLAAC", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Addressing Type:{ans_438}"})
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
                ans_439 = result['LAN Setting']['IPv6']['RADVD'].get('Prefix Delegation WAN')
                if 'ip2' == ans_439:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: ip2", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Prefix Delegation WAN:{ans_439}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_441(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_type = result.get('Type')
                    if iface_type == 'PPPoe':
                        if sub_dict.get('VLAN') == '0,35':
                            self._dict_result.update({"obs": 'Type: PPPoE | VLAN: 0,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Type: PPPoE | VLAN: {sub_dict.get("VLAN")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f' Teste incorreto, retorno Type: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_442(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')

        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('VLAN')
                    if iface_type == '8,35':
                        if sub_dict.get('Type') == 'PPPoE':
                            self._dict_result.update({"obs": 'Type: PPPoE | VLAN: 0,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno VLAN: 8,35, Type: {sub_dict.get("Type")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno VLAN: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_443(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')

        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'ip2':
                        if sub_dict.get('Adm.State') == 'Habilitado':
                            self._dict_result.update({"obs": 'Interfac: ip2 | Adm.State: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": 'Teste incorreto, retorno Interface: ip2 | Adm.State: Desabilitado'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_2_usernamePppDefault_445(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
            
        cpe_config = config_collection.find_one()
        if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
            usuario = result['Configurações']['Internet'].get('Usuário:')
            if usuario == 'cliente@cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Usuário: cliente@cliente', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Usuário: {usuario}'})
        else:
            self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        return self._dict_result


    def vivo_2_passwordPppDefault_446(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
            
        cpe_config = config_collection.find_one()
        if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
            senha = result['Configurações']['Internet'].get('Senha:')
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
                for idx, sub_dict in result.items():
                    if idx == ('IPv6'):
                        if sub_dict.get('Adm.State') == 'Dual Stack' :
                            self._dict_result.update({"obs": 'IPv6: Adm.State: Dual Stack', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else: 
                            self._dict_result.update({"obs": f'Teste incorreto, retorno IPv6: Adm.State: {sub_dict.get("Adm.State")}'})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno {idx}'})
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
                ans_448 = result['IPv6'].get('Addressing Type')
                if 'SLAAC' == ans_448:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Addressing Type igual a SLAAC", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Testes incorreto, retorno Addressing Type: {ans_448}"})
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
                ans_439 = result['LAN Setting']['IPv6']['RADVD'].get('Prefix Delegation WAN')
                if 'ip2' == ans_439:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: ip2", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Prefix Delegation WAN: {ans_439}"})
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
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'ip4':
                        if sub_dict.get('VLAN') == '20':
                            self._dict_result.update({"obs": 'Name: ip4 | VLAN: 20', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: ip4 | VLAN {sub_dict.get("VLAN")}'})
                            break
                    else:
                        self._dict_result.update({"obs":  f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})

        return self._dict_result

        
    def vivo_1_prioridadeIptv_451(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'ip4':
                        if sub_dict.get('Priority') == '3':
                            self._dict_result.update({"obs": 'Name: ip4 | Priority: 3', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: ip4 | Priority: {sub_dict.get("Priority")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_validarNatIptv_452(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'ip4':
                        if sub_dict.get('Adm.State') == 'Habilitado':
                            self._dict_result.update({"obs": 'Interface: ip4 | Adm.State: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Ip4 | Adm.State: {sub_dict.get("Adm.State")} '})
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
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'ip2':
                        if sub_dict.get('IGMP') == 'Habilitado':
                            self._dict_result.update({"obs": 'Interface: ip2, IGMP: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: ip2, IGMP: {sub_dict.get("IGMP")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
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
                    iface_type = result.get('Name')
                    if iface_type == 'ip5':
                        if sub_dict.get('VLAN') == '602':
                            self._dict_result.update({"obs": 'Name: ip5, VLAN: 602', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: ip5, VLAN: {sub_dict.get("VLAN")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo2_validarNatIPTV_455(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 e 423 seja executado em conjunto
        try:
            result1 = session.get_result_from_test(flask_username, 'checkWanInterface_420')
            result2 = session.get_result_from_test(flask_username, 'checkNatSettings_423')

        except KeyError as exception:
            self._dict_result.update({"obs": 'Execute o teste 420 e o teste 423 primeiro'})

        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result1.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict.get('Priority')
                    if iface_type == '3':
                        if sub_dict.get('VLAN') == '602':
                            iface_name = sub_dict.get('Name')
                            break

                for _, sub_dict in result2.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == iface_name:
                        if sub_dict.get('Adm.State') == 'Habilitado':
                            self._dict_result.update({"obs": 'Adm.State:  Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Adm.State: {sub_dict.get("Adm.State")} '})
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
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'ip5':
                        if sub_dict.get('IGMP') == 'Habilitado':
                            self._dict_result.update({"obs": 'Interface: ip5 | IGMP: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: ip5 | IGMP: {sub_dict.get("IGMP")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
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
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'ip5':
                        if sub_dict.get('VLAN') == '4000':
                            self._dict_result.update({"obs": 'Name: ip5 | VLAN: 4000', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: ip5 | VLAN: {sub_dict.get("VLAN")} '})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def natMulticastVivo2_458(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Interface')
                if iface_type == 'ip4':
                    if sub_dict.get('Adm.State') == 'Desabilitado':
                        self._dict_result.update({"obs": 'Interface: ip4 | Adm.State: Desabilitado', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: ip4 | Adm.State: {sub_dict.get("Adm.State")} '})
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
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Interface')
                if iface_type == 'ip4':
                    if sub_dict.get('IGMP') == 'Habilitado':
                        self._dict_result.update({"obs": 'Interface: ip4 | IGMP: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface == ip4 | IGMP: {sub_dict.get("IGMP")} '})
                        break
            else:
                self._dict_result.update({"obs":  f'Teste incorreto, retorno Interface: {iface_type}'})
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
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'ip3':
                        if sub_dict.get('VLAN') == '30':
                            obs_result = 'Name: ip3 | VLAN: 30'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result = f'Teste incorreto, retorno Name: ip3, VLAN: {sub_dict.get("VLAN")}'
                            break
                    else:
                        obs_result = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"
            
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'ip3':
                        if sub_dict.get('VLAN') == '601':
                            obs_result2 = 'Name: ip3 | VLAN: 601'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Name: ip3, VLAN: {sub_dict.get("VLAN")}'
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
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'ip3':
                        if sub_dict.get('Priority') == '5':
                            obs_result = 'Name: ip3 | Priority: 5'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result = f'Teste incorreto, retorno Name: ip3 | Priority: {sub_dict.get("Priority")}'
                            break
                    else:
                        obs_result = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"

            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'ip3':
                        if sub_dict.get('Priority') == '601':
                            obs_result2 = 'Name: ip3 | Priority: 601'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Name: ip3 | Priority: {sub_dict.get("Priority")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
        
            self._dict_result.update({"obs": f"Teste 461_1: {obs_result}, Teste 461_2: {obs_result2}" })
        return self._dict_result


    def vivo1_validarNatVoip_462(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        try:
            result1 = session.get_result_from_test(flask_username, 'checkWanInterface_420')
            result2 = session.get_result_from_test(flask_username, 'checkNatSettings_423')

        except KeyError as exception:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})

        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result1.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict.get('Priority')
                    if iface_type == '5':
                        if sub_dict.get('VLAN') == '30':
                            iface_name = sub_dict.get('Name')
                            obs_result1 = f"Name: {iface_name}"
                            break
                        else:
                            obs_result1 = (f'Teste incorreto, retorno Priority == 5 | VLAN: {sub_dict.get("VLAN")}')
                            break
                    else:
                        obs_result1 = (f'Teste incorreto, retorno Priority: {iface_type}')
            

                for _, sub_dict in result2.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == iface_name:
                        if sub_dict.get('Adm.State') == 'Habilitado':
                            obs_result1 = 'Adm.State: Habilitado'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result1 = f'Teste incorreto, retorno Adm.State: {sub_dict.get("Adm.State")}'
                            break
                    else:
                        obs_result1 = f'Teste incorreto, retorno {iface_type} diferente de {iface_name}'

            else:
                obs_result1 = f"REDE:{cpe_config['REDE']}"
        
        #2
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result1.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict.get('Priority')
                    if iface_type == '5':
                        if sub_dict.get('VLAN') == '601':
                            iface_name = sub_dict.get('Name')
                            obs_result2 = f"Name: {iface_name}"
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Priority: 5, VLAN: {sub_dict.get("VLAN")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Priority: {iface_type}'
                    
                for _, sub_dict in result2.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == iface_name:
                        if sub_dict.get('Adm.State') == 'Habilitado':
                            obs_result2 = 'Adm.State: Habilitado'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Adm.State: {sub_dict.get("Adm.State")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno {iface_type} diferente de {iface_name}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
         
        finally:
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
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'ip3':
                        if sub_dict.get('IGMP') == 'Habilitado':
                            obs_result = 'Interface: ip3 | IGMP: Habilitado'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result = f'Teste incorreto, retorno Interface: ip3 | IGMP: {sub_dict.get("IGMP")}'
                            break
                else:
                    obs_result =  f'Teste incorreto, retorno Interface: {iface_type}'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"
            
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Interface')
                    if iface_type == 'ip3':
                        if sub_dict.get('IGMP') == 'Habilitado':
                            obs_result2 = 'Interface: ip3 | IGMP: Habilitado'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 =  f'Teste incorreto, retorno Interface: ip3 | IGMP: {sub_dict.get("IGMP")}'
                            break
                else:
                    obs_result2 =  f'Teste incorreto, retorno Interface: {iface_type}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
            self._dict_result.update({"obs": f"463_1: {obs_result}, 463_2: {obs_result2}"})
        return self._dict_result

    
    def checkLANDHCPSettings_x_464(self, flask_username, port='4'):
        
        usuario = self._username
        senha = self._password
        porta = port

        try:
            print('\n\n == Abrindo URL == ')
            self._driver.get('http://' + self._address_ip + '/padrao')

            user_input = self._driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = self._driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            self._driver.switch_to.frame('menuFrm')
            print('\n#############################################'
                  '\n MENU >> LAN DHCP SETTINGS  '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         LAN SETTINGS > IP INTERFACE
            ### ------------------------------------------ ###
            lanSettings = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/p[1]/b').text
            print(lanSettings)
            lanSettings_dhcp= self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[2]').click()
            time.sleep(1)
            lanSettings_dhcp = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[2]').text
            print(lanSettings_dhcp)
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('mainFrm')
            lanSettings_dhcpServer = self._driver.find_element_by_xpath('//*[@id="DHCPServerList"]/legend').text
            print(lanSettings_dhcpServer)

            countHead = len(self._driver.find_elements_by_xpath('//*[@id="DHCPServerList"]/table/thead/tr/th'))
            tableHead = []
            for col in range(2, countHead):
                teste = self._driver.find_element_by_xpath('//*[@id="DHCPServerList"]/table/thead/tr/th['+str(col)+']').text
                tableHead.append(teste)
            print(tableHead)
            countlinhas = len(self._driver.find_elements_by_xpath('//*[@id="DHCPServerList"]/table/tbody/tr'))
            countcols = len(self._driver.find_elements_by_xpath('//*[@id="DHCPServerList"]/table/tbody/tr[1]/td'))

            table = []
            for linha in range(1, countlinhas+1):
                for col in range(2, countcols):
                    teste = self._driver.find_element_by_xpath('//*[@id="DHCPServerList"]/table/tbody/tr['+str(linha)+']/td['+str(col)+']').text
                    table.append(teste)
            print(table)
            

            # if port == '1':
            #     index0 = self._driver.find_element_by_xpath('//*[@id="DHCPServerList"]/table/tbody/tr[1]/td[2]/a').click()
            #     dhcpServerSett = self._driver.find_element_by_xpath('//*[@id="DHCPServerShow"]/div/ul/li[1]/a').text
            #     print(dhcpServerSett)
            #     dhcpServerSett_AdmState = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[1]/label').text
            #     print(dhcpServerSett_AdmState)
            #     dhcpServerSett_AdmState_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[1]/input[1]').get_property('value')
            #     if dhcpServerSett_AdmState_valor == '1':
            #         dhcpServerSett_AdmState_valor = 'Habilitado'
            #     else:
            #         dhcpServerSett_AdmState_valor = 'Desabilitado'
            #     print(dhcpServerSett_AdmState_valor)
            #     dhcpServerSett_AssocIntfc = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[2]/label').text
            #     print(dhcpServerSett_AssocIntfc)
            #     dhcpServerSett_AssocIntfc_valor = self._driver.find_element_by_xpath('//*[@id="IPIntfId"]/option').get_property('value')
            #     if dhcpServerSett_AssocIntfc_valor == '1':
            #         dhcpServerSett_AssocIntfc_valor = 'ip1'
            #     print(dhcpServerSett_AssocIntfc_valor)
            #     dhcpServerSett_Prior = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[3]/label').text
            #     print(dhcpServerSett_Prior)
            #     dhcpServerSett_Prior_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[3]/input').get_property('value')
            #     if dhcpServerSett_Prior_valor == '1':
            #         dhcpServerSett_Prior_valor = 'Highest'
            #     elif dhcpServerSett_Prior_valor == '2':
            #         dhcpServerSett_Prior_valor = 'Insert as Order'
            #     elif dhcpServerSett_Prior_valor == '3':
            #         dhcpServerSett_Prior_valor = 'Lowest'
            #     print(dhcpServerSett_Prior_valor)
            #
            #     dhcpServerSett_ClientConf = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/legend').text
            #     dhcpServerSett_ClientConf_IPRange = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/label').text
            #     print(dhcpServerSett_ClientConf_IPRange)
            #     dhcpServerSett_ClientConf_IPRange_ini = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[1]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[2]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[3]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[4]').get_property('value') )
            #     print(dhcpServerSett_ClientConf_IPRange_ini)
            #     dhcpServerSett_ClientConf_IPRange_fim = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[6]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[7]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[8]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[9]').get_property('value'))
            #     print(dhcpServerSett_ClientConf_IPRange_fim)
            #     dhcpServerSett_ClientConf_Mask = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/label').text
            #     print(dhcpServerSett_ClientConf_Mask)
            #     dhcpServerSett_ClientConf_Mask_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[1]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[2]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[3]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[4]').get_property('value') )
            #     print(dhcpServerSett_ClientConf_Mask_valor)
            #     dhcpServerSett_ClientConf_Gtw = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/label').text
            #     print(dhcpServerSett_ClientConf_Gtw)
            #     dhcpServerSett_ClientConf_Gtw_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[1]').get_property('value') + '.' +
            #                                             self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[2]').get_property('value') + '.' +
            #                                             self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[3]').get_property('value') + '.' +
            #                                             self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[4]').get_property('value'))
            #     print(dhcpServerSett_ClientConf_Gtw_valor)
            #     dhcpServerSett_ClientConf_DNS = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/label').text
            #     print(dhcpServerSett_ClientConf_DNS)
            #     dhcpServerSett_ClientConf_DNS_ini = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[1]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[2]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[3]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[4]').get_property('value'))
            #     print(dhcpServerSett_ClientConf_DNS_ini)
            #     dhcpServerSett_ClientConf_DNS_fim = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[6]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[7]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[8]').get_property('value') + '.' +
            #                                              self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[9]').get_property('value'))
            #     print(dhcpServerSett_ClientConf_DNS_fim)
            #     dhcpServerSett_ClientConf_Lease = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[5]/label').text
            #     print(dhcpServerSett_ClientConf_Lease)
            #     dhcpServerSett_ClientConf_Lease_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[5]/input[1]').get_property('value')
            #     print(dhcpServerSett_ClientConf_Lease_valor)
            #
            #     dhcpServerSett_Pool = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/legend').text
            #     print(dhcpServerSett_Pool)
            #     dhcpServerSett_Pool_vendorID = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[1]/input[1]').get_attribute('checked') ### VendorID valor
            #     if dhcpServerSett_Pool_vendorID == 'true':
            #         dhcpServerSett_Pool_vendorID = 'Habilitado'
            #     else:
            #         dhcpServerSett_Pool_vendorID = 'Desabilitado'
            #     print(dhcpServerSett_Pool_vendorID)
            #     dhcpServerSett_Pool_vendorID_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[1]/input[2]').get_property('value')
            #     print(dhcpServerSett_Pool_vendorID_valor)
            #     dhcpServerSett_Pool_MatchRange = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[2]/span').text
            #     print(dhcpServerSett_Pool_MatchRange)
            #     dhcpServerSett_Pool_MatchRange_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            #     if dhcpServerSett_Pool_MatchRange_valor == 'true':
            #         dhcpServerSett_Pool_MatchRange_valor = 'Include'
            #     else:
            #         dhcpServerSett_Pool_MatchRange_valor = 'Exclude'
            #     print(dhcpServerSett_Pool_MatchRange_valor)
            #     dhcpServerSett_Pool_MatchMode = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[3]/span').text
            #     print(dhcpServerSett_Pool_MatchMode)
            #     dhcpServerSett_Pool_MatchMode_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[3]/input[1]').get_property('value')
            #     if dhcpServerSett_Pool_MatchMode_valor == '0':
            #         dhcpServerSett_Pool_MatchMode_valor = 'Exato'
            #     elif dhcpServerSett_Pool_MatchMode_valor == '1':
            #         dhcpServerSett_Pool_MatchMode_valor = 'Prefixo'
            #     elif dhcpServerSett_Pool_MatchMode_valor == '2':
            #         dhcpServerSett_Pool_MatchMode_valor = 'Sufixo'
            #     elif dhcpServerSett_Pool_MatchMode_valor == '3':
            #         dhcpServerSett_Pool_MatchMode_valor = 'Substring'
            #     print(dhcpServerSett_Pool_MatchMode_valor)
            #     dhcpServerSett_Pool_clientID = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[4]/input[1]').get_attribute('checked')  ### ClientID valor
            #     if dhcpServerSett_Pool_clientID == 'true':
            #         dhcpServerSett_Pool_clientID = 'Habilitado'
            #     else:
            #         dhcpServerSett_Pool_clientID = 'Desabilitado'
            #     print(dhcpServerSett_Pool_clientID)
            #     dhcpServerSett_Pool_clientID_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[4]/input[2]').get_property('value')
            #     print(dhcpServerSett_Pool_clientID_valor)
            #     dhcpServerSett_Pool_MatchRange2 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[5]/span').text
            #     print(dhcpServerSett_Pool_MatchRange2)
            #     dhcpServerSett_Pool_MatchRange_valor2 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            #     if dhcpServerSett_Pool_MatchRange_valor2 == 'true':
            #         dhcpServerSett_Pool_MatchRange_valor2 = 'Include'
            #     else:
            #         dhcpServerSett_Pool_MatchRange_valor2 = 'Exclude'
            #     print(dhcpServerSett_Pool_MatchRange_valor2)
            #     dhcpServerSett_Pool_UserClassID = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[6]/input[1]').get_attribute('checked') ### UserClassID
            #     print(dhcpServerSett_Pool_UserClassID)
            #     if dhcpServerSett_Pool_UserClassID == 'true':
            #         dhcpServerSett_Pool_UserClassID = 'Habilitado'
            #     else:
            #         dhcpServerSett_Pool_UserClassID = 'Desabilitado'
            #     dhcpServerSett_Pool_UserClassID_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[4]/input[2]').get_property('value')
            #     print(dhcpServerSett_Pool_UserClassID_valor)
            #     dhcpServerSett_Pool_MatchRange3 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[5]/span').text
            #     print(dhcpServerSett_Pool_MatchRange3)
            #     dhcpServerSett_Pool_MatchRange_valor3 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[7]/input[1]').get_attribute('checked')
            #     if dhcpServerSett_Pool_MatchRange_valor3 == 'true':
            #         dhcpServerSett_Pool_MatchRange_valor3 = 'Include'
            #     else:
            #         dhcpServerSett_Pool_MatchRange_valor3 = 'Exclude'
            #     print(dhcpServerSett_Pool_MatchRange_valor3)
            #     dhcpServerSett_Pool_MAC = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[8]/input').get_attribute('checked')  ### MAC
            #     print(dhcpServerSett_Pool_MAC)
            #     if dhcpServerSett_Pool_MAC == 'true':
            #         dhcpServerSett_Pool_MAC = 'Habilitado'
            #     else:
            #         dhcpServerSett_Pool_MAC = 'Desabilitado'
            #     print(dhcpServerSett_Pool_MAC)
            #     dhcpServerSett_Pool_MACAddr = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/label').text
            #     print(dhcpServerSett_Pool_MACAddr)
            #     dhcpServerSett_Pool_MACAddr_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[1]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[2]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[3]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[4]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[5]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[6]').get_property('value') )
            #     print(dhcpServerSett_Pool_MACAddr_valor)
            #     dhcpServerSett_Pool_Mask = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/label').text
            #     print(dhcpServerSett_Pool_Mask)
            #     dhcpServerSett_Pool_Mask_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[1]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[2]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[3]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[4]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[5]').get_property('value') + ':' +
            #                                          self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[6]').get_property('value'))
            #     print(dhcpServerSett_Pool_Mask_valor)
            #     dhcpServerSett_Pool_MatchRange4 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[11]/span').text
            #     print(dhcpServerSett_Pool_MatchRange4)
            #     dhcpServerSett_Pool_MatchRange_valor4 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[11]/input[1]').get_attribute('checked')
            #     if dhcpServerSett_Pool_MatchRange_valor4 == 'true':
            #         dhcpServerSett_Pool_MatchRange_valor4 = 'Include'
            #     else:
            #         dhcpServerSett_Pool_MatchRange_valor4 = 'Exclude'
            #     print(dhcpServerSett_Pool_MatchRange_valor4)
            #
            #
            #     options = self._driver.find_element_by_xpath('//*[@id="DHCPServerShow"]/div/ul/li[4]/a').click()
            #     options = self._driver.find_element_by_xpath('//*[@id="DHCPServerShow"]/div/ul/li[4]/a').text
            #     print(options)
            #     countHeadOptions = len(self._driver.find_elements_by_xpath('//*[@id="Tab4_1"]/table/thead/tr/th'))
            #     tableHeadoptions = []
            #     for col in range(2, countHeadOptions+1):
            #         teste = self._driver.find_element_by_xpath('//*[@id="Tab4_1"]/table/thead/tr/th[' + str(col) + ']').text
            #         tableHeadoptions.append(teste)
            #     print(tableHeadoptions)
            #     countlinhas = len(self._driver.find_elements_by_xpath('//*[@id="Tab4_1"]/table/tbody/tr'))
            #     countcols = len(self._driver.find_elements_by_xpath('//*[@id="Tab4_1"]/table/tbody/tr[1]/td'))
            #
            #     tableOptions = []
            #     for linha in range(1, countlinhas + 1):
            #         for col in range(2, countcols+1):
            #             teste = self._driver.find_element_by_xpath('//*[@id="Tab4_1"]/table/tbody/tr[' + str(linha) + ']/td[' + str(col) + ']').text
            #             tableOptions.append(teste)
            #     print(tableOptions)
            #
            #     json_saida = {
            #         lanSettings_dhcp:
            #             {
            #                 tableHead[0] + ' #' + table[0]:
            #                     {
            #                         tableHead[1]: table[1],
            #                         tableHead[2]: table[2],
            #                         tableHead[3]: table[3],
            #                         tableHead[4]: table[4],
            #                         'Detalhes':
            #                             {
            #                                 dhcpServerSett:
            #                                     {
            #                                         dhcpServerSett_AdmState:dhcpServerSett_AdmState_valor,
            #                                         dhcpServerSett_AssocIntfc:dhcpServerSett_AssocIntfc_valor,
            #                                         dhcpServerSett_Prior:dhcpServerSett_Prior_valor,
            #                                         dhcpServerSett_ClientConf:
            #                                             {
            #                                                 dhcpServerSett_ClientConf_IPRange:
            #                                                     {
            #                                                         'inicio':dhcpServerSett_ClientConf_IPRange_ini,
            #                                                         'fim':dhcpServerSett_ClientConf_IPRange_fim
            #                                                     },
            #                                                 dhcpServerSett_ClientConf_Mask:dhcpServerSett_ClientConf_Mask_valor,
            #                                             dhcpServerSett_ClientConf_Gtw:dhcpServerSett_ClientConf_Gtw_valor,
            #                                             dhcpServerSett_ClientConf_DNS:
            #                                                     {
            #                                                         'inicio':dhcpServerSett_ClientConf_DNS_ini,
            #                                                         'fim':dhcpServerSett_ClientConf_DNS_fim
            #                                                     },
            #                                             dhcpServerSett_ClientConf_Lease:dhcpServerSett_ClientConf_Lease_valor
            #                                             },
            #                                         dhcpServerSett_Pool:
            #                                             {
            #                                                 'VendorID (Option 60)':dhcpServerSett_Pool_vendorID,
            #                                                 'valor VendorID':dhcpServerSett_Pool_vendorID_valor,
            #                                                 dhcpServerSett_Pool_MatchRange:dhcpServerSett_Pool_MatchRange_valor,
            #                                                 dhcpServerSett_Pool_MatchMode:dhcpServerSett_Pool_MatchMode_valor,
            #                                                 'ClientID (Option 61)':dhcpServerSett_Pool_clientID,
            #                                                 'valor ClientID': dhcpServerSett_Pool_clientID_valor,
            #                                                 dhcpServerSett_Pool_MatchRange2: dhcpServerSett_Pool_MatchRange_valor2,
            #                                                 'UserClassID (Option 77)':dhcpServerSett_Pool_UserClassID,
            #                                                 'valor UserClassID':dhcpServerSett_Pool_UserClassID_valor,
            #                                                 dhcpServerSett_Pool_MatchRange3:dhcpServerSett_Pool_MatchRange_valor3,
            #                                                 'MAC':dhcpServerSett_Pool_MAC,
            #                                                 dhcpServerSett_Pool_MACAddr:dhcpServerSett_Pool_MACAddr_valor,
            #                                                 dhcpServerSett_Pool_Mask:dhcpServerSett_Pool_Mask_valor,
            #                                                 dhcpServerSett_Pool_MatchRange4:dhcpServerSett_Pool_MatchRange_valor4
            #                                             }
            #                                     },
            #                                 options:
            #                                     {
            #                                         tableHeadoptions[0] + ' #' + tableOptions[0]:
            #                                             {
            #                                                 tableHeadoptions[1]:tableOptions[1],
            #                                                 tableHeadoptions[2]: tableOptions[2],
            #                                                 tableHeadoptions[3]: tableOptions[3],
            #                                                 tableHeadoptions[4]: tableOptions[4],
            #                                             },
            #                                         tableHeadoptions[0] + ' #' + tableOptions[5]:
            #                                             {
            #                                                 tableHeadoptions[1]: tableOptions[6],
            #                                                 tableHeadoptions[2]: tableOptions[7],
            #                                                 tableHeadoptions[3]: tableOptions[8],
            #                                                 tableHeadoptions[4]: tableOptions[9]
            #                                             }
            #                                     }
            #                             }
            #                     }
            #             }
            #     }
            #     print(json_saida)


            index1 = self._driver.find_element_by_xpath('//*[@id="DHCPServerList"]/table/tbody/tr['+str(porta)+']/td[2]/a').click()
            dhcpServerSett = self._driver.find_element_by_xpath('//*[@id="DHCPServerShow"]/div/ul/li[1]/a').text
            print(dhcpServerSett)
            dhcpServerSett_AdmState = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[1]/label').text
            print(dhcpServerSett_AdmState)
            dhcpServerSett_AdmState_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[1]/input[1]').get_property('value')
            if dhcpServerSett_AdmState_valor == '1':
                dhcpServerSett_AdmState_valor = 'Habilitado'
            else:
                dhcpServerSett_AdmState_valor = 'Desabilitado'
            print(dhcpServerSett_AdmState_valor)
            dhcpServerSett_AssocIntfc = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[2]/label').text
            print(dhcpServerSett_AssocIntfc)
            dhcpServerSett_AssocIntfc_valor = self._driver.find_element_by_xpath('//*[@id="IPIntfId"]/option').get_property('value')
            if dhcpServerSett_AssocIntfc_valor == '1':
                dhcpServerSett_AssocIntfc_valor = 'ip1'
            print(dhcpServerSett_AssocIntfc_valor)
            dhcpServerSett_Prior = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[3]/label').text
            print(dhcpServerSett_Prior)
            dhcpServerSett_Prior_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[3]/input').get_property('value')
            if dhcpServerSett_Prior_valor == '1':
                dhcpServerSett_Prior_valor = 'Highest'
            elif dhcpServerSett_Prior_valor == '2':
                dhcpServerSett_Prior_valor = 'Insert as Order'
            elif dhcpServerSett_Prior_valor == '3':
                dhcpServerSett_Prior_valor = 'Lowest'
            print(dhcpServerSett_Prior_valor)

            dhcpServerSett_ClientConf = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/legend').text
            dhcpServerSett_ClientConf_IPRange = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/label').text
            print(dhcpServerSett_ClientConf_IPRange)
            dhcpServerSett_ClientConf_IPRange_ini = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[1]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[2]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[3]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[4]').get_property('value') )
            print(dhcpServerSett_ClientConf_IPRange_ini)
            dhcpServerSett_ClientConf_IPRange_fim = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[6]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[7]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[8]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[1]/input[9]').get_property('value'))
            print(dhcpServerSett_ClientConf_IPRange_fim)
            dhcpServerSett_ClientConf_Mask = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/label').text
            print(dhcpServerSett_ClientConf_Mask)
            dhcpServerSett_ClientConf_Mask_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[1]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[2]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[3]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[2]/input[4]').get_property('value') )
            print(dhcpServerSett_ClientConf_Mask_valor)
            dhcpServerSett_ClientConf_Gtw = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/label').text
            print(dhcpServerSett_ClientConf_Gtw)
            dhcpServerSett_ClientConf_Gtw_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[1]').get_property('value') + '.' +
                                                    self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[2]').get_property('value') + '.' +
                                                    self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[3]').get_property('value') + '.' +
                                                    self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[3]/input[4]').get_property('value'))
            print(dhcpServerSett_ClientConf_Gtw_valor)
            dhcpServerSett_ClientConf_DNS = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/label').text
            print(dhcpServerSett_ClientConf_DNS)
            dhcpServerSett_ClientConf_DNS_ini = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[1]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[2]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[3]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[4]').get_property('value'))
            print(dhcpServerSett_ClientConf_DNS_ini)
            dhcpServerSett_ClientConf_DNS_fim = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[6]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[7]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[8]').get_property('value') + '.' +
                                                     self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[4]/input[9]').get_property('value'))
            print(dhcpServerSett_ClientConf_DNS_fim)
            dhcpServerSett_ClientConf_Lease = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[5]/label').text
            print(dhcpServerSett_ClientConf_Lease)
            dhcpServerSett_ClientConf_Lease_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[1]/div[5]/input[1]').get_property('value')
            print(dhcpServerSett_ClientConf_Lease_valor)

            dhcpServerSett_Pool = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/legend').text
            print(dhcpServerSett_Pool)
            dhcpServerSett_Pool_vendorID = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[1]/input[1]').get_attribute('checked') ### VendorID valor
            if dhcpServerSett_Pool_vendorID == 'true':
                dhcpServerSett_Pool_vendorID = 'Habilitado'
            else:
                dhcpServerSett_Pool_vendorID = 'Desabilitado'
            print(dhcpServerSett_Pool_vendorID)
            dhcpServerSett_Pool_vendorID_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[1]/input[2]').get_property('value')
            print(dhcpServerSett_Pool_vendorID_valor)
            dhcpServerSett_Pool_MatchRange = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[2]/span').text
            print(dhcpServerSett_Pool_MatchRange)
            dhcpServerSett_Pool_MatchRange_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if dhcpServerSett_Pool_MatchRange_valor == 'true':
                dhcpServerSett_Pool_MatchRange_valor = 'Include'
            else:
                dhcpServerSett_Pool_MatchRange_valor = 'Exclude'
            print(dhcpServerSett_Pool_MatchRange_valor)
            dhcpServerSett_Pool_MatchMode = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[3]/span').text
            print(dhcpServerSett_Pool_MatchMode)
            dhcpServerSett_Pool_MatchMode_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[3]/input[1]').get_property('value')
            if dhcpServerSett_Pool_MatchMode_valor == '0':
                dhcpServerSett_Pool_MatchMode_valor = 'Exato'
            elif dhcpServerSett_Pool_MatchMode_valor == '1':
                dhcpServerSett_Pool_MatchMode_valor = 'Prefixo'
            elif dhcpServerSett_Pool_MatchMode_valor == '2':
                dhcpServerSett_Pool_MatchMode_valor = 'Sufixo'
            elif dhcpServerSett_Pool_MatchMode_valor == '3':
                dhcpServerSett_Pool_MatchMode_valor = 'Substring'
            print(dhcpServerSett_Pool_MatchMode_valor)
            dhcpServerSett_Pool_clientID = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[4]/input[1]').get_attribute('checked')  ### ClientID valor
            if dhcpServerSett_Pool_clientID == 'true':
                dhcpServerSett_Pool_clientID = 'Habilitado'
            else:
                dhcpServerSett_Pool_clientID = 'Desabilitado'
            print(dhcpServerSett_Pool_clientID)
            dhcpServerSett_Pool_clientID_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[4]/input[2]').get_property('value')
            print(dhcpServerSett_Pool_clientID_valor)
            dhcpServerSett_Pool_MatchRange2 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[5]/span').text
            print(dhcpServerSett_Pool_MatchRange2)
            dhcpServerSett_Pool_MatchRange_valor2 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if dhcpServerSett_Pool_MatchRange_valor2 == 'true':
                dhcpServerSett_Pool_MatchRange_valor2 = 'Include'
            else:
                dhcpServerSett_Pool_MatchRange_valor2 = 'Exclude'
            print(dhcpServerSett_Pool_MatchRange_valor2)
            dhcpServerSett_Pool_UserClassID = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[6]/input[1]').get_attribute('checked') ### UserClassID
            print(dhcpServerSett_Pool_UserClassID)
            if dhcpServerSett_Pool_UserClassID == 'true':
                dhcpServerSett_Pool_UserClassID = 'Habilitado'
            else:
                dhcpServerSett_Pool_UserClassID = 'Desabilitado'
            dhcpServerSett_Pool_UserClassID_valor = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[4]/input[2]').get_property('value')
            print(dhcpServerSett_Pool_UserClassID_valor)
            dhcpServerSett_Pool_MatchRange3 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[5]/span').text
            print(dhcpServerSett_Pool_MatchRange3)
            dhcpServerSett_Pool_MatchRange_valor3 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[7]/input[1]').get_attribute('checked')
            if dhcpServerSett_Pool_MatchRange_valor3 == 'true':
                dhcpServerSett_Pool_MatchRange_valor3 = 'Include'
            else:
                dhcpServerSett_Pool_MatchRange_valor3 = 'Exclude'
            print(dhcpServerSett_Pool_MatchRange_valor3)
            dhcpServerSett_Pool_MAC = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[8]/input').get_attribute('checked')  ### MAC
            print(dhcpServerSett_Pool_MAC)
            if dhcpServerSett_Pool_MAC == 'true':
                dhcpServerSett_Pool_MAC = 'Habilitado'
            else:
                dhcpServerSett_Pool_MAC = 'Desabilitado'
            print(dhcpServerSett_Pool_MAC)
            dhcpServerSett_Pool_MACAddr = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/label').text
            print(dhcpServerSett_Pool_MACAddr)
            dhcpServerSett_Pool_MACAddr_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[1]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[2]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[3]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[4]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[5]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[9]/input[6]').get_property('value') )
            print(dhcpServerSett_Pool_MACAddr_valor)
            dhcpServerSett_Pool_Mask = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/label').text
            print(dhcpServerSett_Pool_Mask)
            dhcpServerSett_Pool_Mask_valor = (self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[1]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[2]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[3]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[4]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[5]').get_property('value') + ':' +
                                                 self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[10]/input[6]').get_property('value'))
            print(dhcpServerSett_Pool_Mask_valor)
            dhcpServerSett_Pool_MatchRange4 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[11]/span').text
            print(dhcpServerSett_Pool_MatchRange4)
            dhcpServerSett_Pool_MatchRange_valor4 = self._driver.find_element_by_xpath('//*[@id="DHCPServerSettingForm"]/div[4]/fieldset[2]/div[11]/input[1]').get_attribute('checked')
            if dhcpServerSett_Pool_MatchRange_valor4 == 'true':
                dhcpServerSett_Pool_MatchRange_valor4 = 'Include'
            else:
                dhcpServerSett_Pool_MatchRange_valor4 = 'Exclude'
            print(dhcpServerSett_Pool_MatchRange_valor4)


            options = self._driver.find_element_by_xpath('//*[@id="DHCPServerShow"]/div/ul/li[4]/a').click()
            options = self._driver.find_element_by_xpath('//*[@id="DHCPServerShow"]/div/ul/li[4]/a').text
            print(options)
            countHeadOptions = len(self._driver.find_elements_by_xpath('//*[@id="Tab4_1"]/table/thead/tr/th'))
            tableHeadoptions = []
            for col in range(2, countHeadOptions+1):
                teste = self._driver.find_element_by_xpath('//*[@id="Tab4_1"]/table/thead/tr/th[' + str(col) + ']').text
                tableHeadoptions.append(teste)
            print(tableHeadoptions)
            countlinhas = len(self._driver.find_elements_by_xpath('//*[@id="Tab4_1"]/table/tbody/tr'))
            countcols = len(self._driver.find_elements_by_xpath('//*[@id="Tab4_1"]/table/tbody/tr[1]/td'))

            tableOptions = []
            for linha in range(1, countlinhas + 1):
                for col in range(2, countcols+1):
                    teste = self._driver.find_element_by_xpath('//*[@id="Tab4_1"]/table/tbody/tr[' + str(linha) + ']/td[' + str(col) + ']').text
                    tableOptions.append(teste)
            print(tableOptions)

            self._driver.quit()

            if porta == '1':
                json_saida464 = {
                    lanSettings_dhcp:
                        {
                            tableHead[0] + ' #' + table[0]:
                                {
                                    tableHead[1]: table[1],
                                    tableHead[2]: table[2],
                                    tableHead[3]: table[3],
                                    tableHead[4]: table[4],
                                    'Detalhes':
                                        {
                                            dhcpServerSett:
                                                {
                                                    dhcpServerSett_AdmState:dhcpServerSett_AdmState_valor,
                                                    dhcpServerSett_AssocIntfc:dhcpServerSett_AssocIntfc_valor,
                                                    dhcpServerSett_Prior:dhcpServerSett_Prior_valor,
                                                    dhcpServerSett_ClientConf:
                                                        {
                                                            dhcpServerSett_ClientConf_IPRange:
                                                                {
                                                                    'inicio':dhcpServerSett_ClientConf_IPRange_ini,
                                                                    'fim':dhcpServerSett_ClientConf_IPRange_fim
                                                                },
                                                            dhcpServerSett_ClientConf_Mask:dhcpServerSett_ClientConf_Mask_valor,
                                                            dhcpServerSett_ClientConf_Gtw:dhcpServerSett_ClientConf_Gtw_valor,
                                                            dhcpServerSett_ClientConf_DNS:
                                                                {
                                                                    'inicio':dhcpServerSett_ClientConf_DNS_ini,
                                                                    'fim':dhcpServerSett_ClientConf_DNS_fim
                                                                },
                                                        dhcpServerSett_ClientConf_Lease:dhcpServerSett_ClientConf_Lease_valor
                                                        },
                                                    dhcpServerSett_Pool:
                                                        {
                                                            'VendorID (Option 60)':dhcpServerSett_Pool_vendorID,
                                                            'valor VendorID':dhcpServerSett_Pool_vendorID_valor,
                                                            dhcpServerSett_Pool_MatchRange:dhcpServerSett_Pool_MatchRange_valor,
                                                            dhcpServerSett_Pool_MatchMode:dhcpServerSett_Pool_MatchMode_valor,
                                                            'ClientID (Option 61)':dhcpServerSett_Pool_clientID,
                                                            'valor ClientID': dhcpServerSett_Pool_clientID_valor,
                                                            dhcpServerSett_Pool_MatchRange2: dhcpServerSett_Pool_MatchRange_valor2,
                                                            'UserClassID (Option 77)':dhcpServerSett_Pool_UserClassID,
                                                            'valor UserClassID':dhcpServerSett_Pool_UserClassID_valor,
                                                            dhcpServerSett_Pool_MatchRange3:dhcpServerSett_Pool_MatchRange_valor3,
                                                            'MAC':dhcpServerSett_Pool_MAC,
                                                            dhcpServerSett_Pool_MACAddr:dhcpServerSett_Pool_MACAddr_valor,
                                                            dhcpServerSett_Pool_Mask:dhcpServerSett_Pool_Mask_valor,
                                                            dhcpServerSett_Pool_MatchRange4:dhcpServerSett_Pool_MatchRange_valor4
                                                        }
                                                },
                                            options:
                                                {
                                                    tableHeadoptions[0] + ' #' + tableOptions[0]:
                                                        {
                                                            tableHeadoptions[1]:tableOptions[1],
                                                            tableHeadoptions[2]: tableOptions[2],
                                                            tableHeadoptions[3]: tableOptions[3],
                                                            tableHeadoptions[4]: tableOptions[4],
                                                        },
                                                    tableHeadoptions[0] + ' #' + tableOptions[5]:
                                                        {
                                                            tableHeadoptions[1]: tableOptions[6],
                                                            tableHeadoptions[2]: tableOptions[7],
                                                            tableHeadoptions[3]: tableOptions[8],
                                                            tableHeadoptions[4]: tableOptions[9]
                                                        }
                                                }
                                        }
                                }
                        }
                }
                if json_saida464['LAN DHCP']['Index #3']['Detalhes']['DHCP Server Setting']['Client Configuration'].get('Gateway') == '192.168.16.1':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": json_saida464, "result":"passed"})
                else:
                    self._dict_result.update({"obs": json_saida464})

                self.update_global_result_memory(flask_username, 'checkLANDHCPSettings_x_464', json_saida464)
                return self._dict_result

            elif porta == '2':
                json_saida464 = {
                    lanSettings_dhcp:
                        {
                            tableHead[0] + ' #' + table[5]:
                                {
                                    tableHead[1]: table[6],
                                    tableHead[2]: table[7],
                                    tableHead[3]: table[8],
                                    tableHead[4]: table[9],
                                    'Detalhes':
                                        {
                                            dhcpServerSett:
                                                {
                                                    dhcpServerSett_AdmState: dhcpServerSett_AdmState_valor,
                                                    dhcpServerSett_AssocIntfc: dhcpServerSett_AssocIntfc_valor,
                                                    dhcpServerSett_Prior: dhcpServerSett_Prior_valor,
                                                    dhcpServerSett_ClientConf:
                                                        {
                                                            dhcpServerSett_ClientConf_IPRange:
                                                                {
                                                                    'inicio': dhcpServerSett_ClientConf_IPRange_ini,
                                                                    'fim': dhcpServerSett_ClientConf_IPRange_fim
                                                                },
                                                            dhcpServerSett_ClientConf_Mask: dhcpServerSett_ClientConf_Mask_valor,
                                                            dhcpServerSett_ClientConf_Gtw: dhcpServerSett_ClientConf_Gtw_valor,
                                                            dhcpServerSett_ClientConf_DNS:
                                                                {
                                                                    'inicio': dhcpServerSett_ClientConf_DNS_ini,
                                                                    'fim': dhcpServerSett_ClientConf_DNS_fim
                                                                },
                                                            dhcpServerSett_ClientConf_Lease: dhcpServerSett_ClientConf_Lease_valor
                                                        },
                                                    dhcpServerSett_Pool:
                                                        {
                                                            'VendorID (Option 60)': dhcpServerSett_Pool_vendorID,
                                                            'valor VendorID': dhcpServerSett_Pool_vendorID_valor,
                                                            dhcpServerSett_Pool_MatchRange: dhcpServerSett_Pool_MatchRange_valor,
                                                            dhcpServerSett_Pool_MatchMode: dhcpServerSett_Pool_MatchMode_valor,
                                                            'ClientID (Option 61)': dhcpServerSett_Pool_clientID,
                                                            'valor ClientID': dhcpServerSett_Pool_clientID_valor,
                                                            dhcpServerSett_Pool_MatchRange2: dhcpServerSett_Pool_MatchRange_valor2,
                                                            'UserClassID (Option 77)': dhcpServerSett_Pool_UserClassID,
                                                            'valor UserClassID': dhcpServerSett_Pool_UserClassID_valor,
                                                            dhcpServerSett_Pool_MatchRange3: dhcpServerSett_Pool_MatchRange_valor3,
                                                            'MAC': dhcpServerSett_Pool_MAC,
                                                            dhcpServerSett_Pool_MACAddr: dhcpServerSett_Pool_MACAddr_valor,
                                                            dhcpServerSett_Pool_Mask: dhcpServerSett_Pool_Mask_valor,
                                                            dhcpServerSett_Pool_MatchRange4: dhcpServerSett_Pool_MatchRange_valor4
                                                        }
                                                },
                                            options:
                                                {
                                                    tableHeadoptions[0] + ' #' + tableOptions[0]:
                                                        {
                                                            tableHeadoptions[1]: tableOptions[1],
                                                            tableHeadoptions[2]: tableOptions[2],
                                                            tableHeadoptions[3]: tableOptions[3],
                                                            tableHeadoptions[4]: tableOptions[4],
                                                        },
                                                    tableHeadoptions[0] + ' #' + tableOptions[5]:
                                                        {
                                                            tableHeadoptions[1]: tableOptions[6],
                                                            tableHeadoptions[2]: tableOptions[7],
                                                            tableHeadoptions[3]: tableOptions[8],
                                                            tableHeadoptions[4]: tableOptions[9]
                                                        }
                                                }
                                        }
                                }
                        }
                }
                if json_saida464['LAN DHCP']['Index #3']['Detalhes']['DHCP Server Setting']['Client Configuration'].get('Gateway') == '192.168.16.1':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": json_saida464, "result":"passed"})
                else:
                    self._dict_result.update({"obs": json_saida464})
                
                self.update_global_result_memory(flask_username, 'checkLANDHCPSettings_x_464', json_saida464)
                return self._dict_result
            elif porta == '3':
                json_saida464 = {
                    lanSettings_dhcp:
                        {
                            tableHead[0] + ' #' + table[10]:
                                {
                                    tableHead[1]: table[11],
                                    tableHead[2]: table[12],
                                    tableHead[3]: table[13],
                                    tableHead[4]: table[14],
                                    'Detalhes':
                                        {
                                            dhcpServerSett:
                                                {
                                                    dhcpServerSett_AdmState: dhcpServerSett_AdmState_valor,
                                                    dhcpServerSett_AssocIntfc: dhcpServerSett_AssocIntfc_valor,
                                                    dhcpServerSett_Prior: dhcpServerSett_Prior_valor,
                                                    dhcpServerSett_ClientConf:
                                                        {
                                                            dhcpServerSett_ClientConf_IPRange:
                                                                {
                                                                    'inicio': dhcpServerSett_ClientConf_IPRange_ini,
                                                                    'fim': dhcpServerSett_ClientConf_IPRange_fim
                                                                },
                                                            dhcpServerSett_ClientConf_Mask: dhcpServerSett_ClientConf_Mask_valor,
                                                            dhcpServerSett_ClientConf_Gtw: dhcpServerSett_ClientConf_Gtw_valor,
                                                            dhcpServerSett_ClientConf_DNS:
                                                                {
                                                                    'inicio': dhcpServerSett_ClientConf_DNS_ini,
                                                                    'fim': dhcpServerSett_ClientConf_DNS_fim
                                                                },
                                                            dhcpServerSett_ClientConf_Lease: dhcpServerSett_ClientConf_Lease_valor
                                                        },
                                                    dhcpServerSett_Pool:
                                                        {
                                                            'VendorID (Option 60)': dhcpServerSett_Pool_vendorID,
                                                            'valor VendorID': dhcpServerSett_Pool_vendorID_valor,
                                                            dhcpServerSett_Pool_MatchRange: dhcpServerSett_Pool_MatchRange_valor,
                                                            dhcpServerSett_Pool_MatchMode: dhcpServerSett_Pool_MatchMode_valor,
                                                            'ClientID (Option 61)': dhcpServerSett_Pool_clientID,
                                                            'valor ClientID': dhcpServerSett_Pool_clientID_valor,
                                                            dhcpServerSett_Pool_MatchRange2: dhcpServerSett_Pool_MatchRange_valor2,
                                                            'UserClassID (Option 77)': dhcpServerSett_Pool_UserClassID,
                                                            'valor UserClassID': dhcpServerSett_Pool_UserClassID_valor,
                                                            dhcpServerSett_Pool_MatchRange3: dhcpServerSett_Pool_MatchRange_valor3,
                                                            'MAC': dhcpServerSett_Pool_MAC,
                                                            dhcpServerSett_Pool_MACAddr: dhcpServerSett_Pool_MACAddr_valor,
                                                            dhcpServerSett_Pool_Mask: dhcpServerSett_Pool_Mask_valor,
                                                            dhcpServerSett_Pool_MatchRange4: dhcpServerSett_Pool_MatchRange_valor4
                                                        }
                                                },
                                            options:
                                                {
                                                    tableHeadoptions[0] + ' #' + tableOptions[0]:
                                                        {
                                                            tableHeadoptions[1]: tableOptions[1],
                                                            tableHeadoptions[2]: tableOptions[2],
                                                            tableHeadoptions[3]: tableOptions[3],
                                                            tableHeadoptions[4]: tableOptions[4],
                                                        },
                                                    tableHeadoptions[0] + ' #' + tableOptions[5]:
                                                        {
                                                            tableHeadoptions[1]: tableOptions[6],
                                                            tableHeadoptions[2]: tableOptions[7],
                                                            tableHeadoptions[3]: tableOptions[8],
                                                            tableHeadoptions[4]: tableOptions[9]
                                                        }
                                                }
                                        }
                                }
                        }
                }
                if json_saida464['LAN DHCP']['Index #3']['Detalhes']['DHCP Server Setting']['Client Configuration'].get('Gateway') == '192.168.16.1':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": json_saida464, "result":"passed"})
                else:
                    self._dict_result.update({"obs": json_saida464})
                self.update_global_result_memory(flask_username, 'checkLANDHCPSettings_x_464', json_saida464)
                return self._dict_result
            elif porta == '4':
                json_saida464 = {
                    lanSettings_dhcp:
                        {
                            tableHead[0] + ' #' + table[15]:
                                {
                                    tableHead[1]: table[16],
                                    tableHead[2]: table[17],
                                    tableHead[3]: table[18],
                                    tableHead[4]: table[19],
                                    'Detalhes':
                                        {
                                            dhcpServerSett:
                                                {
                                                    dhcpServerSett_AdmState: dhcpServerSett_AdmState_valor,
                                                    dhcpServerSett_AssocIntfc: dhcpServerSett_AssocIntfc_valor,
                                                    dhcpServerSett_Prior: dhcpServerSett_Prior_valor,
                                                    dhcpServerSett_ClientConf:
                                                        {
                                                            dhcpServerSett_ClientConf_IPRange:
                                                                {
                                                                    'inicio': dhcpServerSett_ClientConf_IPRange_ini,
                                                                    'fim': dhcpServerSett_ClientConf_IPRange_fim
                                                                },
                                                            dhcpServerSett_ClientConf_Mask: dhcpServerSett_ClientConf_Mask_valor,
                                                            dhcpServerSett_ClientConf_Gtw: dhcpServerSett_ClientConf_Gtw_valor,
                                                            dhcpServerSett_ClientConf_DNS:
                                                                {
                                                                    'inicio': dhcpServerSett_ClientConf_DNS_ini,
                                                                    'fim': dhcpServerSett_ClientConf_DNS_fim
                                                                },
                                                            dhcpServerSett_ClientConf_Lease: dhcpServerSett_ClientConf_Lease_valor
                                                        },
                                                    dhcpServerSett_Pool:
                                                        {
                                                            'VendorID (Option 60)': dhcpServerSett_Pool_vendorID,
                                                            'valor VendorID': dhcpServerSett_Pool_vendorID_valor,
                                                            dhcpServerSett_Pool_MatchRange: dhcpServerSett_Pool_MatchRange_valor,
                                                            dhcpServerSett_Pool_MatchMode: dhcpServerSett_Pool_MatchMode_valor,
                                                            'ClientID (Option 61)': dhcpServerSett_Pool_clientID,
                                                            'valor ClientID': dhcpServerSett_Pool_clientID_valor,
                                                            dhcpServerSett_Pool_MatchRange2: dhcpServerSett_Pool_MatchRange_valor2,
                                                            'UserClassID (Option 77)': dhcpServerSett_Pool_UserClassID,
                                                            'valor UserClassID': dhcpServerSett_Pool_UserClassID_valor,
                                                            dhcpServerSett_Pool_MatchRange3: dhcpServerSett_Pool_MatchRange_valor3,
                                                            'MAC': dhcpServerSett_Pool_MAC,
                                                            dhcpServerSett_Pool_MACAddr: dhcpServerSett_Pool_MACAddr_valor,
                                                            dhcpServerSett_Pool_Mask: dhcpServerSett_Pool_Mask_valor,
                                                            dhcpServerSett_Pool_MatchRange4: dhcpServerSett_Pool_MatchRange_valor4
                                                        }
                                                },
                                            options:
                                                {
                                                    tableHeadoptions[0] + ' #' + tableOptions[0]:
                                                        {
                                                            tableHeadoptions[1]: tableOptions[1],
                                                            tableHeadoptions[2]: tableOptions[2],
                                                            tableHeadoptions[3]: tableOptions[3],
                                                            tableHeadoptions[4]: tableOptions[4],
                                                        },
                                                    tableHeadoptions[0] + ' #' + tableOptions[5]:
                                                        {
                                                            tableHeadoptions[1]: tableOptions[6],
                                                            tableHeadoptions[2]: tableOptions[7],
                                                            tableHeadoptions[3]: tableOptions[8],
                                                            tableHeadoptions[4]: tableOptions[9]
                                                        }
                                                }
                                        }
                                }
                        }
                }
                gateway = json_saida464['LAN DHCP']['Index #3']['Detalhes']['DHCP Server Setting']['Client Configuration'].get('Gateway')
                if gateway == '192.168.16.1':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": f"Gateway: 192.168.16.1", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Gateway: {gateway}"})

                self.update_global_result_memory(flask_username, 'checkLANDHCPSettings_x_464', json_saida464)
                return self._dict_result
        except Exception as e:
            self._dict_result.update({"obs": e})
            return self._dict_result


    def poolDhcpLan_465(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            start_addr = result['LAN DHCP']['Index #3']['Detalhes']['DHCP Server Setting'] \
                         ['Client Configuration']['IP Address Range'].get('inicio')
            end_addr = result['LAN DHCP']['Index #3']['Detalhes']['DHCP Server Setting'] \
                         ['Client Configuration']['IP Address Range'].get('fim')
            if start_addr == '192.168.16.2' and end_addr == '192.168.15.200':
                self._dict_result.update({"obs": 'IP Address Range OK', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": 'IP Address Range NOK'})
        return self._dict_result


    def leaseTime_466(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            ans_466 = result['LAN DHCP']['Index #3']['Detalhes']['DHCP Server Setting'] \
                            ['Client Configuration'].get('Lease Time (seconds)')
            if '14400' == ans_466:
                self._dict_result.update({"obs": 'Lease Time: 14400', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Lease Time: {ans_466}'})      
        return self._dict_result



    def vendorIdIptvEnable_467(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.frame('menuFrm')
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[2]').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        self._driver.find_element_by_xpath('/html/body/fieldset[1]/table/tbody/tr[2]/td[2]/a').click()
        time.sleep(1)

        vendorID = self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[2]/div[1]').text
        vendorID_check = self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[2]/div[1]/input[1]').get_attribute('checked')
        if vendorID_check:
            vendorID_check = 'Habilitado'
        else:
            vendorID_check = 'Desabilitado'
        print(vendorID+': '+vendorID_check)
        vendorValue = self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[2]/div[1]/input[2]').get_attribute('value')
        print(vendorValue)

        print('IP Address Range')
        ipRangeInicioValue = self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[1]').get_attribute('value')+'.'+\
            self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[2]').get_attribute('value')+'.'+\
            self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[3]').get_attribute('value')+'.'+\
            self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[4]').get_attribute('value')   
        print(ipRangeInicioValue)
        ipRangeFimValue = self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[6]').get_attribute('value')+'.'+\
            self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[7]').get_attribute('value')+'.'+\
            self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[8]').get_attribute('value')+'.'+\
            self._driver.find_element_by_xpath('/html/body/fieldset[2]/div/div/div[1]/form/div[4]/fieldset[1]/div[1]/input[9]').get_attribute('value')   
        print(ipRangeFimValue)

        #############################
        json_saida467 = {'LAN DHCP': {'Index 1': {'Detalhes': {'DHCP Server Setting': {'Pool Condition': 
                        {vendorID: vendorID_check, 'valor vendorID': vendorValue}, 'Client Configuration': {'IP Address Range' : {'inicio': ipRangeInicioValue,\
                            'fim': ipRangeFimValue}}}}}}}
        print(json_saida467)
        #############################
        self._driver.quit()

        cpe_config = config_collection.find_one()
        
        #1
        if vendorID_check == 'Habilitado':
            obs_result1 = f'VendorID esta Habilitado'
            self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
        else:
            obs_result1 = f"Teste incorreto, retorno VendorID: {vendorID_check}"

        #2
        if cpe_config['REDE'] == 'VIVO_1':
            if vendorValue == 'MSFT_IPTV,TEF_IPTV':
                obs_result2 = f'Valor VendorID: {vendorValue}'
                self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})

            else:
                obs_result2 = f"Teste incorreto, retorno Valor VendorID: {vendorValue}"
        else:
            obs_result2 = f"REDE:{cpe_config['REDE']}"
        
        #3
        if cpe_config['REDE'] == 'VIVO_2':
        
            if vendorValue == 'GVT-STB,RSTIH89-500_HD,DSTIH78_GVT,VM1110,DSTIH79_GVT,VM1110_HD_HYBRID,DSITH79_GVT_HD':
                obs_result3 = f'Valor VendorID: {vendorValue}'
                self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
            else:
                obs_result3 = f"Teste incorreto, retorno Valor VendorID: {vendorValue}"

        else:
            obs_result3 = f"REDE:{cpe_config['REDE']}"

        self._dict_result.update({"obs": f"467_1: {obs_result1} | 467_2: {obs_result2} | 467_3: {obs_result3}"})

        
        self.update_global_result_memory(flask_username, 'vendorIdIptvEnable_467', json_saida467)
        return self._dict_result


    def poolDhcpIptv_468(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 467 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'vendorIdIptvEnable_467')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 467 primeiro'})
        else:
            ip_inicio = result['LAN DHCP']['Index 1']['Detalhes']['DHCP Server Setting']['Client Configuration']['IP Address Range'].get('inicio')
            ip_fim = result['LAN DHCP']['Index 1']['Detalhes']['DHCP Server Setting']['Client Configuration']['IP Address Range'].get('fim')
            if ip_inicio == '192.168.16.230' and ip_fim == '192.168.16.254':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'IP Address Range: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno IP Address Range: {ip_inicio} | {ip_fim}'})         
        return self._dict_result


    def igmpSnoopingLAN_469(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            for idx, sub_dict in result.items():
                iface_type = sub_dict.get('IP Interface')
                if iface_type.get('IGMP Snooping') == 'Habilitado':
                    self._dict_result.update({"obs": 'IGMP Snooping: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                    break
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno IGMP Snooping: {iface_type.get("IGMP Snooping")}'})
        return self._dict_result


    def verificarWifi24SsidDefault_470(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_ssid = result['Configurações']['Rede Wifi 2.4Ghz']['Básico'].get('SSID:')
            ssid = re.findall("^VIVOFIBRA-\w{4}", result_ssid)
            if ssid:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'SSID: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'SSID: NOK'})
            
        return self._dict_result


    def verificarWifi24Habilitado_471(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            rede_pv = result['Configurações']['Rede Wifi 2.4Ghz']['Básico'].get('Rede Wi-Fi Privada:')
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
            modo_ope = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado'].get('Modo de Operação:')
            if modo_ope == '802.11g/n':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11g/n', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Operação: {modo_ope}'})
  
        return self._dict_result


    def frequencyPlan_473(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.frame('menuFrm')      
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[1]').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        bandwidth24G = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[4]/fieldset/div[3]/label').text
        bandwidth24G_value = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[4]/fieldset/div[3]/select').get_attribute('value')
        if bandwidth24G_value == '1':
            bandwidth24G_value = '20MHz'
        if bandwidth24G_value == '2':
            bandwidth24G_value = '20MHz/40MHz'
        print(bandwidth24G, '=', bandwidth24G_value)

        channel24G = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[4]/fieldset/div[5]/label').text
        channel24G_values = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[4]/fieldset/div[5]/select')
        channel24G_list = [x.get_attribute('value') for x in channel24G_values.find_elements_by_tag_name("option")]
        indice = channel24G_list.index('0')
        channel24G_list[indice] = 'Auto'
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
            if canal == '0':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Canal: 0', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Canal: {canal}'})
            
        return self._dict_result

    def verificarWifi24LarguraBanda_475(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            larg_banda_canal = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado'].get('Largura de Banda do Canal:')
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
            seguranca = result['Configurações']['Rede Wifi 2.4Ghz']['Básico'].get('Modo de Segurança:')
            if seguranca == 'WPA2':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Segurança: WPA2', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Segurança: {seguranca}'})          
        return self._dict_result


    def verificarWifi24PasswordDefault_477(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.frame('menuFrm')      
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/a').click()

        passphrase_value = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/fieldset[1]/div/div[4]/div[1]/input').get_attribute('value')
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
        self._driver.switch_to.frame('menuFrm')      
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/a').click()

        encryption = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/fieldset[1]/div/div[2]/label').text
        encryption_value = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/fieldset[1]/div/div[2]/select').get_attribute('value')
        if encryption_value == '4': encryption_value = "AES"
        print(encryption,"=", encryption_value)
     
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
            wps = result['Configurações']['Rede Wifi 2.4Ghz']['Básico'].get('WPS:')
            if wps == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'WPS: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno WPS: {wps}'})          
        return self._dict_result
    
#### 5GHz ####
    def verificarWifi5SsidDefault_480(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_ssid = result['Configurações']['Rede Wifi 5Ghz']['Básico'].get('SSID:')
            ssid = re.findall("^VIVOFIBRA-\w{4}.*-5G$", result_ssid)
            if ssid:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'SSID: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno SSID: NOK'})
            
        return self._dict_result


    def verificarWifi5Habilitado_481(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            rede_pv = result['Configurações']['Rede Wifi 5Ghz']['Básico'].get('Rede Wi-Fi Privada:')
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
            modo_ope = result['Configurações']['Rede Wifi 5Ghz']['Avançado'].get('Modo de Operação:')
            if modo_ope == '802.11n/ac':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11n/ac', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Modo de Operação: {modo_ope}'})           
        return self._dict_result

    def frequencyPlan5GHz_483(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.frame('menuFrm')      
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        bandwidth5G = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[5]/fieldset/div[3]/label').text
        bandwidth5G_value = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[5]/fieldset/div[3]/select').get_attribute('value')
        if bandwidth5G_value == '1':
            bandwidth5G_value = '20MHz'
        if bandwidth5G_value == '2':
            bandwidth5G_value = '20MHz/40MHz'
        if bandwidth5G_value == '3':
           bandwidth5G_value = '20MHz/40MHz/80MHz'
        print(bandwidth5G, '=', bandwidth5G_value)

        channel5G = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[5]/fieldset/div[4]/label[1]').text
        channel5G_values = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[5]/fieldset/div[4]/select')
        channel5G_list = [x.get_attribute('value') for x in channel5G_values.find_elements_by_tag_name("option")]
        for x in range(0,len(channel5G_list)):
            if int(channel5G_list[x]) >=52 and int(channel5G_list[x]) <=140:
                channel5G_list[x] = channel5G_list[x]+'(DFS)'
        
        indice = channel5G_list.index('0')
        channel5G_list[indice] = 'Auto'
        print(channel5G, '=', channel5G_list)
        self._driver.quit()

        cpe_config = config_collection.find_one()
        

        if bandwidth5G_value == '20MHz':
            ref_list = cpe_config["REF_CHANNEL_5_20MHz"]              
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

       
        if bandwidth5G_value == '20MHz/40MHz':
            ref_list = ref_list = cpe_config["REF_CHANNEL_5_40MHz"]      
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
         
        if bandwidth5G_value == '20MHz/40MHz/80MHz':
            ref_list = ref_list = cpe_config["REF_CHANNEL_5_80MHz"]    
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
            canal = result['Configurações']['Rede Wifi 5Ghz']['Avançado'].get('Canal:')
            if canal == '0':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Canal: 0', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Canal: {canal}'})         
        return self._dict_result

    def verificarWifi5LarguraBanda_485(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            larg_banda_canal = result['Configurações']['Rede Wifi 5Ghz']['Avançado'].get('Largura de Banda do Canal:')
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
            seguranca = result['Configurações']['Rede Wifi 5Ghz']['Básico'].get('Modo de Segurança:')
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
            result_senha = result['Configurações']['Rede Wifi 5Ghz']['Básico'].get('Senha:')
            senha = re.findall("^\w{8}", result_senha)
            if senha:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Senha: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno Senha: NOK'})          
        return self._dict_result

    def cipherModeDefault5GHz_488(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.frame('menuFrm')      
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/a').click()

        encryption = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/fieldset[1]/div/div[2]/label').text
        encryption_value = self._driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/form/fieldset[1]/div/div[2]/select').get_attribute('value')
        self._driver.quit()
        if encryption_value == '4': encryption_value = "AES"
        print(encryption,"=", encryption_value)
     
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
            wps = result['Configurações']['Rede Wifi 5Ghz']['Básico'].get('WPS:')
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
            self._driver.switch_to.frame('menuFrm')
            voiceBasic = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[1]').click()
            voiceBasic = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[1]').text
            print(voiceBasic)
            time.sleep(1)
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('mainFrm')
            voiceBasic_SipService = self._driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
            print(voiceBasic_SipService)
            voiceBasic_SipService_ActOutProxy = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[1]/label[1]').text
            print(voiceBasic_SipService_ActOutProxy)
            voiceBasic_SipService_ActOutProxy_valor = self._driver.find_element_by_xpath('//*[@id="opr_outbound_proxy"]').get_attribute('value')
            print(voiceBasic_SipService_ActOutProxy_valor)
            voiceBasic_SipService_AdmState = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[2]/label').text
            print(voiceBasic_SipService_AdmState)
            voiceBasic_SipService_AdmState_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[2]/input[2]').get_attribute('checked')
            if voiceBasic_SipService_AdmState_valor == 'true':
                voiceBasic_SipService_AdmState_valor = 'Habilitado'
            else:
                voiceBasic_SipService_AdmState_valor = 'Desabilitado'
            print(voiceBasic_SipService_AdmState_valor)
            voiceBasic_SipService_BoundInterface = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[1]/label[1]').text
            print(voiceBasic_SipService_BoundInterface)
            voiceBasic_SipService_BoundInterface_valor = self._driver.find_element_by_xpath('//*[@id="opr_outbound_proxy"]').get_attribute('value')
            print(voiceBasic_SipService_BoundInterface_valor)

            voiceBasic_SipService_SipNet = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/legend').text
            print(voiceBasic_SipService_SipNet)
            voiceBasic_SipService_SipNet_UsrAgtDomain = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/label[1]').text
            print(voiceBasic_SipService_SipNet_UsrAgtDomain)
            voiceBasic_SipService_SipNet_UsrAgtDomain_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/input[1]').get_attribute('value')
            print(voiceBasic_SipService_SipNet_UsrAgtDomain_valor)
            voiceBasic_SipService_SipNet_UsrAgtDomain_port = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/label[2]').text
            print(voiceBasic_SipService_SipNet_UsrAgtDomain_port)
            voiceBasic_SipService_SipNet_UsrAgtDomain_port_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/input[2]').get_attribute('value')
            print(voiceBasic_SipService_SipNet_UsrAgtDomain_port_valor)
            voiceBasic_SipService_SipNet_UsrAgtDomain_Transp = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/label[3]').text
            print(voiceBasic_SipService_SipNet_UsrAgtDomain_Transp)
            voiceBasic_SipService_SipNet_UsrAgtDomain_Transp_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/select').get_attribute('value')
            print(voiceBasic_SipService_SipNet_UsrAgtDomain_Transp_valor)

            voiceBasic_SipService_SipNet_OutProxy = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/label[1]').text
            print(voiceBasic_SipService_SipNet_OutProxy)
            voiceBasic_SipService_SipNet_OutProxy_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/input[1]').get_attribute('value')
            print(voiceBasic_SipService_SipNet_OutProxy_valor)
            voiceBasic_SipService_SipNet_OutProxy_port = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/label[2]').text
            print(voiceBasic_SipService_SipNet_OutProxy_port)
            voiceBasic_SipService_SipNet_OutProxy_port_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/input[2]').get_attribute('value')
            print(voiceBasic_SipService_SipNet_OutProxy_port_valor)

            voiceBasic_SipService_SipNet_RegServer = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/label[1]').text
            print(voiceBasic_SipService_SipNet_RegServer)
            voiceBasic_SipService_SipNet_RegServer_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/input[1]').get_attribute('value')
            print(voiceBasic_SipService_SipNet_RegServer_valor)
            voiceBasic_SipService_SipNet_RegServer_port = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/label[2]').text
            print(voiceBasic_SipService_SipNet_RegServer_port)
            voiceBasic_SipService_SipNet_RegServer_port_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/input[2]').get_attribute('value')
            print(voiceBasic_SipService_SipNet_RegServer_port_valor)
            voiceBasic_SipService_SipNet_RegServer_Transp = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/label[3]').text
            print(voiceBasic_SipService_SipNet_RegServer_Transp)
            voiceBasic_SipService_SipNet_RegServer_Transp_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/select').get_attribute('value')
            print(voiceBasic_SipService_SipNet_RegServer_Transp_valor)

            voiceBasic_SipService_SipNet_ConfCallURL = self._driver.find_element_by_xpath('//*[@id="conference"]/label').text
            print(voiceBasic_SipService_SipNet_ConfCallURL)
            voiceBasic_SipService_SipNet_ConfCallURL_valor = self._driver.find_element_by_xpath('//*[@id="conference"]/input').get_attribute('value')
            print(voiceBasic_SipService_SipNet_ConfCallURL_valor)

            voiceBasic_SipService_SipBasicSettings = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/legend').text
            print(voiceBasic_SipService_SipBasicSettings)
            voiceBasic_SipService_SipBasicSettings_DigiMap = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[1]/label').text
            print(voiceBasic_SipService_SipBasicSettings_DigiMap)
            voiceBasic_SipService_SipBasicSettings_DigiMap_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[1]/textarea').get_attribute('value')
            print(voiceBasic_SipService_SipBasicSettings_DigiMap_valor)
            voiceBasic_SipService_SipBasicSettings_DTMFMeth = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[2]/label').text
            print(voiceBasic_SipService_SipBasicSettings_DTMFMeth)
            voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[2]/select').get_attribute('value')
            if voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor == '1':
                voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = 'InBand'
            elif voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor == '2':
                voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = 'RFC2833'
            elif voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor == '1':
                voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = 'SIPInfo'
            print(voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor)
            voiceBasic_SipService_SipBasicSettings_Hook = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[3]/label').text
            print(voiceBasic_SipService_SipBasicSettings_Hook)
            voiceBasic_SipService_SipBasicSettings_Hook_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[3]/select').get_attribute('value')
            print(voiceBasic_SipService_SipBasicSettings_Hook_valor)
            voiceBasic_SipService_SipBasicSettings_Fax = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[4]/label').text
            print(voiceBasic_SipService_SipBasicSettings_Fax)
            voiceBasic_SipService_SipBasicSettings_Fax_valor = self._driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if voiceBasic_SipService_SipBasicSettings_Fax_valor == 'true':
                voiceBasic_SipService_SipBasicSettings_Fax_valor = 'Habilitado'
            else:
                voiceBasic_SipService_SipBasicSettings_Fax_valor = 'Desabilitado'
            print(voiceBasic_SipService_SipBasicSettings_Fax_valor)

            voiceBasic_LineSettings = self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            time.sleep(1)
            voiceBasic_LineSettings = self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
            print(voiceBasic_LineSettings)
            headcol = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))
            header = []
            for head in range(2, headcol+1):
                teste = self._driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th[' + str(head) + ']').text
                header.append(teste)
            print(header)
            count_linhas = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
            count_cols = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td'))
            voiceBasic_LineSettings_table = []
            for l in range(1, count_linhas+1):
                for c in range(2, count_cols+1):
                    teste = self._driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[' + str(l) + ']/td[' + str(c) + ']').text
                    voiceBasic_LineSettings_table.append(teste)
            print(voiceBasic_LineSettings_table)
            voiceBasic_LineSettings_accessIndex = self._driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td[1]/a').click()
            time.sleep(1)
            voiceBasic_LineSettings_accessIndex_AdmState = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/div/label').text
            print(voiceBasic_LineSettings_accessIndex_AdmState)
            voiceBasic_LineSettings_accessIndex_AdmState_valor = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/div/input[1]').get_attribute('checked')
            if voiceBasic_LineSettings_accessIndex_AdmState_valor == 'true':
                voiceBasic_LineSettings_accessIndex_AdmState_valor = 'Habilitado'
            else:
                voiceBasic_LineSettings_accessIndex_AdmState_valor = 'Desabilitado'
            print(voiceBasic_LineSettings_accessIndex_AdmState_valor)
            voiceBasic_LineSettings_accessIndex_SIPClient = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/legend').text
            print(voiceBasic_LineSettings_accessIndex_SIPClient)
            voiceBasic_LineSettings_accessIndex_SIPClient_URI = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[1]/label').text
            print(voiceBasic_LineSettings_accessIndex_SIPClient_URI)
            voiceBasic_LineSettings_accessIndex_SIPClient_URI_valor = self._driver.find_element_by_xpath('//*[@id="register_uri"]').get_attribute('value')
            print(voiceBasic_LineSettings_accessIndex_SIPClient_URI_valor)
            voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[2]/label').text
            print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser)
            voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser_valor = self._driver.find_element_by_xpath('//*[@id="auth_username"]').get_attribute('value')
            print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser_valor)
            voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[3]/label').text
            print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass)
            voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass_valor = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[3]/input').get_attribute('value')
            print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass_valor)
            voiceBasic_LineSettings_accessIndex_CODEC = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[2]/legend').text
            print(voiceBasic_LineSettings_accessIndex_CODEC)
            voiceBasic_LineSettings_accessIndex_CODEC_VAD = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[2]/div/label').text
            print(voiceBasic_LineSettings_accessIndex_CODEC_VAD)
            voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor = self._driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[2]/div/input[1]').get_attribute('checked')
            if voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor == 'true':
                voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor = 'Habilitado'
            else:
                voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor = 'Desabilitado'
            print(voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor)
            codec_head = self._driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[1]').text
            print(codec_head)
            count_linhas = len(self._driver.find_elements_by_xpath('//*[@id="codec"]/tbody/tr'))
            codec_table = []
            for linha in range(1, count_linhas + 1):
                teste = self._driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[1]').text
                codec_table.append(teste)
            print(codec_table)
            order_head = self._driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[2]').text
            print(order_head)
            order_table = []
            for linha in range(1, count_linhas + 1):
                teste = self._driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[2]/select').get_attribute('value')
                order_table.append(teste)
            print(order_table)
            admState_head = self._driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[3]').text
            print(admState_head)
            admState_table = []
            for linha in range(1, count_linhas + 1):
                teste = self._driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[3]/input').get_attribute('checked')
                admState_table.append(teste)
            print(admState_table)
            ptime_head = self._driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[4]').text
            print(ptime_head)
            ptime_table = []
            for linha in range(1, count_linhas + 1):
                teste = self._driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[4]/select').get_attribute('value')
                if teste == '2':
                    teste = '10'
                elif teste == '4':
                    teste = '20'
                elif teste == '8':
                    teste = '30'
                elif teste == '6':
                    teste = '10,20'
                elif teste == '10':
                    teste = '10,30'
                elif teste == '12':
                    teste = '20,30'
                elif teste == '14':
                    teste = '10,20,30'
                ptime_table.append(teste)
            print(ptime_table)




            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('menuFrm')
            voiceAdvc = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[2]').click()
            time.sleep(1)
            voiceAdvc = self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[2]').text
            print(voiceAdvc)
            self._driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            self._driver.switch_to.frame('mainFrm')
            voiceAdvc_SipServ = self._driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
            print(voiceAdvc_SipServ)

            voiceAdvc_SipServ = self._driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
            print(voiceAdvc_SipServ)
            voiceAdvc_SipServ_AdmState = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[1]/label').text
            print(voiceAdvc_SipServ_AdmState)
            voiceAdvc_SipServ_AdmState_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[1]/input[1]').get_attribute('checked')
            if voiceAdvc_SipServ_AdmState_valor == 'true':
                voiceAdvc_SipServ_AdmState_valor = 'Habilitado'
            else:
                voiceAdvc_SipServ_AdmState_valor = 'Desabilitado'
            print(voiceAdvc_SipServ_AdmState_valor)
            voiceAdvc_SipServ_region = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[2]/label').text
            print(voiceAdvc_SipServ_region)
            voiceAdvc_SipServ_region_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[2]/input').get_attribute('value')
            print(voiceAdvc_SipServ_region_valor)
            voiceAdvc_SipServ_SIPAdv = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/legend').text
            print(voiceAdvc_SipServ_SIPAdv)
            voiceAdvc_SipServ_SIPAdv_RegPeri = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[1]/label').text
            print(voiceAdvc_SipServ_SIPAdv_RegPeri)
            voiceAdvc_SipServ_SIPAdv_RegPeri_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[1]/input').get_attribute('value')
            print(voiceAdvc_SipServ_SIPAdv_RegPeri_valor)
            voiceAdvc_SipServ_SIPAdv_RegRetry = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[2]/label').text
            print(voiceAdvc_SipServ_SIPAdv_RegRetry)
            voiceAdvc_SipServ_SIPAdv_RegRetry_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[2]/input').get_attribute('value')
            print(voiceAdvc_SipServ_SIPAdv_RegRetry_valor)
            voiceAdvc_SipServ_SIPAdv_RegExpi = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[3]/label').text
            print(voiceAdvc_SipServ_SIPAdv_RegExpi)
            voiceAdvc_SipServ_SIPAdv_RegExpi_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[3]/input').get_attribute('value')
            print(voiceAdvc_SipServ_SIPAdv_RegExpi_valor)
            voiceAdvc_SipServ_SIPAdv_SessionExpi = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[4]/label').text
            print(voiceAdvc_SipServ_SIPAdv_SessionExpi)
            voiceAdvc_SipServ_SIPAdv_SessionExpi_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[4]/input').get_attribute('value')
            print(voiceAdvc_SipServ_SIPAdv_SessionExpi_valor)
            voiceAdvc_SipServ_SIPAdv_MinSession = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[5]/label').text
            print(voiceAdvc_SipServ_SIPAdv_MinSession)
            voiceAdvc_SipServ_SIPAdv_MinSession_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[5]/input').get_attribute('value')
            print(voiceAdvc_SipServ_SIPAdv_MinSession_valor)
            voiceAdvc_SipServ_SIPAdv_DSCPSIP = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[6]/label').text
            print(voiceAdvc_SipServ_SIPAdv_DSCPSIP)
            voiceAdvc_SipServ_SIPAdv_DSCPSIP_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[6]/input').get_attribute('value')
            print(voiceAdvc_SipServ_SIPAdv_DSCPSIP_valor)
            voiceAdvc_SipServ_SIPAdv_DSCPRTP = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[7]/label').text
            print(voiceAdvc_SipServ_SIPAdv_DSCPRTP)
            voiceAdvc_SipServ_SIPAdv_DSCPRTP_valor = self._driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[7]/input').get_attribute('value')
            print(voiceAdvc_SipServ_SIPAdv_DSCPRTP_valor)

            voiceAdvc_Line = self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            time.sleep(1)
            voiceAdvc_Line = self._driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
            print(voiceAdvc_Line)
            headcol = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))
            header2 = []
            for head in range(2, headcol + 1):
                teste = self._driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th[' + str(head) + ']').text
                header2.append(teste)
            print(header2)
            count_linhas = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
            count_cols = len(self._driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td'))
            voiceAdvc_Line_table = []
            for l in range(1, count_linhas + 1):
                for c in range(2, count_cols + 1):
                    teste = self._driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[' + str(l) + ']/td[' + str(c) + ']').text
                    voiceAdvc_Line_table.append(teste)
            print(voiceAdvc_Line_table)
            json_saida490 = {
                voiceBasic:
                    {
                        voiceBasic_SipService:
                            {
                                voiceBasic_SipService_ActOutProxy:voiceBasic_SipService_ActOutProxy_valor,
                                voiceBasic_SipService_AdmState:voiceBasic_SipService_AdmState_valor,
                                voiceBasic_SipService_BoundInterface:voiceBasic_SipService_BoundInterface_valor
                            },
                        voiceBasic_SipService_SipNet:
                            {
                                voiceBasic_SipService_SipNet_UsrAgtDomain:voiceBasic_SipService_SipNet_UsrAgtDomain_valor,
                                voiceBasic_SipService_SipNet_UsrAgtDomain_port:voiceBasic_SipService_SipNet_UsrAgtDomain_port_valor,
                                voiceBasic_SipService_SipNet_UsrAgtDomain_Transp:voiceBasic_SipService_SipNet_UsrAgtDomain_Transp_valor,
                                voiceBasic_SipService_SipNet_OutProxy:voiceBasic_SipService_SipNet_OutProxy_valor,
                                voiceBasic_SipService_SipNet_OutProxy_port:voiceBasic_SipService_SipNet_OutProxy_port_valor,
                                voiceBasic_SipService_SipNet_RegServer:voiceBasic_SipService_SipNet_RegServer_valor,
                                voiceBasic_SipService_SipNet_RegServer_port:voiceBasic_SipService_SipNet_RegServer_port_valor,
                                voiceBasic_SipService_SipNet_RegServer_Transp:voiceBasic_SipService_SipNet_RegServer_Transp_valor,
                                voiceBasic_SipService_SipNet_ConfCallURL:voiceBasic_SipService_SipNet_ConfCallURL_valor
                            },
                        voiceBasic_SipService_SipBasicSettings:
                            {
                                voiceBasic_SipService_SipBasicSettings_DigiMap:voiceBasic_SipService_SipBasicSettings_DigiMap_valor,
                                voiceBasic_SipService_SipBasicSettings_DTMFMeth:voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor,
                                voiceBasic_SipService_SipBasicSettings_Hook:voiceBasic_SipService_SipBasicSettings_Hook_valor,
                                voiceBasic_SipService_SipBasicSettings_Fax:voiceBasic_SipService_SipBasicSettings_Fax_valor
                            },
                        voiceBasic_LineSettings:
                            {
                                header[0]:voiceBasic_LineSettings_table[0],
                                header[1]: voiceBasic_LineSettings_table[1],
                                header[2]: voiceBasic_LineSettings_table[2],
                                header[3]: voiceBasic_LineSettings_table[3],
                                header[4]: voiceBasic_LineSettings_table[4],
                                "Access Index #0":
                                    {
                                        voiceBasic_LineSettings_accessIndex_AdmState:voiceBasic_LineSettings_accessIndex_AdmState_valor,
                                        voiceBasic_LineSettings_accessIndex_SIPClient:
                                            {
                                                voiceBasic_LineSettings_accessIndex_SIPClient_URI:voiceBasic_LineSettings_accessIndex_SIPClient_URI_valor,
                                                voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser:voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser_valor,
                                                voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass:voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass_valor,
                                            },
                                        voiceBasic_LineSettings_accessIndex_CODEC:
                                            {
                                                voiceBasic_LineSettings_accessIndex_CODEC_VAD:voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor,
                                                codec_head:
                                                    {
                                                        codec_table[0]:
                                                            {
                                                                order_head:order_table[0],
                                                                admState_head:admState_table[0],
                                                                ptime_head:ptime_table[0]
                                                            },
                                                        codec_table[1]:
                                                            {
                                                                order_head: order_table[1],
                                                                admState_head: admState_table[1],
                                                                ptime_head: ptime_table[1]
                                                            },
                                                        codec_table[2]:
                                                            {
                                                                order_head: order_table[2],
                                                                admState_head: admState_table[2],
                                                                ptime_head: ptime_table[2]
                                                            }
                                                    }
                                            }
                                    }
                            }
                    },
                voiceAdvc:
                    {
                        voiceAdvc_SipServ:
                            {
                                voiceAdvc_SipServ_AdmState: voiceAdvc_SipServ_AdmState_valor,
                                voiceAdvc_SipServ_region: voiceAdvc_SipServ_region_valor,
                                voiceAdvc_SipServ_SIPAdv:
                                    {
                                        voiceAdvc_SipServ_SIPAdv_RegPeri: voiceAdvc_SipServ_SIPAdv_RegPeri_valor,
                                        voiceAdvc_SipServ_SIPAdv_RegRetry: voiceAdvc_SipServ_SIPAdv_RegRetry_valor,
                                        voiceAdvc_SipServ_SIPAdv_RegExpi: voiceAdvc_SipServ_SIPAdv_RegExpi_valor,
                                        voiceAdvc_SipServ_SIPAdv_SessionExpi: voiceAdvc_SipServ_SIPAdv_SessionExpi_valor,
                                        voiceAdvc_SipServ_SIPAdv_MinSession: voiceAdvc_SipServ_SIPAdv_MinSession_valor,
                                        voiceAdvc_SipServ_SIPAdv_DSCPSIP: voiceAdvc_SipServ_SIPAdv_DSCPSIP_valor,
                                        voiceAdvc_SipServ_SIPAdv_DSCPRTP: voiceAdvc_SipServ_SIPAdv_DSCPRTP_valor
                                    }
                            },
                        voiceAdvc_Line:
                            {
                                header2[0]: voiceAdvc_Line_table[0],
                                header2[1]: voiceAdvc_Line_table[1],
                                header2[2]: voiceAdvc_Line_table[2],
                                header2[3]: voiceAdvc_Line_table[3]
                            }
                    }
            }

            self._driver.quit()
            basic_setting = json_saida490['Basic']['SIP Basic Setting']

            cpe_config = config_collection.find_one()
            
            for idx, sub_dict in basic_setting.items():
                if cpe_config['REDE'] == 'VIVO_1':
                    if idx == 'Fax T38':
                        if sub_dict == 'Desabilitado':
                            obs_result1 =  f"Fax T38: Desabilitado"
                            self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                            break
                        else:
                            obs_result1 = f"Teste incorreto, retorno Fax T38: {sub_dict}"
                            break
                    else:
                        obs_result1 = f"Teste incorreto, retorno {idx}"
                else: 
                    obs_result1 = f"REDE:{cpe_config['REDE']}"
                
                if cpe_config['REDE'] == 'VIVO_2':
                    if idx == 'Fax T38':
                        if sub_dict == 'Desabilitado':
                            obs_result2 =  f"Fax T38: Desabilitado"
                            self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                            break
                        else:
                            obs_result2 = f"Teste incorreto, retorno Fax T38: {sub_dict}"
                            break
                    else:
                        obs_result2 = f"Teste incorreto, retorno {idx}"
                else: 
                    obs_result2 = f"REDE:{cpe_config['REDE']}"
        except Exception as e:
            self._dict_result.update({"obs": str(e)})
        finally:
            self._dict_result.update({"obs": f"490_1: {obs_result1} | 490_2: {obs_result2}"})
            
            self.update_global_result_memory(flask_username, 'checkVoIPSettings_490', json_saida490)
            return self._dict_result


    def verificarDtmfMethod_491(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            basic_setting = result['Basic']['SIP Basic Setting']
            for idx, sub_dict in basic_setting.items():
                if idx == 'DTMF Method':
                    if sub_dict == 'RFC2833':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "DTMF Method: RFC2833", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno DTMF Method: {sub_dict}"})
                        break
                else:
                    self._dict_result.update({"obs": "DTMF Method não existe"})
        return self._dict_result
    

    def prioridadeCodec_0_493(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            list_codec = result['Basic']['Line Setting']['Access Index #0']['Codec']['Codec']
            for keys in list_codec:
                prior_codec = list_codec[keys].get('Order')
                print('order', prior_codec)
                if prior_codec == '0':
                    if keys == 'G.711ALaw':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Order: 0 = G.711ALaw", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Order: 0 = {keys} "})
                        break
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Order: {prior_codec}"})
        return self._dict_result


    def prioridadeCodec_1_494(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            list_codec = result['Basic']['Line Setting']['Access Index #0']['Codec']['Codec']
            for keys in list_codec:
                prior_codec = list_codec[keys].get('Order')
                if prior_codec == '1':
                    if keys == 'G.729':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Order: 1 = G.729", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Order: 1 = {keys} "})
                        break
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Order: {prior_codec}"})
        return self._dict_result


    def checkNATALGSettings_495(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.frame('menuFrm')      
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[3]').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        sip = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/input[4]').get_attribute('value') 
        time.sleep(1)
        self._driver.quit()
        
        if sip == 'on': sip = 'Habilitado'
        else: ' Desabilitado'
        print('SIP = ', sip)

        cpe_config = config_collection.find_one()
        rede = cpe_config['REDE']

        if rede == 'VIVO_1':   
            if sip == 'Desabilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": f'SIP: Desabilitado (Rede = {rede})', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno SIP: {sip} (Rede = {rede})'})
            return self._dict_result

        elif rede == 'VIVO_2':   
            if sip == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": f'SIP == Habilitado (Rede = {rede})', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno SIP: {sip} (Rede = {rede})'})
            return self._dict_result 
        
        else:
            self._dict_result.update({"obs": f'REDE: {rede})'})
            return self._dict_result
        

    def checkUPnP_497(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.frame('menuFrm')      
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[8]/a').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('mainFrm')
        upnp = self._driver.find_element_by_xpath('/html/body/div/fieldset/form/div[1]/input[1]').get_attribute('value')
 
        if upnp == '1': upnp = 'Habilitado'
        else: upnp = 'Desabilitado'
        
        if upnp == 'Habilitado':
            self._dict_result.update({"Resultado_Probe": "OK", "obs": 'UPnP: Habilitado', "result":"passed"})
        else:
            self._dict_result.update({"obs": f'Teste incorreto, retorno UPnP: {upnp}'})

        self._driver.quit()
        
        return self._dict_result


    def linkLocalType_498(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            linkLocal = result['Status']['Internet']['IPv6']['Endereço IPv6 Link-Local - LAN:'].split('/')[1]
            if linkLocal == '64':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "link local: 64", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno link local: {linkLocal}"})

        return self._dict_result


    def lanGlobalType_499(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            linkGlobal = result['Status']['Internet']['IPv6']['Endereço IPv6 Global - WAN:']
            try: 
                if linkGlobal.split('/')[1] == '64':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "LAN global identifier: 64", "result":"passed"})
            except:
                self._dict_result.update({"obs": f"Teste incorreto, retorno LAN global identifier: {linkGlobal}"})
        return self._dict_result


    def prefixDelegationfromInet_500(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            ans_500 = result['LAN Setting']['IPv6']['RADVD'].get('Prefix Delegation WAN')
            if 'ip2' == ans_500:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: ip2", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Prefix Delegation WAN: {ans_500}"})
        return self._dict_result

