from ipaddress import ip_address, ip_interface
import time
from webdriver.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import json
import re
from HGUmodels.factory import HGUModelFactory





class gui:
    def __init__(self):
        self.ip = []
        self.username = []
        self.password = []
    ### ------------------------------------------ ###
    ###         FUNÇÕES DE VERIFICAÇÃO
    ### ------------------------------------------ ###

    def getUrlWEBGuiDefault(self, ip=None):
        
        driver = WebDriver.get_driver()        
        print(ip)
        try:
            driver.get(f'http://{ip}')
            return{"name_test": "testeAberturaWEBGui", "Resultado": "Pagina aberta com SUCESSO!!!"}
        except Exception as e:
            print('Excecao', e)
        # driver.quit()


    # 17
    def checkSpeedEthernetCable(self, ip, username, password, flask_username, model_name, **kwargs):
        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "checkSpeedEthernetCable", 
                        "Probe#": "XXXXXX", 
                        "Description": "Verificar a velocidade de transmissao no cabo de rede Ethernet" 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.checkSpeedEthernetCable_17(flask_username)


    # 18
    def checkSpeed2GHz(self, ip, username, password, flask_username, model_name, **kwargs):
        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "checkSpeed2GHz", 
                        "Probe#": "XXXXXX", 
                        "Description": "Verificar a velocidade de transmissao no WiFi 2.4GHz" 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.checkSpeed2GHz_18(flask_username)


    # 19
    def checkSpeed5GHz(self, ip, username, password, flask_username, model_name, **kwargs):
        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "checkSpeed5GHz", 
                        "Probe#": "XXXXXX", 
                        "Description": "Verificar a velocidade de transmissao no WiFi 5GHz" 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.checkSpeed5GHz_19(flask_username)

    
    # 32
    def UpgradeDowngradeFirmware(self, ip, username, password, flask_username, model_name, **kwargs):

        driver = WebDriver.get_driver()
        
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "UpgradeDowngradeFirmware", 
                       "Probe#": "32", 
                       "Description": "Upgrade/Downgrade de Firmware,Permanecer tentando conseguir um endereco de IP se nenhuma resposta for retornada."}
                       
        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.UpgradeDowngradeFirmware_32(flask_username)


    # 41
    def validiteConectStbTv(self, ip, username, password, flask_username, model_name, **kwargs):
        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "validiteConectStbTv", 
                        "Probe#": "41", 
                        "Description": "Validar conectividade STB x TV com as conexoes RCA e HDMI(Modelos de TV diferentes)" 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.validiteConectStbTv_41(flask_username)


    # 48
    def validiteDefaultModeAfterReset(self, ip, username, password, flask_username, model_name, **kwargs):
        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "validiteDefaultModeAfterReset", 
                        "Probe#": "48", 
                        "Description": "Verificar se o dispositivo esta online no ACS depois de resetar no HGU e atualizar FW" 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.validiteDefaultModeAfterReset_48(flask_username)


    # 50
    def validiteSerialNumberAndMac(self, ip, username, password, flask_username, model_name, **kwargs):
        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "validiteSerialNumberAndMac", 
                        "Probe#": "50", 
                        "Description": "Verificar o numero de serie e MAN da Wan depois de resetar para default" 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.validiteSerialNumberAndMac_50(flask_username)


     # 64
    def validiteUrlsWancfgCmd(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "validiteUrlsWancfgCmd", 
                        "Probe#": "64", 
                        "Description": "Validar que nao eh possivel acessar interface avancada por ip/wancfg.cmd", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.validiteUrlsWancfgCmd_64(flask_username)

    # 65
    def validiteUrlsWancfgCmdActionView(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "validiteUrlsWancfgCmdActionView", 
                        "Probe#": "65", 
                        "Description": "Validar que nao eh possivel acessar interface avancada por ip/wancfg.cmd?action=view", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.validiteUrlsWancfgCmdActionView_65(flask_username)

    # 66
    def changePasswordAccess(self, ip, username, password, flask_username, model_name, **kwargs):

        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "changePasswordAccess", 
                        "Probe#": "66", 
                        "Description": "Alterar a senha de acesso ao dispositivo", 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        new_password ='S@oP@ulo*15'

        res1 = hgu.changePasswordAccess_66(flask_username, new_password)

        hgu2 = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        res2 = hgu2.accessWizard_401(flask_username)

        return res2
    
    # 68
    def pingDifferNetwork(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "pingDifferNetwork", 
                        "Probe#": "68", 
                        "Description": "Pingar rede diferente", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.pingDifferNetwork_68(flask_username)


    #69
    def changeAdminPassword(self, ip, username, password, flask_username, model_name, **kwargs):

        driver = WebDriver.get_driver()

        dict_result =  {"result":'failed', 
                        "obs":None,
                        "Resultado_Probe": "NOK", 
                        "ProbeName": "changeAdminPassword", 
                        "Probe#": "XXXXXX", 
                        "Description": "Alterar a senha de acesso ao dispositivo e validar que após a alteração é solicitado nova autenticação", 
                       }

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        new_password ='S@oP@ulo*15'

        res1 = hgu.changeAdminPassword_69(flask_username, new_password)

        hgu2 = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        res2 = hgu2.accessWizard_401(flask_username)

        return res2


    def habilitaSSHASKEY3505(self):
        
        driver = WebDriver.get_driver()
        usuario = 'support'
        senha = '6dikiovt'

        try:
            driver.get(f'http://{ip}/padrao')
        except:
            print('Excecao')
        # driver.quit()

        driver.switch_to.frame('loginfrm')
        user_input = driver.find_element_by_id('txtUser')
        user_input.send_keys(usuario)
        pass_input = driver.find_element_by_id('txtPass')
        pass_input.send_keys(senha)
        login_button = driver.find_element_by_id('btnLogin')
        login_button.click()

        driver.switch_to.frame('menufrm')
        link = driver.find_element_by_link_text('Management')
        link.click()
        link = driver.find_element_by_link_text('Access Control')
        link.click()
        link = driver.find_element_by_link_text('Remote Administration')
        link.click()

        #check_ssh = driver.find_element_by_xpath('//*[@id="ctrlSshd"]/td[2]/label/input')
        driver.switch_to.parent_frame() ## é necessario voltar um nivel na hierarquia para encontrar o elemento
        driver.switch_to.frame('basefrm')
        check_ssh = driver.find_element_by_name('chkSsh')
        if check_ssh.is_selected():
            #driver.quit()
            return{"name_test": "testeHabilitarSSH", "Resultado": "SSH JÁ ESTAVA HABILITADO!!!"}
        else:
            check_ssh.click()
            save_button = driver.find_element_by_name('apply')
            save_button.click()
            #driver.quit()
            return {"name_test": "testeHabilitarSSH", "Resultado": "SSH AGORA ESTÁ HABILITADO COM SUCESSO!!!"}

    def openingVideo(self):
        
        driver = WebDriver.get_driver()

        try:
            driver.get('https://youtube.com')
            driver.find_element_by_name("search_query").send_keys("jacobschwarz")
            driver.find_element_by_id("search-icon-legacy").click()
            time.sleep(2)
            driver.find_element_by_class_name("style-scope ytd-vertical-list-renderer").click()
            # // *[ @ id = "movie_player"] / div[28] / div[2] / div[2] / button[4]
        except NoSuchElementException as exception:
            print('Excecao')
            print('Elemento não encontrado' )

        try:
            # settings_button = driver.find_element_by_class_name('ytp-settings-button')
            # settings_button[0].click()
            # time.sleep(10)
            #
            # print("Initial Page Title is : %s" % driver.title)
            # windows_before = driver.current_window_handle
            # print("First Window Handle is : %s" % windows_before)
            driver.find_element_by_css_selector('button.ytp-button.ytp-settings-button')
            driver.find_element_by_xpath("//div[contains(text(),'Quality')]").click()

            time.sleep(2)  # you can adjust this time
            quality = driver.find_element_by_xpath("//span[contains(string(),'144p')]")
            print("Element is visible? " + str(quality.is_displayed()))
        except NoSuchElementException as exception:
            print(exception)

    def accessWizardASKEY3505(self,ip,username,password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print()
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)

        try:
            driver.get('http://'+ip+'/')
            driver.switch_to.frame('mainFrame')
            link = driver.find_element_by_link_text('Configurações')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_link_text('Rede Wi-Fi 2,4 GHz')
            link.click()
            print('clicou no botao Rede Wifi')
            time.sleep(1)
            driver.switch_to.frame('mainFrame')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            return {"ProbeName": "accessWizard", "Probe#": "0001", "Description": "Valida acesso à WEBGUI", "Resultado":"PASS"}
        except NoSuchElementException as exception:
            print(exception)
        # driver.quit()


    #401
    def accessWizard(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK

        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkPPPoEStatus", 
                       "Probe#": "78", 
                       "Description": "Acessar página padrão "}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.accessWizard_401(flask_username)

    
    #373
    def accessWizard_2(self, ip, username, password, flask_username, model_name, **kwargs): 
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkPPPoEStatus", 
                       "Probe#": "78", 
                       "Description": "Acessar página padrão "}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.accessWizard_373(flask_username)


    def accessPadraoASKEY3505(self,ip,username,password): ### DISPOSITIVO ASKEY3505
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print()
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)

        try:
            driver.get('http://'+ip+'/padrao')
            driver.switch_to.frame('loginfrm')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            return {"ProbeName": "accessPadrao", "Probe#": "0002", "Description": "Valida acesso à Página Padrão",
                    "Resultado": "PASS"}
        except:
            print('Excecao')
        # driver.quit()

    def checkACSUrlManagedASKEY3505(self,ip,username,password): ###DISPOSITIVO ASKEY 3505
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print()
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)

        try:
            driver.get('http://' + ip + '/padrao')
            driver.switch_to.frame('loginfrm')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()

            driver.switch_to.frame('menufrm')
            link = driver.find_element_by_link_text('Management')
            link.click()
            link = driver.find_element_by_link_text('TR-069 Client')
            link.click()
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('basefrm')
            informInterval = driver.find_element_by_name('informInterval').get_property('value')
            ACS_URL = driver.find_element_by_name('acsURL').get_property('value')
            print('informInterval = ' + informInterval)
            print('ACS_URL = ' + ACS_URL)
            if (informInterval == '68400' or informInterval == '108400') and (ACS_URL == 'http://200.207.192.3:7015/cwmpWeb/CPEMgt' or ACS_URL == 'http://acs.telesp.net.br:7015/cwmpWeb/CPEMgt'):
                return {"ProbeName": "checkACSUrlManaged", "Probe#": "0003", "Description": "Valida URL do ACS",
                    "Resultado": "PASS"}
            else:
                return {"ProbeName": "checkACSUrlManaged", "Probe#": "0003", "Description": "Valida URL do ACS",
                        "Resultado": "NOT PASS"}
        except:
            print('Excecao')
        # driver.quit()

    def logoutWizardASKEY3505(self,ip,username,password):###DISPOSITIVO ASKEY 3505
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print()
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)

        try:
            driver.get('http://' + ip + '/')
            driver.switch_to.frame('mainFrame')
            link = driver.find_element_by_link_text('Configurações')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_link_text('Rede Wi-Fi 2,4 GHz')
            link.click()
            print('clicou no botao Rede Wifi')
            time.sleep(1)
            driver.switch_to.frame('mainFrame')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(5)
            driver.switch_to.frame('mainFrame')
            link = driver.find_element_by_link_text('Sair')
            link.click()
            time.sleep(5)
            return {"ProbeName": "logoutWizard", "Probe#": "0004", "Description": "Valida logout da WEBGUI", "Resultado":"PASS"}
        except NoSuchElementException as exception:
            print(exception)


    """
    def logoutWizard(self,ip,username,password): ### TUDO OK
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print()
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            
            logout = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a').click()
            time.sleep(1)
            driver.quit()
            return {"Resultado_Probe": "OK", "ProbeName": "logoutWizard", "Probe#": "138", "Description": "Logout na GUI básica de usuário (Wizard) ", "Resultado": "200_OK"}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ProbeName": "logoutWizard", "Probe#": "138", "Description": "Logout na GUI básica de usuário (Wizard) ", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ProbeName": "logoutWizard", "Probe#": "138", "Description": "Logout na GUI básica de usuário (Wizard) ", "Resultado": str(e)}
    """

    #374
    def logoutWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "logoutWizard", 
                        "Probe#": "138", 
                        "Description": "Logout na GUI básica de usuário (Wizard)", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.logoutWizard_374(flask_username)

#   def checkRedeGpon(self,ip): ### TUDO OK

    #     driver = WebDriver.get_driver()
    #     print()
    #     print()
    #     print('-=-' * 20)
    #     print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
    #     print('-=-' * 20)
    #     print('\n\n -- PARAMETROS DE ENTRADA --')
    #     print('ip = ' + ip)
    #     print('-=-' * 20)
    #     try:
    #         print('\n\n == Abrindo URL == ')
    #         driver.get('http://' + ip + '/index_cliente.asp')
    #         gpon = driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
    #         divOptical = driver.find_element_by_id('divOptical').text
    #         divOptical = divOptical.split("\n")
    #         print(divOptical)
    #         divOptRx = driver.find_element_by_id('divOptRx').text
    #         divOptRx = divOptRx.split("\n")
    #         print(divOptRx)
    #         divOptTx = driver.find_element_by_id('divOptTx').text
    #         divOptTx = divOptTx.split("\n")
    #         print(divOptTx)
    #         time.sleep(2)
    #         print('\n\n\n == Criando JSON de saída... == ')
    #         json_saida = {
    #             "Status":
    #                 {
    #                     gpon:
    #                         {
    #                             divOptical[0]: divOptical[1],
    #                             divOptRx[0]: divOptRx[1],
    #                             divOptTx[0]: divOptTx[1]
    #                         }
    #                 }
    #         }

    #         #json_saida = json.dumps(json_saida, ensure_ascii=False)
    #         print(json_saida)
    #         driver.quit()
    #         return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "36", "Description": "Verifica o status da conexão PPPoE", "Resultado": json_saida}
    #     except NoSuchElementException as exception:
    #         print(exception)
    #         driver.quit()
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "36", "Description": "Verifica o status da conexão PPPoE", "Resultado": str(exception)}
    #     except Exception as e:
    #         print(e)
    #         driver.quit()
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui","ProbeName": "checkPPPoEStatus", "Probe#": "36", "Description": "Verifica o status da conexão PPPoE", "Resultado": str(e)}


    # 375
    def checkRedeGpon(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkPPPoEStatus", 
                        "Probe#": "36", 
                        "Description": "Verifica o status da conexão PPPoE", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkRedeGpon_375(flask_username)


    # def changePPPoESettingsWrong(self, ip, username, password, pppoe_user, pppoe_paswd):
        
    #     driver = WebDriver.get_driver()
    #     driver.execute_script("window.alert = function() {};")
    #     usuario = username
    #     senha = password
    #     pppoe_user = pppoe_user
    #     pppoe_paswd = pppoe_paswd
    #     print()
    #     print()
    #     print('-=-' * 20)
    #     print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
    #     print('-=-' * 20)
    #     print('\n\n -- PARAMETROS DE ENTRADA --')
    #     print('ip = ' + ip)
    #     print('username = ' + username)
    #     print('password = ' + password)
    #     print('pppoe_user = ' + pppoe_user)
    #     print('pppoe_paswd = ' + pppoe_paswd)
    #     print('-=-' * 20)

    #     try:
    #         print('\n\n == Abrindo URL == ')
    #         driver.get('http://' + ip + '/')
    #         link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
    #         link.click()
    #         time.sleep(1)
    #         link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
    #         link.click()
    #         time.sleep(1)
    #         print(' == Autenticando == ')
    #         driver.get('http://' + ip + '/login.asp')
    #         driver.switch_to.default_content()
    #         user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
    #         user_input.send_keys(usuario)
    #         pass_input = driver.find_element_by_id('txtPass')
    #         pass_input.send_keys(senha)
    #         login_button = driver.find_element_by_id('btnLogin')
    #         time.sleep(1)
    #         login_button.click()
    #         time.sleep(1)
    #         config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
    #         print('Clicou em Configurações')
    #         time.sleep(1)
    #         config_internet = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
    #         print('Clicou em Internet')
    #         time.sleep(1)
    #         config_internet_user = driver.find_element_by_xpath('//*[@id="txtUsername"]').clear()
    #         config_internet_user = driver.find_element_by_xpath('//*[@id="txtUsername"]').send_keys(pppoe_user)
    #         config_internet_passwd = driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
    #         config_internet_passwd = driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(pppoe_paswd)
    #         config_internet_salvar = driver.find_element_by_xpath('//*[@id="btnSave"]').click()
    #         if driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/div[2]/table/tbody/tr[2]/td[2]/span'):
    #             result = '200_OK'
    #         else:
    #             result = '400_NOK'

    #         time.sleep(8)
    #         driver.quit()

    #         return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changePPPoESettingsWrong", "Probe#": "XXXXXXX", "Description": "Altera usuário/senha de PPPoE via Web GUI", "Resultado": result}

    #     except NoSuchElementException as exception:
    #         print(exception)
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changePPPoESettingsWrong", "Probe#": "XXXXXXX", "Description": "Altera usuário/senha de PPPoE via Web GUI", "Resultado": str(exception)}

    #     except Exception as e:
    #         print(e)
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changePPPoESettingsWrong", "Probe#": "XXXXXXX", "Description": "Altera usuário/senha de PPPoE via Web GUI", "Resultado": str(e)}


    # 376
    def changePPPoESettingsWrong(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "changePPPoESettingsWrong", 
                        "Probe#": "XXXXXXX", 
                        "Description": "Altera usuário/senha de PPPoE via Web GUI", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.changePPPoESettingsWrong_376(flask_username)

    # 377
    def changePPPoESettingsWrong_2(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "changePPPoESettingsWrong", 
                        "Probe#": "XXXXXXX", 
                        "Description": "Altera usuário/senha de PPPoE via Web GUI", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.changePPPoESettingsWrong_377(flask_username)

    # 378 #mlv
    def changePPPoESettingsWrongAuthentication(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "changePPPoESettingsWrongAuthentication", 
                        "Probe#": "XXXXXXX", 
                        "Description": "Erro de autenticacao com as credenciais PPPoE inseridas pelo usuario.", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.changePPPoESettingsWrongAuthentication_378(flask_username)

    # def connectWizardhttps(self,ip,username,password): ### TUDO OK
        
    #     driver = WebDriver.get_driver()
    #     usuario = username
    #     senha = password
    #     print()
    #     print()
    #     print('-=-' * 20)
    #     print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
    #     print('-=-' * 20)
    #     print('\n\n -- PARAMETROS DE ENTRADA --')
    #     print('ip = ' + ip)
    #     print('username = ' + username)
    #     print('password = ' + password)
    #     print('-=-' * 20)
    #     try:
    #         print('\n\n == Abrindo URL == ')
    #         driver.get('https://' + ip + '/')
    #     except NoSuchElementException as exception:
    #         print(exception)
    #         driver.quit()
    #         return {"Resultado_Probe": "NOK", "ProbeName": "connectWizardhttps", "Probe#": "349", "Description": "Validar erro de conexão com metodo https ", "Resultado": str(exception)}
    #     except Exception as e:
    #         print(e)
    #         driver.quit()
    #         return {"Resultado_Probe": "OK", "ProbeName": "connectWizardhttps", "Probe#": "349", "Description": "Validar erro de conexão com metodo https ", "Resultado": str(e)}


    # 379
    def connectWizardhttps(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "connectWizardhttps", 
                        "Probe#": "346", 
                        "Description": "Validar erro de conexão com metodo https", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.connectWizardhttps_379(flask_username)

    
    # def checkPPPoEStatus(self,ip): ### TUDO OK
        
    #     driver = WebDriver.get_driver()
    #     print()
    #     print()
    #     print('-=-' * 20)
    #     print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
    #     print('-=-' * 20)
    #     print('\n\n -- PARAMETROS DE ENTRADA --')
    #     print('ip = ' + ip)
    #     print('-=-' * 20)
    #     try:
    #         print('\n\n == Abrindo URL == ')
    #         driver.get('http://' + ip + '/index_cliente.asp')
    #         print('\n#############################################'
    #               '\n MENU >> STATUS >> INTERNET'
    #               '\n#############################################\n')
    #         ### ------------------------------------------ ###
    #         ###         STATUS > INTERNET
    #         ### ------------------------------------------ ###
    #         internet = driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[3]/th/span').text
    #         print(internet)
    #         divPpp = driver.find_element_by_id('divPpp').text
    #         divPpp = divPpp.split("\n")
    #         print(divPpp)
    #         detalhes_internet = driver.find_element_by_link_text('Detalhes')
    #         print(detalhes_internet.text)
    #         detalhes_internet.click()
    #         detalhes_IPv4_head = driver.find_element_by_link_text('IPv4').text
    #         print(detalhes_IPv4_head)
    #         detalhes_IPv4 = driver.find_element_by_id('tabip-02')
    #         detalhes_IPv4 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[1]')
    #         time.sleep(1)
    #         items_key_internet_ipv4 = detalhes_IPv4.find_elements_by_tag_name("li")
    #         detalhes_IPv4_nome = []
    #         for i in items_key_internet_ipv4:
    #             teste = i.text
    #             # print(i.text)
    #             detalhes_IPv4_nome.append(teste)
    #         print(detalhes_IPv4_nome)
    #         detalhes_IPv4 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[2]')
    #         items_key = detalhes_IPv4.find_elements_by_tag_name("li")
    #         detalhes_IPv4_valor = []
    #         for i in items_key:
    #             teste = i.text
    #             # print(i.text)
    #             detalhes_IPv4_valor.append(teste)
    #         print(detalhes_IPv4_valor)
    #         time.sleep(2)
    #         detalhes_IPv6 = driver.find_element_by_link_text('IPv6')
    #         detalhes_IPv6.click()
    #         time.sleep(1)
    #         detalhes_IPv6_head = driver.find_element_by_link_text('IPv6').text
    #         print(detalhes_IPv6_head)
    #         detalhes_IPv6 = driver.find_element_by_id('tabip-02')
    #         detalhes_IPv6 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[1]')
    #         time.sleep(1)
    #         items_key = detalhes_IPv6.find_elements_by_tag_name("li")
    #         detalhes_IPv6_nome = []
    #         for item in items_key:
    #             teste = item.text
    #             # print(item.text)
    #             detalhes_IPv6_nome.append(teste)
    #         print(detalhes_IPv6_nome)
    #         detalhes_IPv6 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[2]')
    #         items_key = detalhes_IPv6.find_elements_by_tag_name("li")
    #         detalhes_IPv6_valor = []
    #         for item in items_key:
    #             teste = item.text
    #             # print(item.text)
    #             detalhes_IPv6_valor.append(teste)
    #         print(detalhes_IPv6_valor)
    #         time.sleep(2)
    #         print('\n\n\n == Criando JSON de saída... == ')
    #         json_saida = {
    #             "Status":
    #                 {
    #                     internet:
    #                         {
    #                             divPpp[0]: divPpp[1],
    #                             detalhes_IPv4_head:
    #                                 {
    #                                     detalhes_IPv4_nome[0]: detalhes_IPv4_valor[0],
    #                                     detalhes_IPv4_nome[1]: detalhes_IPv4_valor[1],
    #                                     detalhes_IPv4_nome[2]: detalhes_IPv4_valor[2],
    #                                     detalhes_IPv4_nome[3]: detalhes_IPv4_valor[3],
    #                                     detalhes_IPv4_nome[4]: detalhes_IPv4_valor[4]
    #                                 },
    #                             detalhes_IPv6_head:
    #                                 {
    #                                     detalhes_IPv6_nome[0]: detalhes_IPv6_valor[0],
    #                                     detalhes_IPv6_nome[1]: detalhes_IPv6_valor[1],
    #                                     detalhes_IPv6_nome[2]: detalhes_IPv6_valor[2],
    #                                     detalhes_IPv6_nome[3]: detalhes_IPv6_valor[3],
    #                                     detalhes_IPv6_nome[4]: detalhes_IPv6_valor[4],
    #                                     detalhes_IPv6_nome[5]: detalhes_IPv6_valor[5]
    #                                 }
    #                         }
    #                 }
    #         }

    #         #json_saida = json.dumps(json_saida, ensure_ascii=False)
    #         print(json_saida)
    #         driver.quit()
    #         return {"Resultado_Probe":"OK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "146", "Description": "Verifica o status da conexão PPPoE", "Resultado": json_saida}
    #     except NoSuchElementException as exception:
    #         print(exception)
    #         driver.quit()
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "146", "Description": "Verifica o status da conexão PPPoE", "Resultado": str(exception)}
    #     except Exception as e:
    #         print(e)
    #         driver.quit()
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "146", "Description": "Verifica o status da conexão PPPoE", "Resultado": str(e)}


    # 380
    def checkPPPoEStatus(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkPPPoEStatus", 
                        "Probe#": "146", 
                        "Description": "Verifica o status da conexão PPPoE", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkPPPoEStatus_380(flask_username)

    # 381 #mlv
    def checkPPPoELoginToConfigWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkPPPoELoginToConfigWizard", 
                        "Probe#": "146", 
                        "Description": "Verifica se o usuario esta logado para editar configuracoes no Wizard", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.getFullConfig_381(flask_username)
 
    #382
    def getFullConfig_2(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Idioma padrão do wizard deve ser em Português", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.getFullConfig_382(flask_username)

    # def execPingWizard(self, ip, username, password, destino, tentativas):
        
    #     driver = WebDriver.get_driver()
    #     driver.execute_script("window.alert = function() {};")
    #     usuario = username
    #     senha = password
    #     destino = destino
    #     tentativas = tentativas
    #     print()
    #     print()
    #     print('-=-' * 20)
    #     print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
    #     print('-=-' * 20)
    #     print('\n\n -- PARAMETROS DE ENTRADA --')
    #     print('ip = ' + ip)
    #     print('username = ' + username)
    #     print('password = ' + password)
    #     print('destino = ' + destino)
    #     print('tentativas = ' + tentativas)
    #     print('-=-' * 20)

    #     try:
    #         print('\n\n == Abrindo URL == ')
    #         driver.get('http://' + ip + '/')
    #         link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
    #         link.click()
    #         time.sleep(1)
    #         link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
    #         link.click()
    #         time.sleep(1)
    #         print(' == Autenticando == ')
    #         driver.get('http://' + ip + '/login.asp')
    #         driver.switch_to.default_content()
    #         user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
    #         user_input.send_keys(usuario)
    #         pass_input = driver.find_element_by_id('txtPass')
    #         pass_input.send_keys(senha)
    #         login_button = driver.find_element_by_id('btnLogin')
    #         time.sleep(1)
    #         login_button.click()
    #         time.sleep(1)
    #         gerenc = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
    #         print('Clicou em Gerenciamento')
    #         time.sleep(1)
    #         gerenc_Ferram = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[6]/a').click()
    #         print('Clicou em Ferramentas')
    #         time.sleep(1)
    #         gerenc_Ferram_dest = driver.find_element_by_xpath('//*[@id="txtDest"]').send_keys(destino)
    #         gerenc_Ferram_tenta = driver.find_element_by_xpath('//*[@id="txtNum"]').send_keys(tentativas)
    #         gerenc_Ferram_tenta_exec = driver.find_element_by_xpath('//*[@id="btnTest"]').click()
    #         time.sleep(6)
    #         result = driver.find_element_by_xpath('//*[@id="txtResult"]').get_property('value')

    #         json_saida = {
    #             "Resultados":result
    #         }
    #         print(json_saida)
    #         driver.quit()

    #         return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execPingWizard", "Probe#": "XXXXXXX", "Description": "Executa teste de Ping via Web GUI", "Resultado": result}

    #     except NoSuchElementException as exception:
    #         print(exception)
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execPingWizard", "Probe#": "XXXXXXX", "Description": "Executa teste de Ping via Web GUI", "Resultado": str(exception)}

    #     except Exception as e:
    #         print(e)
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execPingWizard", "Probe#": "XXXXXXX", "Description": "Executa teste de Ping via Web GUI", "Resultado": str(e)}


    #384
    def execPingWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "execPingWizard", 
                        "Probe#": "XXXXXXX", 
                        "Description": "Executa teste de Ping via Web GUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username,
                                     driver=driver,
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.execPingWizard_384(flask_username)

    #386 mlv
    def statusWizardWifi(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Mostrar corretamente o Status do WI-FI 2.4GHz caso possua esse serviço.", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.statusWizardIptv_386(flask_username)

    #387
    def statusWizardInet(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Mostra corretamente o status PPP no índice", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.statusWizardInet_387(flask_username)
    
    
    #388
    def registerWizardVoip(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Mostrar corretamente as Estatísticas de VoIP caso possua esse serviço.", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.registerWizardVoip_388(flask_username)

    
    #389
    def statusWizardIptv(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Mostrar corretamente o Status de TV caso possua esse serviço.", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.statusWizardIptv_389(flask_username)


    #390
    def statusWizardVoip(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Informações sobre a conta SIP no Indice caso possua esse serviço.", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.statusWizardVoip_390(flask_username)


    # 392
    def verifyDnsService(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "verifyDnsService", 
                        "Probe#": "392", 
                        "Description": "Erro na habilitacao do servico DNS", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.verifyDnsService_392(flask_username)
        


    #393 mlv
    def createDmzViaWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "createDmzViaWizard", 
                        "Probe#": "393", 
                        "Description": "Erro de criacao de uma DMZ pelo usuario.", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.createDmzViaWizard_393(flask_username)

    #394 mlv
    def configFirewallViaWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "createDmzViaWizard", 
                        "Probe#": "393", 
                        "Description": "Erro de criacao de uma DMZ pelo usuario.", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.configFirewallViaWizard_394(flask_username)



      #395 mlv
    def configUpnpViaWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "configUpnpViaWizard", 
                        "Probe#": "395", 
                        "Description": "Erro de configuracao de uma UPnP pelo usuario.", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.configUpnpViaWizard_395(flask_username)

    #396 mlv
    def configDdnsViaWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "configDdnsViaWizard", 
                        "Probe#": "396", 
                        "Description": "Fornecer configuracao DDNS pelo usuario.", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.configDdnsViaWizard_396(flask_username)
    
    #397 mlv
    def configIpDhcpViaWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "configIpDhcpViaWizard", 
                        "Probe#": "397", 
                        "Description": "Erro ao associar um endereco de IP no DHCP pelo usuario.", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.configIpDhcpViaWizard_397(flask_username)


    # def testeSite(self,site1, site2, site3): ### TUDO OK
        
        # driver = WebDriver.get_driver()
        # wait = WebDriverWait(driver, 10)
        # size = driver.set_window_size(1280, 600)
        # print()
        # print()
        # print('-=-' * 20)
        # print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        # print('-=-' * 20)
        # print('\n\n -- PARAMETROS DE ENTRADA --')
        # print('site1 = ' + site1)
        # print('site2 = ' + site2)
        # print('site3 = ' + site3)
        # print('-=-' * 20)
        # try:
        #     print('\n\n == Abrindo URL ' + site1+ ' == ')
        #     driver.get(site1 + '/')
        #     print('\n\n == Aguardando redirecionamento de página == ')
        #     time.sleep(1)
        #     gpon = driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
        #     divOptical = driver.find_element_by_id('divOptical').text
        #     divOptical = divOptical.split("\n")
        #     print(divOptical)
        #     divOptRx = driver.find_element_by_id('divOptRx').text
        #     divOptRx = divOptRx.split("\n")
        #     print(divOptRx)
        #     divOptTx = driver.find_element_by_id('divOptTx').text
        #     divOptTx = divOptTx.split("\n")
        #     print(divOptTx)
        #     time.sleep(2)
        #     print('\n\n == Abrindo URL ' + site2+ ' == ')
        #     driver.get(site2 + '/')
        #     print('\n\n == Aguardando redirecionamento de página == ')
        #     time.sleep(1)
        #     user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
        #     user_input.send_keys('usuario')
        #     pass_input = driver.find_element_by_id('txtPass')
        #     pass_input.send_keys('senha')
        #     login_button = driver.find_element_by_id('btnLogin')
        #     print('\n\n == Abrindo URL ' + site3+ ' == ')
        #     driver.get(site3 + '/')
        #     print('\n\n == Aguardando redirecionamento de página == ')
        #     time.sleep(1)
        #     gpon = driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
        #     divOptical = driver.find_element_by_id('divOptical').text
        #     divOptical = divOptical.split("\n")
        #     print(divOptical)
        #     divOptRx = driver.find_element_by_id('divOptRx').text
        #     divOptRx = divOptRx.split("\n")
        #     print(divOptRx)
        #     divOptTx = driver.find_element_by_id('divOptTx').text
        #     divOptTx = divOptTx.split("\n")
        #     print(divOptTx)
        #     time.sleep(2)
        #     driver.quit()
        #     return {"Resultado_Probe": "OK","ProbeName": "testeSite", "Probe#": "44", "Description": "Abrir URL", "Resultado": "200 OK"}
        # except NoSuchElementException as exception:
        #     print(exception)
        #     driver.quit()
        #     return {"Resultado_Probe": "NOK", "ProbeName": "testeSite", "Probe#": "44", "Description": "Abrir URL", "Resultado": str(exception)}
        # except Exception as e:
        #     print(e)
        #     driver.quit()
        #     return {"Resultado_Probe": "NOK", "ProbeName": "testeSite", "Probe#": "44", "Description": "Abrir URL", "Resultado": str(e)}



    #399
    def testeSiteWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "testeSite", 
                        "Probe#": "44", 
                        "Description": "Abrir URL", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username,
                                     driver=driver,
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.testeSiteWizard_399(flask_username)


    # def checkBridgeMode(self, ip, username, password): ### TUDO OK
        
    #     driver = WebDriver.get_driver()
    #     usuario = username
    #     senha = password
    #     print()
    #     print()
    #     print('-=-' * 20)
    #     print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
    #     print('-=-' * 20)
    #     print('\n\n -- PARAMETROS DE ENTRADA --')
    #     print('ip = ' + ip)
    #     print('username = ' + username)
    #     print('password = ' + password)
    #     print('-=-' * 20)
    #     try:
    #         print('\n\n == Abrindo URL == ')
    #         driver.get('http://' + ip + '/')
    #         link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
    #         link.click()
    #         time.sleep(1)
    #         link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
    #         link.click()
    #         time.sleep(1)
    #         print(' == Autenticando == ')
    #         driver.get('http://' + ip + '/login.asp')
    #         driver.switch_to.default_content()
    #         user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
    #         user_input.send_keys(usuario)
    #         pass_input = driver.find_element_by_id('txtPass')
    #         pass_input.send_keys(senha)
    #         login_button = driver.find_element_by_id('btnLogin')
    #         time.sleep(1)
    #         login_button.click()
    #         time.sleep(1)
    #         print('\n#############################################'
    #               '\n MENU >> CONFIGURAÇÕES >> MODO DA WAN '
    #               '\n#############################################\n')
    #         ### ------------------------------------------ ###
    #         ###         CONFIGURAÇÕES > MODO DA WAN
    #         ### ------------------------------------------ ###
    #         config = driver.find_element_by_link_text('Configurações').click()
    #         time.sleep(1)
    #         config_modowan = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[7]/a')
    #         print(config_modowan.text)
    #         config_modowan.click()
    #         config_modowan = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[7]/a').text
    #         time.sleep(1)
    #         config_modowan_bridge = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/thead/tr/th').text
    #         print(config_modowan_bridge)
    #         time.sleep(1)
    #         config_modowan_bridge_modo = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[1]').text
    #         print(config_modowan_bridge_modo)
    #         config_modowan_bridge_modo_valor = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[2]/select').click()
    #         time.sleep(1)
    #         select = Select(driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[2]/select'))
    #         config_modowan_bridge_modo_valor = []
    #         for item in select.options:
    #             teste = item.get_attribute('innerText')
    #             config_modowan_bridge_modo_valor.append(teste)
    #             print(item.get_attribute('value'), item.get_attribute('innerText'))
    #         config_modowan_bridge_modo_valor = json.dumps(config_modowan_bridge_modo_valor, ensure_ascii=False)
    #         print(config_modowan_bridge_modo_valor)
    #         print(type(config_modowan_bridge_modo_valor))
    #         time.sleep(2)
    #         driver.quit()
    #         return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkBridgeMode", "Probe#": "21", "Description": "Verificar se existe campo para habilitar Bridge", "Resultado": config_modowan_bridge_modo_valor}
    #     except NoSuchElementException as exception:
    #         print(exception)
    #         driver.quit()
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkBridgeMode", "Probe#": "21", "Description": "Verificar se existe campo para habilitar Bridge", "Resultado": str(exception)}
    #     except Exception as e:
    #         print(e)
    #         driver.quit()
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkBridgeMode", "Probe#": "21", "Description": "Verificar se existe campo para habilitar Bridge", "Resultado": str(e)}


    #21
    def checkBridgeMode(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkBridgeMode", 
                        "Probe#": "21", 
                        "Description": "Verificar se existe campo para habilitar Bridge", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username,
                                     driver=driver,
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.checkBridgeMode_21(flask_username)

    #29
    def changeIPDhcpViaWizard(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "changeIPDhcpViaWizard", 
                        "Probe#": "29", 
                        "Description": "Mudar range de IP do DHCP Server.", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='functionalProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username,
                                     driver=driver,
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.changeIPDhcpViaWizard_29(flask_username)

        
    

    # 36
    def checkRedeGpon_2(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkPPPoEStatus", 
                        "Probe#": "36", 
                        "Description": "Verifica o status da conexão PPPoE", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.checkRedeGpon_36(flask_username)

        
    # 79
    def accessPadrao_2(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkPPPoEStatus", 
                       "Probe#": "79", 
                       "Description": "Acessar página padrão "}
                       
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.accessPadrao_79(flask_username)


    # 146
    def checkPPPoEStatus_2(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkPPPoEStatus", 
                        "Probe#": "146", 
                        "Description": "Verifica o status da conexão PPPoE", 
                        "obs": None}
                        
        hgu = HGUModelFactory.getHGU(probe='wizardProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkPPPoEStatus_146(flask_username)


    def getFullConfigASKEY3505(self, ip, username, password): ### DISPOSITIVO ASKEY 3505
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print()
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)

        try:
            driver.get('http://' + ip + '/')
            driver.switch_to.frame('mainFrame')
            link = driver.find_element_by_link_text('Configurações')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_link_text('Rede Wi-Fi 2,4 GHz')
            link.click()
            print('clicou no botao Rede Wifi')
            time.sleep(1)
            driver.switch_to.frame('mainFrame')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            driver.switch_to.frame('mainFrame')

            ### ------------------------------------------ ###
            ###         STATUS
            ### ------------------------------------------ ###
            link = driver.find_element_by_link_text('Status')
            print(link.text)
            link.click()
            time.sleep(1)
            ### ------------------------------------------ ###
            ###         STATUS > GPON
            ### ------------------------------------------ ###
            gpon = driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span')
            print(gpon.text)
            divOptical = driver.find_element_by_id('divOptical')
            print(divOptical.text)
            divOptRx = driver.find_element_by_id('divOptRx')
            print(divOptRx.text)
            divOptTx = driver.find_element_by_id('divOptTx')
            print(divOptTx.text)
            ### ------------------------------------------ ###
            ###         STATUS > INTERNET
            ### ------------------------------------------ ###
            internet = driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[3]/th/span')
            print(internet.text)
            divPpp = driver.find_element_by_id('divexcept NoSuchElementException as exception:Ppp')
        #     print(exception)
        #     self._driver.quit()
        #     return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "getFullConfig", "Probe#": "350", "Description": "Coleta as informações da página WebGUI", "Resultado": str(exception)}
        # except Exception as e:
        #     print(e)
        #     self._driver.quit()
        #     return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "getFullConfig", "Probe#": "350", "Description": "Coleta as informações da página WebGUI", "Resultado": str(e)}


            print(divPpp.text)
            detalhes_internet = driver.find_element_by_link_text('Detalhes')
            print(detalhes_internet.text)
            detalhes_internet.click()
            detalhes_IPv4 = driver.find_element_by_link_text('IPv4')
            print(detalhes_IPv4.text)
            time.sleep(1)
            detalhes_IPv4 = driver.find_element_by_id('tabip-02')
            detalhes_IPv4 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[1]')
            time.sleep(1)
            items_key = detalhes_IPv4.find_elements_by_tag_name("li")
            for item in items_key:
                print(item.text)
            detalhes_IPv4 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[2]/div[2]')
            items_key = detalhes_IPv4.find_elements_by_tag_name("li")
            for item in items_key:
                print(item.text)
            print()
            print()
            print()
            time.sleep(2)
            detalhes_IPv6 = driver.find_element_by_link_text('IPv6')
            detalhes_IPv6.click()
            time.sleep(1)
            detalhes_IPv6 = driver.find_element_by_id('tabip-02')
            detalhes_IPv6 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[1]')
            time.sleep(1)
            items_key = detalhes_IPv6.find_elements_by_tag_name("li")
            for item in items_key:
                print(item.text)
            detalhes_IPv6 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div[3]/div[2]')
            items_key = detalhes_IPv6.find_elements_by_tag_name("li")
            for item in items_key:
                print(item.text)
            print()
            print()
            print()
            time.sleep(2)
            ### ------------------------------------------ ###
            ###         STATUS > WIFI 2.4GHz
            ### ------------------------------------------ ###
            wifi_24 = driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[5]/th/span')
            print(wifi_24.text)
            wifi_24_name = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[1]/div')
            print(wifi_24_name.text)
            wifi_24_detalhes = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/a')
            wifi_24_detalhes.click()
            print(wifi_24_detalhes.text)
            wifi_24_detalhes_info = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[1]/div')
            items_key = wifi_24_detalhes_info.find_elements_by_tag_name("li")
            for item in items_key:
                print(item.text)
            wifi_24_detalhes_stations = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td[2]/textarea').get_attribute('value')
            print(wifi_24_detalhes_stations)
            print()
            print()
            print()
            time.sleep(2)
            ### ------------------------------------------ ###
            ###         STATUS > WIFI 5GHz
            ### ------------------------------------------ ###
            wifi_5 = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/th/span')
            print(wifi_5.text)
            wifi_5_name = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/td[1]/div')
            print(wifi_5_name.text)
            wifi_5_detalhes = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[7]/td[2]/a')
            wifi_5_detalhes.click()
            print(wifi_5_detalhes.text)
            wifi_5_detalhes_info = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[1]/div')
            items_key = wifi_5_detalhes_info.find_elements_by_tag_name("li")
            for item in items_key:
                print(item.text)
            wifi_5_detalhes_stations = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[8]/td[2]/textarea').get_attribute('value')
            print(wifi_5_detalhes_stations)
            print()
            print()
            print()
            time.sleep(2)

        except NoSuchElementException as exception:
            print(exception)


    #425 
    def getFullConfig(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.getFullConfig_425(flask_username)

    
    #426
    def verificarSenhaPppDefaultFibra(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarSenhaPppDefaultFibra_426(flask_username)
        
        
   
    def checkFacebook(self): ### TUDO OK
        
        driver = WebDriver.get_driver()

        try:
            driver.get('https://facebook.com')
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="email"]').send_keys('cddbrasil2020@gmail.com')
            driver.find_element_by_xpath('//*[@id="pass"]').send_keys('cdd12345678' + Keys.RETURN)
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="mount_0_0_et"]/div/div[1]/div/div[2]/div[2]/div/div/div/div/label').click()

            print('Botão clicado')
            time.sleep(50)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkFacebook", "Probe#": "47", "Description": "Executar algumas validações site Facebook", "Resultado": "200_OK"}
        except NoSuchElementException as exception:
            print(exception)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkFacebook", "Probe#": "47", "Description": "Executar algumas validações site Facebook", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkFacebook", "Probe#": "47", "Description": "Executar algumas validações site Facebook", "Resultado": str(e)}

    def checkFacebookIPv6(self): ### TUDO OK
        
        driver = WebDriver.get_driver()

        try:
            driver.get('https://v6.facebook.com')
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="email"]').send_keys('cddbrasil2020@gmail.com')
            driver.find_element_by_xpath('//*[@id="pass"]').send_keys('cdd12345678' + Keys.RETURN)
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="mount_0_0_et"]/div/div[1]/div/div[2]/div[2]/div/div/div/div/label').click()

            print('Botão clicado')
            time.sleep(50)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkFacebook", "Probe#": "47", "Description": "Executar algumas validações site Facebook", "Resultado": "200_OK"}
        except NoSuchElementException as exception:
            print(exception)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkFacebook", "Probe#": "47", "Description": "Executar algumas validações site Facebook", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkFacebook", "Probe#": "47", "Description": "Executar algumas validações site Facebook", "Resultado": str(e)}

    def checkInstagram(self): ### TUDO OK
        
        driver = WebDriver.get_driver()

        try:
            driver.get('https://instagram.com')
            time.sleep(1)
            criar = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[2]/div/p/a/span').click()
            print('Botão clicado')
            time.sleep(3)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkInstagram", "Probe#": "46", "Description": "Executar algumas validações site Instagram", "Resultado": "200_OK"}
        except NoSuchElementException as exception:
            print(exception)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkInstagram", "Probe#": "46", "Description": "Executar algumas validações site Instagram", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkInstagram", "Probe#": "46", "Description": "Executar algumas validações site Instagram", "Resultado": str(e)}

    def checkTwitter(self): ### TUDO OK
        
        driver = WebDriver.get_driver()

        try:
            driver.get('https://twitter.com')
            time.sleep(1)
            criar = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[3]/a[2]/div/span/span').click()
            print('Botão clicado')
            time.sleep(3)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkTwitter", "Probe#": "48", "Description": "Executar algumas validações site Twitter", "Resultado": "200_OK"}
        except NoSuchElementException as exception:
            print(exception)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkTwitter", "Probe#": "48", "Description": "Executar algumas validações site Twitter", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkTwitter", "Probe#": "48", "Description": "Executar algumas validações site Twitter", "Resultado": str(e)}


    #403
    def accessPadrao(self, ip, username, password, model_name, **kwargs): ### TUDO OK
        
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkPPPoEStatus", 
                       "Probe#": "79", 
                       "Description": "Acessar página padrão "}
                       
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.accessPadrao_403()


    def getFullConfigPadrao(self,ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('mainFrm')
            device_info = driver.find_element_by_xpath('/html/body/h1').text
            print(device_info)
            device_info_hw_version = driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/th').text
            print(device_info_hw_version)
            device_info_hw_version_valor = driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td').text
            print(device_info_hw_version_valor)

            device_info_fw_version = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/th').text
            print(device_info_fw_version)
            device_info_fw_version_valor = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td').text
            print(device_info_fw_version_valor)

            device_info_system_time = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/th').text
            print(device_info_system_time)
            device_info_system_time_valor = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td').text
            print(device_info_system_time_valor)

            device_info_system_uptime = driver.find_element_by_xpath('/html/body/table/tbody/tr[4]/th').text
            print(device_info_system_uptime)
            device_info_system_uptime_valor = driver.find_element_by_xpath('/html/body/table/tbody/tr[4]/td').text
            print(device_info_system_uptime_valor)

            device_info_gpon_serial = driver.find_element_by_xpath('/html/body/table/tbody/tr[8]/th').text
            print(device_info_gpon_serial)
            device_info_gpon_serial_valor = driver.find_element_by_xpath('/html/body/table/tbody/tr[8]/td').text
            print(device_info_gpon_serial_valor)
            time.sleep(1)

            print('\n#############################################'
                  '\n MENU >> LAN SETTINGS  '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         LAN SETTINGS > IP INTERFACE
            ### ------------------------------------------ ###
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('menuFrm')
            lanSettings = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/p[1]/b').text
            print(lanSettings)
            lanSettings_ipInterfc = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[1]').click()
            time.sleep(1)
            lanSettings_ipInterfc = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[1]').text
            print(lanSettings_ipInterfc)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            lanSettings_ipInterfc_ipv4 = driver.find_element_by_xpath('/html/body/h1').text
            print(lanSettings_ipInterfc_ipv4)
            lanSettings_ipInterfc_ipv4_ipInterfc = driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
            print(lanSettings_ipInterfc_ipv4_ipInterfc)
            lanSettings_ipInterfc_ipv4_ipInterfc_adminState = driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[1]/label').text
            print(lanSettings_ipInterfc_ipv4_ipInterfc_adminState)
            lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor = driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[1]/input[1]').get_attribute('checked')
            if lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor == 'true':
                lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor = 'Habilitado'
            else:
                lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor = 'Desabilitado'
            print(lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor)

            lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping = driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[2]/label').text
            print(lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping)
            lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor = driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[2]/input[1]').get_attribute('checked')
            if lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor == 'true':
                lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor = 'Habilitado'
            else:
                lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor = 'Desabilitado'
            print(lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor)
            lanSettings_ipInterfc_ipv4_ipv4_addr = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            lanSettings_ipInterfc_ipv4_ipv4_addr = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
            print(lanSettings_ipInterfc_ipv4_ipv4_addr)
            lanSettings_ipInterfc_ipv4_ipv4_addr_head = []
            for head in range(1,len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))):
                teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th['+ str(head) + ']').text
                lanSettings_ipInterfc_ipv4_ipv4_addr_head.append(teste)
            print(lanSettings_ipInterfc_ipv4_ipv4_addr_head)
            countlinhas = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
            countcols = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[1]/td'))
            lanSettings_ipInterfc_ipv4_ipv4_addr_table = []
            print(teste)
            for col in range(1, countcols):
                teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td['+ str(col) + ']').text
                lanSettings_ipInterfc_ipv4_ipv4_addr_table.append(teste)
            print(lanSettings_ipInterfc_ipv4_ipv4_addr_table)

            ### ------------------------------------------ ###
            ###         LAN SETTINGS > IPv6
            ### ------------------------------------------ ###
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('menuFrm')
            lanSettings_ipv6 = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[3]').click()
            lanSettings_ipv6 = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[3]').text
            print(lanSettings_ipv6)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            lanSettings_ipv6_Status = driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[1]/label[1]').text
            print(lanSettings_ipv6_Status)
            lanSettings_ipv6_Status_valor = driver.find_element_by_xpath('//*[@id="ipv6_opr_status"]').text
            print(lanSettings_ipv6_Status_valor)
            lanSettings_ipv6_Global = driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[2]/label[1]').text
            print(lanSettings_ipv6_Global)
            lanSettings_ipv6_Global_valor = driver.find_element_by_xpath('//*[@id="g_ipv6addr_all"]').text
            print(lanSettings_ipv6_Global_valor)
            lanSettings_ipv6_AdmState = driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[3]/label').text
            print(lanSettings_ipv6_AdmState)
            lanSettings_ipv6_AdmState_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/div[3]/input[1]').get_attribute('checked')
            if lanSettings_ipv6_AdmState_valor == 'true':
                lanSettings_ipv6_AdmState_valor = 'Habilitado'
            else:
                lanSettings_ipv6_AdmState_valor = 'Desabilitado'
            print(lanSettings_ipv6_AdmState_valor)

            lanSettings_ipv6_RADVD = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/legend').text
            print(lanSettings_ipv6_RADVD)
            lanSettings_ipv6_RADVD_AdmState = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[1]/label').text
            print(lanSettings_ipv6_RADVD_AdmState)
            lanSettings_ipv6_RADVD_AdmState_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[1]/input[1]').get_attribute('checked')
            if lanSettings_ipv6_RADVD_AdmState_valor == 'true':
                lanSettings_ipv6_RADVD_AdmState_valor = 'Habilitado'
            else:
                lanSettings_ipv6_RADVD_AdmState_valor = 'Desabilitado'
            print(lanSettings_ipv6_RADVD_AdmState_valor)
            lanSettings_ipv6_RADVD_PrfxDeleg = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[2]/label').text
            print(lanSettings_ipv6_RADVD_PrfxDeleg)
            lanSettings_ipv6_RADVD_PrfxDeleg_valor = driver.find_element_by_xpath('//*[@id="IPIntfId"]').get_attribute('value')
            if lanSettings_ipv6_RADVD_PrfxDeleg_valor == '2':
                lanSettings_ipv6_RADVD_PrfxDeleg_valor = 'ip2'
            print(lanSettings_ipv6_RADVD_PrfxDeleg_valor)
            lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[3]/input').get_attribute('checked')
            if lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor == 'true':
                lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor = 'Habilitado'
            else:
                lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor = 'Desabilitado'
            print(lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor)
            lanSettings_ipv6_RADVD_Prefix = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[4]/label').text
            print(lanSettings_ipv6_RADVD_Prefix)
            lanSettings_ipv6_RADVD_Prefix_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[4]/input').get_attribute('value')
            print(lanSettings_ipv6_RADVD_Prefix_valor)
            lanSettings_ipv6_RADVD_Preferred = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[5]/label').text
            print(lanSettings_ipv6_RADVD_Preferred)
            lanSettings_ipv6_RADVD_Preferred_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[5]/input').get_attribute('value')
            print(lanSettings_ipv6_RADVD_Preferred_valor)
            lanSettings_ipv6_RADVD_Valid = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[6]/label').text
            print(lanSettings_ipv6_RADVD_Valid)
            lanSettings_ipv6_RADVD_Valid_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[1]/div[6]/input').get_attribute('value')
            print(lanSettings_ipv6_RADVD_Valid_valor)

            lanSettings_ipv6_DHCPv6 = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/legend').text
            print(lanSettings_ipv6_DHCPv6)
            lanSettings_ipv6_DHCPv6_Mode = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/label').text
            print(lanSettings_ipv6_DHCPv6_Mode)
            if driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[1]').get_attribute('checked') == 'true':
                lanSettings_ipv6_DHCPv6_Mode_valor = 'Desabilitado'
            if driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[2]').get_attribute('checked') == 'true':
                lanSettings_ipv6_DHCPv6_Mode_valor = 'Stateless'
            if driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[3]').get_attribute('checked') == 'true':
                lanSettings_ipv6_DHCPv6_Mode_valor = 'Stateful'
            print(lanSettings_ipv6_DHCPv6_Mode_valor)
            lanSettings_ipv6_DHCPv6_Start = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[2]/label').text
            print(lanSettings_ipv6_DHCPv6_Start)
            lanSettings_ipv6_DHCPv6_Start_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[2]/input').get_attribute('value')
            print(lanSettings_ipv6_DHCPv6_Start_valor)
            lanSettings_ipv6_DHCPv6_End = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[3]/label').text
            print(lanSettings_ipv6_DHCPv6_End)
            lanSettings_ipv6_DHCPv6_End_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[3]/input').get_attribute('value')
            print(lanSettings_ipv6_DHCPv6_End_valor)
            lanSettings_ipv6_DHCPv6_Lease = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[4]/label').text
            print(lanSettings_ipv6_DHCPv6_Lease)
            lanSettings_ipv6_DHCPv6_Lease_valor = driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[4]/input').get_attribute('value')
            print(lanSettings_ipv6_DHCPv6_Lease_valor)

            json_saida = {
                lanSettings:
                    {
                        lanSettings_ipInterfc:
                            {
                                lanSettings_ipInterfc_ipv4_ipInterfc_adminState:lanSettings_ipInterfc_ipv4_ipInterfc_adminState_valor,
                                lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping:lanSettings_ipInterfc_ipv4_ipInterfc_IGMPSnooping_valor
                            },
                        lanSettings_ipInterfc_ipv4_ipv4_addr:
                            {
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[2]:lanSettings_ipInterfc_ipv4_ipv4_addr_table[2],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[3]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[3],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[4]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[4],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[5]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[5],
                                lanSettings_ipInterfc_ipv4_ipv4_addr_head[6]: lanSettings_ipInterfc_ipv4_ipv4_addr_table[6]
                            },
                        lanSettings_ipv6:
                            {
                                lanSettings_ipv6_Status:lanSettings_ipv6_Status_valor,
                                lanSettings_ipv6_AdmState:lanSettings_ipv6_RADVD_AdmState_valor,
                                lanSettings_ipv6_Global:lanSettings_ipv6_Global_valor,
                                lanSettings_ipv6_RADVD:
                                    {
                                        lanSettings_ipv6_RADVD_AdmState:lanSettings_ipv6_RADVD_AdmState_valor,
                                        lanSettings_ipv6_RADVD_PrfxDeleg:lanSettings_ipv6_RADVD_PrfxDeleg_valor,
                                        "ULA Prefix":lanSettings_ipv6_RADVD_PrfxDeleg_ULA_valor,
                                        lanSettings_ipv6_RADVD_Prefix:lanSettings_ipv6_RADVD_Prefix_valor,
                                        lanSettings_ipv6_RADVD_Preferred:lanSettings_ipv6_RADVD_Preferred_valor,
                                        lanSettings_ipv6_RADVD_Valid:lanSettings_ipv6_RADVD_Valid_valor
                                    },
                                lanSettings_ipv6_DHCPv6:
                                    {
                                        lanSettings_ipv6_DHCPv6_Mode:lanSettings_ipv6_DHCPv6_Mode_valor,
                                        lanSettings_ipv6_DHCPv6_Start:lanSettings_ipv6_DHCPv6_Start_valor,
                                        lanSettings_ipv6_DHCPv6_End:lanSettings_ipv6_DHCPv6_End_valor,
                                        lanSettings_ipv6_DHCPv6_Lease:lanSettings_ipv6_DHCPv6_Lease_valor
                                    }
                            }

                    }
            }
            print(json_saida)

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "getFullConfigPadrao", "Probe#": "351", "Description": "Coleta as informações da página WebGUI PADRAO ", "Resultado": json_saida}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "getFullConfigPadrao", "Probe#": "351", "Description": "Coleta as informações da página WebGUI PADRAO ", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "getFullConfigPadrao", "Probe#": "351", "Description": "Coleta as informações da página WebGUI PADRAO ", "Resultado": str(e)}

    #411
    def checkACSSettings(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkACSSettings", 
                       "Probe#": "86, 87, 88, 91", 
                       "Description": "Acessar página padrão "}
        
        
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkACSSettings_411(flask_username)

    #412
    def validarDefaultUserACS(self, ip, username, password, model_name, flask_username, **kwargs):
    
        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkACSSettings", 
                       "Probe#": "86, 87, 88, 91", 
                       "Description": "Acessar página padrão, depende do teste 411"}
        
        
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.validarDefaultUserACS_412(flask_username)

    #413
    def validarDefaultPasswordACS(self, ip, username, password, model_name, flask_username, **kwargs):
    
        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkACSSettings", 
                       "Probe#": "86, 87, 88, 91", 
                       "Description": "Acessar página padrão, depende do teste 411"}
        
        
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.validarDefaultPasswordACS_413(flask_username)


    #415
    def periodicInformEnable(self, ip, username, password, model_name, flask_username, **kwargs):
    
        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkACSSettings", 
                       "Probe#": "86, 87, 88, 91", 
                       "Description": "Acessar página padrão, depende do teste 411"}
        
        
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.periodicInformEnable_415(flask_username)


    #416
    def periodicInformInterval(self, ip, username, password, model_name, flask_username, **kwargs):
    
        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkACSSettings", 
                       "Probe#": "86, 87, 88, 91", 
                       "Description": "Acessar página padrão, depende do teste 411"}
        
        
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.periodicInformInterval_416(flask_username)


    #418
    def enableCwmp(self, ip, username, password, model_name, flask_username, **kwargs):
    
        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkACSSettings", 
                       "Probe#": "86, 87, 88, 91", 
                       "Description": "Acessar página padrão, depende do teste 411"}
        
        
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.enableCwmp_418(flask_username)

    #419
    def userConnectionRequest(self, ip, username, password, model_name, flask_username, **kwargs):
    
        dict_result = {'result':'failed', 
                       'obs': None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkACSSettings", 
                       "Probe#": "86, 87, 88, 91", 
                       "Description": "Acessar página padrão, depende do teste 411"}
        
        
        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.userConnectionRequest_419(flask_username)


    def checkRemoteAccess(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            remoteAccess = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[2]').click()
            remoteAccess = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[2]').text
            print(remoteAccess)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            remoteAccess_telnet = driver.find_element_by_xpath('//*[@id="RaccForm"]/div[1]/label').text
            print(remoteAccess_telnet)
            remoteAccess_telnet_valor = driver.find_element_by_xpath('//*[@id="RaccForm"]/div[1]/input').get_attribute('checked')
            if remoteAccess_telnet_valor == 'true':
                remoteAccess_telnet_valor = 'Habilitado'
            else:
                remoteAccess_telnet_valor = 'Desabilitado'
            print(remoteAccess_telnet_valor)
            remoteAccess_SSH = driver.find_element_by_xpath('//*[@id="RaccForm"]/div[2]/label').text
            print(remoteAccess_SSH)
            remoteAccess_SSH_valor = driver.find_element_by_xpath('//*[@id="RaccForm"]/div[2]/input').get_attribute('checked')
            if remoteAccess_SSH_valor == 'true':
                remoteAccess_SSH_valor = 'Habilitado'
            else:
                remoteAccess_SSH_valor = 'Desabilitado'
            print(remoteAccess_SSH_valor)

            json_saida = {
                remoteAccess:
                    {
                        remoteAccess_telnet:remoteAccess_telnet_valor,
                        remoteAccess_SSH:remoteAccess_SSH_valor
                    }
            }
            print(json_saida)





            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkRemoteAccess", "Probe#": "3, 80, 81, 82", "Description": "Coleta informações de Acesso Remoto na página padrão ", "Resultado": json_saida}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkRemoteAccess", "Probe#": "3, 80, 81, 82", "Description": "Coleta informações de Acesso Remoto na página padrão ", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkRemoteAccess", "Probe#": "3, 80, 81, 82", "Description": "Coleta informações de Acesso Remoto na página padrão ", "Resultado": str(e)}

    #405
    def checkTrustDomain(self, ip, username, password, flask_username, model_name, **kwargs):

        driver = WebDriver.get_driver()
        
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkTrustDomain", 
                       "Probe#": "83", 
                       "Description": "Coleta informações de Trust Domain na página padrão"}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.accessRemoteHttp_405(flask_username)

    #406
    def accessRemoteTelnet(self, ip, username, password, flask_username, model_name, **kwargs):

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkTrustDomain", 
                       "Probe#": "83", 
                       "Description": "Coleta informações de Trust Domain na página padrão"}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.accessRemoteTelnet_406(flask_username)
    
    #407
    def accessRemoteSSH(self, ip, username, password, flask_username, model_name, **kwargs):

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkTrustDomain", 
                       "Probe#": "83", 
                       "Description": "Coleta informações de Trust Domain na página padrão"}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.accessRemoteSSH_407(flask_username)

    #408
    def accessRemoteTrustedIP(self, ip, username, password, flask_username, model_name, **kwargs):

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkTrustDomain", 
                       "Probe#": "83", 
                       "Description": "Coleta informações de Trust Domain na página padrão"}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.accessRemoteTrustedIP_408(flask_username)


    #420
    def checkWanInterface(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkWanInterface_420(flask_username)

    #421
    def prioridadePPPoE(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.prioridadePPPoE_421(flask_username)


    #422
    def tipoRedeInet(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.tipoRedeInet_422(flask_username)


    #427
    def checkWanInterface_x(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "gui", 
            "ProbeName": "checkWanInterface_x", 
            "Probe#": "98, 102, 103", 
            "Description": "Coleta informações de WAN Interface por interface na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password,
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkWanInterface_x_427(flask_username, interface='1')

    #428
    def validarDHCPv6Wan(self, ip, username, password, model_name, flask_username, **kwargs):

        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "gui", 
            "ProbeName": "checkWanInterface_x", 
            "Probe#": "98, 102, 103", 
            "Description": "Coleta informações de WAN Interface por interface na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password,
                                     dict_result=dict_result)
        return hgu.validarDHCPv6Wan_428(flask_username)


    #490
    def checkVoIPSettings(self, ip, username, password, model_name, flask_username, **kwargs):

        driver = WebDriver.get_driver()

    
        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK",
            "ControllerName": "gui",
            "ProbeName": "checkVoIPSettings", 
            "Probe#": "98, 102, 103, 127, 129", 
            "Description": "Coleta informações de VoIP na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkVoIPSettings_490(flask_username)

    
    #491
    def verificarDtmfMethod(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK",
            "ControllerName": "gui",
            "ProbeName": "checkVoIPSettings", 
            "Probe#": "98, 102, 103, 127, 129", 
            "Description": "Coleta informações de VoIP na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarDtmfMethod_491(flask_username)


    #493
    def prioridadeCodec_0(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK",
            "ControllerName": "gui",
            "ProbeName": "checkVoIPSettings", 
            "Probe#": "98, 102, 103, 127, 129", 
            "Description": "Coleta informações de VoIP na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.prioridadeCodec_0_493(flask_username)


    #494
    def prioridadeCodec_1(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK",
            "ControllerName": "gui",
            "ProbeName": "checkVoIPSettings", 
            "Probe#": "98, 102, 103, 127, 129", 
            "Description": "Coleta informações de VoIP na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.prioridadeCodec_1_494(flask_username)

    #490
    # def checkVoIPSettings(self, ip, username, password):
        
    #     driver = WebDriver.get_driver()
    #     usuario = username
    #     senha = password
    #     print()
    #     print()
    #     print('-=-' * 20)
    #     print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
    #     print('-=-' * 20)
    #     print('\n\n -- PARAMETROS DE ENTRADA --')
    #     print('ip = ' + ip)
    #     print('username = ' + username)
    #     print('password = ' + password)
    #     print('-=-' * 20)
    #     try:
    #         print('\n\n == Abrindo URL == ')
    #         driver.get('http://' + ip + '/padrao')
    #         user_input = driver.find_element_by_id('txtUser')
    #         user_input.send_keys(usuario)
    #         pass_input = driver.find_element_by_id('txtPass')
    #         pass_input.send_keys(senha)
    #         login_button = driver.find_element_by_id('btnLogin')
    #         login_button.click()
    #         time.sleep(3)
    #         driver.switch_to.frame('menuFrm')
    #         voiceBasic = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[1]').click()
    #         voiceBasic = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[1]').text
    #         print(voiceBasic)
    #         time.sleep(1)
    #         driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
    #         driver.switch_to.frame('mainFrm')
    #         voiceBasic_SipService = driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
    #         print(voiceBasic_SipService)
    #         voiceBasic_SipService_ActOutProxy = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[1]/label[1]').text
    #         print(voiceBasic_SipService_ActOutProxy)
    #         voiceBasic_SipService_ActOutProxy_valor = driver.find_element_by_xpath('//*[@id="opr_outbound_proxy"]').get_attribute('value')
    #         print(voiceBasic_SipService_ActOutProxy_valor)
    #         voiceBasic_SipService_AdmState = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[2]/label').text
    #         print(voiceBasic_SipService_AdmState)
    #         voiceBasic_SipService_AdmState_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[2]/input[2]').get_attribute('checked')
    #         if voiceBasic_SipService_AdmState_valor == 'true':
    #             voiceBasic_SipService_AdmState_valor = 'Habilitado'
    #         else:
    #             voiceBasic_SipService_AdmState_valor = 'Desabilitado'
    #         print(voiceBasic_SipService_AdmState_valor)
    #         voiceBasic_SipService_BoundInterface = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/div[1]/label[1]').text
    #         print(voiceBasic_SipService_BoundInterface)
    #         voiceBasic_SipService_BoundInterface_valor = driver.find_element_by_xpath('//*[@id="opr_outbound_proxy"]').get_attribute('value')
    #         print(voiceBasic_SipService_BoundInterface_valor)

    #         voiceBasic_SipService_SipNet = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/legend').text
    #         print(voiceBasic_SipService_SipNet)
    #         voiceBasic_SipService_SipNet_UsrAgtDomain = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/label[1]').text
    #         print(voiceBasic_SipService_SipNet_UsrAgtDomain)
    #         voiceBasic_SipService_SipNet_UsrAgtDomain_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/input[1]').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_UsrAgtDomain_valor)
    #         voiceBasic_SipService_SipNet_UsrAgtDomain_port = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/label[2]').text
    #         print(voiceBasic_SipService_SipNet_UsrAgtDomain_port)
    #         voiceBasic_SipService_SipNet_UsrAgtDomain_port_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/input[2]').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_UsrAgtDomain_port_valor)
    #         voiceBasic_SipService_SipNet_UsrAgtDomain_Transp = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/label[3]').text
    #         print(voiceBasic_SipService_SipNet_UsrAgtDomain_Transp)
    #         voiceBasic_SipService_SipNet_UsrAgtDomain_Transp_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[1]/select').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_UsrAgtDomain_Transp_valor)

    #         voiceBasic_SipService_SipNet_OutProxy = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/label[1]').text
    #         print(voiceBasic_SipService_SipNet_OutProxy)
    #         voiceBasic_SipService_SipNet_OutProxy_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/input[1]').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_OutProxy_valor)
    #         voiceBasic_SipService_SipNet_OutProxy_port = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/label[2]').text
    #         print(voiceBasic_SipService_SipNet_OutProxy_port)
    #         voiceBasic_SipService_SipNet_OutProxy_port_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[2]/input[2]').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_OutProxy_port_valor)

    #         voiceBasic_SipService_SipNet_RegServer = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/label[1]').text
    #         print(voiceBasic_SipService_SipNet_RegServer)
    #         voiceBasic_SipService_SipNet_RegServer_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/input[1]').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_RegServer_valor)
    #         voiceBasic_SipService_SipNet_RegServer_port = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/label[2]').text
    #         print(voiceBasic_SipService_SipNet_RegServer_port)
    #         voiceBasic_SipService_SipNet_RegServer_port_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/input[2]').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_RegServer_port_valor)
    #         voiceBasic_SipService_SipNet_RegServer_Transp = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/label[3]').text
    #         print(voiceBasic_SipService_SipNet_RegServer_Transp)
    #         voiceBasic_SipService_SipNet_RegServer_Transp_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[1]/div[4]/select').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_RegServer_Transp_valor)

    #         voiceBasic_SipService_SipNet_ConfCallURL = driver.find_element_by_xpath('//*[@id="conference"]/label').text
    #         print(voiceBasic_SipService_SipNet_ConfCallURL)
    #         voiceBasic_SipService_SipNet_ConfCallURL_valor = driver.find_element_by_xpath('//*[@id="conference"]/input').get_attribute('value')
    #         print(voiceBasic_SipService_SipNet_ConfCallURL_valor)

    #         voiceBasic_SipService_SipBasicSettings = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/legend').text
    #         print(voiceBasic_SipService_SipBasicSettings)
    #         voiceBasic_SipService_SipBasicSettings_DigiMap = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[1]/label').text
    #         print(voiceBasic_SipService_SipBasicSettings_DigiMap)
    #         voiceBasic_SipService_SipBasicSettings_DigiMap_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[1]/textarea').get_attribute('value')
    #         print(voiceBasic_SipService_SipBasicSettings_DigiMap_valor)
    #         voiceBasic_SipService_SipBasicSettings_DTMFMeth = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[2]/label').text
    #         print(voiceBasic_SipService_SipBasicSettings_DTMFMeth)
    #         voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[2]/select').get_attribute('value')
    #         if voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor == '1':
    #             voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = 'InBand'
    #         elif voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor == '2':
    #             voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = 'RFC2833'
    #         elif voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor == '1':
    #             voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor = 'SIPInfo'
    #         print(voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor)
    #         voiceBasic_SipService_SipBasicSettings_Hook = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[3]/label').text
    #         print(voiceBasic_SipService_SipBasicSettings_Hook)
    #         voiceBasic_SipService_SipBasicSettings_Hook_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[3]/select').get_attribute('value')
    #         print(voiceBasic_SipService_SipBasicSettings_Hook_valor)
    #         voiceBasic_SipService_SipBasicSettings_Fax = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[4]/label').text
    #         print(voiceBasic_SipService_SipBasicSettings_Fax)
    #         voiceBasic_SipService_SipBasicSettings_Fax_valor = driver.find_element_by_xpath('//*[@id="BasicSipServiceForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
    #         if voiceBasic_SipService_SipBasicSettings_Fax_valor == 'true':
    #             voiceBasic_SipService_SipBasicSettings_Fax_valor = 'Habilitado'
    #         else:
    #             voiceBasic_SipService_SipBasicSettings_Fax_valor = 'Desabilitado'
    #         print(voiceBasic_SipService_SipBasicSettings_Fax_valor)

    #         voiceBasic_LineSettings = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
    #         time.sleep(1)
    #         voiceBasic_LineSettings = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
    #         print(voiceBasic_LineSettings)
    #         headcol = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))
    #         header = []
    #         for head in range(2, headcol+1):
    #             teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th[' + str(head) + ']').text
    #             header.append(teste)
    #         print(header)
    #         count_linhas = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
    #         count_cols = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td'))
    #         voiceBasic_LineSettings_table = []
    #         for l in range(1, count_linhas+1):
    #             for c in range(2, count_cols+1):
    #                 teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[' + str(l) + ']/td[' + str(c) + ']').text
    #                 voiceBasic_LineSettings_table.append(teste)
    #         print(voiceBasic_LineSettings_table)
    #         voiceBasic_LineSettings_accessIndex = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td[1]/a').click()
    #         time.sleep(1)
    #         voiceBasic_LineSettings_accessIndex_AdmState = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/div/label').text
    #         print(voiceBasic_LineSettings_accessIndex_AdmState)
    #         voiceBasic_LineSettings_accessIndex_AdmState_valor = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/div/input[1]').get_attribute('checked')
    #         if voiceBasic_LineSettings_accessIndex_AdmState_valor == 'true':
    #             voiceBasic_LineSettings_accessIndex_AdmState_valor = 'Habilitado'
    #         else:
    #             voiceBasic_LineSettings_accessIndex_AdmState_valor = 'Desabilitado'
    #         print(voiceBasic_LineSettings_accessIndex_AdmState_valor)
    #         voiceBasic_LineSettings_accessIndex_SIPClient = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/legend').text
    #         print(voiceBasic_LineSettings_accessIndex_SIPClient)
    #         voiceBasic_LineSettings_accessIndex_SIPClient_URI = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[1]/label').text
    #         print(voiceBasic_LineSettings_accessIndex_SIPClient_URI)
    #         voiceBasic_LineSettings_accessIndex_SIPClient_URI_valor = driver.find_element_by_xpath('//*[@id="register_uri"]').get_attribute('value')
    #         print(voiceBasic_LineSettings_accessIndex_SIPClient_URI_valor)
    #         voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[2]/label').text
    #         print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser)
    #         voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser_valor = driver.find_element_by_xpath('//*[@id="auth_username"]').get_attribute('value')
    #         print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser_valor)
    #         voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[3]/label').text
    #         print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass)
    #         voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass_valor = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[1]/div[3]/input').get_attribute('value')
    #         print(voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass_valor)
    #         voiceBasic_LineSettings_accessIndex_CODEC = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[2]/legend').text
    #         print(voiceBasic_LineSettings_accessIndex_CODEC)
    #         voiceBasic_LineSettings_accessIndex_CODEC_VAD = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[2]/div/label').text
    #         print(voiceBasic_LineSettings_accessIndex_CODEC_VAD)
    #         voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor = driver.find_element_by_xpath('//*[@id="BasicLineSettingForm"]/fieldset/fieldset[2]/div/input[1]').get_attribute('checked')
    #         if voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor == 'true':
    #             voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor = 'Habilitado'
    #         else:
    #             voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor = 'Desabilitado'
    #         print(voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor)
    #         codec_head = driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[1]').text
    #         print(codec_head)
    #         count_linhas = len(driver.find_elements_by_xpath('//*[@id="codec"]/tbody/tr'))
    #         codec_table = []
    #         for linha in range(1, count_linhas + 1):
    #             teste = driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[1]').text
    #             codec_table.append(teste)
    #         print(codec_table)
    #         order_head = driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[2]').text
    #         print(order_head)
    #         order_table = []
    #         for linha in range(1, count_linhas + 1):
    #             teste = driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[2]/select').get_attribute('value')
    #             order_table.append(teste)
    #         print(order_table)
    #         admState_head = driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[3]').text
    #         print(admState_head)
    #         admState_table = []
    #         for linha in range(1, count_linhas + 1):
    #             teste = driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[3]/input').get_attribute('checked')
    #             admState_table.append(teste)
    #         print(admState_table)
    #         ptime_head = driver.find_element_by_xpath('//*[@id="codec"]/thead/tr/th[4]').text
    #         print(ptime_head)
    #         ptime_table = []
    #         for linha in range(1, count_linhas + 1):
    #             teste = driver.find_element_by_xpath('//*[@id="codec"]/tbody/tr[' + str(linha) + ']/td[4]/select').get_attribute('value')
    #             if teste == '2':
    #                 teste = '10'
    #             elif teste == '4':
    #                 teste = '20'
    #             elif teste == '8':
    #                 teste = '30'
    #             elif teste == '6':
    #                 teste = '10,20'
    #             elif teste == '10':
    #                 teste = '10,30'
    #             elif teste == '12':
    #                 teste = '20,30'
    #             elif teste == '14':
    #                 teste = '10,20,30'
    #             ptime_table.append(teste)
    #         print(ptime_table)




    #         driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
    #         driver.switch_to.frame('menuFrm')
    #         voiceAdvc = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[2]').click()
    #         time.sleep(1)
    #         voiceAdvc = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[7]/a[2]').text
    #         print(voiceAdvc)
    #         driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
    #         driver.switch_to.frame('mainFrm')
    #         voiceAdvc_SipServ = driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
    #         print(voiceAdvc_SipServ)

    #         voiceAdvc_SipServ = driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
    #         print(voiceAdvc_SipServ)
    #         voiceAdvc_SipServ_AdmState = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[1]/label').text
    #         print(voiceAdvc_SipServ_AdmState)
    #         voiceAdvc_SipServ_AdmState_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[1]/input[1]').get_attribute('checked')
    #         if voiceAdvc_SipServ_AdmState_valor == 'true':
    #             voiceAdvc_SipServ_AdmState_valor = 'Habilitado'
    #         else:
    #             voiceAdvc_SipServ_AdmState_valor = 'Desabilitado'
    #         print(voiceAdvc_SipServ_AdmState_valor)
    #         voiceAdvc_SipServ_region = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[2]/label').text
    #         print(voiceAdvc_SipServ_region)
    #         voiceAdvc_SipServ_region_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/div[2]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_region_valor)
    #         voiceAdvc_SipServ_SIPAdv = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/legend').text
    #         print(voiceAdvc_SipServ_SIPAdv)
    #         voiceAdvc_SipServ_SIPAdv_RegPeri = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[1]/label').text
    #         print(voiceAdvc_SipServ_SIPAdv_RegPeri)
    #         voiceAdvc_SipServ_SIPAdv_RegPeri_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[1]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_SIPAdv_RegPeri_valor)
    #         voiceAdvc_SipServ_SIPAdv_RegRetry = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[2]/label').text
    #         print(voiceAdvc_SipServ_SIPAdv_RegRetry)
    #         voiceAdvc_SipServ_SIPAdv_RegRetry_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[2]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_SIPAdv_RegRetry_valor)
    #         voiceAdvc_SipServ_SIPAdv_RegExpi = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[3]/label').text
    #         print(voiceAdvc_SipServ_SIPAdv_RegExpi)
    #         voiceAdvc_SipServ_SIPAdv_RegExpi_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[3]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_SIPAdv_RegExpi_valor)
    #         voiceAdvc_SipServ_SIPAdv_SessionExpi = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[4]/label').text
    #         print(voiceAdvc_SipServ_SIPAdv_SessionExpi)
    #         voiceAdvc_SipServ_SIPAdv_SessionExpi_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[4]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_SIPAdv_SessionExpi_valor)
    #         voiceAdvc_SipServ_SIPAdv_MinSession = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[5]/label').text
    #         print(voiceAdvc_SipServ_SIPAdv_MinSession)
    #         voiceAdvc_SipServ_SIPAdv_MinSession_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[5]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_SIPAdv_MinSession_valor)
    #         voiceAdvc_SipServ_SIPAdv_DSCPSIP = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[6]/label').text
    #         print(voiceAdvc_SipServ_SIPAdv_DSCPSIP)
    #         voiceAdvc_SipServ_SIPAdv_DSCPSIP_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[6]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_SIPAdv_DSCPSIP_valor)
    #         voiceAdvc_SipServ_SIPAdv_DSCPRTP = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[7]/label').text
    #         print(voiceAdvc_SipServ_SIPAdv_DSCPRTP)
    #         voiceAdvc_SipServ_SIPAdv_DSCPRTP_valor = driver.find_element_by_xpath('//*[@id="AdvanceSipServiceForm"]/fieldset/div[7]/input').get_attribute('value')
    #         print(voiceAdvc_SipServ_SIPAdv_DSCPRTP_valor)

    #         voiceAdvc_Line = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
    #         time.sleep(1)
    #         voiceAdvc_Line = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
    #         print(voiceAdvc_Line)
    #         headcol = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))
    #         header2 = []
    #         for head in range(2, headcol + 1):
    #             teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th[' + str(head) + ']').text
    #             header2.append(teste)
    #         print(header2)
    #         count_linhas = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
    #         count_cols = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr/td'))
    #         voiceAdvc_Line_table = []
    #         for l in range(1, count_linhas + 1):
    #             for c in range(2, count_cols + 1):
    #                 teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[' + str(l) + ']/td[' + str(c) + ']').text
    #                 voiceAdvc_Line_table.append(teste)
    #         print(voiceAdvc_Line_table)
    #         json_saida = {
    #             voiceBasic:
    #                 {
    #                     voiceBasic_SipService:
    #                         {
    #                             voiceBasic_SipService_ActOutProxy:voiceBasic_SipService_ActOutProxy_valor,
    #                             voiceBasic_SipService_AdmState:voiceBasic_SipService_AdmState_valor,
    #                             voiceBasic_SipService_BoundInterface:voiceBasic_SipService_BoundInterface_valor
    #                         },
    #                     voiceBasic_SipService_SipNet:
    #                         {
    #                             voiceBasic_SipService_SipNet_UsrAgtDomain:voiceBasic_SipService_SipNet_UsrAgtDomain_valor,
    #                             voiceBasic_SipService_SipNet_UsrAgtDomain_port:voiceBasic_SipService_SipNet_UsrAgtDomain_port_valor,
    #                             voiceBasic_SipService_SipNet_UsrAgtDomain_Transp:voiceBasic_SipService_SipNet_UsrAgtDomain_Transp_valor,
    #                             voiceBasic_SipService_SipNet_OutProxy:voiceBasic_SipService_SipNet_OutProxy_valor,
    #                             voiceBasic_SipService_SipNet_OutProxy_port:voiceBasic_SipService_SipNet_OutProxy_port_valor,
    #                             voiceBasic_SipService_SipNet_RegServer:voiceBasic_SipService_SipNet_RegServer_valor,
    #                             voiceBasic_SipService_SipNet_RegServer_port:voiceBasic_SipService_SipNet_RegServer_port_valor,
    #                             voiceBasic_SipService_SipNet_RegServer_Transp:voiceBasic_SipService_SipNet_RegServer_Transp_valor,
    #                             voiceBasic_SipService_SipNet_ConfCallURL:voiceBasic_SipService_SipNet_ConfCallURL_valor
    #                         },
    #                     voiceBasic_SipService_SipBasicSettings:
    #                         {
    #                             voiceBasic_SipService_SipBasicSettings_DigiMap:voiceBasic_SipService_SipBasicSettings_DigiMap_valor,
    #                             voiceBasic_SipService_SipBasicSettings_DTMFMeth:voiceBasic_SipService_SipBasicSettings_DTMFMeth_valor,
    #                             voiceBasic_SipService_SipBasicSettings_Hook:voiceBasic_SipService_SipBasicSettings_Hook_valor,
    #                             voiceBasic_SipService_SipBasicSettings_Fax:voiceBasic_SipService_SipBasicSettings_Fax_valor
    #                         },
    #                     voiceBasic_LineSettings:
    #                         {
    #                             header[0]:voiceBasic_LineSettings_table[0],
    #                             header[1]: voiceBasic_LineSettings_table[1],
    #                             header[2]: voiceBasic_LineSettings_table[2],
    #                             header[3]: voiceBasic_LineSettings_table[3],
    #                             header[4]: voiceBasic_LineSettings_table[4],
    #                             "Access Index #0":
    #                                 {
    #                                     voiceBasic_LineSettings_accessIndex_AdmState:voiceBasic_LineSettings_accessIndex_AdmState_valor,
    #                                     voiceBasic_LineSettings_accessIndex_SIPClient:
    #                                         {
    #                                             voiceBasic_LineSettings_accessIndex_SIPClient_URI:voiceBasic_LineSettings_accessIndex_SIPClient_URI_valor,
    #                                             voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser:voiceBasic_LineSettings_accessIndex_SIPClient_AuthUser_valor,
    #                                             voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass:voiceBasic_LineSettings_accessIndex_SIPClient_AuthPass_valor,
    #                                         },
    #                                     voiceBasic_LineSettings_accessIndex_CODEC:
    #                                         {
    #                                             voiceBasic_LineSettings_accessIndex_CODEC_VAD:voiceBasic_LineSettings_accessIndex_CODEC_VAD_valor,
    #                                             codec_head:
    #                                                 {
    #                                                     codec_table[0]:
    #                                                         {
    #                                                             order_head:order_table[0],
    #                                                             admState_head:admState_table[0],
    #                                                             ptime_head:ptime_table[0]
    #                                                         },
    #                                                     codec_table[1]:
    #                                                         {
    #                                                             order_head: order_table[1],
    #                                                             admState_head: admState_table[1],
    #                                                             ptime_head: ptime_table[1]
    #                                                         },
    #                                                     codec_table[2]:
    #                                                         {
    #                                                             order_head: order_table[2],
    #                                                             admState_head: admState_table[2],
    #                                                             ptime_head: ptime_table[2]
    #                                                         }
    #                                                 }
    #                                         }
    #                                 }
    #                         }
    #                 },
    #             voiceAdvc:
    #                 {
    #                     voiceAdvc_SipServ:
    #                         {
    #                             voiceAdvc_SipServ_AdmState: voiceAdvc_SipServ_AdmState_valor,
    #                             voiceAdvc_SipServ_region: voiceAdvc_SipServ_region_valor,
    #                             voiceAdvc_SipServ_SIPAdv:
    #                                 {
    #                                     voiceAdvc_SipServ_SIPAdv_RegPeri: voiceAdvc_SipServ_SIPAdv_RegPeri_valor,
    #                                     voiceAdvc_SipServ_SIPAdv_RegRetry: voiceAdvc_SipServ_SIPAdv_RegRetry_valor,
    #                                     voiceAdvc_SipServ_SIPAdv_RegExpi: voiceAdvc_SipServ_SIPAdv_RegExpi_valor,
    #                                     voiceAdvc_SipServ_SIPAdv_SessionExpi: voiceAdvc_SipServ_SIPAdv_SessionExpi_valor,
    #                                     voiceAdvc_SipServ_SIPAdv_MinSession: voiceAdvc_SipServ_SIPAdv_MinSession_valor,
    #                                     voiceAdvc_SipServ_SIPAdv_DSCPSIP: voiceAdvc_SipServ_SIPAdv_DSCPSIP_valor,
    #                                     voiceAdvc_SipServ_SIPAdv_DSCPRTP: voiceAdvc_SipServ_SIPAdv_DSCPRTP_valor
    #                                 }
    #                         },
    #                     voiceAdvc_Line:
    #                         {
    #                             header2[0]: voiceAdvc_Line_table[0],
    #                             header2[1]: voiceAdvc_Line_table[1],
    #                             header2[2]: voiceAdvc_Line_table[2],
    #                             header2[3]: voiceAdvc_Line_table[3]
    #                         }
    #                 }
    #         }

    #         print(json_saida)
    #         driver.quit()
    #         return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkVoIPSettings", "Probe#": "98, 102, 103, 127, 129", "Description": "Coleta informações de VoIP na página padrão ", "Resultado": json_saida}

    #     except NoSuchElementException as exception:
    #         print(exception)
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkVoIPSettings", "Probe#": "98, 102, 103, 127, 129", "Description": "Coleta informações de VoIP na página padrão ", "Resultado": str(exception)}
    #     except Exception as e:
    #         print(e)
    #         return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkVoIPSettings", "Probe#": "98, 102, 103, 127, 129", "Description": "Coleta informações de VoIP na página padrão ", "Resultado": str(e)}

    
    #423
    def checkNatSettings(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkNatSettings_423(flask_username)


    #429
    def checkLANSettings(self, ip, username, password, model_name, flask_username, **kwargs):

        driver = WebDriver.get_driver()

        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkLANSettings", 
                       "Probe#": "352", 
                       "Description": "Coleta as informações de LAN da página WebGUI PADRAO ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkLANSettings_429(flask_username)

    #431
    def vivo_1_ADSL_vlanIdPPPoE_1(self, ip, username, password, model_name, flask_username, **kwargs):

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_ADSL_vlanIdPPPoE_431(flask_username)

    #432
    def vivo_1_ADSL_vlanIdPPPoE_2(self, ip, username, password, model_name, flask_username, **kwargs):

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_ADSL_vlanIdPPPoE_432(flask_username)
    
    #433
    def vivo_1_ADSL_vlanIdPPPoE_3(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_ADSL_vlanIdPPPoE_433(flask_username)

   #435
    def vivo_1_usernamePppDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_usernamePppDefault_435(flask_username)

    #436
    def vivo_1_passwordPppDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_passwordPppDefault_436(flask_username)


    #437
    def checkWanInterface_x_2(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "gui", 
            "ProbeName": "checkWanInterface_x", 
            "Probe#": "98, 102, 103", 
            "Description": "Coleta informações de WAN Interface por interface na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password,
                                     dict_result=dict_result)
        return hgu.checkWanInterface_x_437(flask_username)

    #438
    def validarDHCPv6Wan_2(self, ip, username, password, model_name, flask_username, **kwargs):

        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "gui", 
            "ProbeName": "checkWanInterface_x", 
            "Probe#": "98, 102, 103", 
            "Description": "Coleta informações de WAN Interface por interface na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password,
                                     dict_result=dict_result)
        return hgu.validarDHCPv6Wan_438(flask_username)

    #439
    def checkLANSettings_2(self, ip, username, password, model_name, flask_username, **kwargs):

        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkLANSettings", 
                       "Probe#": "352", 
                       "Description": "Coleta as informações de LAN da página WebGUI PADRAO ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.checkLANSettings_439(flask_username)

    #441
    def vivo_2_ADSL_vlanIdPPPoE_1(self, ip, username, password, model_name, flask_username, **kwargs):
        

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_2_ADSL_vlanIdPPPoE_441(flask_username)

    #442
    def vivo_2_ADSL_vlanIdPPPoE_2(self, ip, username, password, model_name, flask_username, **kwargs):
        

        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_2_ADSL_vlanIdPPPoE_442(flask_username)

    #443
    def vivo_2_ADSL_vlanIdPPPoE_3(self, ip, username, password, model_name, flask_username, **kwargs):
        

        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_2_ADSL_vlanIdPPPoE_443(flask_username)

    #445
    def vivo_2_usernamePppDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_2_usernamePppDefault_445(flask_username)

    #446
    def vivo_2_passwordPppDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_2_passwordPppDefault_446(flask_username)


    #447
    def validarDualStack(self, ip, username, password, model_name, flask_username, **kwargs):
        

        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "gui", 
            "ProbeName": "checkWanInterface_x", 
            "Probe#": "98, 102, 103", 
            "Description": "Coleta informações de WAN Interface por interface na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password,
                                     dict_result=dict_result)
        return hgu.validarDualStack_447(flask_username)

    
    #448
    def validarDHCPv6Wan_3(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {
            "result":"failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "gui", 
            "ProbeName": "checkWanInterface_x", 
            "Probe#": "98, 102, 103", 
            "Description": "Coleta informações de WAN Interface por interface na página padrão ", 
            "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password,
                                     dict_result=dict_result)
        return hgu.validarDHCPv6Wan_448(flask_username)


    #449
    def prefixDelegationInet(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkLANSettings", 
                       "Probe#": "352", 
                       "Description": "Coleta as informações de LAN da página WebGUI PADRAO ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)

        return hgu.prefixDelegationInet_449(flask_username)


    #450
    def vivo_1_vlanIdIptvVivo1(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_vlanIdIptvVivo1_450(flask_username)



    #451
    def vivo_1_prioridadeIptv(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_prioridadeIptv_451(flask_username)
    
    #452
    def vivo_1_validarNatIptv(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_validarNatIptv_452(flask_username)

    #453
    def vivo_1_igmpIptv(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "OK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkMulticastSettings", 
                       "Probe#": "XXXXXXXXX", 
                       "Description": "Coleta informações de Multicast IGMP na página padrão ", 
                       "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_igmpIptv_453(flask_username)


    #454
    def vlanIdVodVivo2(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vlanIdVodVivo2_454(flask_username)
    
    #455
    def vivo2_validarNatIPTV(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104, 100, 111, 118", 
                        "Description": "Coleta informações de WAN Interface na página padrão. Coleta informações de NAT na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo2_validarNatIPTV_455(flask_username)
    
    #456
    def vivo_2_igmpVoD(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "OK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkMulticastSettings", 
                       "Probe#": "XXXXXXXXX", 
                       "Description": "Coleta informações de Multicast IGMP na página padrão ", 
                       "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_2_igmpVoD_456(flask_username)
    
    #457
    def vlanIdMulticastVivo2(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vlanIdMulticastVivo2_457(flask_username)
    

    #458
    def natMulticastVivo2(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkNatSettings", 
                       "Probe#": "100, 111, 118", 
                       "Description": "Coleta informações de NAT na página padrão ", 
                       "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.natMulticastVivo2_458(flask_username)
    
    #459
    def checkIGMPVivo2(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "OK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkMulticastSettings", 
                       "Probe#": "XXXXXXXXX", 
                       "Description": "Coleta informações de Multicast IGMP na página padrão ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.checkIGMPVivo2_459(flask_username)
    
    #460
    def vivo1_vlanIdVoip(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo1_vlanIdVoip_460(flask_username)


    #461 
    def vivo2_prioridadeVoip(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                        address_ip=ip, 
                                        model_name=model_name, 
                                        username=username, 
                                        password=password, 
                                        dict_result=dict_result)
        return hgu.vivo2_prioridadeVoip_461(flask_username)

    
    #462
    def vivo1_validarNatVoip(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkWanInterface", 
                        "Probe#": "97, 99, 104", 
                        "Description": "Coleta informações de WAN Interface na página padrão ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo1_validarNatVoip_462(flask_username)

    #463
    def vivo_1_igmpVoip(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "OK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkMulticastSettings", 
                       "Probe#": "XXXXXXXXX", 
                       "Description": "Coleta informações de Multicast IGMP na página padrão ", 
                       "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.vivo_1_igmpVoip_463(flask_username)


    #469
    def igmpSnoopingLAN(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkLANSettings", 
                       "Probe#": "352", 
                       "Description": "Coleta as informações de LAN da página WebGUI PADRAO ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.igmpSnoopingLAN_469(flask_username)

    
    #470
    def verificarWifi24SsidDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24SsidDefault_470(flask_username)


    #471
    def verificarWifi24Habilitado(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24Habilitado_471(flask_username)


    #472
    def verificarWifi24Padrao(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24Padrao_472(flask_username)

    #473
    def frequencyPlan(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()


        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.frequencyPlan_473(flask_username)    

    #474
    def verificarWifi24AutoChannel(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24AutoChannel_474(flask_username)

    #475
    def verificarWifi24LarguraBanda(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24LarguraBanda_475(flask_username)

    #476
    def verificarWifi24Seguranca(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24Seguranca_476(flask_username)      


    #477
    def verificarWifi24PasswordDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24PasswordDefault_477(flask_username)  

    #478
    def cipherModeDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.cipherModeDefault_478(flask_username)  

    #479
    def verificarWifi24WPS(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi24WPS_479(flask_username) 

### 5GHz ###
    #480
    def verificarWifi5SsidDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5SsidDefault_480(flask_username)


    #481
    def verificarWifi5Habilitado(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5Habilitado_481(flask_username)


    #482
    def verificarWifi5Padrao(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5Padrao_482(flask_username)
    
    #483
    def frequencyPlan5GHz(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()


        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.frequencyPlan5GHz_483(flask_username)   

    #484
    def verificarWifi5AutoChannel(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5AutoChannel_484(flask_username)

    #485
    def verificarWifi5LarguraBanda(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5LarguraBanda_485(flask_username)

    #486
    def verificarWifi5Seguranca(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5Seguranca_486(flask_username)      

    #487
    def verificarWifi5PasswordDefault(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5PasswordDefault_487(flask_username)

   #488
    def cipherModeDefault5GHz(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.cipherModeDefault5GHz_488(flask_username)  

    #489
    def verificarWifi5WPS(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "getFullConfig", 
                        "Probe#": "350", 
                        "Description": "Coleta as informações da página WebGUI", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.verificarWifi5WPS_489(flask_username) 


    #495
    def checkNATALGSettings(self, ip, username, password, model_name, flask_username, **kwargs):
        driver = WebDriver.get_driver()

        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkNATALGSettings", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de LAN ALG da página WebGUI PADRAO", 
                        "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        return hgu.checkNATALGSettings_495(flask_username)  
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            print('\n#############################################'
                  '\n MENU >> LAN SETTINGS >> ALG '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         LAN SETTINGS > IP INTERFACE
            ### ------------------------------------------ ###
            lanSettings = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/p[1]/b').text
            print(lanSettings)
            lanSettings_ALG = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[3]').click()
            lanSettings_ALG = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[3]').text
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            lanSettings_ALG_FTP = driver.find_element_by_xpath('//*[@id="NatAlgForm"]/input[1]').get_attribute('checked')
            if lanSettings_ALG_FTP == 'true':
                lanSettings_ALG_FTP = 'Habilitado'
            else:
                lanSettings_ALG_FTP = 'Desabilitado'
            print(lanSettings_ALG_FTP)
            lanSettings_ALG_H323 = driver.find_element_by_xpath('//*[@id="NatAlgForm"]/input[2]').get_attribute('checked')
            if lanSettings_ALG_H323 == 'true':
                lanSettings_ALG_H323 = 'Habilitado'
            else:
                lanSettings_ALG_H323 = 'Desabilitado'
            print(lanSettings_ALG_H323)
            lanSettings_ALG_PPTP = driver.find_element_by_xpath('//*[@id="NatAlgForm"]/input[3]').get_attribute('checked')
            if lanSettings_ALG_PPTP == 'true':
                lanSettings_ALG_PPTP = 'Habilitado'
            else:
                lanSettings_ALG_PPTP = 'Desabilitado'
            print(lanSettings_ALG_PPTP)
            lanSettings_ALG_SIP = driver.find_element_by_xpath('//*[@id="NatAlgForm"]/input[4]').get_attribute('checked')
            if lanSettings_ALG_SIP == 'true':
                lanSettings_ALG_SIP = 'Habilitado'
            else:
                lanSettings_ALG_SIP = 'Desabilitado'
            print(lanSettings_ALG_SIP)

            json_saida = {
                lanSettings:
                    {
                        lanSettings_ALG:
                            {
                                'FTP':lanSettings_ALG_FTP,
                                'H323': lanSettings_ALG_H323,
                                'PPTP': lanSettings_ALG_PPTP,
                                'SIP': lanSettings_ALG_SIP
                            }
                    }
            }
            print(json_saida)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkNATALGSettings", "Probe#": "XXXXXXXXX", "Description": "Coleta as informações de LAN ALG da página WebGUI PADRAO ", "Resultado": json_saida}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkNATALGSettings", "Probe#": "XXXXXXXXX", "Description": "Coleta as informações de LAN ALG da página WebGUI PADRAO ", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkNATALGSettings", "Probe#": "XXXXXXXXX", "Description": "Coleta as informações de LAN ALG da página WebGUI PADRAO ", "Resultado": str(e)}

    
    
    #424
    def checkMulticastSettings(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()

        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkMulticastSettings", 
                       "Probe#": "XXXXXXXXX", 
                       "Description": "Coleta informações de Multicast IGMP na página padrão ", 
                       "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkMulticastSettings_424(flask_username)
    
    #464
    def checkLANDHCPSettings_x(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()


        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkLANDHCPSettings_x_464(flask_username)

    #465
    def poolDhcpLan(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.poolDhcpLan_465(flask_username)
        
    #466
    def leaseTime(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.leaseTime_466(flask_username)  

    
    #467
    def vendorIdIptvEnable(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()


        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.vendorIdIptvEnable_467(flask_username)
  
    #468
    def poolDhcpIptv(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.poolDhcpIptv_468(flask_username)  

    #495
    def checkNATALGSettings(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()


        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkNATALGSettings_495(flask_username) 

   #497
    def checkUPnP(self, ip, username, password, model_name, flask_username, **kwargs):
        
        driver = WebDriver.get_driver()


        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)
        return hgu.checkUPnP_497(flask_username) 


   #498
    def linkLocalType(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.linkLocalType_498(flask_username)  


   #499
    def lanGlobalType(self, ip, username, password, model_name, flask_username, **kwargs):
        
        dict_result = {"result": "failed" ,
                        "Resultado_Probe": "NOK", 
                        "ControllerName": "gui", 
                        "ProbeName": "checkLANDHCPSettings_x", 
                        "Probe#": "XXXXXXXXXX", 
                        "Description": "Coleta as informações de DHCP da LAN da página WebGUI PADRAO ", 
                        "obs": None}


        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.lanGlobalType_499(flask_username)  


    #500
    def prefixDelegationfromInet(self, ip, username, password, model_name, flask_username, **kwargs):
        dict_result = {"result":"failed",
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "checkLANSettings", 
                       "Probe#": "352", 
                       "Description": "Coleta as informações de LAN da página WebGUI PADRAO ", 
                       "obs": None}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.prefixDelegationfromInet_500(flask_username)



    def checkWifiSettingsPadrao(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            print('\n#############################################'
                  '\n MENU >> WIFI 2.4GHz SETTINGS  '
                  '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         WIFI 2.4GHz
            ### ------------------------------------------ ###
            wifi = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/p[4]').text
            print(wifi)
            wifi24 = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[1]').click()
            time.sleep(1)
            wifi24 = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[1]').text
            print(wifi24)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            wifi24_PhysSett = driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
            print(wifi24_PhysSett)
            wifi24_PhysSett_OprState = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[1]/label[1]').text
            print(wifi24_PhysSett_OprState)
            wifi24_PhysSett_OprState_valor = driver.find_element_by_xpath('//*[@id="tef_opr_status"]').text
            print(wifi24_PhysSett_OprState_valor)
            wifi24_PhysSett_Channel = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[2]/label[1]').text
            print(wifi24_PhysSett_Channel)
            wifi24_PhysSett_Channel_valor = driver.find_element_by_xpath('//*[@id="opr_channel"]').text
            print(wifi24_PhysSett_Channel_valor)
            wifi24_PhysSett_AdmState = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[3]/label').text
            print(wifi24_PhysSett_AdmState)
            wifi24_PhysSett_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[3]/input[1]').get_attribute('checked')
            if wifi24_PhysSett_AdmState_valor == 'true':
                wifi24_PhysSett_AdmState_valor = 'Habilitado'
            else:
                wifi24_PhysSett_AdmState_valor = 'Desabilitado'
            print(wifi24_PhysSett_AdmState_valor)

            wifi24_PhysSett_Advc = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/legend').text
            print(wifi24_PhysSett_Advc)
            wifi24_PhysSett_Advc_Country = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[1]/label').text
            print(wifi24_PhysSett_Advc_Country)
            wifi24_PhysSett_Advc_Country_valor = driver.find_element_by_xpath('//*[@id="country_code"]').get_property('value')
            print(wifi24_PhysSett_Advc_Country_valor)
            wifi24_PhysSett_Advc_Stand = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[2]/label').text
            print(wifi24_PhysSett_Advc_Stand)
            wifi24_PhysSett_Advc_Stand_valor = driver.find_element_by_xpath('//*[@id="standard"]').get_property('value')
            if wifi24_PhysSett_Advc_Stand_valor == '2':
                wifi24_PhysSett_Advc_Stand_valor = 'b'
            elif wifi24_PhysSett_Advc_Stand_valor == '4':
                wifi24_PhysSett_Advc_Stand_valor = 'g'
            elif wifi24_PhysSett_Advc_Stand_valor == '8':
                wifi24_PhysSett_Advc_Stand_valor = 'n'
            elif wifi24_PhysSett_Advc_Stand_valor == '6':
                wifi24_PhysSett_Advc_Stand_valor = 'b/g'
            elif wifi24_PhysSett_Advc_Stand_valor == '12':
                wifi24_PhysSett_Advc_Stand_valor = 'g/n'
            elif wifi24_PhysSett_Advc_Stand_valor == '14':
                wifi24_PhysSett_Advc_Stand_valor = 'b/g/n'
            print(wifi24_PhysSett_Advc_Stand_valor)
            wifi24_PhysSett_Advc_BandWidth = driver.find_element_by_xpath('//*[@id="div_bandwidth"]/label').text
            print(wifi24_PhysSett_Advc_BandWidth)
            wifi24_PhysSett_Advc_BandWidth_valor = driver.find_element_by_xpath('//*[@id="adm_bandwidth"]').get_property('value')
            if wifi24_PhysSett_Advc_BandWidth_valor == '1':
                wifi24_PhysSett_Advc_BandWidth_valor = '20MHz'
            elif wifi24_PhysSett_Advc_BandWidth_valor == '2':
                wifi24_PhysSett_Advc_BandWidth_valor = '20MHz/40Mhz'
            print(wifi24_PhysSett_Advc_BandWidth_valor)
            wifi24_PhysSett_Advc_Channel = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[5]/label').text
            print(wifi24_PhysSett_Advc_Channel)
            wifi24_PhysSett_Advc_Channel_valor = driver.find_element_by_xpath('//*[@id="adm_channel"]').get_property('value')
            if wifi24_PhysSett_Advc_Channel_valor == '0':
                wifi24_PhysSett_Advc_Channel_valor = 'Auto'
            print(wifi24_PhysSett_Advc_Channel_valor)
            list = driver.find_element_by_xpath('//*[@id="adm_channel"]')       #### INTERESSANTE SABER!!!!!!
            wifi24_PhysSett_Advc_ChannelList = [option.text for option in list.find_elements_by_tag_name('option')]
            print(wifi24_PhysSett_Advc_ChannelList)
            wifi24_PhysSett_Advc_Data = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[7]/label').text
            print(wifi24_PhysSett_Advc_Data)
            wifi24_PhysSett_Advc_Data_valor = driver.find_element_by_xpath('//*[@id="Nrate"]').get_property('value')
            if wifi24_PhysSett_Advc_Data_valor == '-1':
                wifi24_PhysSett_Advc_Data_valor = 'Auto'
            print(wifi24_PhysSett_Advc_Data_valor)
            wifi24_PhysSett_Advc_SpatialStream = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[8]/label').text
            print(wifi24_PhysSett_Advc_SpatialStream)
            wifi24_PhysSett_Advc_SpatialStream_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[8]/select').get_property('value')
            print(wifi24_PhysSett_Advc_SpatialStream_valor)
            wifi24_PhysSett_Advc_Fragm = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[9]/label').text
            print(wifi24_PhysSett_Advc_Fragm)
            wifi24_PhysSett_Advc_Fragm_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[9]/input').get_property('value')
            print(wifi24_PhysSett_Advc_Fragm_valor)
            wifi24_PhysSett_Advc_RTS = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[10]/label').text
            print(wifi24_PhysSett_Advc_RTS)
            wifi24_PhysSett_Advc_RTS_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[10]/input').get_property('value')
            print(wifi24_PhysSett_Advc_RTS_valor)
            wifi24_PhysSett_Advc_Beacon = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[11]/label').text
            print(wifi24_PhysSett_Advc_Beacon)
            wifi24_PhysSett_Advc_Beacon_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[11]/input').get_property('value')
            print(wifi24_PhysSett_Advc_Beacon_valor)
            wifi24_PhysSett_Advc_DTIM = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[12]/label').text
            print(wifi24_PhysSett_Advc_DTIM)
            wifi24_PhysSett_Advc_DTIM_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[12]/input').get_property('value')
            print(wifi24_PhysSett_Advc_DTIM_valor)
            wifi24_PhysSett_Advc_TransmPower = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[13]/label').text
            print(wifi24_PhysSett_Advc_TransmPower)
            wifi24_PhysSett_Advc_TransmPower_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[13]/select').get_property('value')
            print(wifi24_PhysSett_Advc_TransmPower_valor)
            wifi24_PhysSett_Advc_Preambl = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[14]/label').text
            print(wifi24_PhysSett_Advc_Preambl)
            wifi24_PhysSett_Advc_Preambl_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[14]/input[1]').get_attribute('checked')
            if wifi24_PhysSett_Advc_Preambl_valor == 'true':
                wifi24_PhysSett_Advc_Preambl_valor = 'Curto'
            else:
                wifi24_PhysSett_Advc_Preambl_valor = 'Longo'
            print(wifi24_PhysSett_Advc_Preambl_valor)
            wifi24_PhysSett_Advc_Guard = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[15]/label').text
            print(wifi24_PhysSett_Advc_Guard)
            if driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[15]/input[1]').get_attribute('checked') == 'true':
                wifi24_PhysSett_Advc_Guard_valor = 'Auto'
            elif driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[15]/input[2]').get_attribute('checked') == 'true':
                wifi24_PhysSett_Advc_Guard_valor = '400ns'
            elif driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/fieldset/div[15]/input[3]').get_attribute('checked') == 'true':
                 wifi24_PhysSett_Advc_Guard_valor = '800ns'
            print(wifi24_PhysSett_Advc_Guard_valor)


            wifi24_AP = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi24_AP = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
            time.sleep(2)
            countwifi24_AP_tableHead = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))
            wifi24_AP_tableHead = []
            for col in range(1, countwifi24_AP_tableHead+1):
                teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th[' + str(col) + ']').text
                wifi24_AP_tableHead.append(teste)
            print(wifi24_AP_tableHead)
            countlinhas = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
            countcols = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[1]/td'))

            wifi24_AP_table = []
            for linha in range(1, countlinhas + 1):
                for col in range(1, countcols+1):
                    teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[' + str(linha) + ']/td[' + str(col) + ']').text
                    wifi24_AP_table.append(teste)
            print(wifi24_AP_table)

            ### ------------------------------------------ ###
            ###         WIFI 2.4GHz >> INDEX 0
            ### ------------------------------------------ ###

            wifi24_AP_0 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[1]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi24_AP_0_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi24_AP_0_OprState)
            wifi24_AP_0_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').get_property('value')
            print(wifi24_AP_0_OprState_valor)
            wifi24_AP_0_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi24_AP_0_AdmState)
            wifi24_AP_0_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_0_AdmState_valor == 'true':
                wifi24_AP_0_AdmState_valor = 'Habilitado'
            else:
                wifi24_AP_0_AdmState_valor = 'Desabilitado'
            print(wifi24_AP_0_AdmState_valor)
            wifi24_AP_0_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi24_AP_0_SSID)
            wifi24_AP_0_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi24_AP_0_SSID_valor)
            wifi24_AP_0_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi24_AP_0_SSID_hide == 'true':
                wifi24_AP_0_SSID_hide = 'Rede Oculta'
            else:
                wifi24_AP_0_SSID_hide = 'Exibindo Rede'
            print(wifi24_AP_0_SSID_hide)
            wifi24_AP_0_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi24_AP_0_BSSID)
            wifi24_AP_0_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi24_AP_0_BSSID_valor)
            wifi24_AP_0_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi24_AP_0_Sec)
            wifi24_AP_0_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi24_AP_0_Sec_Auth)
            wifi24_AP_0_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi24_AP_0_Sec_Auth_valor == '0':
                wifi24_AP_0_Sec_Auth_valor = 'Aberta'
            elif wifi24_AP_0_Sec_Auth_valor == '3':
                wifi24_AP_0_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi24_AP_0_Sec_Auth_valor == '4':
                wifi24_AP_0_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi24_AP_0_Sec_Auth_valor)
            wifi24_AP_0_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi24_AP_0_Sec_Encr)
            wifi24_AP_0_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi24_AP_0_Sec_Encr_valor == '0':
                wifi24_AP_0_Sec_Encr_valor = 'AES'
            print(wifi24_AP_0_Sec_Encr_valor)
            wifi24_AP_0_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi24_AP_0_Sec_Passw)
            wifi24_AP_0_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi24_AP_0_Sec_Passw_valor)
            wifi24_AP_0_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi24_AP_0_Sec_Rekey)
            wifi24_AP_0_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi24_AP_0_Sec_Rekey_valor)
            wifi24_AP_0_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi24_AP_0_Advanced)
            wifi24_AP_0_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi24_AP_0_Advanced_MaxCli)
            wifi24_AP_0_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi24_AP_0_Advanced_MaxCli_valor)
            wifi24_AP_0_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi24_AP_0_Advanced_WMM)
            wifi24_AP_0_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_0_Advanced_WMM_valor == 'true':
                wifi24_AP_0_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi24_AP_0_Advanced_WMM_valor = 'Desabilitado'
            print(wifi24_AP_0_Advanced_WMM_valor)
            wifi24_AP_0_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi24_AP_0_Advanced_WMMPower)
            wifi24_AP_0_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi24_AP_0_Advanced_WMMPower_valor == 'true':
                wifi24_AP_0_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi24_AP_0_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi24_AP_0_Advanced_WMMPower_valor)
            wifi24_AP_0_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi24_AP_0_Advanced_ClientIso)
            wifi24_AP_0_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi24_AP_0_Advanced_ClientIso_valor == 'true':
                wifi24_AP_0_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi24_AP_0_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi24_AP_0_Advanced_ClientIso_valor)
            wifi24_AP_0_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi24_AP_0_Advanced_GuestNet)
            wifi24_AP_0_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi24_AP_0_Advanced_GuestNet_valor == 'true':
                wifi24_AP_0_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi24_AP_0_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi24_AP_0_Advanced_GuestNet_valor)

            ### ------------------------------------------ ###
            ###         WIFI 2.4GHz >> INDEX 1
            ### ------------------------------------------ ###

            driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi24_AP_1 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[2]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi24_AP_1_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi24_AP_1_OprState)
            wifi24_AP_1_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').get_property('value')
            print(wifi24_AP_1_OprState_valor)
            wifi24_AP_1_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi24_AP_1_AdmState)
            wifi24_AP_1_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_1_AdmState_valor == 'true':
                wifi24_AP_1_AdmState_valor = 'Habilitado'
            else:
                wifi24_AP_1_AdmState_valor = 'Desabilitado'
            print(wifi24_AP_1_AdmState_valor)
            wifi24_AP_1_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi24_AP_1_SSID)
            wifi24_AP_1_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi24_AP_1_SSID_valor)
            wifi24_AP_1_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi24_AP_1_SSID_hide == 'true':
                wifi24_AP_1_SSID_hide = 'Rede Oculta'
            else:
                wifi24_AP_1_SSID_hide = 'Exibindo Rede'
            print(wifi24_AP_1_SSID_hide)
            wifi24_AP_1_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi24_AP_1_BSSID)
            wifi24_AP_1_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi24_AP_1_BSSID_valor)
            wifi24_AP_1_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi24_AP_1_Sec)
            wifi24_AP_1_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi24_AP_1_Sec_Auth)
            wifi24_AP_1_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi24_AP_1_Sec_Auth_valor == '0':
                wifi24_AP_1_Sec_Auth_valor = 'Aberta'
            elif wifi24_AP_1_Sec_Auth_valor == '3':
                wifi24_AP_1_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi24_AP_1_Sec_Auth_valor == '4':
                wifi24_AP_1_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi24_AP_1_Sec_Auth_valor)
            wifi24_AP_1_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi24_AP_1_Sec_Encr)
            wifi24_AP_1_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi24_AP_1_Sec_Encr_valor == '0':
                wifi24_AP_1_Sec_Encr_valor = 'AES'
            print(wifi24_AP_1_Sec_Encr_valor)
            wifi24_AP_1_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi24_AP_1_Sec_Passw)
            wifi24_AP_1_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi24_AP_1_Sec_Passw_valor)
            wifi24_AP_1_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi24_AP_1_Sec_Rekey)
            wifi24_AP_1_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi24_AP_1_Sec_Rekey_valor)
            wifi24_AP_1_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi24_AP_1_Advanced)
            wifi24_AP_1_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi24_AP_1_Advanced_MaxCli)
            wifi24_AP_1_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi24_AP_1_Advanced_MaxCli_valor)
            wifi24_AP_1_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi24_AP_1_Advanced_WMM)
            wifi24_AP_1_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_1_Advanced_WMM_valor == 'true':
                wifi24_AP_1_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi24_AP_1_Advanced_WMM_valor = 'Desabilitado'
            print(wifi24_AP_1_Advanced_WMM_valor)
            wifi24_AP_1_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi24_AP_1_Advanced_WMMPower)
            wifi24_AP_1_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi24_AP_1_Advanced_WMMPower_valor == 'true':
                wifi24_AP_1_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi24_AP_1_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi24_AP_1_Advanced_WMMPower_valor)
            wifi24_AP_1_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi24_AP_1_Advanced_ClientIso)
            wifi24_AP_1_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi24_AP_1_Advanced_ClientIso_valor == 'true':
                wifi24_AP_1_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi24_AP_1_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi24_AP_1_Advanced_ClientIso_valor)
            wifi24_AP_1_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi24_AP_1_Advanced_GuestNet)
            wifi24_AP_1_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi24_AP_1_Advanced_GuestNet_valor == 'true':
                wifi24_AP_1_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi24_AP_1_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi24_AP_1_Advanced_GuestNet_valor)

            ### ------------------------------------------ ###
            ###         WIFI 2.4GHz >> INDEX 2
            ### ------------------------------------------ ###

            driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi24_AP_2 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[3]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi24_AP_2_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi24_AP_2_OprState)
            wifi24_AP_2_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').get_property('value')
            print(wifi24_AP_2_OprState_valor)
            wifi24_AP_2_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi24_AP_2_AdmState)
            wifi24_AP_2_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_2_AdmState_valor == 'true':
                wifi24_AP_2_AdmState_valor = 'Habilitado'
            else:
                wifi24_AP_2_AdmState_valor = 'Desabilitado'
            print(wifi24_AP_2_AdmState_valor)
            wifi24_AP_2_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi24_AP_2_SSID)
            wifi24_AP_2_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi24_AP_2_SSID_valor)
            wifi24_AP_2_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi24_AP_2_SSID_hide == 'true':
                wifi24_AP_2_SSID_hide = 'Rede Oculta'
            else:
                wifi24_AP_2_SSID_hide = 'Exibindo Rede'
            print(wifi24_AP_2_SSID_hide)
            wifi24_AP_2_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi24_AP_2_BSSID)
            wifi24_AP_2_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi24_AP_2_BSSID_valor)
            wifi24_AP_2_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi24_AP_2_Sec)
            wifi24_AP_2_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi24_AP_2_Sec_Auth)
            wifi24_AP_2_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi24_AP_2_Sec_Auth_valor == '0':
                wifi24_AP_2_Sec_Auth_valor = 'Aberta'
            elif wifi24_AP_2_Sec_Auth_valor == '3':
                wifi24_AP_2_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi24_AP_2_Sec_Auth_valor == '4':
                wifi24_AP_2_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi24_AP_2_Sec_Auth_valor)
            wifi24_AP_2_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi24_AP_2_Sec_Encr)
            wifi24_AP_2_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi24_AP_2_Sec_Encr_valor == '0':
                wifi24_AP_2_Sec_Encr_valor = 'AES'
            print(wifi24_AP_2_Sec_Encr_valor)
            wifi24_AP_2_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi24_AP_2_Sec_Passw)
            wifi24_AP_2_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi24_AP_2_Sec_Passw_valor)
            wifi24_AP_2_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi24_AP_2_Sec_Rekey)
            wifi24_AP_2_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi24_AP_2_Sec_Rekey_valor)
            wifi24_AP_2_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi24_AP_2_Advanced)
            wifi24_AP_2_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi24_AP_2_Advanced_MaxCli)
            wifi24_AP_2_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi24_AP_2_Advanced_MaxCli_valor)
            wifi24_AP_2_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi24_AP_2_Advanced_WMM)
            wifi24_AP_2_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_2_Advanced_WMM_valor == 'true':
                wifi24_AP_2_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi24_AP_2_Advanced_WMM_valor = 'Desabilitado'
            print(wifi24_AP_2_Advanced_WMM_valor)
            wifi24_AP_2_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi24_AP_2_Advanced_WMMPower)
            wifi24_AP_2_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi24_AP_2_Advanced_WMMPower_valor == 'true':
                wifi24_AP_2_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi24_AP_2_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi24_AP_2_Advanced_WMMPower_valor)
            wifi24_AP_2_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi24_AP_2_Advanced_ClientIso)
            wifi24_AP_2_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi24_AP_2_Advanced_ClientIso_valor == 'true':
                wifi24_AP_2_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi24_AP_2_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi24_AP_2_Advanced_ClientIso_valor)
            wifi24_AP_2_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi24_AP_2_Advanced_GuestNet)
            wifi24_AP_2_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi24_AP_2_Advanced_GuestNet_valor == 'true':
                wifi24_AP_2_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi24_AP_2_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi24_AP_2_Advanced_GuestNet_valor)


            ### ------------------------------------------ ###
            ###         WIFI 2.4GHz >> INDEX 3
            ### ------------------------------------------ ###

            driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi24_AP_3 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[4]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi24_AP_3_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi24_AP_3_OprState)
            wifi24_AP_3_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').get_property('value')
            print(wifi24_AP_3_OprState_valor)
            wifi24_AP_3_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi24_AP_3_AdmState)
            wifi24_AP_3_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_3_AdmState_valor == 'true':
                wifi24_AP_3_AdmState_valor = 'Habilitado'
            else:
                wifi24_AP_3_AdmState_valor = 'Desabilitado'
            print(wifi24_AP_3_AdmState_valor)
            wifi24_AP_3_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi24_AP_3_SSID)
            wifi24_AP_3_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi24_AP_3_SSID_valor)
            wifi24_AP_3_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi24_AP_3_SSID_hide == 'true':
                wifi24_AP_3_SSID_hide = 'Rede Oculta'
            else:
                wifi24_AP_3_SSID_hide = 'Exibindo Rede'
            print(wifi24_AP_3_SSID_hide)
            wifi24_AP_3_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi24_AP_3_BSSID)
            wifi24_AP_3_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi24_AP_3_BSSID_valor)
            wifi24_AP_3_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi24_AP_3_Sec)
            wifi24_AP_3_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi24_AP_3_Sec_Auth)
            wifi24_AP_3_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi24_AP_3_Sec_Auth_valor == '0':
                wifi24_AP_3_Sec_Auth_valor = 'Aberta'
            elif wifi24_AP_3_Sec_Auth_valor == '3':
                wifi24_AP_3_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi24_AP_3_Sec_Auth_valor == '4':
                wifi24_AP_3_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi24_AP_3_Sec_Auth_valor)
            wifi24_AP_3_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi24_AP_3_Sec_Encr)
            wifi24_AP_3_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi24_AP_3_Sec_Encr_valor == '0':
                wifi24_AP_3_Sec_Encr_valor = 'AES'
            print(wifi24_AP_3_Sec_Encr_valor)
            wifi24_AP_3_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi24_AP_3_Sec_Passw)
            wifi24_AP_3_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi24_AP_3_Sec_Passw_valor)
            wifi24_AP_3_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi24_AP_3_Sec_Rekey)
            wifi24_AP_3_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi24_AP_3_Sec_Rekey_valor)
            wifi24_AP_3_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi24_AP_3_Advanced)
            wifi24_AP_3_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi24_AP_3_Advanced_MaxCli)
            wifi24_AP_3_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi24_AP_3_Advanced_MaxCli_valor)
            wifi24_AP_3_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi24_AP_3_Advanced_WMM)
            wifi24_AP_3_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi24_AP_3_Advanced_WMM_valor == 'true':
                wifi24_AP_3_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi24_AP_3_Advanced_WMM_valor = 'Desabilitado'
            print(wifi24_AP_3_Advanced_WMM_valor)
            wifi24_AP_3_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi24_AP_3_Advanced_WMMPower)
            wifi24_AP_3_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi24_AP_3_Advanced_WMMPower_valor == 'true':
                wifi24_AP_3_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi24_AP_3_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi24_AP_3_Advanced_WMMPower_valor)
            wifi24_AP_3_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi24_AP_3_Advanced_ClientIso)
            wifi24_AP_3_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi24_AP_3_Advanced_ClientIso_valor == 'true':
                wifi24_AP_3_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi24_AP_3_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi24_AP_3_Advanced_ClientIso_valor)
            wifi24_AP_3_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi24_AP_3_Advanced_GuestNet)
            wifi24_AP_3_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi24_AP_3_Advanced_GuestNet_valor == 'true':
                wifi24_AP_3_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi24_AP_3_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi24_AP_3_Advanced_GuestNet_valor)


            wifi24_WPS = driver.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()
            wifi24_WPS = driver.find_element_by_xpath('/html/body/div/ul/li[3]/a').text
            print(wifi24_WPS)
            wifi24_WPS_Status = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[1]/label[1]').text
            print(wifi24_WPS_Status)
            wifi24_WPS_Status_valor = driver.find_element_by_xpath('//*[@id="wps_status_string"]').get_property('value')
            print(wifi24_WPS_Status_valor)
            wifi24_WPS_SelAP = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[2]/label').text
            print(wifi24_WPS_SelAP)
            wifi24_WPS_SelAP_valor = driver.find_element_by_xpath('//*[@id="SelectApSsid"]').get_property('value')
            print(wifi24_WPS_SelAP_valor)
            if wifi24_WPS_SelAP_valor == '0':
                wifi24_WPS_SelAP_valor = wifi24_AP_table[2]
            elif wifi24_WPS_SelAP_valor == '2':
                wifi24_WPS_SelAP_valor = wifi24_AP_table[11]
            elif wifi24_WPS_SelAP_valor == '4':
                wifi24_WPS_SelAP_valor = wifi24_AP_table[20]
            elif wifi24_WPS_SelAP_valor == '6':
                wifi24_WPS_SelAP_valor = wifi24_AP_table[29]
            print(wifi24_WPS_SelAP_valor)
            wifi24_WPS_AdmState = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[3]/label').text
            print(wifi24_WPS_AdmState)
            wifi24_WPS_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[3]/input[1]').get_attribute('checked')
            if wifi24_WPS_AdmState_valor == 'true':
                wifi24_WPS_AdmState_valor = 'Habilitado'
            else:
                wifi24_WPS_AdmState_valor = 'Desabilitado'
            print(wifi24_WPS_AdmState_valor)
            print()
            print()
            print()
            print()




            ### ------------------------------------------ ###
            ###         WIFI 5GHz
            ### ------------------------------------------ ###
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('menuFrm')
            wifi5 = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').click()
            wifi5 = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[4]/a[2]').text
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            time.sleep(1)
            wifi5_PhysSett = driver.find_element_by_xpath('/html/body/div/ul/li[1]/a').text
            print(wifi5_PhysSett)
            wifi5_PhysSett_OprStatus = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[1]/label[1]').text
            print(wifi5_PhysSett_OprStatus)
            wifi5_PhysSett_OprStatus_valor = driver.find_element_by_xpath('//*[@id="tef_opr_status"]').text
            print(wifi5_PhysSett_OprStatus_valor)
            wifi5_PhysSett_Channel = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[2]/label[1]').text
            print(wifi5_PhysSett_Channel)
            wifi5_PhysSett_Channel_valor = driver.find_element_by_xpath('//*[@id="opr_channel"]').text
            print(wifi5_PhysSett_Channel_valor)
            wifi5_PhysSett_CACStatus = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[3]/label[1]').text
            print(wifi5_PhysSett_CACStatus)
            wifi5_PhysSett_CACStatus_valor = driver.find_element_by_xpath('//*[@id="opr_off_cac"]').text
            print(wifi5_PhysSett_CACStatus_valor)
            wifi5_PhysSett_AdmState = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/label').text
            print(wifi5_PhysSett_AdmState)
            wifi5_PhysSett_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[4]/input[1]').get_attribute('checked')
            if wifi5_PhysSett_AdmState_valor == 'true':
                wifi5_PhysSett_AdmState_valor = 'Habilitado'
            else:
                wifi5_PhysSett_AdmState_valor = 'Desabilitado'
            print(wifi5_PhysSett_AdmState_valor)

            wifi5_PhysSett_Advc = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/legend').text
            print(wifi5_PhysSett_Advc)
            wifi5_PhysSett_Advc_Country = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[1]/label').text
            print(wifi5_PhysSett_Advc_Country)
            wifi5_PhysSett_Advc_Country_valor = driver.find_element_by_xpath('//*[@id="country_code"]').get_property('value')
            print(wifi5_PhysSett_Advc_Country_valor)
            wifi5_PhysSett_Advc_Stand = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[2]/label').text
            print(wifi5_PhysSett_Advc_Stand)
            wifi5_PhysSett_Advc_Stand_valor = driver.find_element_by_xpath('//*[@id="standard"]').get_property('value')
            if wifi5_PhysSett_Advc_Stand_valor == '1':
                wifi5_PhysSett_Advc_Stand_valor = 'a'
            elif wifi5_PhysSett_Advc_Stand_valor == '9':
                wifi5_PhysSett_Advc_Stand_valor = 'a/n'
            elif wifi5_PhysSett_Advc_Stand_valor == '25':
                wifi5_PhysSett_Advc_Stand_valor = 'a/n/ac'
            print(wifi5_PhysSett_Advc_Stand_valor)
            wifi5_PhysSett_Advc_BandWidth = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[3]/label').text
            print(wifi5_PhysSett_Advc_BandWidth)
            wifi5_PhysSett_Advc_BandWidth_valor = driver.find_element_by_xpath('//*[@id="adm_bandwidth"]').get_property('value')
            if wifi5_PhysSett_Advc_BandWidth_valor == '1':
                wifi5_PhysSett_Advc_BandWidth_valor = '20MHz'
            elif wifi5_PhysSett_Advc_BandWidth_valor == '2':
                wifi5_PhysSett_Advc_BandWidth_valor = '20MHz/40Mhz'
            elif wifi5_PhysSett_Advc_BandWidth_valor == '3':
                wifi5_PhysSett_Advc_BandWidth_valor = '20MHz/40Mhz/80Mhz'
            print(wifi5_PhysSett_Advc_BandWidth_valor)
            wifi5_PhysSett_Advc_Channel = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[4]/label[1]').text
            print(wifi5_PhysSett_Advc_Channel)
            wifi5_PhysSett_Advc_Channel_valor = driver.find_element_by_xpath('//*[@id="adm_channel"]').get_property('value')
            if wifi5_PhysSett_Advc_Channel_valor == '0':
                wifi5_PhysSett_Advc_Channel_valor = 'Auto'
            print(wifi5_PhysSett_Advc_Channel_valor)
            list = driver.find_element_by_xpath('//*[@id="adm_channel"]')  #### INTERESSANTE SABER!!!!!!
            wifi5_PhysSett_Advc_ChannelList = [option.text for option in list.find_elements_by_tag_name('option')]
            print(wifi5_PhysSett_Advc_ChannelList)
            wifi5_PhysSett_Advc_Data = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[5]/label').text
            print(wifi5_PhysSett_Advc_Data)
            wifi5_PhysSett_Advc_Data_valor = driver.find_element_by_xpath('//*[@id="Arate"]').get_property('value')
            if wifi5_PhysSett_Advc_Data_valor == '-1':
                wifi5_PhysSett_Advc_Data_valor = 'Auto'
            print(wifi5_PhysSett_Advc_Data_valor)
            wifi5_PhysSett_Advc_SpatialStream = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[6]/label').text
            print(wifi5_PhysSett_Advc_SpatialStream)
            wifi5_PhysSett_Advc_SpatialStream_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[6]/select').get_property('value')
            print(wifi5_PhysSett_Advc_SpatialStream_valor)
            wifi5_PhysSett_Advc_Beacon = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[7]/label').text
            print(wifi5_PhysSett_Advc_Beacon)
            wifi5_PhysSett_Advc_Beacon_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[7]/input').get_property('value')
            print(wifi5_PhysSett_Advc_Beacon_valor)
            wifi5_PhysSett_Advc_DTIM = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[8]/label').text
            print(wifi5_PhysSett_Advc_DTIM)
            wifi5_PhysSett_Advc_DTIM_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[8]/input').get_property('value')
            print(wifi5_PhysSett_Advc_DTIM_valor)
            wifi5_PhysSett_Advc_TransmPower = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[9]/label').text
            print(wifi5_PhysSett_Advc_TransmPower)
            wifi5_PhysSett_Advc_TransmPower_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[9]/select').get_property('value')
            print(wifi5_PhysSett_Advc_TransmPower_valor)
            wifi5_PhysSett_Advc_Preambl = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[10]/label').text
            print(wifi5_PhysSett_Advc_Preambl)
            if driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[10]/input[1]').get_attribute('checked') == 'true':
                wifi5_PhysSett_Advc_Preambl_valor = 'Auto'
            elif driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[10]/input[2]').get_attribute('checked') == 'true':
                wifi5_PhysSett_Advc_Preambl_valor = 'Curto'
            elif driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[10]/input[3]').get_attribute('checked') == 'true':
                wifi5_PhysSett_Advc_Preambl_valor = 'Longo'
            print(wifi5_PhysSett_Advc_Preambl_valor)
            wifi5_PhysSett_Advc_Guard = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[11]/label').text
            print(wifi5_PhysSett_Advc_Guard)
            if driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[11]/input[1]').get_attribute('checked') == 'true':
                wifi5_PhysSett_Advc_Guard_valor = 'Auto'
            elif driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[11]/input[2]').get_attribute('checked') == 'true':
                wifi5_PhysSett_Advc_Guard_valor = '400ns'
            elif driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[11]/input[3]').get_attribute('checked') == 'true':
                wifi5_PhysSett_Advc_Guard_valor = '800ns'
            print(wifi5_PhysSett_Advc_Guard_valor)
            wifi5_PhysSett_SmartChannel = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[12]/label').text
            print(wifi5_PhysSett_SmartChannel)
            wifi5_PhysSett_SmartChannel_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[12]/input[1]').get_attribute('checked')
            if wifi5_PhysSett_SmartChannel_valor == 'true':
                wifi5_PhysSett_SmartChannel_valor = 'Habilitado'
            else:
                wifi5_PhysSett_SmartChannel_valor = 'Desabilitado'
            print(wifi5_PhysSett_SmartChannel_valor)
            wifi5_PhysSett_CAC = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[13]/label').text
            print(wifi5_PhysSett_CAC)
            wifi5_PhysSett_CAC_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[13]/input[1]').get_attribute('checked')
            if wifi5_PhysSett_CAC_valor == 'true':
                wifi5_PhysSett_CAC_valor = 'Habilitado'
            else:
                wifi5_PhysSett_CAC_valor = 'Desabilitado'
            print(wifi5_PhysSett_CAC_valor)
            wifi5_PhysSett_QHOP = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[14]/label').text
            print(wifi5_PhysSett_QHOP)
            wifi5_PhysSett_QHOP_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[14]/input[1]').get_attribute('checked')
            if wifi5_PhysSett_QHOP_valor == 'true':
                wifi5_PhysSett_QHOP_valor = 'Habilitado'
            else:
                wifi5_PhysSett_QHOP_valor = 'Desabilitado'
            print(wifi5_PhysSett_QHOP_valor)
            wifi5_PhysSett_BeamForm = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[15]/label').text
            print(wifi5_PhysSett_BeamForm)
            wifi5_PhysSett_BeamForm_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[15]/input[1]').get_attribute('checked')
            if wifi5_PhysSett_BeamForm_valor == 'true':
                wifi5_PhysSett_BeamForm_valor = 'Habilitado'
            else:
                wifi5_PhysSett_BeamForm_valor = 'Desabilitado'
            print(wifi5_PhysSett_BeamForm_valor)
            wifi5_PhysSett_Roaming = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[16]/label').text
            print(wifi5_PhysSett_Roaming)
            wifi5_PhysSett_Roaming_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[16]/input[1]').get_attribute('checked')
            if wifi5_PhysSett_Roaming_valor == 'true':
                wifi5_PhysSett_Roaming_valor = 'Habilitado'
            else:
                wifi5_PhysSett_Roaming_valor = 'Desabilitado'
            print(wifi5_PhysSett_Roaming_valor)
            wifi5_PhysSett_RoamingRole = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[17]/label').text
            print(wifi5_PhysSett_RoamingRole)
            wifi5_PhysSett_RoamingRole_valor = driver.find_element_by_xpath('//*[@id="WiFiPhysicalSettingForm"]/div[5]/fieldset/div[17]/input[1]').get_attribute('checked')
            if wifi5_PhysSett_RoamingRole_valor == 'true':
                wifi5_PhysSett_RoamingRole_valor = 'Master'
            else:
                wifi5_PhysSett_RoamingRole_valor = 'Slave'
            print(wifi5_PhysSett_RoamingRole_valor)

            wifi5_AP = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi5_AP = driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').text
            time.sleep(2)
            countwifi5_AP_tableHead = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th'))
            wifi5_AP_tableHead = []
            for col in range(1, countwifi5_AP_tableHead + 1):
                teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/thead/tr/th[' + str(col) + ']').text
                wifi5_AP_tableHead.append(teste)
            print(wifi5_AP_tableHead)
            countlinhas = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr'))
            countcols = len(driver.find_elements_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[1]/td'))

            wifi5_AP_table = []
            for linha in range(1, countlinhas + 1):
                for col in range(1, countcols + 1):
                    teste = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[' + str(linha) + ']/td[' + str(col) + ']').text
                    wifi5_AP_table.append(teste)
            print(wifi5_AP_table)

            ### ------------------------------------------ ###
            ###         WIFI 5GHz >> INDEX 0
            ### ------------------------------------------ ###

            wifi5_AP_0 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[1]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi5_AP_0_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi5_AP_0_OprState)
            wifi5_AP_0_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').text
            print(wifi5_AP_0_OprState_valor)
            wifi5_AP_0_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi5_AP_0_AdmState)
            wifi5_AP_0_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_0_AdmState_valor == 'true':
                wifi5_AP_0_AdmState_valor = 'Habilitado'
            else:
                wifi5_AP_0_AdmState_valor = 'Desabilitado'
            print(wifi5_AP_0_AdmState_valor)
            wifi5_AP_0_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi5_AP_0_SSID)
            wifi5_AP_0_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi5_AP_0_SSID_valor)
            wifi5_AP_0_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi5_AP_0_SSID_hide == 'true':
                wifi5_AP_0_SSID_hide = 'Rede Oculta'
            else:
                wifi5_AP_0_SSID_hide = 'Exibindo Rede'
            print(wifi5_AP_0_SSID_hide)
            wifi5_AP_0_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi5_AP_0_BSSID)
            wifi5_AP_0_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi5_AP_0_BSSID_valor)
            wifi5_AP_0_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi5_AP_0_Sec)
            wifi5_AP_0_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi5_AP_0_Sec_Auth)
            wifi5_AP_0_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi5_AP_0_Sec_Auth_valor == '0':
                wifi5_AP_0_Sec_Auth_valor = 'Aberta'
            elif wifi5_AP_0_Sec_Auth_valor == '3':
                wifi5_AP_0_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi5_AP_0_Sec_Auth_valor == '4':
                wifi5_AP_0_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi5_AP_0_Sec_Auth_valor)
            wifi5_AP_0_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi5_AP_0_Sec_Encr)
            wifi5_AP_0_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi5_AP_0_Sec_Encr_valor == '0':
                wifi5_AP_0_Sec_Encr_valor = 'AES'
            print(wifi5_AP_0_Sec_Encr_valor)
            wifi5_AP_0_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi5_AP_0_Sec_Passw)
            wifi5_AP_0_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi5_AP_0_Sec_Passw_valor)
            wifi5_AP_0_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi5_AP_0_Sec_Rekey)
            wifi5_AP_0_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi5_AP_0_Sec_Rekey_valor)
            wifi5_AP_0_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi5_AP_0_Advanced)
            wifi5_AP_0_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi5_AP_0_Advanced_MaxCli)
            wifi5_AP_0_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi5_AP_0_Advanced_MaxCli_valor)
            wifi5_AP_0_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi5_AP_0_Advanced_WMM)
            wifi5_AP_0_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_0_Advanced_WMM_valor == 'true':
                wifi5_AP_0_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi5_AP_0_Advanced_WMM_valor = 'Desabilitado'
            print(wifi5_AP_0_Advanced_WMM_valor)
            wifi5_AP_0_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi5_AP_0_Advanced_WMMPower)
            wifi5_AP_0_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi5_AP_0_Advanced_WMMPower_valor == 'true':
                wifi5_AP_0_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi5_AP_0_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi5_AP_0_Advanced_WMMPower_valor)
            wifi5_AP_0_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi5_AP_0_Advanced_ClientIso)
            wifi5_AP_0_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi5_AP_0_Advanced_ClientIso_valor == 'true':
                wifi5_AP_0_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi5_AP_0_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi5_AP_0_Advanced_ClientIso_valor)
            wifi5_AP_0_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi5_AP_0_Advanced_GuestNet)
            wifi5_AP_0_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi5_AP_0_Advanced_GuestNet_valor == 'true':
                wifi5_AP_0_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi5_AP_0_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi5_AP_0_Advanced_GuestNet_valor)

            ### ------------------------------------------ ###
            ###         WIFI 5GHz >> INDEX 1
            ### ------------------------------------------ ###

            driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi5_AP_1 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[2]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi5_AP_1_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi5_AP_1_OprState)
            wifi5_AP_1_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').text
            print(wifi5_AP_1_OprState_valor)
            wifi5_AP_1_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi5_AP_1_AdmState)
            wifi5_AP_1_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_1_AdmState_valor == 'true':
                wifi5_AP_1_AdmState_valor = 'Habilitado'
            else:
                wifi5_AP_1_AdmState_valor = 'Desabilitado'
            print(wifi5_AP_1_AdmState_valor)
            wifi5_AP_1_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi5_AP_1_SSID)
            wifi5_AP_1_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi5_AP_1_SSID_valor)
            wifi5_AP_1_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi5_AP_1_SSID_hide == 'true':
                wifi5_AP_1_SSID_hide = 'Rede Oculta'
            else:
                wifi5_AP_1_SSID_hide = 'Exibindo Rede'
            print(wifi5_AP_1_SSID_hide)
            wifi5_AP_1_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi5_AP_1_BSSID)
            wifi5_AP_1_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi5_AP_1_BSSID_valor)
            wifi5_AP_1_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi5_AP_1_Sec)
            wifi5_AP_1_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi5_AP_1_Sec_Auth)
            wifi5_AP_1_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi5_AP_1_Sec_Auth_valor == '0':
                wifi5_AP_1_Sec_Auth_valor = 'Aberta'
            elif wifi5_AP_1_Sec_Auth_valor == '3':
                wifi5_AP_1_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi5_AP_1_Sec_Auth_valor == '4':
                wifi5_AP_1_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi5_AP_1_Sec_Auth_valor)
            wifi5_AP_1_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi5_AP_1_Sec_Encr)
            wifi5_AP_1_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi5_AP_1_Sec_Encr_valor == '0':
                wifi5_AP_1_Sec_Encr_valor = 'AES'
            print(wifi5_AP_1_Sec_Encr_valor)
            wifi5_AP_1_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi5_AP_1_Sec_Passw)
            wifi5_AP_1_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi5_AP_1_Sec_Passw_valor)
            wifi5_AP_1_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi5_AP_1_Sec_Rekey)
            wifi5_AP_1_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi5_AP_1_Sec_Rekey_valor)
            wifi5_AP_1_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi5_AP_1_Advanced)
            wifi5_AP_1_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi5_AP_1_Advanced_MaxCli)
            wifi5_AP_1_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi5_AP_1_Advanced_MaxCli_valor)
            wifi5_AP_1_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi5_AP_1_Advanced_WMM)
            wifi5_AP_1_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_1_Advanced_WMM_valor == 'true':
                wifi5_AP_1_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi5_AP_1_Advanced_WMM_valor = 'Desabilitado'
            print(wifi5_AP_1_Advanced_WMM_valor)
            wifi5_AP_1_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi5_AP_1_Advanced_WMMPower)
            wifi5_AP_1_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi5_AP_1_Advanced_WMMPower_valor == 'true':
                wifi5_AP_1_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi5_AP_1_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi5_AP_1_Advanced_WMMPower_valor)
            wifi5_AP_1_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi5_AP_1_Advanced_ClientIso)
            wifi5_AP_1_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi5_AP_1_Advanced_ClientIso_valor == 'true':
                wifi5_AP_1_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi5_AP_1_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi5_AP_1_Advanced_ClientIso_valor)
            wifi5_AP_1_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi5_AP_1_Advanced_GuestNet)
            wifi5_AP_1_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi5_AP_1_Advanced_GuestNet_valor == 'true':
                wifi5_AP_1_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi5_AP_1_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi5_AP_1_Advanced_GuestNet_valor)


            ### ------------------------------------------ ###
            ###         WIFI 5GHz >> INDEX 2
            ### ------------------------------------------ ###

            driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi5_AP_2 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[3]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi5_AP_2_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi5_AP_2_OprState)
            wifi5_AP_2_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').text
            print(wifi5_AP_2_OprState_valor)
            wifi5_AP_2_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi5_AP_2_AdmState)
            wifi5_AP_2_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_2_AdmState_valor == 'true':
                wifi5_AP_2_AdmState_valor = 'Habilitado'
            else:
                wifi5_AP_2_AdmState_valor = 'Desabilitado'
            print(wifi5_AP_2_AdmState_valor)
            wifi5_AP_2_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi5_AP_2_SSID)
            wifi5_AP_2_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi5_AP_2_SSID_valor)
            wifi5_AP_2_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi5_AP_2_SSID_hide == 'true':
                wifi5_AP_2_SSID_hide = 'Rede Oculta'
            else:
                wifi5_AP_2_SSID_hide = 'Exibindo Rede'
            print(wifi5_AP_2_SSID_hide)
            wifi5_AP_2_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi5_AP_2_BSSID)
            wifi5_AP_2_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi5_AP_2_BSSID_valor)
            wifi5_AP_2_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi5_AP_2_Sec)
            wifi5_AP_2_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi5_AP_2_Sec_Auth)
            wifi5_AP_2_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi5_AP_2_Sec_Auth_valor == '0':
                wifi5_AP_2_Sec_Auth_valor = 'Aberta'
            elif wifi5_AP_2_Sec_Auth_valor == '3':
                wifi5_AP_2_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi5_AP_2_Sec_Auth_valor == '4':
                wifi5_AP_2_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi5_AP_2_Sec_Auth_valor)
            wifi5_AP_2_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi5_AP_2_Sec_Encr)
            wifi5_AP_2_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi5_AP_2_Sec_Encr_valor == '0':
                wifi5_AP_2_Sec_Encr_valor = 'AES'
            print(wifi5_AP_2_Sec_Encr_valor)
            wifi5_AP_2_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi5_AP_2_Sec_Passw)
            wifi5_AP_2_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi5_AP_2_Sec_Passw_valor)
            wifi5_AP_2_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi5_AP_2_Sec_Rekey)
            wifi5_AP_2_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi5_AP_2_Sec_Rekey_valor)
            wifi5_AP_2_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi5_AP_2_Advanced)
            wifi5_AP_2_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi5_AP_2_Advanced_MaxCli)
            wifi5_AP_2_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi5_AP_2_Advanced_MaxCli_valor)
            wifi5_AP_2_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi5_AP_2_Advanced_WMM)
            wifi5_AP_2_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_2_Advanced_WMM_valor == 'true':
                wifi5_AP_2_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi5_AP_2_Advanced_WMM_valor = 'Desabilitado'
            print(wifi5_AP_2_Advanced_WMM_valor)
            wifi5_AP_2_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi5_AP_2_Advanced_WMMPower)
            wifi5_AP_2_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi5_AP_2_Advanced_WMMPower_valor == 'true':
                wifi5_AP_2_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi5_AP_2_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi5_AP_2_Advanced_WMMPower_valor)
            wifi5_AP_2_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi5_AP_2_Advanced_ClientIso)
            wifi5_AP_2_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi5_AP_2_Advanced_ClientIso_valor == 'true':
                wifi5_AP_2_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi5_AP_2_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi5_AP_2_Advanced_ClientIso_valor)
            wifi5_AP_2_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi5_AP_2_Advanced_GuestNet)
            wifi5_AP_2_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi5_AP_2_Advanced_GuestNet_valor == 'true':
                wifi5_AP_2_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi5_AP_2_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi5_AP_2_Advanced_GuestNet_valor)


            ### ------------------------------------------ ###
            ###         WIFI 5GHz >> INDEX 3
            ### ------------------------------------------ ###

            driver.find_element_by_xpath('/html/body/div/ul/li[2]/a').click()
            wifi5_AP_3 = driver.find_element_by_xpath('//*[@id="Tab2_1"]/table/tbody/tr[4]/td[1]/a').click()  ### INDEX 0 CLICK
            wifi5_AP_3_OprState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[1]/label[1]').text
            print(wifi5_AP_3_OprState)
            wifi5_AP_3_OprState_valor = driver.find_element_by_xpath('//*[@id="opr_status"]').text
            print(wifi5_AP_3_OprState_valor)
            wifi5_AP_3_AdmState = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/label').text
            print(wifi5_AP_3_AdmState)
            wifi5_AP_3_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_3_AdmState_valor == 'true':
                wifi5_AP_3_AdmState_valor = 'Habilitado'
            else:
                wifi5_AP_3_AdmState_valor = 'Desabilitado'
            print(wifi5_AP_3_AdmState_valor)
            wifi5_AP_3_SSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[3]/label').text
            print(wifi5_AP_3_SSID)
            wifi5_AP_3_SSID_valor = driver.find_element_by_xpath('//*[@id="ssid"]').get_property('value')
            print(wifi5_AP_3_SSID_valor)
            wifi5_AP_3_SSID_hide = driver.find_element_by_xpath('//*[@id="ssid_hide"]').get_attribute('checked')
            if wifi5_AP_3_SSID_hide == 'true':
                wifi5_AP_3_SSID_hide = 'Rede Oculta'
            else:
                wifi5_AP_3_SSID_hide = 'Exibindo Rede'
            print(wifi5_AP_3_SSID_hide)
            wifi5_AP_3_BSSID = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/div[5]/label[1]').text
            print(wifi5_AP_3_BSSID)
            wifi5_AP_3_BSSID_valor = driver.find_element_by_xpath('//*[@id="bssid"]').get_property('value')
            print(wifi5_AP_3_BSSID_valor)
            wifi5_AP_3_Sec = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/legend').text
            print(wifi5_AP_3_Sec)
            wifi5_AP_3_Sec_Auth = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[1]/label').text
            print(wifi5_AP_3_Sec_Auth)
            wifi5_AP_3_Sec_Auth_valor = driver.find_element_by_xpath('//*[@id="authentication"]').get_property('value')
            if wifi5_AP_3_Sec_Auth_valor == '0':
                wifi5_AP_3_Sec_Auth_valor = 'Aberta'
            elif wifi5_AP_3_Sec_Auth_valor == '3':
                wifi5_AP_3_Sec_Auth_valor = 'WPA2-PSK'
            elif wifi5_AP_3_Sec_Auth_valor == '4':
                wifi5_AP_3_Sec_Auth_valor = 'WPA-PSK/WPA2-PSK Mixed'
            print(wifi5_AP_3_Sec_Auth_valor)
            wifi5_AP_3_Sec_Encr = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[2]/label').text
            print(wifi5_AP_3_Sec_Encr)
            wifi5_AP_3_Sec_Encr_valor = driver.find_element_by_xpath('//*[@id="encryption"]').get_property('value')
            if wifi5_AP_3_Sec_Encr_valor == '0':
                wifi5_AP_3_Sec_Encr_valor = 'AES'
            print(wifi5_AP_3_Sec_Encr_valor)
            wifi5_AP_3_Sec_Passw = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/label').text
            print(wifi5_AP_3_Sec_Passw)
            wifi5_AP_3_Sec_Passw_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[1]/input').get_property('value')
            print(wifi5_AP_3_Sec_Passw_valor)
            wifi5_AP_3_Sec_Rekey = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/label').text
            print(wifi5_AP_3_Sec_Rekey)
            wifi5_AP_3_Sec_Rekey_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[1]/div/div[4]/div[2]/input').get_property('value')
            print(wifi5_AP_3_Sec_Rekey_valor)
            wifi5_AP_3_Advanced = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/legend').text
            print(wifi5_AP_3_Advanced)
            wifi5_AP_3_Advanced_MaxCli = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/label').text
            print(wifi5_AP_3_Advanced_MaxCli)
            wifi5_AP_3_Advanced_MaxCli_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[1]/input').get_property('value')
            print(wifi5_AP_3_Advanced_MaxCli_valor)
            wifi5_AP_3_Advanced_WMM = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/label').text
            print(wifi5_AP_3_Advanced_WMM)
            wifi5_AP_3_Advanced_WMM_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[2]/input[1]').get_attribute('checked')
            if wifi5_AP_3_Advanced_WMM_valor == 'true':
                wifi5_AP_3_Advanced_WMM_valor = 'Habilitado'
            else:
                wifi5_AP_3_Advanced_WMM_valor = 'Desabilitado'
            print(wifi5_AP_3_Advanced_WMM_valor)
            wifi5_AP_3_Advanced_WMMPower = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/label').text
            print(wifi5_AP_3_Advanced_WMMPower)
            wifi5_AP_3_Advanced_WMMPower_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[3]/input[1]').get_attribute('checked')
            if wifi5_AP_3_Advanced_WMMPower_valor == 'true':
                wifi5_AP_3_Advanced_WMMPower_valor = 'Habilitado'
            else:
                wifi5_AP_3_Advanced_WMMPower_valor = 'Desabilitado'
            print(wifi5_AP_3_Advanced_WMMPower_valor)
            wifi5_AP_3_Advanced_ClientIso = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/label').text
            print(wifi5_AP_3_Advanced_ClientIso)
            wifi5_AP_3_Advanced_ClientIso_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[4]/input[1]').get_attribute('checked')
            if wifi5_AP_3_Advanced_ClientIso_valor == 'true':
                wifi5_AP_3_Advanced_ClientIso_valor = 'Habilitado'
            else:
                wifi5_AP_3_Advanced_ClientIso_valor = 'Desabilitado'
            print(wifi5_AP_3_Advanced_ClientIso_valor)
            wifi5_AP_3_Advanced_GuestNet = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/label').text
            print(wifi5_AP_3_Advanced_GuestNet)
            wifi5_AP_3_Advanced_GuestNet_valor = driver.find_element_by_xpath('//*[@id="WiFiAPSettingForm"]/fieldset[2]/div[5]/input[1]').get_attribute('checked')
            if wifi5_AP_3_Advanced_GuestNet_valor == 'true':
                wifi5_AP_3_Advanced_GuestNet_valor = 'Habilitado'
            else:
                wifi5_AP_3_Advanced_GuestNet_valor = 'Desabilitado'
            print(wifi5_AP_3_Advanced_GuestNet_valor)

            wifi5_WPS = driver.find_element_by_xpath('/html/body/div/ul/li[3]/a').click()
            wifi5_WPS = driver.find_element_by_xpath('/html/body/div/ul/li[3]/a').text
            print(wifi5_WPS)
            wifi5_WPS_Status = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[1]/label[1]').text
            print(wifi5_WPS_Status)
            wifi5_WPS_Status_valor = driver.find_element_by_xpath('//*[@id="wps_status_string"]').text
            print(wifi5_WPS_Status_valor)
            wifi5_WPS_SelAP = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[2]/label').text
            print(wifi5_WPS_SelAP)
            wifi5_WPS_SelAP_valor = driver.find_element_by_xpath('//*[@id="SelectApSsid"]').get_property('value')
            if wifi5_WPS_SelAP_valor == '1':
                wifi5_WPS_SelAP_valor = wifi5_AP_table[2]
            elif wifi5_WPS_SelAP_valor == '3':
                wifi5_WPS_SelAP_valor = wifi5_AP_table[11]
            elif wifi5_WPS_SelAP_valor == '5':
                wifi5_WPS_SelAP_valor = wifi5_AP_table[20]
            elif wifi5_WPS_SelAP_valor == '7':
                wifi5_WPS_SelAP_valor = wifi5_AP_table[29]
            print(wifi5_WPS_SelAP_valor)
            wifi5_WPS_AdmState = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[3]/label').text
            print(wifi5_WPS_AdmState)
            wifi5_WPS_AdmState_valor = driver.find_element_by_xpath('//*[@id="WiFiWPSSettingForm"]/div[3]/input[1]').get_attribute('checked')
            if wifi5_WPS_AdmState_valor == 'true':
                wifi5_WPS_AdmState_valor = 'Habilitado'
            else:
                wifi5_WPS_AdmState_valor = 'Desabilitado'
            print(wifi5_WPS_AdmState_valor)

            json_saida = {
                wifi:
                    {
                        wifi24:
                            {
                                wifi24_PhysSett:
                                    {
                                        wifi24_PhysSett_OprState:wifi24_PhysSett_OprState_valor,
                                        wifi24_PhysSett_Channel:wifi24_PhysSett_Channel_valor,
                                        wifi24_PhysSett_AdmState:wifi24_PhysSett_AdmState_valor,
                                        wifi24_PhysSett_Advc:
                                            {
                                                wifi24_PhysSett_Advc_Country:wifi24_PhysSett_Advc_Country_valor,
                                                wifi24_PhysSett_Advc_Stand:wifi24_PhysSett_Advc_Stand_valor,
                                                wifi24_PhysSett_Advc_BandWidth:wifi24_PhysSett_Advc_BandWidth_valor,
                                                wifi24_PhysSett_Advc_Channel:wifi24_PhysSett_Advc_Channel_valor,
                                                "Canais Disponíveis":wifi24_PhysSett_Advc_ChannelList,
                                                wifi24_PhysSett_Advc_Data:wifi24_PhysSett_Advc_Data_valor,
                                                wifi24_PhysSett_Advc_SpatialStream:wifi24_PhysSett_Advc_SpatialStream_valor,
                                                wifi24_PhysSett_Advc_Fragm:wifi24_PhysSett_Advc_Fragm_valor,
                                                wifi24_PhysSett_Advc_RTS:wifi24_PhysSett_Advc_RTS_valor,
                                                wifi24_PhysSett_Advc_Beacon:wifi24_PhysSett_Advc_Beacon_valor,
                                                wifi24_PhysSett_Advc_DTIM:wifi24_PhysSett_Advc_DTIM_valor,
                                                wifi24_PhysSett_Advc_TransmPower:wifi24_PhysSett_Advc_TransmPower_valor,
                                                wifi24_PhysSett_Advc_Preambl:wifi24_PhysSett_Advc_Preambl_valor,
                                                wifi24_PhysSett_Advc_Guard:wifi24_PhysSett_Advc_Guard_valor
                                            },
                                        wifi24_WPS:
                                            {
                                                wifi24_WPS_Status:wifi24_WPS_Status_valor,
                                                wifi24_WPS_SelAP:wifi24_WPS_SelAP_valor,
                                                wifi24_WPS_AdmState:wifi24_WPS_AdmState_valor
                                            },
                                        wifi24_AP:
                                            {
                                                wifi24_AP_tableHead[0] + ' ' +wifi24_AP_table[0]:
                                                    {
                                                        wifi24_AP_tableHead[2]:wifi24_AP_table[2],
                                                        wifi24_AP_tableHead[3]: wifi24_AP_table[3],
                                                        wifi24_AP_tableHead[4]: wifi24_AP_table[4],
                                                        wifi24_AP_tableHead[5]: wifi24_AP_table[5],
                                                        wifi24_AP_tableHead[6]: wifi24_AP_table[6],
                                                        wifi24_AP_tableHead[7]: wifi24_AP_table[7],
                                                        wifi24_AP_tableHead[8]: wifi24_AP_table[8],
                                                        "Detalhes":
                                                            {
                                                                wifi24_AP_0_OprState:wifi24_AP_0_OprState_valor,
                                                                wifi24_AP_0_AdmState:wifi24_AP_0_AdmState_valor,
                                                                wifi24_AP_0_SSID:wifi24_AP_0_SSID_valor,
                                                                'Visibilidade':wifi24_AP_0_SSID_hide,
                                                                wifi24_AP_0_Sec:
                                                                    {
                                                                        wifi24_AP_0_Sec_Auth: wifi24_AP_0_Sec_Auth_valor,
                                                                        wifi24_AP_0_Sec_Encr: wifi24_AP_0_Sec_Encr_valor,
                                                                        wifi24_AP_0_Sec_Passw: wifi24_AP_0_Sec_Passw_valor,
                                                                        wifi24_AP_0_Sec_Rekey:wifi24_AP_0_Sec_Rekey_valor
                                                                    },
                                                                wifi24_AP_0_Advanced:
                                                                    {
                                                                        wifi24_AP_0_Advanced_MaxCli:wifi24_AP_0_Advanced_MaxCli_valor,
                                                                        wifi24_AP_0_Advanced_WMM:wifi24_AP_0_Advanced_WMM_valor,
                                                                        wifi24_AP_0_Advanced_WMMPower:wifi24_AP_0_Advanced_WMMPower_valor,
                                                                        wifi24_AP_0_Advanced_ClientIso:wifi24_AP_0_Advanced_ClientIso_valor,
                                                                        wifi24_AP_0_Advanced_GuestNet:wifi24_AP_0_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    },
                                                wifi24_AP_tableHead[0] + ' ' + wifi24_AP_table[9]:
                                                    {
                                                        wifi24_AP_tableHead[2]: wifi24_AP_table[11],
                                                        wifi24_AP_tableHead[3]: wifi24_AP_table[12],
                                                        wifi24_AP_tableHead[4]: wifi24_AP_table[13],
                                                        wifi24_AP_tableHead[5]: wifi24_AP_table[14],
                                                        wifi24_AP_tableHead[6]: wifi24_AP_table[15],
                                                        wifi24_AP_tableHead[7]: wifi24_AP_table[16],
                                                        wifi24_AP_tableHead[8]: wifi24_AP_table[17],
                                                        "Detalhes":
                                                            {
                                                                wifi24_AP_1_OprState: wifi24_AP_1_OprState_valor,
                                                                wifi24_AP_1_AdmState: wifi24_AP_1_AdmState_valor,
                                                                wifi24_AP_1_SSID: wifi24_AP_1_SSID_valor,
                                                                'Visibilidade': wifi24_AP_1_SSID_hide,
                                                                wifi24_AP_1_Sec:
                                                                    {
                                                                        wifi24_AP_1_Sec_Auth: wifi24_AP_1_Sec_Auth_valor,
                                                                        wifi24_AP_1_Sec_Encr: wifi24_AP_1_Sec_Encr_valor,
                                                                        wifi24_AP_1_Sec_Passw: wifi24_AP_1_Sec_Passw_valor,
                                                                        wifi24_AP_1_Sec_Rekey: wifi24_AP_1_Sec_Rekey_valor
                                                                    },
                                                                wifi24_AP_1_Advanced:
                                                                    {
                                                                        wifi24_AP_1_Advanced_MaxCli: wifi24_AP_1_Advanced_MaxCli_valor,
                                                                        wifi24_AP_1_Advanced_WMM: wifi24_AP_1_Advanced_WMM_valor,
                                                                        wifi24_AP_1_Advanced_WMMPower: wifi24_AP_1_Advanced_WMMPower_valor,
                                                                        wifi24_AP_1_Advanced_ClientIso: wifi24_AP_1_Advanced_ClientIso_valor,
                                                                        wifi24_AP_1_Advanced_GuestNet: wifi24_AP_1_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    },
                                                wifi24_AP_tableHead[0] + ' '  + wifi24_AP_table[18]:
                                                    {
                                                        wifi24_AP_tableHead[2]: wifi24_AP_table[20],
                                                        wifi24_AP_tableHead[3]: wifi24_AP_table[21],
                                                        wifi24_AP_tableHead[4]: wifi24_AP_table[22],
                                                        wifi24_AP_tableHead[5]: wifi24_AP_table[23],
                                                        wifi24_AP_tableHead[6]: wifi24_AP_table[24],
                                                        wifi24_AP_tableHead[7]: wifi24_AP_table[25],
                                                        wifi24_AP_tableHead[8]: wifi24_AP_table[26],
                                                        "Detalhes":
                                                            {
                                                                wifi24_AP_2_OprState: wifi24_AP_2_OprState_valor,
                                                                wifi24_AP_2_AdmState: wifi24_AP_2_AdmState_valor,
                                                                wifi24_AP_2_SSID: wifi24_AP_2_SSID_valor,
                                                                'Visibilidade': wifi24_AP_2_SSID_hide,
                                                                wifi24_AP_2_Sec:
                                                                    {
                                                                        wifi24_AP_2_Sec_Auth: wifi24_AP_2_Sec_Auth_valor,
                                                                        wifi24_AP_2_Sec_Encr: wifi24_AP_2_Sec_Encr_valor,
                                                                        wifi24_AP_2_Sec_Passw: wifi24_AP_2_Sec_Passw_valor,
                                                                        wifi24_AP_2_Sec_Rekey: wifi24_AP_2_Sec_Rekey_valor
                                                                    },
                                                                wifi24_AP_2_Advanced:
                                                                    {
                                                                        wifi24_AP_2_Advanced_MaxCli: wifi24_AP_2_Advanced_MaxCli_valor,
                                                                        wifi24_AP_2_Advanced_WMM: wifi24_AP_2_Advanced_WMM_valor,
                                                                        wifi24_AP_2_Advanced_WMMPower: wifi24_AP_2_Advanced_WMMPower_valor,
                                                                        wifi24_AP_2_Advanced_ClientIso: wifi24_AP_2_Advanced_ClientIso_valor,
                                                                        wifi24_AP_2_Advanced_GuestNet: wifi24_AP_2_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    },
                                                wifi24_AP_tableHead[0] + ' '  + wifi24_AP_table[27]:
                                                    {
                                                        wifi24_AP_tableHead[2]: wifi24_AP_table[29],
                                                        wifi24_AP_tableHead[3]: wifi24_AP_table[30],
                                                        wifi24_AP_tableHead[4]: wifi24_AP_table[31],
                                                        wifi24_AP_tableHead[5]: wifi24_AP_table[32],
                                                        wifi24_AP_tableHead[6]: wifi24_AP_table[33],
                                                        wifi24_AP_tableHead[7]: wifi24_AP_table[34],
                                                        wifi24_AP_tableHead[8]: wifi24_AP_table[35],
                                                        "Detalhes":
                                                            {
                                                                wifi24_AP_3_OprState: wifi24_AP_3_OprState_valor,
                                                                wifi24_AP_3_AdmState: wifi24_AP_3_AdmState_valor,
                                                                wifi24_AP_3_SSID: wifi24_AP_3_SSID_valor,
                                                                'Visibilidade': wifi24_AP_3_SSID_hide,
                                                                wifi24_AP_3_Sec:
                                                                    {
                                                                        wifi24_AP_3_Sec_Auth: wifi24_AP_3_Sec_Auth_valor,
                                                                        wifi24_AP_3_Sec_Encr: wifi24_AP_3_Sec_Encr_valor,
                                                                        wifi24_AP_3_Sec_Passw: wifi24_AP_3_Sec_Passw_valor,
                                                                        wifi24_AP_3_Sec_Rekey: wifi24_AP_3_Sec_Rekey_valor
                                                                    },
                                                                wifi24_AP_3_Advanced:
                                                                    {
                                                                        wifi24_AP_3_Advanced_MaxCli: wifi24_AP_3_Advanced_MaxCli_valor,
                                                                        wifi24_AP_3_Advanced_WMM: wifi24_AP_3_Advanced_WMM_valor,
                                                                        wifi24_AP_3_Advanced_WMMPower: wifi24_AP_3_Advanced_WMMPower_valor,
                                                                        wifi24_AP_3_Advanced_ClientIso: wifi24_AP_3_Advanced_ClientIso_valor,
                                                                        wifi24_AP_3_Advanced_GuestNet: wifi24_AP_3_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    }
                                            }
                                    }
                            },
                        wifi5:
                            {
                                wifi5_PhysSett:
                                    {
                                        wifi5_PhysSett_OprStatus:wifi5_PhysSett_OprStatus_valor,
                                        wifi5_PhysSett_Channel:wifi5_PhysSett_Channel_valor,
                                        wifi5_PhysSett_AdmState:wifi5_PhysSett_AdmState_valor,
                                        wifi5_PhysSett_Advc:
                                            {
                                                wifi5_PhysSett_Advc_Country:wifi5_PhysSett_Advc_Country_valor,
                                                wifi5_PhysSett_Advc_Stand:wifi5_PhysSett_Advc_Stand_valor,
                                                wifi5_PhysSett_Advc_BandWidth:wifi5_PhysSett_Advc_BandWidth_valor,
                                                wifi5_PhysSett_Advc_Channel:wifi5_PhysSett_Advc_Channel_valor,
                                                "Canais Disponíveis":wifi5_PhysSett_Advc_ChannelList,
                                                wifi5_PhysSett_Advc_Data:wifi5_PhysSett_Advc_Data_valor,
                                                wifi5_PhysSett_Advc_SpatialStream:wifi5_PhysSett_Advc_SpatialStream_valor,
                                                wifi5_PhysSett_Advc_Beacon:wifi5_PhysSett_Advc_Beacon_valor,
                                                wifi5_PhysSett_Advc_DTIM:wifi5_PhysSett_Advc_DTIM_valor,
                                                wifi5_PhysSett_Advc_TransmPower:wifi5_PhysSett_Advc_TransmPower_valor,
                                                wifi5_PhysSett_Advc_Preambl:wifi5_PhysSett_Advc_Preambl_valor,
                                                wifi5_PhysSett_Advc_Guard:wifi5_PhysSett_Advc_Guard_valor,
                                                wifi5_PhysSett_CAC:wifi5_PhysSett_CAC_valor,
                                                wifi5_PhysSett_QHOP:wifi5_PhysSett_QHOP_valor,
                                                wifi5_PhysSett_BeamForm:wifi5_PhysSett_BeamForm_valor,
                                                wifi5_PhysSett_Roaming:wifi5_PhysSett_Roaming_valor,
                                                wifi5_PhysSett_RoamingRole:wifi5_PhysSett_RoamingRole_valor
                                            },
                                        wifi5_WPS:
                                            {
                                                wifi5_WPS_Status:wifi5_WPS_Status_valor,
                                                wifi5_WPS_SelAP:wifi5_WPS_SelAP_valor,
                                                wifi5_WPS_AdmState:wifi5_WPS_AdmState_valor
                                            },
                                        wifi5_AP:
                                            {
                                                wifi5_AP_tableHead[0] + ' ' +wifi5_AP_table[0]:
                                                    {
                                                        wifi5_AP_tableHead[2]:wifi5_AP_table[2],
                                                        wifi5_AP_tableHead[3]: wifi5_AP_table[3],
                                                        wifi5_AP_tableHead[4]: wifi5_AP_table[4],
                                                        wifi5_AP_tableHead[5]: wifi5_AP_table[5],
                                                        wifi5_AP_tableHead[6]: wifi5_AP_table[6],
                                                        wifi5_AP_tableHead[7]: wifi5_AP_table[7],
                                                        wifi5_AP_tableHead[8]: wifi5_AP_table[8],
                                                        "Detalhes":
                                                            {
                                                                wifi5_AP_0_OprState:wifi5_AP_0_OprState_valor,
                                                                wifi5_AP_0_AdmState:wifi5_AP_0_AdmState_valor,
                                                                wifi5_AP_0_SSID:wifi5_AP_0_SSID_valor,
                                                                'Visibilidade':wifi5_AP_0_SSID_hide,
                                                                wifi5_AP_0_Sec:
                                                                    {
                                                                        wifi5_AP_0_Sec_Auth: wifi5_AP_0_Sec_Auth_valor,
                                                                        wifi5_AP_0_Sec_Encr: wifi5_AP_0_Sec_Encr_valor,
                                                                        wifi5_AP_0_Sec_Passw: wifi5_AP_0_Sec_Passw_valor,
                                                                        wifi5_AP_0_Sec_Rekey:wifi5_AP_0_Sec_Rekey_valor
                                                                    },
                                                                wifi5_AP_0_Advanced:
                                                                    {
                                                                        wifi5_AP_0_Advanced_MaxCli:wifi5_AP_0_Advanced_MaxCli_valor,
                                                                        wifi5_AP_0_Advanced_WMM:wifi5_AP_0_Advanced_WMM_valor,
                                                                        wifi5_AP_0_Advanced_WMMPower:wifi5_AP_0_Advanced_WMMPower_valor,
                                                                        wifi5_AP_0_Advanced_ClientIso:wifi5_AP_0_Advanced_ClientIso_valor,
                                                                        wifi5_AP_0_Advanced_GuestNet:wifi5_AP_0_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    },
                                                wifi5_AP_tableHead[0] + ' ' + wifi5_AP_table[9]:
                                                    {
                                                        wifi5_AP_tableHead[2]: wifi5_AP_table[11],
                                                        wifi5_AP_tableHead[3]: wifi5_AP_table[12],
                                                        wifi5_AP_tableHead[4]: wifi5_AP_table[13],
                                                        wifi5_AP_tableHead[5]: wifi5_AP_table[14],
                                                        wifi5_AP_tableHead[6]: wifi5_AP_table[15],
                                                        wifi5_AP_tableHead[7]: wifi5_AP_table[16],
                                                        wifi5_AP_tableHead[8]: wifi5_AP_table[17],
                                                        "Detalhes":
                                                            {
                                                                wifi5_AP_1_OprState: wifi5_AP_1_OprState_valor,
                                                                wifi5_AP_1_AdmState: wifi5_AP_1_AdmState_valor,
                                                                wifi5_AP_1_SSID: wifi5_AP_1_SSID_valor,
                                                                'Visibilidade': wifi5_AP_1_SSID_hide,
                                                                wifi5_AP_1_Sec:
                                                                    {
                                                                        wifi5_AP_1_Sec_Auth: wifi5_AP_1_Sec_Auth_valor,
                                                                        wifi5_AP_1_Sec_Encr: wifi5_AP_1_Sec_Encr_valor,
                                                                        wifi5_AP_1_Sec_Passw: wifi5_AP_1_Sec_Passw_valor,
                                                                        wifi5_AP_1_Sec_Rekey: wifi5_AP_1_Sec_Rekey_valor
                                                                    },
                                                                wifi5_AP_1_Advanced:
                                                                    {
                                                                        wifi5_AP_1_Advanced_MaxCli: wifi5_AP_1_Advanced_MaxCli_valor,
                                                                        wifi5_AP_1_Advanced_WMM: wifi5_AP_1_Advanced_WMM_valor,
                                                                        wifi5_AP_1_Advanced_WMMPower: wifi5_AP_1_Advanced_WMMPower_valor,
                                                                        wifi5_AP_1_Advanced_ClientIso: wifi5_AP_1_Advanced_ClientIso_valor,
                                                                        wifi5_AP_1_Advanced_GuestNet: wifi5_AP_1_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    },
                                                wifi5_AP_tableHead[0] + ' '  + wifi5_AP_table[18]:
                                                    {
                                                        wifi5_AP_tableHead[2]: wifi5_AP_table[20],
                                                        wifi5_AP_tableHead[3]: wifi5_AP_table[21],
                                                        wifi5_AP_tableHead[4]: wifi5_AP_table[22],
                                                        wifi5_AP_tableHead[5]: wifi5_AP_table[23],
                                                        wifi5_AP_tableHead[6]: wifi5_AP_table[24],
                                                        wifi5_AP_tableHead[7]: wifi5_AP_table[25],
                                                        wifi5_AP_tableHead[8]: wifi5_AP_table[26],
                                                        "Detalhes":
                                                            {
                                                                wifi5_AP_2_OprState: wifi5_AP_2_OprState_valor,
                                                                wifi5_AP_2_AdmState: wifi5_AP_2_AdmState_valor,
                                                                wifi5_AP_2_SSID: wifi5_AP_2_SSID_valor,
                                                                'Visibilidade': wifi5_AP_2_SSID_hide,
                                                                wifi5_AP_2_Sec:
                                                                    {
                                                                        wifi5_AP_2_Sec_Auth: wifi5_AP_2_Sec_Auth_valor,
                                                                        wifi5_AP_2_Sec_Encr: wifi5_AP_2_Sec_Encr_valor,
                                                                        wifi5_AP_2_Sec_Passw: wifi5_AP_2_Sec_Passw_valor,
                                                                        wifi5_AP_2_Sec_Rekey: wifi5_AP_2_Sec_Rekey_valor
                                                                    },
                                                                wifi5_AP_2_Advanced:
                                                                    {
                                                                        wifi5_AP_2_Advanced_MaxCli: wifi5_AP_2_Advanced_MaxCli_valor,
                                                                        wifi5_AP_2_Advanced_WMM: wifi5_AP_2_Advanced_WMM_valor,
                                                                        wifi5_AP_2_Advanced_WMMPower: wifi5_AP_2_Advanced_WMMPower_valor,
                                                                        wifi5_AP_2_Advanced_ClientIso: wifi5_AP_2_Advanced_ClientIso_valor,
                                                                        wifi5_AP_2_Advanced_GuestNet: wifi5_AP_2_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    },
                                                wifi5_AP_tableHead[0] + ' '  + wifi5_AP_table[27]:
                                                    {
                                                        wifi5_AP_tableHead[2]: wifi5_AP_table[29],
                                                        wifi5_AP_tableHead[3]: wifi5_AP_table[30],
                                                        wifi5_AP_tableHead[4]: wifi5_AP_table[31],
                                                        wifi5_AP_tableHead[5]: wifi5_AP_table[32],
                                                        wifi5_AP_tableHead[6]: wifi5_AP_table[33],
                                                        wifi5_AP_tableHead[7]: wifi5_AP_table[34],
                                                        wifi5_AP_tableHead[8]: wifi5_AP_table[35],
                                                        "Detalhes":
                                                            {
                                                                wifi5_AP_3_OprState: wifi5_AP_3_OprState_valor,
                                                                wifi5_AP_3_AdmState: wifi5_AP_3_AdmState_valor,
                                                                wifi5_AP_3_SSID: wifi5_AP_3_SSID_valor,
                                                                'Visibilidade': wifi5_AP_3_SSID_hide,
                                                                wifi5_AP_3_Sec:
                                                                    {
                                                                        wifi5_AP_3_Sec_Auth: wifi5_AP_3_Sec_Auth_valor,
                                                                        wifi5_AP_3_Sec_Encr: wifi5_AP_3_Sec_Encr_valor,
                                                                        wifi5_AP_3_Sec_Passw: wifi5_AP_3_Sec_Passw_valor,
                                                                        wifi5_AP_3_Sec_Rekey: wifi5_AP_3_Sec_Rekey_valor
                                                                    },
                                                                wifi5_AP_3_Advanced:
                                                                    {
                                                                        wifi5_AP_3_Advanced_MaxCli: wifi5_AP_3_Advanced_MaxCli_valor,
                                                                        wifi5_AP_3_Advanced_WMM: wifi5_AP_3_Advanced_WMM_valor,
                                                                        wifi5_AP_3_Advanced_WMMPower: wifi5_AP_3_Advanced_WMMPower_valor,
                                                                        wifi5_AP_3_Advanced_ClientIso: wifi5_AP_3_Advanced_ClientIso_valor,
                                                                        wifi5_AP_3_Advanced_GuestNet: wifi5_AP_3_Advanced_GuestNet_valor
                                                                    }
                                                            }
                                                    }
                                            }
                                    }
                            }
                    }
            }
            print(json_saida)

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkWifi24SettingsPadrao", "Probe#": "XXXXXXX", "Description": "Verifica as informações de Wifi 2.4Ghz e 5Ghz via página padrão", "Resultado": json_saida}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkWifi24SettingsPadrao", "Probe#": "XXXXXXXXXX", "Description": "Verifica as informações de Wifi 2.4Ghz e 5Ghz via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkWifi24SettingsPadrao", "Probe#": "XXXXXXXXXX", "Description": "Verifica as informações de Wifi 2.4Ghz e 5Ghz via página padrão", "Resultado": str(e)}


    def checkYoutube(self): ### NECESSARIO CONTA PREMIUM
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)
        try:
            driver.get('https://www.youtube.com/watch?v=K1QICrgxTjA')
            wait = WebDriverWait(driver, 20 * 60)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='movie_player']/div[5]/button")))

            element.click()
            time.sleep(20)
            driver.quit()
            return {"Resultado_Probe": "OK", "ProbeName": "runVideoWifi24", "Probe#": "XXXXXX", "Description": "Validar reprodução de 1h de video Youtube/Netflix ", "Resultado": '200_OK'}
        except NoSuchElementException as exception:
            print(exception)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ProbeName": "runVideoWifi24", "Probe#": "XXXXXX", "Description": "Validar reprodução de 1h de video Youtube/Netflix ", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            driver.quit()
            return {"Resultado_Probe": "OK", "ProbeName": "runVideoWifi24", "Probe#": "XXXXXX", "Description": "Validar reprodução de 1h de video Youtube/Netflix ", "Resultado": str(e)}

    def runSpeedTest(self): ### NECESSARIO CONTA PREMIUM
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)
        try:
            driver.get('https://www.brasilbandalarga.com.br/bbl/')
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnIniciar"]')))
            element.click()
            time.sleep(60)
            Download = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[1]/div[1]/div[2]').text
            print(Download)
            Upload = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[1]/div[2]/div[2]').text
            print(Upload)
            Latencia = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[2]/div[1]/div[2]').text
            print(Latencia)
            Jitter = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[2]/div[2]/div[2]').text
            print(Jitter)
            Perda = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[2]/div[3]/div[2]').text
            print(Perda)
            IP = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[2]/div[2]/div[4]/div[2]').text
            print(IP)
            Rede = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[1]/div[1]').text
            print(Rede)
            Data = driver.find_element_by_xpath('//*[@id="medicao"]/div/div[1]/div[2]').text
            print(Data)

            json_saida={
                "Medições":
                    {
                        "Download":Download,
                        "Upload":Upload,
                        "Latencia":Latencia,
                        "Jitter":Jitter,
                        "Perdas":Perda,
                        "IP":IP,
                        "Rede":Rede,
                        "Data":Data
                    }
            }
            print(json_saida)
            return {"Resultado_Probe": "OK", "ProbeName": "runSpeedTest", "Probe#": "XXXXXX", "Description": "Validar taxa de transferencia", "Resultado": json_saida}
        except NoSuchElementException as exception:
            print(exception)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ProbeName": "runSpeedTest", "Probe#": "XXXXXX", "Description": "Validar reprodução de 1h de video Youtube/Netflix ", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            driver.quit()
            return {"Resultado_Probe": "OK", "ProbeName": "runSpeedTest", "Probe#": "XXXXXX", "Description": "Validar reprodução de 1h de video Youtube/Netflix ", "Resultado": str(e)}

### ------------------------------------------ ###
###         FUNÇÕES DE CONFIGURAÇÃO
### ------------------------------------------ ###

    def shutdownInterfacePPPoE(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wanInterface)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            wanInterface_PPPoE = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
            time.sleep(1)
            wanInterface_PPPoE_AdmState = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/input[2]') ## Botão DISABLE
            if wanInterface_PPPoE_AdmState == 'true':
                shutdown = '200_OK'
            else:
                wanInterface_PPPoE_AdmState = wanInterface_PPPoE_AdmState.click()
                wanInterface_PPPoE_AdmState_off = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()
                shutdown = '200_OK'
            print(shutdown)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "shutdownInterfacePPPoE", "Probe#": "XXXXXXX", "Description": "Desliga a interface PPPoE via Página padrão", "Resultado": shutdown}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "shutdownInterfacePPPoE", "Probe#": "XXXXXXX", "Description": "Coleta informações de WAN Interface por interface na página padrão ", "Resultado": str(exception)}
        except Exception as e:
                print(e)
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "shutdownInterfacePPPoE", "Probe#": "XXXXXXX", "Description": "Coleta informações de WAN Interface por interface na página padrão ", "Resultado": str(e)}

    def execSoftResetGUI(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            gerenciamento = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a')
            print(gerenciamento.text)
            gerenciamento.click()
            time.sleep(1)
            gerenciamento_Reiniciar = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[3]/a').click()
            time.sleep(1)
            driver.find_element_by_xpath("//a[contains(@href,'popup-resets.asp')]").click() ### Span button RESET
            time.sleep(1)
            driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
            gerenciamento_Reiniciar_Exec_Confirm = driver.find_element_by_xpath('//*[@id="btnaAccept"]/span').click()
            shutdown = '200_OK'
            time.sleep(15)

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execSoftReset", "Probe#": "XXXXXXX", "Description": "Executa um SOFT Reset via Web GUI", "Resultado": shutdown}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execSoftReset", "Probe#": "XXXXXXX", "Description": "Executa um SOFT Reset via Web GUI", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execSoftReset", "Probe#": "XXXXXXX", "Description": "Executa um SOFT Reset via Web GUI", "Resultado": str(e)}

    def changeWifi24_Password(self, ip, username, password, senhaWifi):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('senhaWifi = ' + senhaWifi)
        print('-=-' * 20)

        if re.match(r"^.*(?=.{10,})(?=.*\d)(?=.*[a-z]).*$", senhaWifi):
            print('SenhaWifi de Entrada cumpre requisitos...')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
                print('Clicou em Configurações')
                time.sleep(1)
                config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
                print('Clicou em Rede 2.4')
                time.sleep(1)
                config_wifi24_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
                config_wifi24_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(str(senhaWifi))
                time.sleep(1)
                config_wifi24_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click() ### SAVE BUTTON
                time.sleep(1)
                #Alert = driver.switch_to.alert.accept()
                time.sleep(8) ### Tempo para recarregar a página após salvar as configs
                result = '200_OK'
                driver.quit()

                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi24_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 2.4GHz via Web GUI", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                driver.quit()
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi24_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}
            except Exception as e:
                print(e)
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi24_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}
        else:
            print('SenhaWifi de entrada NÃO CUMPRE requisitos.')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
                print('Clicou em Configurações')
                time.sleep(1)
                config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
                print('Clicou em Rede 5')
                time.sleep(1)
                config_wifi5_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
                config_wifi5_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(str(senhaWifi))
                time.sleep(1)
                if driver.find_element_by_xpath('//*[@id="chkLev"]').text != 'Nível de segurança: alta':
                    config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click()  ### SAVE BUTTON
                    time.sleep(1)
                    print('passou aqui ')
                    if driver.switch_to.alert.accept():
                        print('NÃO ESPERADO!')
                        erro = 'Foi possível salvar a senha sem os requisitos mínimos.'
                    else:
                        print('Comportamento esperado!')
                        result = '200_OK'
                driver.quit()

                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi24_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 2.4GHz via Web GUI", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi24_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 2.4GHz via Web GUI", "Resultado": '200_OK ' + str(exception)}
            except Exception as e:
                print(e)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi24_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 2.4GHz via Web GUI", "Resultado": '200_OK ' + str(e)}

    def changeWifi24_SSID(self, ip, username, password, ssid):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('ssid = ' + ssid)
        print('-=-' * 20)


        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            config_wifi24_basico_ssid = driver.find_element_by_xpath('//*[@id="txtSsid"]').clear()
            config_wifi24_basico_ssid = driver.find_element_by_xpath('//*[@id="txtSsid"]').send_keys(str(ssid))
            time.sleep(1)
            config_wifi24_basico_ssid_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click() ### SAVE BUTTON
            time.sleep(1)
            Alert = driver.switch_to.alert.accept()
            time.sleep(8) ### Tempo para recarregar a página após salvar as configs
            result = '200_OK'
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi24_SSID", "Probe#": "XXXXXXX", "Description": "Altera o SSID da rede Wifi 2.4GHz via Web GUI", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi24_SSID", "Probe#": "XXXXXXX", "Description": "Altera o SSID da rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi24_SSID", "Probe#": "XXXXXXX", "Description": "Altera o SSID da rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def changeWifi5_SSID(self, ip, username, password, ssid):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('ssid = ' + ssid)
        print('-=-' * 20)


        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            config_wifi5_basico_ssid = driver.find_element_by_xpath('//*[@id="txtSsid"]').clear()
            config_wifi5_basico_ssid = driver.find_element_by_xpath('//*[@id="txtSsid"]').send_keys(str(ssid))
            time.sleep(1)
            config_wifi5_basico_ssid_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click() ### SAVE BUTTON
            time.sleep(1)
            Alert = driver.switch_to.alert.accept()
            time.sleep(8) ### Tempo para recarregar a página após salvar as configs
            result = '200_OK'
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi5_SSID", "Probe#": "XXXXXXX", "Description": "Altera o SSID da rede Wifi 5GHz via Web GUI", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi5_SSID", "Probe#": "XXXXXXX", "Description": "Altera o SSID da rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi5_SSID", "Probe#": "XXXXXXX", "Description": "Altera o SSID da rede Wifi 5GHz via Web GUI", "Resultado": str(e)}

    def execDisableIPv6(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wanInterface)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            wanInterface_0 = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
            wanInterface_0 = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').text
            wanInterface_0_Disable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[3]').get_attribute('checked')
            if wanInterface_0_Disable == 'true':
                disable = '200_OK'
            else:
                disable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[3]').click()
                disable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()
                disable = '200_OK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableIPv6", "Probe#": "XXXXXXX", "Description": "Desabilita IPv6 na WAN via página padrão", "Resultado": disable}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableIPv6", "Probe#": "XXXXXXX", "Description": "Desabilita IPv6 na WAN via página padrão", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableIPv6", "Probe#": "XXXXXXX", "Description": "Desabilita IPv6 na WAN via página padrão", "Resultado": str(e)}

    def execDisableIPv4(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wanInterface)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            wanInterface_0 = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
            wanInterface_0 = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').text
            wanInterface_0_Disable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[2]').get_attribute('checked')
            if wanInterface_0_Disable == 'true':
                disable = '200_OK'
            else:
                disable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[2]').click()
                disable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()
                disable = '200_OK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableIPv4", "Probe#": "XXXXXXX", "Description": "Desabilita IPv4 na WAN via página padrão", "Resultado": disable}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableIPv4", "Probe#": "XXXXXXX", "Description": "Desabilita IPv4 na WAN via página padrão", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableIPv4", "Probe#": "XXXXXXX", "Description": "Desabilita IPv4 na WAN via página padrão", "Resultado": str(e)}

    def execEnableDualStack(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wanInterface)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            wanInterface_0 = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
            wanInterface_0 = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').text
            wanInterface_0_Enable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[1]').get_attribute('checked')
            if wanInterface_0_Enable == 'true':
                enable = '200_OK'
            else:
                enable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[1]').click()
                enable = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()
                enable = '200_OK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execEnableDualStack", "Probe#": "XXXXXXX", "Description": "Habilita Dual Stack na WAN via página padrão", "Resultado": enable}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableDualStack", "Probe#": "XXXXXXX", "Description": "Habilita Dual Stack na WAN via página padrão", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableDualStack", "Probe#": "XXXXXXX", "Description": "Habilita Dual Stack na WAN via página padrão", "Resultado": str(e)}

    def enablePPPoE(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wanInterface)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            wanInterface_PPPoE = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
            time.sleep(1)
            wanInterface_PPPoE_AdmState = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[1]/input[1]')  ## Botão DISABLE
            if wanInterface_PPPoE_AdmState == 'true':
                enable = '200_OK'
            else:
                wanInterface_PPPoE_AdmState = wanInterface_PPPoE_AdmState.click()
                wanInterface_PPPoE_AdmState_off = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click() ## Botão APPLY
                enable = '200_OK'
            print(enable)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "enablePPPoE", "Probe#": "XXXXXXX", "Description": "Habilita a interface PPPoE via Página padrão", "Resultado": enable}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "enablePPPoE", "Probe#": "XXXXXXX", "Description": "Habilita a interface PPPoE via Página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "enablePPPoE", "Probe#": "XXXXXXX", "Description": "Habilita a interface PPPoE via Página padrão", "Resultado": str(e)}

    def changeWifi5_Password(self, ip, username, password, senhaWifi):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('senhaWifi = ' + senhaWifi)
        print('-=-' * 20)

        if re.match(r"^.*(?=.{10,})(?=.*\d)(?=.*[a-z]).*$", senhaWifi):
            print('SenhaWifi de Entrada cumpre requisitos...')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
                print('Clicou em Configurações')
                time.sleep(1)
                config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
                print('Clicou em Rede 5')
                time.sleep(1)
                config_wifi5_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
                config_wifi5_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(str(senhaWifi))
                time.sleep(1)
                config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click()  ### SAVE BUTTON
                time.sleep(1)
                #Alert = driver.switch_to.alert.accept()
                time.sleep(8)  ### Tempo para recarregar a página após salvar as configs
                result = '200_OK'
                driver.quit()

                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi5_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 5GHz via Web GUI", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                driver.quit()
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi5_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}
            except Exception as e:
                print(e)
                driver.quit()
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi5_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 5GHz via Web GUI", "Resultado": str(e)}
        else:
            print('SenhaWifi de entrada NÃO CUMPRE requisitos.')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
                print('Clicou em Configurações')
                time.sleep(1)
                config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
                print('Clicou em Rede 5')
                time.sleep(1)
                config_wifi5_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
                config_wifi5_basico_ssid_senha_valor = driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(str(senhaWifi))
                time.sleep(1)
                if driver.find_element_by_xpath('//*[@id="chkLev"]').text != 'Nível de segurança: alta':
                    config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click()  ### SAVE BUTTON
                    time.sleep(1)
                    print('passou aqui ')
                    if driver.switch_to.alert.accept():
                        print('NÃO ESPERADO!')
                        erro = 'Foi possível salvar a senha sem os requisitos mínimos.'
                    else:
                        print('Comportamento esperado!')
                        result = '200_OK'
                driver.quit()

                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeWifi5_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 5GHz via Web GUI", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi5_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 5GHz via Web GUI", "Resultado": '200_OK ' + str(exception)}
            except Exception as e:
                print(e)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeWifi5_Password", "Probe#": "XXXXXXX", "Description": "Altera a senha da rede Wifi 5GHz via Web GUI", "Resultado": '200_OK ' + str(e)}

    def execRebootGUI(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            gerenciamento = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[3]/a')
            print(gerenciamento.text)
            gerenciamento.click()
            time.sleep(1)
            gerenciamento_Reiniciar = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[3]/a').click()
            time.sleep(1)
            driver.find_element_by_xpath("//a[contains(@href,'popup-reboot.asp')]").click() ### Span button RESET
            time.sleep(1)
            driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
            gerenciamento_Reiniciar_Exec_Confirm = driver.find_element_by_xpath('//*[@id="btnaAccept"]/span').click()
            shutdown = '200_OK'
            time.sleep(15)

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execRebootGUI", "Probe#": "XXXXXXX", "Description": "Executa um Reboot via Web GUI", "Resultado": shutdown}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execRebootGUI", "Probe#": "XXXXXXX", "Description": "Executa um Reboot via Web GUI", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execSoftRebootGUI", "Probe#": "XXXXXXX", "Description": "Executa um Reboot via Web GUI", "Resultado": str(e)}

    def execDisableWifi24(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            if driver.find_element_by_xpath('//*[@id="radWifiEn0"]').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="radWifiEn0"]').click()
                driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click()
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'

            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableWifi24", "Probe#": "XXXXXXX", "Description": "Desabilita rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi24", "Probe#": "XXXXXXX", "Description": "Desabilita rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi24", "Probe#": "XXXXXXX", "Description": "Desabilita rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def execEnableWifi24(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            if driver.find_element_by_xpath('//*[@id="radWifiEn1"]').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="radWifiEn1"]').click()
                driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click()
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'

            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableWifi24", "Probe#": "XXXXXXX", "Description": "Habilita rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi24", "Probe#": "XXXXXXX", "Description": "Habilita rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi24", "Probe#": "XXXXXXX", "Description": "Habilita rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def execDisableWifi5(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            if driver.find_element_by_xpath('//*[@id="radWifiEn0"]').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="radWifiEn0"]').click()
                driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click()
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'

            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableWifi5", "Probe#": "XXXXXXX", "Description": "Desabilita rede Wifi 5GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi5", "Probe#": "XXXXXXX", "Description": "Desabilita rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi5", "Probe#": "XXXXXXX", "Description": "Desabilita rede Wifi 5GHz via Web GUI", "Resultado": str(e)}

    def execEnableWifi5(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            if driver.find_element_by_xpath('//*[@id="radWifiEn1"]').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="radWifiEn1"]').click()
                driver.find_element_by_xpath('//*[@id="btnBasSave"]/span').click()
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'

            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableWifi5", "Probe#": "XXXXXXX", "Description": "Habilita rede Wifi 5GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi5", "Probe#": "XXXXXXX", "Description": "Habilita rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableWifi5", "Probe#": "XXXXXXX", "Description": "Habilita rede Wifi 5GHz via Web GUI", "Resultado": str(e)}


    def changeAdminPasswordWithoutCurrent(self, ip, username, old_password, new_password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha_antiga = old_password
        senha_nova = new_password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('old_password = ' + old_password)
        print('new_password = ' + new_password)
        print('-=-' * 20)

        if re.match(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$", new_password):
            print('SenhaAdmin de Entrada cumpre requisitos...')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha_antiga)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
                print('Clicou em Gerenciamento')
                time.sleep(1)
                config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/a').click()
                print('Clicou Alterar senha')
                time.sleep(1)
                gerenc_senha_old_valor = driver.find_element_by_xpath('//*[@id="txtOldPass"]').send_keys('')
                time.sleep(1)
                gerenc_senha_new_valor = driver.find_element_by_xpath('//*[@id="txtNewPass"]').send_keys(str(senha_nova))
                time.sleep(1)
                gerenc_senha_new_valor2 = driver.find_element_by_xpath('//*[@id="txtConfirm"]').send_keys(str(senha_nova))
                time.sleep(1)
                config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnSave"]/span').click()  ### SAVE BUTTON
                if driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/div[2]/table/tbody/tr[2]/td[2]/span').text == 'Alteração de senha falhou.':
                    result = '200_OK'
                else:
                    result = '400_NOK'
                time.sleep(8)  ### Tempo para recarregar a página após salvar as configs

                driver.quit()

                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutCurrent", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem inserir senha atual", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutCurrent", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUIUI -- Sem inserir senha atual", "Resultado": str(exception)}

            except Exception as e:
                print(e)
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutCurrent", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem inserir senha atual", "Resultado": str(e)}

        else:
            print('SenhaAdmin de entrada NÃO CUMPRE requisitos.')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha_antiga)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
                print('Clicou em Gerenciamento')
                time.sleep(1)
                config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/a').click()
                print('Clicou Alterar senha')
                time.sleep(1)
                gerenc_senha_old_valor = driver.find_element_by_xpath('//*[@id="txtOldPass"]').send_keys(str(senha_antiga))
                time.sleep(1)
                gerenc_senha_new_valor = driver.find_element_by_xpath('//*[@id="txtNewPass"]').send_keys(str(senha_nova))
                time.sleep(1)
                gerenc_senha_new_valor2 = driver.find_element_by_xpath('//*[@id="txtConfirm"]').send_keys(str(senha_nova))
                time.sleep(1)
                config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnSave"]/span').click()  ### SAVE BUTTON
                time.sleep(1)
                if driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input'):
                    print('NÃO ESPERADO!')
                    erro = 'Foi possível salvar a senha sem os requisitos mínimos.'
                else:
                    print('Comportamento esperado!')
                    result = '200_OK'
                time.sleep(8)  ### Tempo para recarregar a página após salvar as configs
                result = '200_OK'
                driver.quit()

                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutCurrent", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem inserir senha atual", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutCurrent", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem inserir senha atual", "Resultado": '200_OK ' + str(exception)}
            except Exception as e:
                print(e)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutCurrent", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem inserir senha atual", "Resultado": '200_OK ' + str(e)}

    def changeAdminPasswordWithoutReconfirm(self, ip, username, old_password, new_password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha_antiga = old_password
        senha_nova = new_password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('old_password = ' + old_password)
        print('new_password = ' + new_password)
        print('-=-' * 20)

        if re.match(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$", new_password):
            print('SenhaAdmin de Entrada cumpre requisitos...')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha_antiga)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
                print('Clicou em Gerenciamento')
                time.sleep(1)
                config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/a').click()
                print('Clicou Alterar senha')
                time.sleep(1)
                gerenc_senha_old_valor = driver.find_element_by_xpath('//*[@id="txtOldPass"]').send_keys(str(senha_antiga))
                time.sleep(1)
                gerenc_senha_new_valor = driver.find_element_by_xpath('//*[@id="txtNewPass"]').send_keys(str(senha_nova))
                time.sleep(1)
                gerenc_senha_new_valor2 = driver.find_element_by_xpath('//*[@id="txtConfirm"]').send_keys('')
                time.sleep(1)
                config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnSave"]/span').click()  ### SAVE BUTTON
                if driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/div[2]/table/tbody/tr[4]/td[2]/span').text == 'As senhas não combinam.':
                    result = '200_OK'
                else:
                    result = '400_NOK'
                time.sleep(8)  ### Tempo para recarregar a página após salvar as configs

                driver.quit()

                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutReconfirm", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem confirmar senha nova", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutReconfirm", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUIUI -- Sem confirmar senha nova", "Resultado": str(exception)}

            except Exception as e:
                print(e)
                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutReconfirm", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem confirmar senha nova", "Resultado": str(e)}

        else:
            print('SenhaAdmin de entrada NÃO CUMPRE requisitos.')
            try:
                print('\n\n == Abrindo URL == ')
                driver.get('http://' + ip + '/')
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
                link.click()
                time.sleep(1)
                link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
                link.click()
                time.sleep(1)
                print(' == Autenticando == ')
                driver.get('http://' + ip + '/login.asp')
                driver.switch_to.default_content()
                user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
                user_input.send_keys(usuario)
                pass_input = driver.find_element_by_id('txtPass')
                pass_input.send_keys(senha_antiga)
                login_button = driver.find_element_by_id('btnLogin')
                time.sleep(1)
                login_button.click()
                time.sleep(1)
                config = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
                print('Clicou em Gerenciamento')
                time.sleep(1)
                config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/a').click()
                print('Clicou Alterar senha')
                time.sleep(1)
                gerenc_senha_old_valor = driver.find_element_by_xpath('//*[@id="txtOldPass"]').send_keys(str(senha_antiga))
                time.sleep(1)
                gerenc_senha_new_valor = driver.find_element_by_xpath('//*[@id="txtNewPass"]').send_keys(str(senha_nova))
                time.sleep(1)
                gerenc_senha_new_valor2 = driver.find_element_by_xpath('//*[@id="txtConfirm"]').send_keys(str(senha_nova))
                time.sleep(1)
                config_wifi5_basico_ssid_senha_salvar = driver.find_element_by_xpath('//*[@id="btnSave"]/span').click()  ### SAVE BUTTON
                time.sleep(1)
                if driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input'):
                    print('NÃO ESPERADO!')
                    erro = 'Foi possível salvar a senha sem os requisitos mínimos.'
                else:
                    print('Comportamento esperado!')
                    result = '200_OK'
                time.sleep(8)  ### Tempo para recarregar a página após salvar as configs
                result = '200_OK'
                driver.quit()

                return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutReconfirm", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem confirmar senha nova", "Resultado": result}
            except NoSuchElementException as exception:
                print(exception)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutReconfirm", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem confirmar senha nova", "Resultado": '200_OK ' + str(exception)}
            except Exception as e:
                print(e)
                return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAdminPasswordWithoutReconfirm", "Probe#": "XXXXXXX", "Description": "Altera a senha de Admin via Web GUI -- Sem confirmar senha nova", "Resultado": '200_OK ' + str(e)}

    def changeChannelWifi24Wizard(self, ip, username, password, channel):
        if OperationalSystem == 'Windows':
            PATH = 'Setup/Selenium/chromedriver.exe'
        else:
            PATH = '/home/hulrich/PycharmProjects/automacao_b2c/Setup/Selenium/chromedriver'
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('channel = ' + channel)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            config_24_advc = driver.find_element_by_xpath('//*[@id="menu-wireless"]/ul/li[2]/a').click()
            print('Clicou em Rede 2.4 Avançado')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selChannel"]'))
            select.select_by_value(channel)
            config_24_advc_salvar = driver.find_element_by_xpath('//*[@id="btnAdvSave"]/span').click()  ### SAVE BUTTON
            result = '200_OK'



            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeChannelWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Altera canal Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeChannelWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Altera canal Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeChannelWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Altera canal Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def changeChannelWifi5Wizard(self, ip, username, password, channel):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('channel = ' + channel)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            config_5_advc = driver.find_element_by_xpath('//*[@id="menu-wireless"]/ul/li[2]/a').click()
            print('Clicou em Rede 5 Avançado')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selChannel"]'))
            select.select_by_value(channel)
            Alert = driver.switch_to.alert.accept()     ### Primeiro ALERTA
            config_5_advc_salvar = driver.find_element_by_xpath('//*[@id="btnAdvSave"]/span').click()  ### SAVE BUTTON
            driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
            time.sleep(1)
            Alert2 = driver.find_element_by_xpath('//*[@id="btnChannelAccept"]').click()  ### Segundo ALERTA
            result = '200_OK'



            time.sleep(9)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeChannelWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Altera canal Wifi 5GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeChannelWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Altera canal Wifi 5GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeChannelWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Altera canal Wifi 5GHz via Web GUI", "Resultado": str(e)}

    def hideWifi24Wizard(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            config_24_hide = driver.find_element_by_xpath('//*[@id="radBcEn0"]').get_attribute('checked')
            if config_24_hide == 'true':
                result = '200_OK'
                print('Rede já está oculta')
            else:
                config_24_hide = driver.find_element_by_xpath('//*[@id="radBcEn0"]').click()
                time.sleep(1)
                config_24_advc_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                Alert = driver.switch_to.alert.accept()
                driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
                time.sleep(1)
                Alert2 = driver.find_element_by_xpath('//*[@id="btnHideAccept"]').click()  ### Segundo ALERTA
                Alert3 = driver.find_element_by_xpath('//*[@id="btnPasswordAccept"]').click()  ### Terceiro ALERTA
                result = '200_OK'



            time.sleep(8)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "hideWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Oculta rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "hideWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Oculta rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "hideWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Oculta rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def hideWifi5Wizard(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            config_5_hide = driver.find_element_by_xpath('//*[@id="radBcEn0"]').get_attribute('checked')
            if config_5_hide == 'true':
                result = '200_OK'
                print('Rede já está oculta')
            else:
                config_5_hide = driver.find_element_by_xpath('//*[@id="radBcEn0"]').click()
                time.sleep(1)
                config_5_advc_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                Alert = driver.switch_to.alert.accept()
                driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
                time.sleep(1)
                Alert2 = driver.find_element_by_xpath('//*[@id="btnHideAccept"]').click()  ### Segundo ALERTA
                Alert3 = driver.find_element_by_xpath('//*[@id="btnPasswordAccept"]').click()  ### Terceiro ALERTA
                result = '200_OK'



            time.sleep(8)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "hideWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Oculta rede Wifi 5GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "hideWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Oculta rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "hideWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Oculta rede Wifi 5GHz via Web GUI", "Resultado": str(e)}

    def unhideWifi24Wizard(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            config_24_unhide = driver.find_element_by_xpath('//*[@id="radBcEn1"]').get_attribute('checked')
            if config_24_unhide == 'true':
                result = '200_OK'
                print('Rede já está oculta')
            else:
                config_24_unhide = driver.find_element_by_xpath('//*[@id="radBcEn1"]').click()
                time.sleep(1)
                config_24_advc_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'



            time.sleep(10)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "unhideWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Exibe rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "unhideWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Exibe rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "unhideWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Exibe rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def unhideWifi5Wizard(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            config_5_unhide = driver.find_element_by_xpath('//*[@id="radBcEn1"]').get_attribute('checked')
            if config_5_unhide == 'true':
                result = '200_OK'
                print('Rede já está oculta')
            else:
                config_5_unhide = driver.find_element_by_xpath('//*[@id="radBcEn1"]').click()
                time.sleep(1)
                config_5_advc_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'



            time.sleep(10)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "unhideWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Exibe rede Wifi 5GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "unhideWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Exibe rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "unhideWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Exibe rede Wifi 5GHz via Web GUI", "Resultado": str(e)}

    def changeBandWidth24Wizard(self, ip, username, password, bandwidth):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        if bandwidth == '20':
            bandwidth = 1
        elif bandwidth == '40':
            bandwidth = 2
        elif bandwidth == 'Auto':
            bandwidth = 0
        print('bandwidth = ' + str(bandwidth))
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            config_24_advc = driver.find_element_by_xpath('//*[@id="menu-wireless"]/ul/li[2]/a').click()
            print('Clicou em Rede 2.4 Avançado')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selBandwidth"]'))
            select.select_by_value(str(bandwidth))
            config_24_advc_salvar = driver.find_element_by_xpath('//*[@id="btnAdvSave"]').click()  ### SAVE BUTTON
            result = '200_OK'



            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeBandWidth24Wizard", "Probe#": "XXXXXXX", "Description": "Altera a largura de banda da rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeBandWidth24Wizard", "Probe#": "XXXXXXX", "Description": "Altera a largura de banda da rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeBandWidth24Wizard", "Probe#": "XXXXXXX", "Description": "Altera a largura de banda da rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def changeBandWidth5Wizard(self, ip, username, password, bandwidth):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        if bandwidth == '20':
            bandwidth = 1
        elif bandwidth == '40':
            bandwidth = 2
        elif bandwidth == '80':
            bandwidth = 3
        elif bandwidth == 'Auto':
            bandwidth = 0
        print('bandwidth = ' + str(bandwidth))
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            config_5_advc = driver.find_element_by_xpath('//*[@id="menu-wireless"]/ul/li[2]/a').click()
            print('Clicou em Rede 5 Avançado')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selBandwidth"]'))
            select.select_by_value(str(bandwidth))
            config_5_advc_salvar = driver.find_element_by_xpath('//*[@id="btnAdvSave"]').click()  ### SAVE BUTTON
            driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
            time.sleep(1)
            Alert = driver.find_element_by_xpath('//*[@id="btnChannelAccept"]').click()  ###  ALERTA
            result = '200_OK'



            time.sleep(9)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeBandWidth5Wizard", "Probe#": "XXXXXXX", "Description": "Altera a largura de banda da rede Wifi 5GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeBandWidth5Wizard", "Probe#": "XXXXXXX", "Description": "Altera a largura de banda da rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeBandWidth5Wizard", "Probe#": "XXXXXXX", "Description": "Altera a largura de banda da rede Wifi 5GHz via Web GUI", "Resultado": str(e)}

    def accessBancoBrasil(self):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('https://www.bb.com.br/pbb/pagina-inicial#/')
            time.sleep(5)
            acessar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contDesk"]/nav/ul/li[2]/a')))
            acessar.click()
            result = '200_OK'

            time.sleep(1)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "accessBancoBrasil", "Probe#": "XXXXXXX", "Description": "Acessa site Bando do Brasil", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoBrasil", "Probe#": "XXXXXXX", "Description": "Acessa site Bando do Brasil", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoBrasil", "Probe#": "XXXXXXX", "Description": "Acessa site Bando do Brasil", "Resultado": str(e)}

    def accessBancoBradesco(self):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('https://banco.bradesco/html/exclusive/index.shtm')
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="AGN"]').send_keys('1234')
            driver.find_element_by_xpath('//*[@id="CTA"]').send_keys('1234')
            driver.find_element_by_xpath('//*[@id="DIGCTA"]').send_keys('1')

            acessar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Form60"]/fieldset/ul/li[3]/input[1]')))
            acessar.click()
            result = '200_OK'

            time.sleep(1)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "accessBancoBradesco", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Bradesco", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoBradesco", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Bradesco", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoBradesco", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Bradesco", "Resultado": str(e)}

    def accessTestMyIPv6(self, **kwargs):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://v6.testmyipv6.com/')
            time.sleep(5)
            box = driver.find_element_by_xpath('/html/body/center[2]/table/tbody/tr/td/h3').text
            print(box)
            result = '200_OK'

            time.sleep(1)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "accessTestMyIPv6", "Probe#": "XXXXXXX", "Description": "Acessa site TestMyIPv6", "Resultado": result+ ';' +box}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessTestMyIPv6", "Probe#": "XXXXXXX", "Description": "Acessa site TestMyIPv6", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessTestMyIPv6", "Probe#": "XXXXXXX", "Description": "Acessa site TestMyIPv6", "Resultado": str(e)}

    def accessTestIPv6(self):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('https://ipv6.test-ipv6.com/')
            time.sleep(10)
            ipv4 = driver.find_element_by_xpath('//*[@id="your_ipv4"]/table/tbody/tr/td[2]').text
            print(ipv4)
            ipv6 = driver.find_element_by_xpath('//*[@id="your_ipv6"]/table/tbody/tr/td[2]').text
            print(ipv6)
            dns = driver.find_element_by_xpath('//*[@id="tab_main_inside"]/table[3]/tbody/tr/td[2]').text
            print(dns)
            nota = driver.find_element_by_xpath('//*[@id="score10"]').text
            print(nota)


            json_saida = {
                "IPv4": ipv4,
                "IPv6": ipv6,
                "DNS": dns,
                "NOTA": nota
            }
            print(json_saida)
            time.sleep(1)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "accessTestIPv6", "Probe#": "XXXXXXX", "Description": "Acessa site TestIPv6", "Resultado": json_saida}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessTestIPv6", "Probe#": "XXXXXXX", "Description": "Acessa site TestIPv6", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessTestIPv6", "Probe#": "XXXXXXX", "Description": "Acessa site TestIPv6", "Resultado": str(e)}

    def accessVivo(self):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('https://www.vivo.com.br/')
            time.sleep(4)
            driver.find_element_by_xpath('//*[@id="main-menu"]/div[1]/nav/div/a[2]').click()
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/header/div/div/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/nav/ul/li[2]/a').click()
            print('clicou')

            result = '200_OK'

            time.sleep(1)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "accessVivo", "Probe#": "XXXXXXX", "Description": "Acessa site da VIVO", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessVivo", "Probe#": "XXXXXXX", "Description": "Acessa site da VIVO", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessVivo", "Probe#": "XXXXXXX", "Description": "Acessa site da VIVO", "Resultado": str(e)}

    def accessBancoSantander(self):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('https://www.santander.com.br/')
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="appHeader"]/header/login-field/div/form/div/div/div[1]/div/input').send_keys('1234')
            result = '200_OK'

            time.sleep(1)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "accessBancoSantander", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Santander", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoSantander", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Santander", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoSantander", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Santander", "Resultado": str(e)}

    def accessBancoCaixa(self):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('https://www.caixa.gov.br/Paginas/home-caixa.aspx')
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="AcessoAConta"]').click()
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="nomeUsuario"]').send_keys('1234')
            result = '200_OK'

            time.sleep(1)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "accessBancoCaixa", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Caixa", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoCaixa", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Caixa", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "accessBancoCaixa", "Probe#": "XXXXXXX", "Description": "Acessa site Bando Caixa", "Resultado": str(e)}


    def changePPPoESettings(self, ip, username, password, pppoe_user, pppoe_paswd):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        pppoe_user = pppoe_user
        pppoe_paswd = pppoe_paswd
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('pppoe_user = ' + pppoe_user)
        print('pppoe_paswd = ' + pppoe_paswd)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_internet = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
            print('Clicou em Internet')
            time.sleep(1)
            config_internet_user = driver.find_element_by_xpath('//*[@id="txtUsername"]').clear()
            config_internet_user = driver.find_element_by_xpath('//*[@id="txtUsername"]').send_keys(pppoe_user)
            config_internet_passwd = driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
            config_internet_passwd = driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(pppoe_paswd)
            config_internet_salvar = driver.find_element_by_xpath('//*[@id="btnSave"]').click()

            result = '200_OK'



            time.sleep(8)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changePPPoESettings", "Probe#": "XXXXXXX", "Description": "Altera usuário/senha de PPPoE via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changePPPoESettings", "Probe#": "XXXXXXX", "Description": "Altera usuário/senha de PPPoE via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changePPPoESettings", "Probe#": "XXXXXXX", "Description": "Altera usuário/senha de PPPoE via Web GUI", "Resultado": str(e)}


    def execEnablePortMirror(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wanMirror = driver.find_element_by_xpath('/html/body/div[3]/div/fieldset/a[1]').click()
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            if driver.find_element_by_xpath('//*[@id="DiagConfigForm"]/input[1]').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="DiagConfigForm"]/input[1]').click()
                driver.find_element_by_xpath('//*[@id="DiagConfigForm"]/input[3]').click()
                result = '200_OK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execEnablePortMirror", "Probe#": "XXXXXXX", "Description": "Habilita PortMirror na WAN via página padrão", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnablePortMirror", "Probe#": "XXXXXXX", "Description": "Habilita PortMirror na WAN via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnablePortMirror", "Probe#": "XXXXXXX", "Description": "Habilita PortMirror na WAN via página padrão", "Resultado": str(e)}

    
    def execEnableUPnPSettings(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            upnp = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[8]/a').click()
            upnp = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[8]/a').text
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            upnp_AdmState = driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[1]/label').text
            if driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[1]/input[1]').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[1]/input[1]').click()
                driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[2]/input').click()
                result = '200_OK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execEnableUPnPSettings", "Probe#": "XXXXXXX", "Description": "Habilita UPnP via página padrão", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableUPnPSettings", "Probe#": "XXXXXXX", "Description": "Habilita UPnP via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableUPnPSettings", "Probe#": "XXXXXXX", "Description": "Habilita UPnP via página padrão", "Resultado": str(e)}

    def execDisableUPnPSettings(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            upnp = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[8]/a').click()
            upnp = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[8]/a').text
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            upnp_AdmState = driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[1]/label').text
            if driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[1]/input[2]').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[1]/input[2]').click()
                driver.find_element_by_xpath('//*[@id="UpnpForm"]/div[2]/input').click()
                result = '200_OK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableUPnPSettings", "Probe#": "XXXXXXX", "Description": "Desabilita UPnP via página padrão", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableUPnPSettings", "Probe#": "XXXXXXX", "Description": "Desabilita UPnP via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableUPnPSettings", "Probe#": "XXXXXXX", "Description": "Desabilita UPnP via página padrão", "Resultado": str(e)}

    def execFakeFirmwareUpdate(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        print(platform.system())
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            fwUpdate = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/a').click()
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            print(driver.find_element_by_xpath('//*[@id="fsHttp"]/legend').text)
            fwUpdate_file = driver.find_element_by_xpath('//*[@id="fileUpgradeByHTTP"]')
            print('passou')
            if OperationalSystem == 'Windows':
                PATH_FW = 'C:\\ScriptsPython\\automacao_b2c\\Setup\\Selenium\\FakeFirmware.bin'
            else:
                PATH_FW = '/home/hulrich/PycharmProjects/automacao_b2c/Setup/Selenium/FakeFirmware.bin'
            fwUpdate_file.send_keys(PATH_FW)
            driver.find_element_by_xpath('//*[@id="btnUpgradeByHTTP"]').click()
            if driver.find_element_by_xpath('/html/body/h1'):
                result = '200_OK'
            else:
                result = 'NOK'
            time.sleep(1)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execFakeFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa teste de Firmware Update com arquivo fake via página padrão", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execFakeFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa teste de Firmware Update com arquivo fake via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execFakeFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa teste de Firmware Update com arquivo fake via página padrão", "Resultado": str(e)}

    def execSkypeWeb(self, username, password):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('https://www.skype.com/pt-br/')
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="customMeControl"]/a[1]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="customMeControl"]/ul/li[2]/a').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i0116"]').send_keys(username)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
            driver.find_element_by_xpath('//*[@id="i0118"]').send_keys(password)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="i0118"]').submit()
            time.sleep(12)
            driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div[1]/div/div/div/div/div/div[3]/button').click()
            time.sleep(2)
            result = '200_OK'
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execSkypeWeb", "Probe#": "XXXXXXX", "Description": "Acessa Skype Web", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execSkypeWeb", "Probe#": "XXXXXXX", "Description": "Acessa Skype Web", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execSkypeWeb", "Probe#": "XXXXXXX", "Description": "Acessa Skype Web", "Resultado": str(e)}

    def checkForbiddenURLs(self, ip):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            print('\n -=- Testando página http://' + ip + '/router.data')
            driver.get('http://' + ip + '/router.data')
            if driver.find_element_by_xpath('/html/body/h2'):
                teste1 = 'OK'
            else:
                teste1 = 'NOK'
            print('\n -=- Testando página http://' + ip + '/cgi-bin/tech_support_cgi')
            driver.get('http://' + ip + '/cgi-bin/tech_support_cgi')
            if driver.find_element_by_xpath('/html/body/h2'):
                teste2 = 'OK'
            else:
                teste2 = 'NOK'
            print('\n -=- Testando página http://' + ip + '/cgi-bin/restore.exe')
            driver.get('http://' + ip + '/cgi-bin/restore.exe')
            if driver.find_element_by_xpath('/html/body/h2'):
                teste3 = 'OK'
            else:
                teste3 = 'NOK'
            print('\n -=- Testando página http://' + ip + '/saveconf.htm')
            driver.get('http://' + ip + '/saveconf.htm')
            if driver.find_element_by_xpath('/html/body/h2'):
                teste4 = 'OK'
            else:
                teste4 = 'NOK'
            # print('\n -=- Testando página http://' + ip + ':port/rom-0')
            # driver.get('http://' + ip + ':port/rom-0')
            # if driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[2]/button'):
            #     teste5 = 'OK'
            # else:
            #     teste5 = 'NOK'
            if teste1 and teste2 and teste3 and teste4 == 'OK':
                result = '200_OK'
            else:
                result = '400_NOK'

            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkForbiddenURLs", "Probe#": "XXXXXXX", "Description": "Testa URLs que não devem ser abertas", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkForbiddenURLs", "Probe#": "XXXXXXX", "Description": "Testa URLs que não devem ser abertas", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkForbiddenURLs", "Probe#": "XXXXXXX", "Description": "Testa URLs que não devem ser abertas", "Resultado": str(e)}

    def checkRefusedURLs(self, ip):
        
        driver = WebDriver.get_driver()
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')

            print('\n -=- Testando página http://' + ip + ':5555/UD/act?1')
            driver.get('http://' + ip + ':5555/UD/act?1')
            driver.quit()

            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkRefusedURLs", "Probe#": "XXXXXXX", "Description": "Testa URLs que não devem ser abertas", "Resultado": "400_NOK;Foi posspivel abrir a página"}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkRefusedURLs", "Probe#": "XXXXXXX", "Description": "Testa URLs que não devem ser abertas", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkRefusedURLs", "Probe#": "XXXXXXX", "Description": "Testa URLs que não devem ser abertas", "Resultado": str(e)}

    def teste(self):
        PATH = 'Setup/Selenium/geckodriver.exe'
        driver = webdriver.Firefox(executable_path=PATH)
        size = driver.set_window_size(1280, 600)
        try:
            driver.get('http://www.google.com')
            return 'OK'
        except NoSuchElementException as exception:
            print(exception)
            return str(exception)
        except Exception as e:
            print(e)
            return str(e)

    def execCreateFirewallRule(self, ip, username, password, ruleName, ruleProtocol, ruleLocalPort, ruleRemotePort, ruleLocalIP, ruleRemoteIP, ruleAction):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        ruleName = ruleName
        ruleProtocol = ruleProtocol
        ruleLocalPort = ruleLocalPort
        ruleRemotePort = ruleRemotePort
        ruleLocalIP = ruleLocalIP
        ruleRemoteIP = ruleRemoteIP
        ruleAction = ruleAction
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('ruleName = ' + ruleName)
        print('ruleProtocol = ' + ruleProtocol)
        print('ruleLocalPort = ' + ruleLocalPort)
        print('ruleRemotePort = ' + ruleRemotePort)
        print('ruleLocalIP = ' + ruleLocalIP)
        print('ruleRemoteIP = ' + ruleRemoteIP)
        print('ruleAction = ' + ruleAction)
        print('-=-' * 20)

        if ruleAction == 'Rejeita Local':
            ruleAction = 'rjctLocal'
        elif ruleAction == 'Rejeita Remoto':
            ruleAction = 'rjctRemote'
        elif ruleAction == 'Aceita Local':
            ruleAction = 'acptLocal'
        elif ruleAction == 'Aceita Remoto':
            ruleAction = 'acptRemote'
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_firewall = driver.find_element_by_xpath('//*[@id="firewall"]/a').click()
            print('Clicou em Firewall')
            time.sleep(1)
            config_firewall_nome = driver.find_element_by_xpath('//*[@id="txtFirewallName"]').send_keys(ruleName)
            config_firewall_protoc = Select(driver.find_element_by_xpath('//*[@id="selFirewallProtocol"]'))
            config_firewall_protoc.select_by_value(str(ruleProtocol))
            config_firewall_localPort = driver.find_element_by_xpath('//*[@id="txtFirewallLocalPort"]').send_keys(ruleLocalPort)
            config_firewall_remotePort = driver.find_element_by_xpath('//*[@id="txtFirewallRemotePort"]').send_keys(ruleRemotePort)
            config_firewall_localIP = driver.find_element_by_xpath('//*[@id="txtFirewallLocalAddress"]').send_keys(ruleLocalIP)
            config_firewall_remoteIP = driver.find_element_by_xpath('//*[@id="txtFirewallRemoteAddress"]').send_keys(ruleRemoteIP)
            config_firewall_action = Select(driver.find_element_by_xpath('//*[@id="selFirewallAction"]'))
            config_firewall_action.select_by_value(str(ruleAction))

            gerenc_Ferram_tenta_exec = driver.find_element_by_xpath('//*[@id="aFirewallApply"]').click() ### Botão ADD
            time.sleep(8)
            result = '200_OK'
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execCreateFirewallRule", "Probe#": "XXXXXXX", "Description": "Cria regra de Firewall via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execCreateFirewallRule", "Probe#": "XXXXXXX", "Description": "Cria regra de Firewall via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execCreateFirewallRule", "Probe#": "XXXXXXX", "Description": "Cria regra de Firewall via Web GUI", "Resultado": str(e)}

    def checkCofoneIPv6(self, **kwargs): ### TUDO OK

        print('IPV6 TEST')
        
        driver = WebDriver.get_driver()

        try:
            driver.get('http://www.cofone.eu/')
            time.sleep(1)
            if driver.find_element_by_xpath('/html/body/center/h1'):
                result = '200_OK'
            else:
                result = '400_NOK'
            time.sleep(5)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkCofoneIPv6", "Probe#": "XXXXXXXXX", "Description": "Executar algumas validações site Cofone", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkCofoneIPv6", "Probe#": "XXXXXXXXX", "Description": "Executar algumas validações site Cofone", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            driver.quit()
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkCofoneIPv6", "Probe#": "XXXXXXXXX", "Description": "Executar algumas validações site Cofone", "Resultado": str(e)}

    def checkSessionExpirationWizard(self, ip, username, password):
        if OperationalSystem == 'Windows':
            PATH = 'Setup/Selenium/geckodriver.exe'
        else:
            PATH = 'Setup/Selenium/geckodriver'
        driver = webdriver.Firefox(executable_path=PATH)
        size = driver.set_window_size(1280, 600)
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(900)
            print('Ja passou 15min...')
            driver.refresh()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            if driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input'):
                result = '200_OK'
            else:
                result = '400_NOK'



            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkSessionExpirationWizard", "Probe#": "XXXXXXX", "Description": "Verifica o timeout da sesão Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkSessionExpirationWizard", "Probe#": "XXXXXXX", "Description": "Verifica o timeout da sesão Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkSessionExpirationWizard", "Probe#": "XXXXXXX", "Description": "Verifica o timeout da sesão Web GUI", "Resultado": str(e)}

    def execEnableSSHWizard(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            remoteAccess = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[2]').click()
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            if driver.find_element_by_xpath('//*[@id="RaccForm"]/div[2]/input').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="RaccForm"]/div[2]/input').click()
                driver.find_element_by_xpath('//*[@id="RaccForm"]/div[3]/input').click()
                result = '200_OK'
            time.sleep(3)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execEnableSSHWizard", "Probe#": "XXXXXXX", "Description": "Habilita SSH na LAN & WAN via página padrão", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableSSHWizard", "Probe#": "XXXXXXX", "Description": "Habilita SSH na LAN & WAN via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableSSHWizard", "Probe#": "XXXXXXX", "Description": "Habilita SSH na LAN & WAN via página padrão", "Resultado": str(e)}

    def execEnableTelnetWizard(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            remoteAccess = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[2]').click()
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            if driver.find_element_by_xpath('//*[@id="RaccForm"]/div[1]/input').get_attribute('checked') == 'true':
                result = '200_OK'
            else:
                driver.find_element_by_xpath('//*[@id="RaccForm"]/div[1]/input').click()
                driver.find_element_by_xpath('//*[@id="RaccForm"]/div[3]/input').click()
                result = '200_OK'
            time.sleep(3)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execEnableTelnetWizard", "Probe#": "XXXXXXX", "Description": "Habilita Telnet na LAN & WAN via página padrão", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableTelnetWizard", "Probe#": "XXXXXXX", "Description": "Habilita Telnet na LAN & WAN via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableTelnetWizard", "Probe#": "XXXXXXX", "Description": "Habilita Telnet na LAN & WAN via página padrão", "Resultado": str(e)}

    def changeAuthModeWifi24Wizard(self, ip, username, password, authentication):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('authentication = ' + str(authentication))
        if authentication == 'WPA2':
            authentication = 34
        elif authentication == 'WPA / WPA2':
            authentication = 44
        elif authentication == 'WEP':
            authentication = '02'
        elif authentication == 'Aberta':
            authentication = '00'
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selAuthMode"]'))
            result = ''
            if authentication == 44:
                select.select_by_value(str(authentication))
                Alert = driver.switch_to.alert.accept()
                config_24_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                time.sleep(1)
                Alert = driver.switch_to.alert.accept()
                time.sleep(1)
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'
            elif authentication == 34:
                select.select_by_value(str(authentication))
                config_24_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                time.sleep(1)
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'
            elif authentication == '02':
                select.select_by_value(str(authentication))
                Alert = driver.switch_to.alert.accept()
                config_24_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                time.sleep(1)
                Alert2 = driver.find_element_by_xpath('//*[@id="btnModeAccept"]').click()  ### Segundo ALERTA
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'
            elif authentication == '00':
                select.select_by_value(str(authentication))
                config_24_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                time.sleep(3)
                result = '200_OK'

            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAuthModeWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Altera o método de Autenticação da rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAuthModeWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Altera o método de Autenticação da rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAuthModeWifi24Wizard", "Probe#": "XXXXXXX", "Description": "Altera o método de Autenticação da rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def changeAuthModeWifi5Wizard(self, ip, username, password, authentication):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('authentication = ' + str(authentication))
        if authentication == 'WPA2':
            authentication = 34
        elif authentication == 'Aberta':
            authentication = '00'

        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selAuthMode"]'))
            result = ''
            if authentication == 34:
                select.select_by_value(str(authentication))
                config_5_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                time.sleep(1)
                Alert = driver.switch_to.alert.accept()
                result = '200_OK'
            elif authentication == '00':
                select.select_by_value(str(authentication))
                config_5_salvar = driver.find_element_by_xpath('//*[@id="btnBasSave"]').click()  ### SAVE BUTTON
                time.sleep(3)
                result = '200_OK'



            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeAuthModeWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Altera o método de Autenticação da rede Wifi 5GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAuthModeWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Altera o método de Autenticação da rede Wifi 5GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeAuthModeWifi5Wizard", "Probe#": "XXXXXXX", "Description": "Altera o método de Autenticação da rede Wifi 5GHz via Web GUI", "Resultado": str(e)}

    def changeStandard24Wizard(self, ip, username, password, standard):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('standard = ' + str(standard))
        if standard == '802.11g/n':
            standard = 12
        elif standard == '802.11b':
            standard = 2
        elif standard == '802.11g':
            standard = 4
        elif standard == '802.11b/g':
            standard = 6
        elif standard == '802.11n':
            standard = 8
        elif standard == '802.11b/g/n':
            standard = 14
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_24 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
            print('Clicou em Rede 2.4')
            time.sleep(1)
            config_24_advc = driver.find_element_by_xpath('//*[@id="menu-wireless"]/ul/li[2]/a').click()
            print('Clicou em Rede 2.4 Avançado')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selMode"]'))
            select.select_by_value(str(standard))
            config_24_advc_salvar = driver.find_element_by_xpath('//*[@id="btnAdvSave"]').click()  ### SAVE BUTTON
            result = '200_OK'



            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeStandard24Wizard", "Probe#": "XXXXXXX", "Description": "Altera o padrão de operação (b/g/n) da rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeStandard24Wizard", "Probe#": "XXXXXXX", "Description": "Altera o padrão de operação (b/g/n) da rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeStandard24Wizard", "Probe#": "XXXXXXX", "Description": "Altera o padrão de operação (b/g/n) da rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def changeStandard5Wizard(self, ip, username, password, standard):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('standard = ' + str(standard))
        if standard == '802.11n/ac':
            standard = '25'
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_5 = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[4]/a').click()
            print('Clicou em Rede 5')
            time.sleep(1)
            config_5_advc = driver.find_element_by_xpath('//*[@id="menu-wireless"]/ul/li[2]/a').click()
            print('Clicou em Rede 5 Avançado')
            time.sleep(1)
            select = Select(driver.find_element_by_xpath('//*[@id="selMode"]'))
            select.select_by_value(str(standard))
            config_5_advc_salvar = driver.find_element_by_xpath('//*[@id="btnAdvSave"]').click()  ### SAVE BUTTON
            result = '200_OK'



            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "changeStandard5Wizard", "Probe#": "XXXXXXX", "Description": "Altera o padrão de operação (b/g/n/ac) da rede Wifi 2.4GHz via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeStandard5Wizard", "Probe#": "XXXXXXX", "Description": "Altera o padrão de operação (b/g/n/ac) da rede Wifi 2.4GHz via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "changeStandard5Wizard", "Probe#": "XXXXXXX", "Description": "Altera o padrão de operação (b/g/n/ac) da rede Wifi 2.4GHz via Web GUI", "Resultado": str(e)}

    def execSoftResetPadrao(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            restoreDefault = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/div/a[4]').click()
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            reset = driver.find_element_by_xpath('//*[@id="btnRestore"]').click()
            Alert = driver.switch_to.alert.accept()
            shutdown = '200_OK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execSoftResetPadrao", "Probe#": "XXXXXXX", "Description": "Executa um SOFT Reset via página padrão", "Resultado": shutdown}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execSoftResetPadrao", "Probe#": "XXXXXXX", "Description": "Executa um SOFT Reset via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execSoftResetPadrao", "Probe#": "XXXXXXX", "Description": "Executa um SOFT Reset via página padrão", "Resultado": str(e)}

    def execCreateFirewallRuleACS(self, ip, username, password, ruleName, ruleProtocol, ruleLocalPort, ruleRemotePort, ruleLocalIP, ruleRemoteIP, ruleAction):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        ruleName = ruleName
        ruleProtocol = ruleProtocol
        ruleLocalPort = ruleLocalPort
        ruleRemotePort = ruleRemotePort
        ruleLocalIP = ruleLocalIP
        ruleRemoteIP = ruleRemoteIP
        ruleAction = ruleAction
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('ruleName = ' + ruleName)
        print('ruleProtocol = ' + ruleProtocol)
        print('ruleLocalPort = ' + ruleLocalPort)
        print('ruleRemotePort = ' + ruleRemotePort)
        print('ruleLocalIP = ' + ruleLocalIP)
        print('ruleRemoteIP = ' + ruleRemoteIP)
        print('ruleAction = ' + ruleAction)
        print('-=-' * 20)

        if ruleAction == 'Rejeita Local':
            ruleAction = 'rjctLocal'
        elif ruleAction == 'Rejeita Remoto':
            ruleAction = 'rjctRemote'
        elif ruleAction == 'Aceita Local':
            ruleAction = 'acptLocal'
        elif ruleAction == 'Aceita Remoto':
            ruleAction = 'acptRemote'
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config_firewall = driver.find_element_by_xpath('//*[@id="firewall"]/a').click()
            print('Clicou em Firewall')
            time.sleep(1)
            config_firewall_nome = driver.find_element_by_xpath('//*[@id="txtFirewallName"]').send_keys(ruleName)
            config_firewall_protoc = Select(driver.find_element_by_xpath('//*[@id="selFirewallProtocol"]'))
            config_firewall_protoc.select_by_value(str(ruleProtocol))
            config_firewall_localPort = driver.find_element_by_xpath('//*[@id="txtFirewallLocalPort"]').send_keys(ruleLocalPort)
            config_firewall_remotePort = driver.find_element_by_xpath('//*[@id="txtFirewallRemotePort"]').send_keys(ruleRemotePort)
            config_firewall_localIP = driver.find_element_by_xpath('//*[@id="txtFirewallLocalAddress"]').send_keys(ruleLocalIP)
            config_firewall_remoteIP = driver.find_element_by_xpath('//*[@id="txtFirewallRemoteAddress"]').send_keys(ruleRemoteIP)
            config_firewall_action = Select(driver.find_element_by_xpath('//*[@id="selFirewallAction"]'))
            config_firewall_action.select_by_value(str(ruleAction))

            gerenc_Ferram_tenta_exec = driver.find_element_by_xpath('//*[@id="aFirewallApply"]').click() ### Botão ADD
            if driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/div[2]/table[2]/tbody[3]/tr[3]/td[2]/span').text == 'Nao pode incluir tr069 na porta':
                result = '200_OK'
            else:
                result = '400_NOK'
            time.sleep(2)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execCreateFirewallRuleACS", "Probe#": "XXXXXXX", "Description": "Tenta criar regra de Firewall especifica para mesma porta do ACS via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execCreateFirewallRuleACS", "Probe#": "XXXXXXX", "Description": "Tenta criar regra de Firewall especifica para mesma porta do ACS via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execCreateFirewallRuleACS", "Probe#": "XXXXXXX", "Description": "Tenta criar regra de Firewall especifica para mesma porta do ACS via Web GUI", "Resultado": str(e)}

    def accessWizardFirefox(self, ip, username, password): ### TUDO OK
        if OperationalSystem == 'Windows':
            PATH = 'Setup/Selenium/geckodriver.exe'
        else:
            PATH = 'Setup/Selenium/geckodriver'
        driver = webdriver.Firefox(executable_path=PATH)
        size = driver.set_window_size(1280, 600)
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "78", "Description": "Acessar página padrão ", "Resultado": "200 - OK"}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "78", "Description": "Acessar página padrão ", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "checkPPPoEStatus", "Probe#": "78", "Description": "Acessar página padrão ", "Resultado": str(e)}

    def execFirmwareUpdate(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        print(platform.system())
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            fwUpdate = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/a').click()
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            print(driver.find_element_by_xpath('//*[@id="fsHttp"]/legend').text)
            fwUpdate_file = driver.find_element_by_xpath('//*[@id="fileUpgradeByHTTP"]')
            if OperationalSystem == 'Windows':
                PATH_FW = 'C:\\ScriptsPython\\automacao_b2c\\Setup\\Selenium\\FirmwareOficial\\BR_g12.6_RTF_TEF001_V7.11.S9_V014'
            else:
                PATH_FW = '/home/hulrich/PycharmProjects/automacao_b2c/Setup/Selenium/FirmwareOficial/BR_g12.6_RTF_TEF001_V7.11.S9_V014'
            fwUpdate_file.send_keys(PATH_FW)
            driver.find_element_by_xpath('//*[@id="btnUpgradeByHTTP"]').click()
            time.sleep(60)
            if driver.find_element_by_xpath('/html/body/h1'):
                result = '200_OK'
            else:
                result = '400_NOK'
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa teste de Firmware Update com arquivo oficial via página padrão", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa teste de Firmware Update com arquivo oficial via página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execFirmwareUpdate", "Probe#": "XXXXXXX", "Description": "Executa teste de Firmware Update com arquivo oficial via página padrão", "Resultado": str(e)}

    def execConfigDNS(self, ip, username, password, primaryDNS, secondaryDNS):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('DNS Primario = ' + primaryDNS)
        print('DNS Secundário = ' + secondaryDNS)
        print('-=-' * 20)

        primaryDNS = primaryDNS.split('.')
        secondaryDNS = secondaryDNS.split('.')

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wanInterface = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wanInterface)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            wanInterface_PPPoE = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
            time.sleep(1)
            primaryDNS_01 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[1]').clear()
            primaryDNS_01 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[1]').send_keys(primaryDNS[0])
            primaryDNS_02 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[2]').clear()
            primaryDNS_02 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[2]').send_keys(primaryDNS[1])
            primaryDNS_03 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[3]').clear()
            primaryDNS_03 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[3]').send_keys(primaryDNS[2])
            primaryDNS_04 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[4]').clear()
            primaryDNS_04 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[2]/input[4]').send_keys(primaryDNS[3])

            secondaryDNS_01 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[1]').clear()
            secondaryDNS_01 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[1]').send_keys(secondaryDNS[0])
            secondaryDNS_02 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[2]').clear()
            secondaryDNS_02 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[2]').send_keys(secondaryDNS[1])
            secondaryDNS_03 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[3]').clear()
            secondaryDNS_03 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[3]').send_keys(secondaryDNS[2])
            secondaryDNS_04 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[4]').clear()
            secondaryDNS_04 = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[3]/div[3]/input[4]').send_keys(secondaryDNS[3])

            salvar = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click() ### Botão Salvar
            time.sleep(5)
            result = '200_OK'
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execConfigDNS", "Probe#": "XXXXXXX", "Description": "Configura DNS primário e secundário via Página padrão", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execConfigDNS", "Probe#": "XXXXXXX", "Description": "Configura DNS primário e secundário via Página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execConfigDNS", "Probe#": "XXXXXXX", "Description": "Configura DNS primário e secundário via Página padrão", "Resultado": str(e)}

    def execEnableDMZ(self, ip, username, password, DMZHost):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('DMZHost = ' + DMZHost)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            natDMZ = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[2]').click()
            natDMZ = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[2]').text
            print(natDMZ)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            if driver.find_element_by_xpath('//*[@id="DmzForm"]/div[1]/input[1]').get_attribute('checked') == 'true':
                natDMZ_admState = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[1]/input[1]')
                natDMZ_Host = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[2]/input').get_property('value')
                time.sleep(1)
            else:
                natDMZ_admState = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[1]/input[1]').click()
                natDMZ_Host = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[2]/input').clear()
                natDMZ_Host = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[2]/input').send_keys(DMZHost)
                salvar = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[3]/input[4]').click()
                time.sleep(5)
            result = '200_OK'
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execEnableDMZ", "Probe#": "XXXXXXX", "Description": "Habilita DMZ via Página padrão", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableDMZ", "Probe#": "XXXXXXX", "Description": "Habilita DMZ via Página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execEnableDMZ", "Probe#": "XXXXXXX", "Description": "Habilita DMZ via Página padrão", "Resultado": str(e)}

    def execDisableDMZ(self, ip, username, password):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            natDMZ = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[2]').click()
            natDMZ = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[3]/a[2]').text
            print(natDMZ)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            if driver.find_element_by_xpath('//*[@id="DmzForm"]/div[1]/input[2]').get_attribute('checked') == 'true':
                natDMZ_admState = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[1]/input[2]')
                time.sleep(1)
            else:
                natDMZ_admState = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[1]/input[2]').click()
                salvar = driver.find_element_by_xpath('//*[@id="DmzForm"]/div[3]/input[4]').click()
                time.sleep(5)
            result = '200_OK'
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableDMZ", "Probe#": "XXXXXXX", "Description": "Desabilita DMZ via Página padrão", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableDMZ", "Probe#": "XXXXXXX", "Description": "Desabilita DMZ via Página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableDMZ", "Probe#": "XXXXXXX", "Description": "Desabilita DMZ via Página padrão", "Resultado": str(e)}

    def execAddDDNS(self, ip, username, password, provider, hostname, interface, ddnsUsername, ddnsPassword):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('provider = ' + provider)
        print('hostname = ' + hostname)
        print('interface = ' + interface)
        print('ddnsUsername = ' + ddnsUsername)
        print('ddnsPassword = ' + ddnsPassword)
        print('-=-' * 20)

        if provider == 'No-IP':
            provider = 0
        elif provider == 'Now-IP':
            provider = 1
        elif provider == 'DynDNS':
            provider = 2
        elif provider == 'Now-DNS':
            provider = 3

        if interface == 'ip2':
            interface = 2
        elif interface == 'ip3':
            interface = 3
        elif interface == 'ip4':
            interface = 4

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            ddns = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[4]/a[2]').click()
            ddns = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[3]/div[4]/a[2]').text
            print(ddns)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            add = driver.find_element_by_xpath('//*[@id="AddDdns"]').click()
            ddnProvider = Select(driver.find_element_by_xpath('//*[@id="iProvider"]'))
            ddnProvider.select_by_value(str(provider))
            ddnsHostname = driver.find_element_by_xpath('//*[@id="DdnsSettingForm"]/div[3]/input').send_keys(hostname)
            ddnsInterface = Select(driver.find_element_by_xpath('//*[@id="wan_ip_intf"]'))
            ddnsInterface.select_by_value(str(interface))
            ddnsUser = driver.find_element_by_xpath('//*[@id="DdnsSettingForm"]/div[5]/input').send_keys(ddnsUsername)
            ddnsPasswd = driver.find_element_by_xpath('//*[@id="DdnsSettingForm"]/div[6]/input').send_keys(ddnsPassword)
            salvar = driver.find_element_by_xpath('//*[@id="DdnsSettingForm"]/div[7]/input[2]').click()

            result = '200_OK'
            time.sleep(3)
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDisableDMZ", "Probe#": "XXXXXXX", "Description": "Desabilita DMZ via Página padrão", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableDMZ", "Probe#": "XXXXXXX", "Description": "Desabilita DMZ via Página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDisableDMZ", "Probe#": "XXXXXXX", "Description": "Desabilita DMZ via Página padrão", "Resultado": str(e)}

    def execChangeDHCPRange(self, ip, username, password, dhcpRangeMin, dhcpRangeMax):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('dhcpRangeMin = ' + dhcpRangeMin)
        print('dhcpRangeMax = ' + dhcpRangeMax)
        print('-=-' * 20)

        dhcpRangeMin = dhcpRangeMin.split('.')
        dhcpRangeMax = dhcpRangeMax.split('.')

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[2]/a').click()
            print('Clicou em Rede Local')
            time.sleep(1)
            dhcpMin_01 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[1]').clear()
            dhcpMin_01 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[1]').send_keys(dhcpRangeMin[0])
            dhcpMin_02 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[2]').clear()
            dhcpMin_02 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[2]').send_keys(dhcpRangeMin[1])
            dhcpMin_03 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[3]').clear()
            dhcpMin_03 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[3]').send_keys(dhcpRangeMin[2])
            dhcpMin_04 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[4]').clear()
            dhcpMin_04 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[5]/td[2]/input[4]').send_keys(dhcpRangeMin[3])

            dhcpMax_01 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[1]').clear()
            dhcpMax_01 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[1]').send_keys(dhcpRangeMax[0])
            dhcpMax_02 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[2]').clear()
            dhcpMax_02 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[2]').send_keys(dhcpRangeMax[1])
            dhcpMax_03 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[3]').clear()
            dhcpMax_03 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[3]').send_keys(dhcpRangeMax[2])
            dhcpMax_04 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[4]').clear()
            dhcpMax_04 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[1]/tbody/tr[6]/td/input[4]').send_keys(dhcpRangeMax[3])

            salvar = driver.find_element_by_xpath('//*[@id="btnDhcpSave"]').click() ### Botão Salvar
            result = '200_OK'

            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execChangeDHCPRange", "Probe#": "XXXXXXX", "Description": "Altera o range de IP DHCP via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execChangeDHCPRange", "Probe#": "XXXXXXX", "Description": "Altera o range de IP DHCP via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execChangeDHCPRange", "Probe#": "XXXXXXX", "Description": "Altera o range de IP DHCP via Web GUI", "Resultado": str(e)}

    def execChangeVLAN(self, ip, username, password, interface, vlanValue):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('interface = ' + interface)
        print('vlanValue = ' + vlanValue)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            wan = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
            wan = driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').text
            print(wan)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            if interface == 'ip2':
                index = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
                vlanID = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').clear()
                vlanID = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').send_keys(vlanValue)
                salvar = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click() ### Botão Salvar
            elif interface == 'ip3':
                index = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[2]/td[2]/a').click()
                vlanID = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').clear()
                vlanID = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').send_keys(vlanValue)
                salvar = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click() ### Botão Salvar
            elif interface == 'ip4':
                index = driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[3]/td[2]/a').click()
                vlanID = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').clear()
                vlanID = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[1]/div[2]/input').send_keys(vlanValue)
                salvar = driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()  ### Botão Salvar
                time.sleep(5)
            result = '200_OK'
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execChangeVLAN", "Probe#": "XXXXXXX", "Description": "Altera o valor da VLAN via Página padrão", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execChangeVLAN", "Probe#": "XXXXXXX", "Description": "Altera o valor da VLAN via Página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execChangeVLAN", "Probe#": "XXXXXXX", "Description": "Altera o valor da VLAN via Página padrão", "Resultado": str(e)}

    def execChangeACSURL(self, ip, username, password, acsURL, periodicInterval):
        
        driver = WebDriver.get_driver()
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('acsURL = ' + acsURL)
        print('periodicInterval = ' + periodicInterval)
        print('-=-' * 20)

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/padrao')
            user_input = driver.find_element_by_id('txtUser')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            login_button.click()
            time.sleep(3)
            driver.switch_to.frame('menuFrm')
            tr69 = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[1]').click()
            tr69 = driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[1]/a[1]').text
            print(tr69)
            time.sleep(1)
            driver.switch_to.parent_frame()  ## é necessario voltar um nivel na hierarquia para encontrar o elemento
            driver.switch_to.frame('mainFrm')
            URL = driver.find_element_by_xpath('//*[@id="Tr69Form"]/div[2]/input').clear()
            URL = driver.find_element_by_xpath('//*[@id="Tr69Form"]/div[2]/input').send_keys(acsURL)
            periodic = driver.find_element_by_xpath('//*[@id="Tr69Form"]/div[6]/input').clear()
            periodic = driver.find_element_by_xpath('//*[@id="Tr69Form"]/div[6]/input').send_keys(periodicInterval)
            time.sleep(5)
            result = '200_OK'
            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execChangeACSURL", "Probe#": "XXXXXXX", "Description": "Altera a URL do ACS e o Periodic Inform via Página padrão", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execChangeACSURL", "Probe#": "XXXXXXX", "Description": "Altera a URL do ACS e o Periodic Inform via Página padrão", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execChangeACSURL", "Probe#": "XXXXXXX", "Description": "Altera a URL do ACS e o Periodic Inform via Página padrão", "Resultado": str(e)}

    def execDHCPReserv(self, ip, username, password, staticIP):
        
        driver = WebDriver.get_driver()
        driver.execute_script("window.alert = function() {};")
        usuario = username
        senha = password
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ip = ' + ip)
        print('username = ' + username)
        print('password = ' + password)
        print('staticIP = ' + staticIP)
        print('-=-' * 20)

        staticIP = staticIP.split('.')

        try:
            print('\n\n == Abrindo URL == ')
            driver.get('http://' + ip + '/')
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a')
            link.click()
            time.sleep(1)
            link = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a')
            link.click()
            time.sleep(1)
            print(' == Autenticando == ')
            driver.get('http://' + ip + '/login.asp')
            driver.switch_to.default_content()
            user_input = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(usuario)
            pass_input = driver.find_element_by_id('txtPass')
            pass_input.send_keys(senha)
            login_button = driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            print('Clicou em Configurações')
            time.sleep(1)
            config = driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[2]/a').click()
            print('Clicou em Rede Local')
            time.sleep(1)
            hostname = Select(driver.find_element_by_xpath('//*[@id="selStaticHost"]'))
            hostname = hostname.select_by_value('0')
            static_01 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[1]').clear()
            static_01 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[1]').send_keys(staticIP[0])
            static_02 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[2]').clear()
            static_02 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[2]').send_keys(staticIP[1])
            static_03 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[3]').clear()
            static_03 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[3]').send_keys(staticIP[2])
            static_04 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[4]').clear()
            static_04 = driver.find_element_by_xpath('//*[@id="tab-01"]/table[2]/tbody/tr[1]/td[3]/input[4]').send_keys(staticIP[3])

            salvar = driver.find_element_by_xpath('//*[@id="spnDhcpReserve"]').click()  ### Botão Salvar
            result = '200_OK'

            time.sleep(5)
            driver.quit()

            return {"Resultado_Probe": "OK", "ControllerName": "gui", "ProbeName": "execDHCPReserv", "Probe#": "XXXXXXX", "Description": "Cria reserva de IP para um dispositivo via Web GUI", "Resultado": result}

        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDHCPReserv", "Probe#": "XXXXXXX", "Description": "Cria reserva de IP para um dispositivo via Web GUI", "Resultado": str(exception)}

        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "gui", "ProbeName": "execDHCPReserv", "Probe#": "XXXXXXX", "Description": "Cria reserva de IP para um dispositivo via Web GUI", "Resultado": str(e)}
