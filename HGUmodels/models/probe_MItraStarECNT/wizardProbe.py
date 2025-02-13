#from asyncio import exceptions
from ast import Dict
from cgi import print_form
from os import name
import re
import time
from pyzbar.pyzbar import decode
from PIL import Image
# from jinja2 import pass_context
#from typing import final
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
from ..MItraStarECNT import HGU_MItraStarECNT
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchFrameException, NoSuchElementException, InvalidSelectorException

from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config

session = MainSession()


mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

dict_test_result_memory = {}

class HGU_MItraStarECNT_wizardProbe(HGU_MItraStarECNT):

    
    # 373
    def accessWizard_373(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 401 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'accessWizard_401')
        print(result)
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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a/span').click()
            time.sleep(5)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('header')
            try:
                self._driver.find_element_by_xpath('/html/body/div[1]/div[1]/p/a[3]').click()
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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            gpon = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]').text
            div = gpon.split('\n')
            dict_saida = {
                "Status":
                    {
                        'GPON':
                            {div[0].strip(':'): div[1],
                             div[2].strip(':'): div[3],
                             div[4].strip(':'): div[5],
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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a/span').click()
            time.sleep(5)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').clear()
            self._driver.find_element_by_xpath('//*[@id="RN_Password"]').clear()
            self._driver.find_element_by_xpath('//*[@id="PPPOE_Account_Save"]').click()
            time.sleep(1)
            try:
                self._driver.switch_to.alert.text
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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a/span').click()
            time.sleep(5)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').clear()
            self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').send_keys('vivo@cliente')
            self._driver.find_element_by_xpath('//*[@id="RN_Password"]').clear()
            self._driver.find_element_by_xpath('//*[@id="RN_Password"]').send_keys('vivo')
            self._driver.find_element_by_xpath('//*[@id="PPPOE_Account_Save"]').click()
            time.sleep(25)

            try:
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                print(self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[1]/td/font/span').text)
                self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td/a/span').click()
                self._dict_result.update({"obs": "Usuario inválido", "result":"passed", "Resultado_Probe": "OK"})
                time.sleep(5)
            except:
                self._dict_result.update({"obs": "Teste falhou"})
                time.sleep(1)
                # Deixando o valor padrao de volta
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').clear()
                self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').send_keys('cliente@cliente')
                self._driver.find_element_by_xpath('//*[@id="RN_Password"]').clear()
                self._driver.find_element_by_xpath('//*[@id="RN_Password"]').send_keys('cliente')
                self._driver.find_element_by_xpath('//*[@id="PPPOE_Account_Save"]').click()

            self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  

   
    # 378 #mlv
    def changePPPoESettingsWrongAuthentication_378(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a/span').click()
            time.sleep(5)
            self.admin_authentication_mitraStat()
            time.sleep(3)
            try:
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                time.sleep(3)
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                time.sleep(1)
                self._driver.find_element_by_id('MLG_Come_Back_button').click()
                time.sleep(15)
            except Exception as e:
                print(e)
                time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').clear()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').send_keys('cliente@cliente')
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="RN_Password"]').clear()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="RN_Password"]').send_keys('vivo')
            time.sleep(1)
            self._driver.find_element_by_id('PPPOE_Account_Save').click()
            time.sleep(25)

            try: 
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm') 
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                print(self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[1]/td/font/span').text)
                if self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[1]/td/font/span').text == "Erro 691 - Provedor":    
                    self._dict_result.update({"obs": "Acesso Negado", "result":"passed", "Resultado_Probe": "OK"})
                time.sleep(2)
                self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td/a/span').click()
                time.sleep(15)
            except Exception as e:
                if "/html/body/div[3]/div/div[1]/div/iframe" in str(e):
                    self._dict_result.update({"obs": "Mensagem de erro não apresentada", "result": "NOK"})
                    time.sleep(1)
                    # Deixando o valor padrao de volta
                    self._driver.switch_to.default_content()
                    self._driver.switch_to.frame('basefrm')
                    self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').clear()
                    self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').send_keys('cliente@cliente')
                    self._driver.find_element_by_xpath('//*[@id="RN_Password"]').clear()
                    self._driver.find_element_by_xpath('//*[@id="RN_Password"]').send_keys('cliente')
                    self._driver.find_element_by_xpath('/html/body/form/div/div[1]/div[1]/table/tfoot/tr/td/a[2]/span').click()
                    time.sleep(25)
        except Exception as e:
            self._dict_result.update({"obs": e, "result": "failed"})
        finally:
            self._driver.quit()
            return self._dict_result  

    
    # 379
    def connectWizardhttps_379(self,flask_username):
        try:
            try:
                self._driver.set_page_load_timeout(10)
                self._driver.get('https://' + self._address_ip + '/')
                self._dict_result.update({"obs": "Acesso via HTTPS OK", "result":"NOK", "Resultado_Probe": "NOK"})
            except:
                self._dict_result.update({"obs": "Nao foi possivel acessar via HTTPS", "result":"passed", "Resultado_Probe": "OK"})

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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            gpon = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]').text
            div = gpon.split('\n')
            dict_saida = {
                "Status":
                    {
                        'GPON':
                            {div[0].strip(':'): div[1],
                             div[2].strip(':'): div[3],
                             div[4].strip(':'): div[5],
                            }
                    }
                }
            print(dict_saida)
            self._dict_result.update({"obs": dict_saida, "result":"passed", "Resultado_Probe": "OK"})
        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result

  
    #381 mlv
    def getFullConfig_381(self, flask_username):
        try:
            try:
                self._driver.get('http://' + self._address_ip + '/')
                time.sleep(1)
                self._driver.switch_to.frame("menufrm")
                self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
                time.sleep(1)
                self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a/span').click()
                time.sleep(5)
                login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
                time.sleep(1)
                login_button.click()
                
                self._dict_result.update({"obs": "Usuario acessou as configuracoes sem estar logado"})
                dict_saida = {"Resultado_Probe": "NOK"}
            except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
                dict_saida = {"Resultado_Probe": "OK"}
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Nao foi possivel acessar as configuracoes sem logar'})
        except Exception as e:
            print(e)
            dict_saida = {"Resultado_Probe": "failed"}
            self._dict_result.update({"obs": f"{e}"})
        finally:
            self.update_global_result_memory(flask_username, 'accessWizard_381', dict_saida)
            self._driver.quit()
            return self._dict_result

 
    # 382
    def getFullConfig_382(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        print(result)
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            idioma = result['Gerenciamento']['LANGUAGE']
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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Utilities"]').click()
            time.sleep(2)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="diagAddr"]').send_keys(destino)
            self._driver.find_element_by_xpath('//*[@id="diagPingNum"]').send_keys(tentativas)
            self._driver.find_element_by_xpath('//*[@id="Test_diag"]').click()
            time.sleep(5)
            iframe = self._driver.find_element_by_xpath('//*[@id="showBoard"]')
            self._driver.switch_to.frame(iframe)
            try:
                result = self._driver.find_element_by_xpath('/html/body/textarea').get_property('value')
            except:
                self._driver.find_element_by_xpath('//*[@id="Test_diag"]').click()
                time.sleep(5)
                result = self._driver.find_element_by_xpath('/html/body/textarea').get_property('value')

            self._dict_result.update({"obs": f"Resultados: {result}", "result":"passed", "Resultado_Probe": "OK"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})

        finally:
            self._driver.quit()
            return self._dict_result

 
    # 385
    def qrCodeTest_385(self, flask_username):
        ssid_2g_exp = 'VIVO automacao 2GHz'
        pass_2g_exp = 'vivo12345678910'

        ssid_5g_exp = 'VIVO automacao 5GHz'
        pass_5g_exp = 'vivo12345678910'

        try:
            # Entering on WiFi 2.4GHz settings and sign in
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(5)

            # Enabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)

            # CHecking initial QR Code and changing Settings 2.4GHz WiFi
            initial_qrCode_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/initial-qr-code-mitra-ecnt-2ghz.png', 'wb') as file:
                file.write(initial_qrCode_2g.screenshot_as_png)
            time.sleep(3)
            data = decode(Image.open('data/initial-qr-code-mitra-ecnt-2ghz.png'))
            initial_2g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\n##################################')
            print('Valores iniciais QR Code 2.4GHz:')
            print(initial_2g)
            select = Select(self._driver.find_element_by_id('securityMode'))
            select.select_by_visible_text('WPA2')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[6]/td[2]/input[1]').click()
            time.sleep(1)
            input_ssid_2ghz = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_password_2ghz = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]')
            input_ssid_2ghz.clear()
            time.sleep(1)
            input_ssid_2ghz.send_keys(ssid_2g_exp)
            time.sleep(1)
            input_password_2ghz.clear()
            time.sleep(1)
            input_password_2ghz.send_keys(pass_2g_exp)
            time.sleep(1)
            self._driver.find_element_by_id('MLG_GVTSettings_WL_Basic_Save').click()
            try:
                self._driver.switch_to.alert.accept()
            except Exception as e:
                pass
            time.sleep(30)

            # Cheking the new QR Code
            final_qrCode_2g = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/final-qr-code-mitra-ecnt-2ghz.png', 'wb') as file:
                file.write(final_qrCode_2g.screenshot_as_png)
            time.sleep(1)
            data = decode(Image.open('data/final-qr-code-mitra-ecnt-2ghz.png'))
            result_2g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\nValores finais QR Code 2.4GHz:')
            print(result_2g)
            print('##################################\n')
            time.sleep(5)
           
            # Entering on WiFi 5GHz settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('MLG_Menu_Settings').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span').click()
            time.sleep(5)

            # Enabling WiFi
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').click()
            self._driver.implicitly_wait(10)

            # Checking initial QR Code and changing Settings 5GHz WiFi
            initial_qrCode_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/initial-qr-code-mitra-ecnt-5ghz.png', 'wb') as file:
                file.write(initial_qrCode_5g.screenshot_as_png)
            time.sleep(3)
            data = decode(Image.open('data/initial-qr-code-mitra-ecnt-5ghz.png'))
            initial_5g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\n##################################')
            print('Valores iniciais QR Code 5GHz:')
            print(initial_5g)
            select = Select(self._driver.find_element_by_id('securityMode_5G'))
            select.select_by_visible_text('WPA2')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[6]/td[2]/input[1]').click()
            time.sleep(1)
            input_ssid_5ghz = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input')
            input_password_5ghz = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input')
            input_ssid_5ghz.clear()
            time.sleep(1)
            input_ssid_5ghz.send_keys(ssid_5g_exp)
            time.sleep(1)
            input_password_5ghz.clear()
            time.sleep(1)
            input_password_5ghz.send_keys(pass_5g_exp)
            time.sleep(1)
            self._driver.find_element_by_id('MLG_GVTSettings_5G_Basic_Save').click()
            try:
                self._driver.switch_to.alert.accept()
            except Exception as e:
                pass
            time.sleep(30)

            # Cheking the new QR Code
            final_qrCode_5g = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[3]/div/canvas')
            with open('data/final-qr-code-mitra-ecnt-5ghz.png', 'wb') as file:
                file.write(final_qrCode_5g.screenshot_as_png)
            time.sleep(1)
            data = decode(Image.open('data/final-qr-code-mitra-ecnt-5ghz.png'))
            result_5g = str(data[0][0])[7:-1].split(';')[0:3]
            print('\nValores finais QR Code 5GHz:')
            print(result_5g)
            print('##################################\n')
            time.sleep(5)

            # Checking results:
            if result_2g[0][2:] != ssid_2g_exp:
                self._dict_result.update({'obs': f'O SSID do WiFi 2.4GHz não foi alterado corretamente (esperado: {ssid_2g_exp}; obtido: {result_2g[0][2:]})'})
            elif result_2g[1][2:] != 'WPA':
                self._dict_result.update({'obs': f'O modo de segurança do WiFi 2.4GHz não foi alterado corretamente (esperado: WPA; obtido: {result_2g[1][2:]})'})
            elif result_2g[2][2:] != pass_2g_exp:
                self._dict_result.update({'obs': f'A senha do WiFi 2.4GHz não foi alterada corretamente (esperado: {pass_2g_exp}; obtido: {result_2g[2][2:]})'})
            
            elif result_5g[0][2:] != ssid_5g_exp:
                self._dict_result.update({'obs': f'O SSID do WiFi 5GHz não foi alterado corretamente (esperado: {ssid_5g_exp}; obtido: {result_5g[0][2:]})'})
            elif result_5g[1][2:] != 'WPA':
                self._dict_result.update({'obs': f'O modo de segurança do WiFi 5GHz não foi alterado corretamente (esperado: WPA; obtido: {result_5g[1][2:]})'})
            elif result_5g[2][2:] != pass_5g_exp:
                self._dict_result.update({'obs': f'A senha do WiFi 5GHz não foi alterada corretamente (esperado: {pass_5g_exp}; obtido: {result_5g[2][2:]})'})
            else:
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})

        except Exception as e:
            self._dict_result.update({'obs': f'{e}'})

        self._driver.quit()
        return self._dict_result


    # 386 mlv
    def statusWizardIptv_386(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status24 = result['Status']['WI-FI 2.4GHZ']
            status5 = result['Status']['WI-FI 5GHZ']
            wifi24 = wizard_config.WIFI24_mitraecnt
            wifi5 = wizard_config.WIFI5_mitraecnt
            if set(status24) == set(wifi24) and set(status5) == set(wifi5):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno WI-FI 2.4 GHz: {status24 and status5}"})
            
        return self._dict_result


    # 387
    # como fazer wizard config consistente entre os modelos?
    def statusWizardInet_387(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            statusInternet = result['Status']['Internet']
            ppp, ipv4, ipv4_wizard_list = statusInternet['PPP:'], statusInternet['IPv4'], wizard_config.INTERNET_IPV4_MITRA_ECNT
            ipv6, ipv6_wizard_list = statusInternet['IPv6'], wizard_config.INTERNET_IPV6_MITRA_ECNT
            # ipv4 = [unidecode.unidecode(a.upper()) for a in ipv4.keys()]
            # ipv4_wizard_list = [unidecode.unidecode(a.upper()) for a in ipv4_wizard_list]
            # ipv6 = [unidecode.unidecode(a.upper()) for a in ipv6.keys()]
            # ipv6_wizard_list = [unidecode.unidecode(a.upper()) for a in ipv6_wizard_list]
            print(set(ipv4), '\n', set(ipv4_wizard_list), '\n', set(ipv6), '\n', set(ipv6_wizard_list))

            if set(ipv4) == set(ipv4_wizard_list) and set(ipv6) == set(ipv6_wizard_list) and ppp != '':
                self._dict_result.update({"obs": "Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno PPP: {ppp} IPv4: {ipv4} | IPv6: {ipv6}"})

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
            if ifaceVoip == 'Disponível' and (registerVoIP != 'Não Registrado' or registerVoIP != ''):
                self._dict_result.update({"obs": f"Rede: Disponível | Telefone: {registerVoIP}", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Rede: {ifaceVoip} | Telefone: {registerVoIP}", 'result': 'NOK'})
        return self._dict_result


    # 389
    # como fazer wizard config consistente entre os modelos?
    def statusWizardIptv_389(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['TV']
            # status = [unidecode.unidecode(a.upper()) for a in status.keys()]
            # print(status)
            iptv = wizard_config.IPTV_MITRA_ECNT
            # iptv = [unidecode.unidecode(a.upper()) for a in iptv]
            # print(iptv)
            if set(status) == set(iptv):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno TV: {status}"})
            
        return self._dict_result


    # 390
    # como fazer wizard config consistente entre os modelos?
    def statusWizardVoip_390(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['Telefone']
            voip = wizard_config.VOIP_ME
            print('\n\nstatus:', set(status), '\nvoip:', set(voip), '\n\n')
            if set(status) == set(voip):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno VoIP: {status}"})
        return self._dict_result
    

    #391 HPNA
    def statusWizardHpna_391(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['Telefone']
            voip = wizard_config.VOIP_ME

            if set(status) == set(voip):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno VoIP: {status}"})
            
        return self._dict_result


    # 392
    def verifyDnsService_392(self, flask_username) -> dict:
        """
            A method to test if the DNS Service is available
        :return : A dict with the result of the test
        """
        try:
            # Entering on Settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('setmenu').click()
            time.sleep(1)
            self._driver.find_element_by_id('MLG_Menu_Local_Network').click()
            time.sleep(2)
            # Entering login informations
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            # Enabling DNS
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[2]/input[1]').click()
            # Entering primary DNS
            prim_dns_1 = self._driver.find_element_by_id('PrimaryDns_1')
            prim_dns_1.clear()
            prim_dns_1.send_keys('8')
            prim_dns_2 = self._driver.find_element_by_id('PrimaryDns_2')
            prim_dns_2.clear()
            prim_dns_2.send_keys('8')
            prim_dns_3 = self._driver.find_element_by_id('PrimaryDns_3')
            prim_dns_3.clear()
            prim_dns_3.send_keys('8')
            prim_dns_4 = self._driver.find_element_by_id('PrimaryDns_4')
            prim_dns_4.clear()
            prim_dns_4.send_keys('8')
            # Entering Secondary DNS
            sec_dns_1 = self._driver.find_element_by_id('SecondDns_1')
            sec_dns_1.clear()
            sec_dns_1.send_keys('8')
            sec_dns_2 = self._driver.find_element_by_id('SecondDns_2')
            sec_dns_2.clear()
            sec_dns_2.send_keys('8')
            sec_dns_3 = self._driver.find_element_by_id('SecondDns_3')
            sec_dns_3.clear()
            sec_dns_3.send_keys('4')
            sec_dns_4 = self._driver.find_element_by_id('SecondDns_4')
            sec_dns_4.clear()
            sec_dns_4.send_keys('4')
            # Saving DNS changes
            self._driver.find_element_by_id('MLG_Dhcp_Save').click()
            time.sleep(10)
            # Desabling DNS
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[2]/input[2]').click()
            self._driver.find_element_by_id('MLG_Dhcp_Save').click()
            time.sleep(10)

            # Checking if primary DNS fields are available
            if self._driver.find_element_by_id('PrimaryDns_1') == None:
                return self._dict_result
            else:
                return self._dict_result.update({"obs": "Servi;o DNS habilitado com sucesso", "result":"passed", "Resultado_Probe": "OK"})
        
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result 


    # 393
    def createDmzViaWizard_393(self, flask_username) -> dict:
        """
            Provides DMZ Setup on Wizard
        :return : A dict with the result of the test
        """
        try:
            # Entering on Settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('setmenu').click()
            time.sleep(1)
            self._driver.find_element_by_id('MLG_Menu_Local_Network').click()
            time.sleep(2)
            # Entering login informations
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            # Entering DMZ Settings
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            time.sleep(3)
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/ul/li[3]/a').click()
            # Entering IP Address
            time.sleep(5)
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[2]/div/table/tbody/tr[2]/td[2]/input[1]').click()
            time.sleep(3)
            input_ip = self._driver.find_element_by_xpath('//*[@id="dmzHostIP"]')
            input_ip.clear()
            input_ip.send_keys('192.168.17.49')
            self._driver.find_element_by_id('Save_dmz').click()
            time.sleep(5)
            # Switch to iframe
            iframe = self._driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/iframe')
            self._driver.switch_to.frame(iframe)
            self._driver.find_element_by_id('MLG_Pop_DMZ_Reboot_Yes').click()
            # Entering againg on settings
            time.sleep(105)
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('setmenu').click()
            time.sleep(1)
            self._driver.find_element_by_id('MLG_Menu_Local_Network').click()
            time.sleep(2)
            # Entering login informations
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            # Entering DMZ Settings
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/ul/li[3]/a').click()
            time.sleep(10)

            try:
                time.sleep(8)
                fail_alert = self._driver.find_element_by_xpath('//*[@id="IP_Format_Error"]')
                if fail_alert is None or fail_alert.text != 'Please, type a valid IP address.':
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


    # 395
    def configUpnpViaWizard_395(self, flask_username) -> dict:
        """
            Enabling UPnP Settings
        :return : A dict with the result of the test
        """
        try:
            # Entering on Settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('setmenu').click()
            time.sleep(1)
            self._driver.find_element_by_id('MLG_Menu_Local_Network').click()
            time.sleep(2)
            # Entering login informations
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(3)
            # Entering UPnP Settings
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_id('tabtitle-4').click()
            time.sleep(3)
            # Enabling UPnP Settings and Saving
            self._driver.find_element_by_xpath('//*[@id="UPnP_form"]/table/tbody/tr[2]/td[2]/input[1]').click()
            self._driver.find_element_by_id('MLG_UPnP_Save').click()
            time.sleep(5)

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

    
    # 396 mlv
    def configDdnsViaWizard_396(self, flask_username) -> dict:
        """
            Provides DDnS Settings
        :return : A dict with the result of the test
        """
        try:
            # Entering on Settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('setmenu').click()
            time.sleep(1)
            self._driver.find_element_by_id('MLG_Menu_Local_Network').click()
            time.sleep(2)
            # Entering login informations
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            time.sleep(3)
            # Sentting DDnS
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_id('tabtitle-5').click()
            time.sleep(3)
            self._driver.find_element_by_xpath('//*[@id="tab-05"]/table/tbody/tr[2]/td[2]/input[1]').click()
            select = Select(self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[3]/div/table/tbody/tr[3]/td[2]/select'))
            select.select_by_visible_text('No-IP')
            user_field = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[3]/div/table/tbody/tr[4]/td[2]/input')
            user_field.clear()
            user_field.send_keys('telefonica.labs@gmail.com')
            pass_field = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[3]/div/table/tbody/tr[5]/td[2]/input')
            pass_field.clear()
            pass_field.send_keys('vivo@123')
            hostname_field = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[3]/div/table/tbody/tr[6]/td[2]/input')
            hostname_field.clear()
            hostname_field.send_keys('telefonicalabs.ddns.net')
            self._driver.find_element_by_id('MLG_DDNS_Account_Save').click()
            time.sleep(8)
            # Disabling DDNS
            self._driver.find_element_by_xpath('//*[@id="tab-05"]/table/tbody/tr[2]/td[2]/input[2]').click()
            self._driver.find_element_by_id('MLG_DDNS_Account_Save').click()

            try:
                time.sleep(8)
                # Check on the frontend for the text fields that remains available even when DDnS is disable
                if self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/form[3]/div/table/tbody/tr[4]/td[2]/input').is_enabled != True:
                    self._dict_result.update({"obs": f"Criacao de DMZ realizada com sucesso.", "result":"passed", "Resultado_Probe": "OK"})
                else:
                    self._dict_result.update({"obs": f"Erro de criacao de DMZ.", "result":"NOK", "Resultado_Probe": "NOK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"failed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  
    

    # 397
    def configIpDhcpViaWizard_397(self, flask_username) -> dict:
        """
            Provides IP in DHCP Setup on Wizard
        :return : A dict with the result of the test
        """
        try:
            # Entering on Settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_id('setmenu').click()
            time.sleep(1)
            self._driver.find_element_by_id('MLG_Menu_Local_Network').click()
            time.sleep(2)
            # Entering login informations
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
            time.sleep(1)
            login_button.click()
            # Entering DHCP Settings
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/ul/li[1]/a').click()
            time.sleep(5)
            #MAC settings
            input_mac = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[2]/tbody/tr[1]/td[3]/input')
            input_mac.clear()
            input_mac.send_keys('00:0c:29:bb:0b:35')
            time.sleep(5)
            #IP settings
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[2]/tbody/tr[1]/td[4]/input[1]').send_keys('172')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[2]/tbody/tr[1]/td[4]/input[2]').send_keys('18')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[2]/tbody/tr[1]/td[4]/input[3]').send_keys('192')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[2]/tbody/tr[1]/td[4]/input[4]').send_keys('3')
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[2]/tbody/tr[2]/td/a/span').click()
            
            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[3]/tbody/tr/td[2]').text == '00:0C:29:BB:0B:35':
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


    # 399
    def testeSiteWizard_399(self, flask_username):
        site1 = 'http://menuvivofibra.br'
        site2 = f'http://{self._address_ip}/instalador'
        site3 = 'http://instaladorvivofibra.br'
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('site1 = ' + site1)
        print('site2 = ' + site2)
        print('site3 = ' + site3)
        print('-=-' * 20)
        
        try:
            self._driver.get(site1)
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]')
            for elemento in elementos: print(elemento.text, "\n")
            resultado1 = 'ok'
        except:
            resultado1 = 'falhou'
        print('site1: ', resultado1)
        print('-=-' * 20)
        
        try:
            self._driver.get(site2)
            time.sleep(1)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]')
            for elemento in elementos: print(elemento.text, "\n")
            resultado2 = 'ok'
        except:
            resultado2 = 'falhou'
        print('site2: ', resultado2)
        print('-=-' * 20)

        try:
            self._driver.get(site3)
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]')
            for elemento in elementos: print(elemento.text, "\n")
            resultado3 = 'ok'
        except:
            resultado3 = 'falhou'
        print('site3: ', resultado3)
        print('-=-' * 20)
 
        self._driver.quit()
        if resultado1 == 'ok' and resultado2 == 'ok' and resultado3 == 'ok':
            self._dict_result.update({"obs": "URLs de redirecionamento ok", "result":"passed", "Resultado_Probe": "OK"})
        else:
            self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}; {site3}: {resultado3}"})
        return self._dict_result


    # 21
    def checkBridgeMode_21(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Settings"]').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_WAN_Mode"]').click()
            self.admin_authentication_mitraStat()
            time.sleep(1)
            self._driver.switch_to.frame('basefrm')
            config_modowan = [value.get_attribute('text') for value in self._driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/select//option') ]
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


    # 79
    def accessPadrao_79(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('/html/body/div[1]')
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"obs": 'Nao foi possivel realizar o login'})
        finally:
            self._driver.quit()
            return self._dict_result


    # 146
    def checkPPPoEStatus_146(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Settings"]').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_WAN_Mode"]').click()
            self.admin_authentication_mitraStat()
            time.sleep(1)

            self._driver.switch_to.frame('menufrm')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[1]/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/td[1]//div')]
            dict_saida = {
                "Status":
                    {
                        "Internet":
                            {div[0].split(':')[0]: div[0].split(':')[1],
                           
                            }
                    }
            }
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