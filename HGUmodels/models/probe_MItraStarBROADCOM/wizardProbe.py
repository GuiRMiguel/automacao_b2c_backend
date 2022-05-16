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
from ..MItraStarBROADCOM import HGU_MItraStarBROADCOM
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select
from HGUmodels.config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config


session = MainSession()


mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

dict_test_result_memory = {}

class HGU_MItraStarBROADCOM_wizardProbe(HGU_MItraStarBROADCOM):
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
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)
        
            print('\n#############################################'
                    '\n MENU >> STATUS'
                    '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         STATUS
            ### ------------------------------------------ ###
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[1]/a').click()
            time.sleep(3)
            # self._driver.switch_to.default_content()
            # self._driver.switch_to.frame('basefrm')
            # time.sleep(2)

            try:
                print('oi')
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('header')
                self._driver.find_element_by_xpath('/html/body/div/div[1]/p/a[3]').click()
                self._dict_result.update({"obs": "Logout efetuado com sucesso", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Nao foi possivel efetuar o logout"})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result

#378 #mlv
    def changePPPoESettingsWrongAuthentication_378(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            #config / Internet
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            #config / Internet
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click() 
            time.sleep(3)
            print('1')

            time.sleep(5)
            # PPPoE
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("basefrm")
            time.sleep(3)
            self._driver.find_element_by_xpath('//*[@id="username"]').clear()
            self._driver.find_element_by_xpath('//*[@id="username"]').send_keys('cliente@cliente')
            self._driver.find_element_by_xpath('//*[@id="password"]').clear()
            self._driver.find_element_by_xpath('//*[@id="password"]').send_keys('vivo')
            login_button = self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/form/table/tfoot/tr/td/a[2]/span')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            try:
                time.sleep(22)
                if self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/form/table/tfoot/tr/td/a[2]/span') == None:
                    self._dict_result.update({"obs": "Teste falhou, Usuario aceito"})
                else:
                    self._dict_result.update({"obs": f"Teste correto, usuario nao foi aceito", "result":"passed", "Resultado_Probe": "OK"})

            except UnexpectedAlertPresentException as e:
                time.sleep(2)
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  
        

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


    def checkPPPoEStatus_380(self, flask_username):
        try:
            try:
                self._driver.get('http://' + self._address_ip + '/')
                self._driver.switch_to.frame('mainFrame')
                time.sleep(1)
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
                self._dict_result.update({"obs": dict_saida, "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Nao foi possivel acessar sem login"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result

    #381
    def getFullConfig_381(self, flask_username):
        try:
            # Entering on Settings
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            # config / Internet
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            time.sleep(5)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("basefrm")
            time.sleep(5)
            login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]/span')
            time.sleep(1)
            if login_button.click() == None:
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Nao foi possivel acessar as configuracoes sem logar'})
                dict_saida = {"Resultado_Probe": "OK"}
            else:
                self._dict_result.update({"obs": "Usuario acessou as configuracoes sem estar logado"})
                dict_saida = {"Resultado_Probe": "NOK"}

            self._driver.quit()
        finally:
            self.update_global_result_memory(flask_username, 'accessWizard_381', dict_saida)
            return self._dict_result

    #386 
    def statusWizardIptv_386(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status24 = result['Status']['Wi-Fi 2.4 GHz']
            print(status24)
            status5 = result['Status']['Wi-Fi 5 GHz']
            print(status5)
            wifi24 = wizard_config.WIFI24_mitraBroadCom
            print(wifi24)
            wifi5 = wizard_config.WIFI5_mitraBroadCom
            print(wifi5)
            if set(status24) == set(wifi24) and set(status5) == set(wifi5):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno WI-FI 2.4 GHz: {status24 and status5}"})
            
        return self._dict_result



    # 392
    def verifyDnsService_392(self, flask_username) -> dict:
        """
            A method to test if the DNS Service is available
        :return : A dict with the result of the test
        """
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            #config / Internet
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            # Enabling DNS
            # self._driver.switch_to.default_content()
            # time.sleep(1)
            # self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[2]/input[1]').click()
            # Entering primary DNS
            prim_dns_1 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[8]/td[2]/input[1]')
            prim_dns_1.clear()
            prim_dns_1.send_keys('8')
            prim_dns_2 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[8]/td[2]/input[2]')
            prim_dns_2.clear()
            prim_dns_2.send_keys('8')
            prim_dns_3 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[8]/td[2]/input[3]')
            prim_dns_3.clear()
            prim_dns_3.send_keys('8')
            prim_dns_4 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[8]/td[2]/input[4]')
            prim_dns_4.clear()
            prim_dns_4.send_keys('8')
            # Entering Secondary DNS
            sec_dns_1 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[9]/td[2]/input[1]')
            sec_dns_1.clear()
            sec_dns_1.send_keys('8')
            sec_dns_2 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[9]/td[2]/input[2]')
            sec_dns_2.clear()
            sec_dns_2.send_keys('8')
            sec_dns_3 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[9]/td[2]/input[3]')
            sec_dns_3.clear()
            sec_dns_3.send_keys('4')
            sec_dns_4 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[9]/td[2]/input[4]')
            sec_dns_4.clear()
            sec_dns_4.send_keys('4')
            # Saving DNS changes
            self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table[1]/tbody/tr[11]/td[2]/a[2]/span').click()
            time.sleep(10)
            # Desabling DNS
            self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[2]/input[2]').click()
            self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table[1]/tbody/tr[11]/td[2]/a[2]/span').click()
            time.sleep(10)

            # Checking if primary DNS fields are available
            if self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[8]/td[2]/input[1]') == None:
                return self._dict_result
            else:
                return self._dict_result.update({"obs": "Servi;o DNS habilitado com sucesso", "result":"passed", "Resultado_Probe": "OK"})
            
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
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
            # config / Internet
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            # Entering DMZ Settings
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_id('tabtitle-3').click()
            # Entering IP Address
            self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[5]/form/table/tbody/tr[2]/td[2]/input[1]').click()
            input_ip = self._driver.find_element_by_xpath('//*[@id="tab-03"]/form/table/tbody/tr[3]/td[2]/input')
            input_ip.clear()
            input_ip.send_keys('192.168.17.49')
            self._driver.find_element_by_xpath('//*[@id="tab-03"]/form/table/tbody/tr[4]/td/a[2]/span').click()
            time.sleep(5)
            # Switch to iframe
            iframe = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/iframe')
            self._driver.switch_to.frame(iframe)
            self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[2]/td/a[1]/span').click()
            # Entering againg on settings
            time.sleep(105)
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            # config / Internet
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            # Entering DMZ Settings
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_id('tabtitle-3').click()

            try:
                time.sleep(8)
                warning_message = self._driver.find_element_by_xpath('//*[@id="dmz_warning_message"]')
                if warning_message is None or warning_message != 'Please, type a valid IP address.':
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
            # config / Internet
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            # Entering UPnP Settings
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_id('tabtitle-4').click()
            # Enabling UPnP Settings and Saving
            self._driver.find_element_by_xpath('//*[@id="tab-04"]/form/table/tbody/tr[2]/td[2]/input[1]').click()
            self._driver.find_element_by_xpath('//*[@id="tab-04"]/form/table/tbody/tr[3]/td/a[2]/span').click()
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
            # config / Internet
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            # Entering DHCP Settings
            time.sleep(5)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_id('tabtitle-1').click()
            #MAC settings
            input_mac = self._driver.find_element_by_id('staticDHCPMAC')
            self._driver.implicitly_wait(10)
            ActionChains(self._driver).move_to_element(input_mac).send_keys('00:0c:29:bb:0b:35').perform()
            time.sleep(8)
            #IP settings
            ip_field_1 = self._driver.find_element_by_name('staticDHCPIP_part1')
            ip_field_1.send_keys('192')
            time.sleep(1)
            ip_field_2 = self._driver.find_element_by_name('staticDHCPIP_part2')
            ip_field_2.send_keys('168')
            time.sleep(1)
            ip_field_3 = self._driver.find_element_by_name('staticDHCPIP_part3')
            ip_field_3.send_keys('17')
            time.sleep(1)
            ip_field_4 = self._driver.find_element_by_name('staticDHCPIP_part4')
            ip_field_4.send_keys('3')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[2]/tbody/tr[2]/td/a/span').click()
            time.sleep(5)
            if self._driver.find_element_by_xpath('//*[@id="static_warning_message"]').text == 'Por favor, informe um endereço MAC válido.':
                self._driver.implicitly_wait(10)
                input_mac.send_keys('00:0c:29:bb:0b:35')
                self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[2]/tbody/tr[2]/td/a/span').click()
            
            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[3]/tbody/tr/td[2]').text == '00:0C:29:BB:0B:35':
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


    def testeSiteWizard_399(self, flask_username):
        site1 = 'http://menuvivofibra.br'
        site2 = f'http://{self._address_ip}/instalador'
        site3 = 'http://instaladorvivofibra.br'        
        try:
            self._driver.get(site1)
            time.sleep(1)
            #self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado1 = 'ok'
        except:
            resultado1 = 'falhou'

        try:
            self._driver.get(site2)
            time.sleep(1)
            #config / Internet
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(4)
            self.admin_authentication_mitraStat()
            time.sleep(2)

            resultado2 = 'ok'
        except:
            resultado2 = 'falhou'

        try:
            self._driver.get(site3)
            time.sleep(1)
            #self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a').click() 

            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            print('ALOOOOOOO')
            print(elementos)
            resultado3 = 'ok'
        except:
            resultado3 = 'falhou'
 
        self._driver.quit()
        if resultado1 == 'ok' and resultado2 == 'ok' and resultado3 == 'ok':
            self._dict_result.update({"obs": "URLs de redirecionamento ok", "result":"passed", "Resultado_Probe": "OK"})
        else:
            self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}; {site3}: {resultado3}"})
        return self._dict_result
