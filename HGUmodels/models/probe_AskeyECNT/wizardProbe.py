from audioop import lin2lin
from gc import collect
from http import client
from re import sub
import re
import time
from datetime import datetime
import urllib
# from turtle import up
# from tkinter.messagebox import NO
from ..AskeyECNT import HGU_AskeyECNT
from json import JSONEncoder
import json
import requests
import sys
import pandas as pd
from pyzbar.pyzbar import decode
from PIL import Image
from collections import namedtuple
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException
from selenium.webdriver.support.ui import Select

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

class HGU_AskeyECNT_wizardProbe(HGU_AskeyECNT):


    # 373
    def accessWizard_373(self, flask_username):
            #TODO: Fazer logica no frontend para garantir que o teste 401 seja executado em conjunto
            result = session.get_result_from_test(flask_username, 'accessWizard_401')
            if len(result) == 0:
                self._dict_result.update({"obs": 'Execute o teste 401 primeiro'})
            else:
                ans_500 = result['Resultado_Probe']
                if 'OK' == ans_500:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Teste OK", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno: {ans_500}"})
            return self._dict_result


    # 374
    def logoutWizard_374(self, flask_username):
        try:
            self.doLogin()
            try:
                self._driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a').click()
                self._dict_result.update({"obs": "Logout efetuado com sucesso", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Nao foi possivel efetuar o logout"})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result


    # 375
    def checkRedeGpon_375(self, flask_username):
        try:
            self.doLogin()
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            time.sleep(1)
            gpon = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]//div')]
            dict_saida = {
                "Status":
                    {
                        gpon:
                            {div[0].split(':')[0]: div[0].split(':')[1],
                            div[1].split(':')[0]: div[1].split(':')[1],
                            div[2].split(':')[0]: div[2].split(':')[1],
                            }
                    }
            }
            print(dict_saida)
            link = dict_saida['Status']['GPON']['Link']
            self._driver.quit()

            if link == 'Não Estabelecido':
                self._dict_result.update({"obs": "Link: Não Estabelecido", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Link: {link}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self.update_global_result_memory(flask_username, 'checkRedeGpon_375', dict_saida)
            return self._dict_result
    

    # 376
    def changePPPoESettingsWrong_376(self, flask_username):
        try:
            self.doLogin()
            config = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            time.sleep(1)
            config_internet = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
            self._driver.find_element_by_xpath('//*[@id="btnSave"]').click()
            time.sleep(1)
            try:
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/span') or self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/span'):
                    self._dict_result.update({"obs": "Verificacao OK", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Teste falhou"})
            self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  


    # 377
    def changePPPoESettingsWrong_377(self, flask_username):
        try:
            self.doLogin()
            config = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            time.sleep(1)
            config_internet = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').send_keys('vivo@cliente')
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys('vivo')
            self._driver.find_element_by_xpath('//*[@id="btnSave"]').click()
            time.sleep(15)
            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td/label/font').text == 'Conectado':
                    if self._driver.find_element_by_xpath('//*[@id="txtUsername"]').get_attribute('value') == 'vivo@cliente':
                        self._dict_result.update({"obs": "Usuario aceito"})
                    else:
                        self._dict_result.update({"obs": f"Teste falhou, usuario nao foi aceito", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  


    #378
    def changePPPoESettingsWrongAuthentication_378(self, flask_username):
        try:
            self.doLogin()
            config = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            time.sleep(1)
            config_internet = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').send_keys('cliente@cliente')
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys('vivo')
            self._driver.find_element_by_xpath('//*[@id="btnSave"]').click()
            time.sleep(15)
            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td/label/font').text == 'Conectado':
                    if self._driver.find_element_by_xpath('//*[@id="txtUsername"]').get_attribute('value') == 'cliente@cliente':
                        self._dict_result.update({"obs": "Usuario aceito"})
                    else:
                        self._dict_result.update({"obs": f"Erro de autenticacao com as credenciais PPPoE inseridas pelo usuario.", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  


    # 379
    def connectWizardhttps_379(self,flask_username):
        try:
            try:
                self._driver.get('https://' + self._address_ip + '/')
                time.sleep(1)
                self._dict_result.update({"obs": "Acesso via HTTPS OK", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Nao foi possivel acessar via HTTPS"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})
        
        finally:
            self._driver.quit()
            return self._dict_result


    # 380
    def checkPPPoEStatus_380(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/index_cliente.asp')
            time.sleep(1)
            gpon = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]//div')]
            dict_saida = {
                "Status":
                    {
                        gpon:
                            {div[0].split(':')[0]: div[0].split(':')[1],
                            div[1].split(':')[0]: div[1].split(':')[1],
                            div[2].split(':')[0]: div[2].split(':')[1],
                            }
                    }
            }
            print(dict_saida)
            self._dict_result.update({"obs": dict_saida, "result":"passed", "Resultado_Probe": "OK"})
        except NoSuchElementException as exception:
            self._dict_result.update({"obs": 'É necessário fazer o login para visualizar o status.'})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result


    #381
    def getFullConfig_381(self, flask_username):
        dict_saida = {}
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="menu-loc-net"]/ul/li[1]/a').click()
            self._driver.quit()
            
            dict_saida = {"Resultado_Probe": "NOK"}
            self._dict_result.update({"obs": "Usuario acessou as configuracoes sem estar logado"})
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            dict_saida = {"Resultado_Probe": "OK"}
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Nao foi possivel acessar as configuracoes sem logar'})

        finally:
            self.update_global_result_memory(flask_username, 'accessWizard_381', dict_saida)
            return self._dict_result


    # 382
    def getFullConfig_382(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            idioma = result['Gerenciamento']['Idioma']
            if idioma == 'Português':
                self._dict_result.update({"obs": "Idioma: Português", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Idioma: {idioma}"})
        return self._dict_result


    # 384
    def execPingWizard_384(self, flask_username):

        destino = '8.8.8.8',
        tentativas = "1"
        try:
            self.doLogin()
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[6]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="txtDest"]').send_keys(destino)
            self._driver.find_element_by_xpath('//*[@id="txtNum"]').send_keys(tentativas)
            self._driver.find_element_by_xpath('//*[@id="btnTest"]').click()
            time.sleep(5)
            result = self._driver.find_element_by_xpath('//*[@id="txtResult"]').get_property('value')
            self._driver.quit()
            self._dict_result.update({"obs": f"Resultado: {result}", "result":"passed", "Resultado_Probe": "OK"})
        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})

        finally:
            return self._dict_result


    # 385
    def qrCodeTest_385(self, flask_username):
        ssid_2g_exp = 'VIVO automacao 2GHz'
        pass_2g_exp = 'vivo12345678910'

        ssid_5g_exp = 'VIVO automacao 5GHz'
        pass_5g_exp = 'vivo12345678910'

        try:
            # Entering on WiFi 2.4GHz settings and sign in
            self.doLogin()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[3]/a').click()
            time.sleep(10)

            # Enabling WiFi
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)

            # Checking initial QR Code and changing Settings 2.4GHz WiFi
            initial_qrCode_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/initial-qr-code-askey-ecnt-2ghz.png', 'wb') as file:
                file.write(initial_qrCode_2g.screenshot_as_png)
            time.sleep(3)
            data = decode(Image.open('data/initial-qr-code-askey-ecnt-2ghz.png'))
            initial_2g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\n##################################')
            print('Valores iniciais QR Code 2.4GHz:')
            print(initial_2g)
            select = Select(self._driver.find_element_by_id('selAuthMode'))
            select.select_by_visible_text('WPA2')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[2]/input[1]').click()
            time.sleep(1)
            input_ssid_2ghz = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_password_2ghz = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_ssid_2ghz.clear()
            time.sleep(1)
            input_ssid_2ghz.send_keys(ssid_2g_exp)
            time.sleep(1)
            input_password_2ghz.clear()
            time.sleep(1)
            input_password_2ghz.send_keys(pass_2g_exp)
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            try:
                self._driver.switch_to.alert.accept()
            except Exception as e:
                pass
            time.sleep(30)

            # Cheking the new QR Code
            final_qrCode_2g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/final-qr-code-askey-ecnt-2ghz.png', 'wb') as file:
                file.write(final_qrCode_2g.screenshot_as_png)
            time.sleep(1)
            data = decode(Image.open('data/final-qr-code-askey-ecnt-2ghz.png'))
            result_2g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\nValores finais QR Code 2.4GHz:')
            print(result_2g)
            print('##################################\n')
            time.sleep(5)
           
            # Entering on WiFi 5GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[4]/a').click()
            time.sleep(4)

            # Enabling WiFi
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)

            # Checking initial QR Code and changing Settings 5GHz WiFi
            initial_qrCode_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/initial-qr-code-askey-ecnt-5ghz.png', 'wb') as file:
                file.write(initial_qrCode_5g.screenshot_as_png)
            time.sleep(3)
            data = decode(Image.open('data/initial-qr-code-askey-ecnt-5ghz.png'))
            initial_5g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\n##################################')
            print('Valores iniciais QR Code 5GHz:')
            print(initial_5g)
            select = Select(self._driver.find_element_by_id('selAuthMode'))
            select.select_by_visible_text('WPA2')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[6]/td[2]/input[1]').click()
            time.sleep(1)
            input_ssid_5ghz = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/input')
            input_password_5ghz = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[2]/input')
            input_ssid_5ghz.clear()
            time.sleep(1)
            input_ssid_5ghz.send_keys(ssid_5g_exp)
            time.sleep(1)
            input_password_5ghz.clear()
            time.sleep(1)
            input_password_5ghz.send_keys(pass_5g_exp)
            time.sleep(1)
            self._driver.find_element_by_id('btnBasSave').click()
            try:
                self._driver.switch_to.alert.accept()
            except Exception as e:
                pass
            time.sleep(30)

            # Cheking the new QR Code
            final_qrCode_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/final-qr-code-askey-ecnt-5ghz.png', 'wb') as file:
                file.write(final_qrCode_5g.screenshot_as_png)
            time.sleep(1)
            data = decode(Image.open('data/final-qr-code-askey-ecnt-5ghz.png'))
            result_5g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\nValores finais QR Code 5GHz:')
            print(result_5g)
            print('##################################\n')
            time.sleep(5)

            # Checking results:
            if result_2g[1][2:] != ssid_2g_exp:
                self._dict_result.update({'obs': f'O SSID do WiFi 2.4GHz não foi alterado corretamente (esperado: {ssid_2g_exp}; obtido: {result_2g[1][2:]})'})
            elif result_2g[0][2:] != 'WPA':
                self._dict_result.update({'obs': f'O modo de segurança do WiFi 2.4GHz não foi alterado corretamente (esperado: WPA; obtido: {result_2g[0][2:]})'})
            elif result_2g[2][2:] != pass_2g_exp:
                self._dict_result.update({'obs': f'A senha do WiFi 2.4GHz não foi alterada corretamente (esperado: {pass_2g_exp}; obtido: {result_2g[2][2:]})'})
            
            elif result_5g[1][2:] != ssid_5g_exp:
                self._dict_result.update({'obs': f'O SSID do WiFi 5GHz não foi alterado corretamente (esperado: {ssid_5g_exp}; obtido: {result_5g[1][2:]})'})
            elif result_5g[0][2:] != 'WPA':
                self._dict_result.update({'obs': f'O modo de segurança do WiFi 5GHz não foi alterado corretamente (esperado: WPA; obtido: {result_5g[0][2:]})'})
            elif result_5g[2][2:] != pass_5g_exp:
                self._dict_result.update({'obs': f'A senha do WiFi 5GHz não foi alterada corretamente (esperado: {pass_5g_exp}; obtido: {result_5g[2][2:]})'})
            else:
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

        except Exception as e:
            self._dict_result.update({'obs': f'{e}'})

        self._driver.quit()
        return self._dict_result


    #386
    def statusWizardIptv_386(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status24 = result['Status']['Wi-Fi 2,4 GHz']
            status5 = result['Status']['Wi-Fi 5 GHz']
            wifi24 = wizard_config.WIFI24
            wifi5 = wizard_config.WIFI5
            if set(status24) == set(wifi24) and set(status5) == set(wifi5):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno WI-FI 2.4 GHz: {status24 and status5}"})
            
        return self._dict_result


    # 387
    def statusWizardInet_387(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            statusInternet = result['Status']['Internet']
            ppp, ipv4, ipv4_wizard_list = statusInternet['PPP:'], statusInternet['IPv4'], wizard_config.INTERNET_IPV4

            ipv6, ipv6_wizard_list = statusInternet['IPv6'], wizard_config.INTERNET_IPV6

            if set(ipv4) == set(ipv4_wizard_list) and set(ipv6) == set(ipv6_wizard_list) and ppp != '':
                self._dict_result.update({"obs": "Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste inscorreto, retorno PPP: {ppp} IPv4: {ipv4} | IPv6: {ipv6}"})

        return self._dict_result


    # 388
    def registerWizardVoip_388(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            ifaceVoip = result['Status']['Telefone']['Rede:']
            registerVoIP = result['Status']['Telefone']['Telefone:']

            if ifaceVoip == 'Disponível' and (registerVoIP != 'Não Registrado' or registerVoIP == ''):
                self._dict_result.update({"obs": f"Rede: Disponível | Telefone: {registerVoIP}", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Rede: Disponível | Telefone: {registerVoIP}"})

        return self._dict_result


    # 389
    def statusWizardIptv_389(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['TV']
            iptv = wizard_config.IPTV
            if set(status) == set(iptv):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno TV: {status}"})
            
        return self._dict_result


    # 390
    def statusWizardVoip_390(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['Telefone']
            voip = wizard_config.VOIP_AE

            if set(status) == set(voip):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno VoIP: {status}"})
            
        return self._dict_result

    
    #391 
    def statusWizardHpna_391(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['Telefone']
            voip = wizard_config.VOIP_AE

            if set(status) == set(voip):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno VoIP: {status}"})
            
        return self._dict_result


    # 392
    def verifyDnsService_392(self, flask_username):
        try:
            self.doLogin()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
            # Enabling DNS
            self._driver.find_element_by_id('radDhcpDnsEn1').click()
            # Entering primary DNS
            prim_dns_1 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[8]/td[2]/input[1]')
            prim_dns_1.send_keys('8')
            prim_dns_2 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[8]/td[2]/input[2]')
            prim_dns_2.send_keys('8')
            prim_dns_3 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[8]/td[2]/input[3]')
            prim_dns_3.send_keys('8')
            prim_dns_4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[8]/td[2]/input[4]')
            prim_dns_4.send_keys('8')
            # Entering Secondary DNS
            sec_dns_1 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[9]/td[2]/input[1]')
            sec_dns_1.send_keys('8')
            sec_dns_2 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[9]/td[2]/input[2]')
            sec_dns_2.send_keys('8')
            sec_dns_3 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[9]/td[2]/input[3]')
            sec_dns_3.send_keys('4')
            sec_dns_4 = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[9]/td[2]/input[4]')
            sec_dns_4.send_keys('4')
            self._driver.find_element_by_id('btnDhcpSave').click()
            time.sleep(1)
            # Desabling DNS
            self._driver.find_element_by_id('radDhcpDnsEn0').click()
            self._driver.find_element_by_id('btnDhcpSave').click()
            time.sleep(1)

            # Checking if primary DNS fields are available
            if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[8]/td[2]/input[1]') == None:
                return self._dict_result
            else:
                return self._dict_result.update({"obs": "Servi;o DNS habilitado com sucesso", "result":"passed", "Resultado_Probe": "OK"})
        
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result 
            

    #393 
    def createDmzViaWizard_393(self, flask_username):
        try:
            self.doLogin()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[3]/a').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[5]/table/tbody/tr[2]/td[2]/input[1]').click()
            self._driver.find_element_by_xpath('//*[@id="txtDmzHostAddress"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtDmzHostAddress"]').send_keys('192.168.15.30')
            self._driver.find_element_by_xpath('//*[@id="aDmzHostSave"]').click()
            time.sleep(5)

            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('//*[@id="txtDmzHostAddress"]').text != 'Please, type a valid IP address.':
                    self._dict_result.update({"obs": f"Criacao de DMZ realizada com sucesso.", "result":"passed", "Resultado_Probe": "OK"})
                else:
                    self._dict_result.update({"obs": f"Erro de criacao de DMZ.", "result":"passed", "Resultado_Probe": "NOK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  
    

    #395 
    def configUpnpViaWizard_395(self, flask_username):
        try:
            self.doLogin()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[4]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="radUpnpEn1"]').click()
            #self._driver.find_element_by_xpath('//*[@id="txtDmzHostAddress"]').clear()
            #self._driver.find_element_by_xpath('//*[@id="txtDmzHostAddress"]').send_keys('192.168.15.30')
            self._driver.find_element_by_xpath('//*[@id="btnUpnpSave"]').click()
            time.sleep(1)

            try:
                #verificar se tem como validar configuracao UPnP
                self._dict_result.update({"obs": f"Configuracao de UPnP realizada com sucesso.", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  


    #396 mlv
    def configDdnsViaWizard_396(self, flask_username):
        """
            Provides DDnS Settings
        :return : A dict with the result of the test
        """
        try:
            self.doLogin()
            # Sentting DDnS
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[5]/a').click() #DDNS
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[7]/table/tbody/tr[2]/td[2]/input[1]').click()
            user_field = self._driver.find_element_by_xpath('//*[@id="idDdnsUsername"]')
            user_field.clear()
            user_field.send_keys('telefonica.labs@gmail.com')
            pass_field = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[7]/table/tbody/tr[5]/td[2]/input')
            pass_field.clear()
            pass_field.send_keys('vivo@123')
            hostname_field = self._driver.find_element_by_xpath('//*[@id="idDdnsHostName"]')
            hostname_field.clear()
            hostname_field.send_keys('telefonicalabs.ddns.net')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[7]/table/tbody/tr[7]/td/a[2]/span').click()
            time.sleep(1)
            # Disabling DDNS
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[7]/table/tbody/tr[2]/td[2]/input[2]').click()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[7]/table/tbody/tr[7]/td/a[2]/span').click()

            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('//*[@id="idDdnsUsername"]').is_enabled != True:
                    self._dict_result.update({"obs": f"Criacao de DMZ realizada com sucesso.", "result":"passed", "Resultado_Probe": "OK"})
                else:
                    self._dict_result.update({"obs": f"Erro de criacao de DMZ.", "result":"passed", "Resultado_Probe": "NOK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  
    

    #397
    def configIpDhcpViaWizard_397(self, flask_username):
        try:
            self.doLogin()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[1]/a').click() #DHCP
            time.sleep(1)
            print('passou aqui 1')

            self._driver.find_element_by_id('txtStaticMac').click()
            print('passou aqui 2')

            self._driver.find_element_by_xpath('//*[@id="txtStaticMac"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtStaticMac"]').send_keys('C8:B4:22:E6:86:71')
            print('passou aqui 3')

            time.sleep(5)
            #self._driver.find_element_by_id('txtStaticMac').click()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[2]/tbody/tr[1]/td[3]/input[1]').send_keys('172')
            time.sleep(5)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[2]/tbody/tr[1]/td[3]/input[2]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[2]/tbody/tr[1]/td[3]/input[3]').send_keys('192')
            time.sleep(5)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[2]/tbody/tr[1]/td[3]/input[4]').send_keys('3')
            time.sleep(5)
            self._driver.find_element_by_xpath('//*[@id="spnDhcpReserve"]').click()
            time.sleep(5)
            
            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[3]/tbody/tr/td[2]').text == 'C8:B4:22:E6:86:71':
                    self._dict_result.update({"obs": f"Associar um endereco de IP no DHCP pelo usuario com sucesso.", "result":"passed", "Resultado_Probe": "OK"})
                else:
                    self._dict_result.update({"obs": f"Erro ao associar um endereco de IP no DHCP pelo usuario.", "result":"passed", "Resultado_Probe": "NOK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  

    
    # 36
    def checkRedeGpon_36(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 375 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkRedeGpon_375')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 375 primeiro'})
        else:
            link = result['Status']['GPON']['Link']
            if link == 'Estabelecido':
                self._dict_result.update({"obs": "Link Estabelecido", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Link: {link}"})
    
        return self._dict_result
     

    # 399
    def testeSiteWizard_399(self, flask_username):
        site1 = 'http://menuvivofibra.br'
        site2 = f'http://{self._address_ip}/instalador'
        site3 = 'http://instaladorvivofibra.br'
        
        try:
            self._driver.get(site1)
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

        try:
            self._driver.get(site3)
            time.sleep(5)
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys('support')
            time.sleep(5)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado3 = 'ok'
        except:
            resultado3 = 'falhou'
 
        self._driver.quit()
        if resultado1 == 'ok' and resultado2 == 'ok' and resultado3 == 'ok':
            self._dict_result.update({"obs": "URLs de redirecionamento ok", "result":"passed", "Resultado_Probe": "OK"})
        else:
            self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}; {site3}: {resultado3}"})
        return self._dict_result


    # 21
    def checkBridgeMode_21(self, flask_username):
        try:
            self.doLogin()
            self._driver.find_element_by_link_text('Configurações').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[7]/a').click()
            config_modowan = [value.get_attribute('text') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[2]/select//option') ]
            if "Bridge" in config_modowan:
                self._dict_result.update({"obs": f"Modo WAN: {config_modowan}", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Modo WAN: {config_modowan}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result


    #29
    def changeIPDhcpViaWizard_29(self, flask_username):
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
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/ul/li[1]/a').click() #DHCP
            time.sleep(2)
            #Changing IP
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[1]').send_keys('172')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[2]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[3]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[3]/td[2]/input[4]').send_keys('3')
            time.sleep(2)
            #Changing address range
            #range-1
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]').send_keys('172')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[3]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[4]').send_keys('4')
            time.sleep(3)
            #renge-2
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[1]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[2]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[3]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[4]').clear()
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[1]').send_keys('172')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[2]').send_keys('17')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[3]').send_keys('192')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/table[1]/tbody/tr[6]/td/input[4]').send_keys('204')

            self._driver.find_element_by_xpath('//*[@id="btnDhcpSave"]/span').click()

            time.sleep(1)
            try:
                time.sleep(2)
                if self._driver.get('http://192.168.15.3/') ==None:
                    self._dict_result.update({"obs": f"Alterar range de IP do DHCP.", "result":"passed", "Resultado_Probe": "OK"})
                else:
                    self._dict_result.update({"obs": f"Erro ao associar alterar range do IP no DHCP pelo usuario.", "result":"passed", "Resultado_Probe": "NOK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  

    
    def checkRedeGpon_36(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 375 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkRedeGpon_375')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 375 primeiro'})
        else:
            link = result['Status']['GPON']['Link']
            if link == 'Estabelecido':
                self._dict_result.update({"obs": "Link Estabelecido", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Link: {link}"})
            
        return self._dict_result
 
   
    # 79
    def accessPadrao_79(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrm')
            self._driver.find_element_by_xpath('//*[@id="tbGPONinfo"]')
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"obs": 'Nao foi possivel realizar o login'})
        finally:
            self._driver.quit()
            return self._dict_result


    # 146
    def checkPPPoEStatus_146(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/login.asp')
            time.sleep(1)
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(1)
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[1]//div')]
            dict_saida = {
                "Status":
                    {
                        "Internet":
                            {div[0].split(':')[0]: div[0].split(':')[1],
                           
                            }
                    }
            }
            print(dict_saida)
            ppp = dict_saida["Status"]["Internet"]["PPP"]
            if ppp == 'Conectado':
                self._dict_result.update({"obs": "PPP: Conectado", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno PPP: {ppp}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result

    def doLogin(self):
        self._driver.get('http://' + self._address_ip + '/login.asp')

        user_input = self._driver.find_element_by_id('txtUser')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_id('txtPass')
        pass_input.send_keys(self._password)
        self._driver.find_element_by_id('btnLogin').click()
        time.sleep(3)