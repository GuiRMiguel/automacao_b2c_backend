#from asyncio import exceptions
from cgi import print_form
from os import name
import re
import time
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

    #378 #mlv
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
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').clear()
            self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').send_keys('cliente@cliente')
            self._driver.find_element_by_xpath('//*[@id="RN_Password"]').clear()
            self._driver.find_element_by_xpath('//*[@id="RN_Password"]').send_keys('vivo')
            self._driver.find_element_by_xpath('//*[@id="PPPOE_Account_Save"]').click()
            time.sleep(25)

            try: 
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                print(self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[1]/td/font/span').text)
                self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td/a/span').click()
                #if self._driver.find_element_by_xpath('//*[@id="MLG_Pop_Fail_691_Title"]/span').text() == "Erro 691 - Provedor":    
                    #self._dict_result.update({"obs": "Acesso Negado", "result":"passed", "Resultado_Probe": "OK"})
            

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


    # Algumas vezes a conexão é realizada, outras vezes fica na tela de conexão sem evolução
    def connectWizardhttps_379(self,flask_username):
        try:
            try:
                self._driver.set_page_load_timeout(3)
                self._driver.get('https://' + self._address_ip + '/')
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
            self._driver.quit()
            
            self._dict_result.update({"obs": "Usuario acessou as configuracoes sem estar logado"})
            dict_saida = {"Resultado_Probe": "NOK"}
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Nao foi possivel acessar as configuracoes sem logar'})
            dict_saida = {"Resultado_Probe": "OK"}
        finally:
            self.update_global_result_memory(flask_username, 'accessWizard_381', dict_saida)
            return self._dict_result




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


    # como fazer wizard config consistente entre os modelos?
    def statusWizardVoip_390(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['Telefone']
            voip = wizard_config.VOIP
            if set(status) == set(voip):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno VoIP: {status}"})
        return self._dict_result

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

# 
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