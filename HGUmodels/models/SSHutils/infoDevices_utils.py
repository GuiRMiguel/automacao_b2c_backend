import time
from datetime import datetime
from HGUmodels.models.SSHutils.services.network import ping, connectSSHE, speedTest
from HGUmodels.models.SSHutils.services.general import macToSerial
from HGUmodels.models.SSHutils.services.methodsHgu import cliHgu, cliAskeyBrcm, cliAskeyEcnt, cliMitraBrcm, cliMitraEcnt
from HGUmodels.models.SSHutils.services.parameters import getDefaultParams

###Instancia de objeto da classe cli HGU AsleyBRCM

def getInfoHgu(pwd, ip_addr):
    dados_hgu = {
        'ip_addr': '',
        'modelo': '',
        'firmware': '',
        'regiao': '',
        'connect_ip': '',
        'connect_ssh': '',
        'macAddress': '',
        'serialNumber': '',
        'vendor': '',
        'status_info_hgu': '',
        'message': '',
        'Result': '',
        'Exception': ''
    }

    print('\n\nSTEP-00: INITIALIZING FUNCTION (getInfoHgu) --> ' + str(datetime.now()))
    time_start = datetime.now()

    tag_pwd = ''

    ##--> Iniciando script para captura das infomrações do HGU
    dados_hgu['status_info_hgu'] = 'OK'

    ##--> Inciando processo de validação de conectividade
    try:
        ##-->Leitura do IP do Hgu
        # ip_addr = dados_input['ip_hgu']
        if ip_addr == '':
            ip_addr = '192.168.15.1'
        dados_hgu['ip_addr'] = ip_addr

        ##-->Leitura da senha do Hgu
        # pwd = dados_input['pwd_hgu']
        if pwd == '':
            tag_pwd = 'NOK'
        else:
            tag_pwd = 'OK'

        ##-->Testes conectividade IP
        print('STEP-01: CHECKING IP CONNECTIVITY TOWARD HGU! --> ' + str(datetime.now()))

        conect = {
                'Resultado': 'OK'
            }
        if conect['Resultado'] == 'OK':
            dados_hgu['connect_ip'] = 'OK'

            ##--> Inciando processo de conexão via SSh
            print('STEP-02: TRYNG TO CONNECT TO HGU BY SSH :| --> ' + str(datetime.now()))
            channel = connectSSHE(ip_addr, 'support', pwd)
            prompt = [' > ', '>', '~ # ', '> ', '# ']

            ##--> Processo de indentificação do modelo e firmware para validar suporte a ferramenta
            if channel['status'] == 'OK':
                print('STEP-03: CONNECTED TO HGU VERIFYING MODEL AND FW SUPPORTED :) --> ' + str(datetime.now()))
                ssh = channel['ssh']
                interact = channel['connection']
                interact.expect(prompt)

                dados_hgu['connect_ssh'] = 'OK'

                hgu_ssh = cliHgu(pwd, ip_addr)

                cmd = 'show device_model'
                interact.send(cmd)
                interact.expect(prompt)
                query = interact.current_output
                ans = hgu_ssh.device_model(query)

                if ans['Result'] == 'OK':
                    dados_hgu['modelo'] = ans['model']
                    dut_model = ans['model']
                    dados_hgu['regiao'] = ans['region']

                    # Deletar objeto para consulta do modelo do dispositivo
                    del hgu_ssh

                    ##-->Leitura do arquivo de parametros dsos firmwares e modelos suportados
                    info = getDefaultParams()

                    ##--> File com informações dos modelos e firmware suportados
                    supported_devices = info['devices']['supported']['general']

                    ##--> Info devices Askey Brcm
                    askey_brcm_model = info['devices']['supported']['askey_brcm_model']
                    askey_bcrm_fw = info['devices']['supported']['askey_bcrm_fw']

                    ##--> Info devices Mitra Ecnt
                    mitra_ecnt_model = info['devices']['supported']['mitra_ecnt_model']
                    mitra_ecnt_fw = info['devices']['supported']['mitra_ecnt_fw']

                    ##--> Info devices Askey Ecnt
                    askey_ecnt_model = info['devices']['supported']['askey_ecnt_model']
                    askey_ecnt_fw = info['devices']['supported']['askey_ecnt_fw']

                    ##--> Info devices Mitra Brcm
                    mitra_brcm_model = info['devices']['supported']['mitra_brcm_model']
                    mitra_brcm_fw = info['devices']['supported']['mitra_brcm_fw']

                    print('STEP-04: CHECKIN GENERAL INFORMATIONS ABOUT THE HGU')
                    if dut_model in supported_devices:

                        ##--> ANALISE ASKEY BRCM
                        if dut_model in askey_brcm_model:
                            try:
                                ###Verificação de informações do HGU
                                hgu = cliAskeyBrcm(pwd, ip_addr)

                                cmd = 'version'
                                interact.send(cmd)
                                interact.expect(prompt)
                                query = interact.current_output
                                device_info = hgu.version(query)
                                dados_hgu['firmware'] = device_info['firmware']

                                dut_fmw = device_info['firmware']

                                ###Configuração de syslog na caixa que impacta comando :(!!
                                print('STEP-05: DISABLE SYSLOG HGU ASKEY BRCM  :|')

                                cmd = 'mdm setpv InternetGatewayDevice.X_VIVO_COM_BR.Debug.SyslogLocal.Enable 0'
                                interact.send(cmd)
                                interact.expect(prompt)

                                cmd = 'save'
                                interact.send(cmd)
                                interact.expect(prompt)

                                ###Verificar versão de firmware do HGU BRCM!!
                                print('STEP-06: VERIFICANDO SERIAL DO HGU ASKEY BRCM  :|')

                                cmd = 'show serial'
                                interact.send(cmd)
                                interact.expect(prompt)
                                query = interact.current_output
                                ans = hgu.getSerial(query)
                                dados_hgu['serialNumber'] = ans['serial']

                                print('STEP-07: VERIFICANDO DEMAIS INFO DO HGU ASKEY BRCM  :|')
                                dados_hgu['vendor'] = 'Askey'

                                try:
                                    dados_hgu['macAddress'] = macToSerial(ans['serial'])
                                except:
                                    pass

                                if dut_fmw in askey_bcrm_fw:
                                    dados_hgu['suporte_magic'] = 'OK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'
                                    dados_hgu['message'] = 'ready_to_test'
                                else:
                                    dados_hgu['status_info_hgu'] = 'NOK'
                                    dados_hgu['suporte_magic'] = 'NOK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'
                                    dados_hgu['message'] = 'error_06'

                                ##--> Validar testes suportados
                                dados_hgu['supported_tests']['sua_conexao'] = \
                                    info['devices']['tests']['askey_brcm']['sua_conexao']
                                dados_hgu['supported_tests']['wan'] = info['devices']['tests']['askey_brcm'][
                                    'wan']
                                dados_hgu['supported_tests']['lan'] = info['devices']['tests']['askey_brcm'][
                                    'lan']
                                dados_hgu['supported_tests']['topologia'] = \
                                    info['devices']['tests']['askey_brcm']['topologia']
                                dados_hgu['supported_tests']['mapa_cobertura'] = \
                                    info['devices']['tests']['askey_brcm']['mapa_cobertura']
                                dados_hgu['supported_tests']['voip'] = info['devices']['tests']['askey_brcm'][
                                    'voip']
                                dados_hgu['supported_tests']['iptv'] = info['devices']['tests']['askey_brcm'][
                                    'iptv']
                                dados_hgu['supported_tests']['jiga'] = info['devices']['tests']['askey_brcm'][
                                    'jiga']
                                dados_hgu['supported_tests']['iot'] = info['devices']['tests']['askey_brcm'][
                                    'iot']
                            except:
                                dados_hgu['status_info_hgu'] = 'NOK'
                                dados_hgu['message'] = 'error_07'
                                dados_hgu['Result'] = 'OK'
                                dados_hgu['Exception'] = 'OK'

                        ##--> ANALISE MITRA ECNT
                        elif dut_model in mitra_ecnt_model:
                            try:
                                ###Verificação de informações do HGU
                                hgu = cliMitraEcnt(pwd, ip_addr)

                                cmd = 'sys atsh'
                                interact.send(cmd)
                                interact.expect(prompt)
                                query = interact.current_output
                                device_info = hgu.version(query)

                                dados_hgu['firmware'] = device_info['firmware']
                                dut_fmw = device_info['firmware']

                                ##Definição de serialNumber
                                dados_hgu['serialNumber'] = device_info['serialNumber']

                                ##Definição de macAddress
                                dados_hgu['macAddress'] = device_info['macAddress']

                                ##--> ProductClass
                                dados_hgu['productClass'] = device_info['Model']

                                ##--> Vendor
                                dados_hgu['vendor'] = device_info['vendor']

                                ##--> Definição de região
                                dut_region_aux = device_info['Model']
                                dut_region_aux = dut_region_aux.split('-')
                                if len(dut_region_aux) > 2:
                                    dut_region = dut_region_aux[2]
                                    dados_hgu['regiao'] = dut_region
                                else:
                                    dados_hgu['regiao'] = 'N1'


                                ##--> Validação de firmware suportado
                                if dut_fmw in mitra_ecnt_fw:
                                    dados_hgu['suporte_magic'] = 'OK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'
                                    dados_hgu['message'] = 'ready_to_test'
                                else:
                                    dados_hgu['status_info_hgu'] = 'NOK'
                                    dados_hgu['message'] = 'error_06'
                                    dados_hgu['suporte_magic'] = 'NOK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'

                                ##--> Validar testes suportados
                                dados_hgu['supported_tests']['sua_conexao'] = \
                                    info['devices']['tests']['mitra_ecnt']['sua_conexao']
                                dados_hgu['supported_tests']['wan'] = info['devices']['tests']['mitra_ecnt'][
                                    'wan']
                                dados_hgu['supported_tests']['lan'] = info['devices']['tests']['mitra_ecnt'][
                                    'lan']
                                dados_hgu['supported_tests']['topologia'] = \
                                    info['devices']['tests']['mitra_ecnt']['topologia']
                                dados_hgu['supported_tests']['mapa_cobertura'] = \
                                    info['devices']['tests']['mitra_ecnt']['mapa_cobertura']
                                dados_hgu['supported_tests']['voip'] = info['devices']['tests']['mitra_ecnt'][
                                    'voip']
                                dados_hgu['supported_tests']['iptv'] = info['devices']['tests']['mitra_ecnt'][
                                    'iptv']
                                dados_hgu['supported_tests']['jiga'] = info['devices']['tests']['mitra_ecnt'][
                                    'jiga']
                                dados_hgu['supported_tests']['iot'] = info['devices']['tests']['mitra_ecnt'][
                                    'iot']
                            except:
                                dados_hgu['status_info_hgu'] = 'NOK'
                                dados_hgu['message'] = 'error_07'
                                dados_hgu['Result'] = 'OK'
                                dados_hgu['Exception'] = 'OK'

                        ##--> ANALISE ASKEY ECNT
                        elif dut_model in askey_ecnt_model:
                            try:
                                ###Verificação de informações do HGU
                                hgu = cliAskeyEcnt(pwd, ip_addr)

                                prompt_shell = '~ # '
                                cmd = 'sh'
                                interact.send(cmd)
                                interact.expect(prompt_shell)
                                query = interact.current_output

                                cmd = 'aspcm_util show_module_info'
                                interact.send(cmd)
                                interact.expect(prompt_shell)
                                query = interact.current_output
                                device_info = hgu.version(query)

                                dados_hgu['firmware'] = device_info['firmware']
                                dut_fmw = device_info['firmware']

                                ##Definição de serialNumber
                                dados_hgu['serialNumber'] = device_info['serialNumber']

                                ##Definição de macAddress
                                dados_hgu['macAddress'] = device_info['macAddress']

                                ##--> ProductClass
                                dados_hgu['productClass'] = device_info['Model']

                                ##--> Vendor
                                dados_hgu['vendor'] = device_info['vendor']

                                ##--> Definição de região
                                cmd = 'bootenv_util show'
                                interact.send(cmd)
                                interact.expect(prompt_shell)
                                query = interact.current_output
                                region_info = hgu.getRegion(query)

                                dados_hgu['regiao'] = region_info['region']

                                ##--> Validar testes suportados
                                dados_hgu['supported_tests']['sua_conexao'] = \
                                    info['devices']['tests']['askey_ecnt']['sua_conexao']
                                dados_hgu['supported_tests']['wan'] = \
                                    info['devices']['tests']['askey_ecnt']['wan']
                                dados_hgu['supported_tests']['lan'] = \
                                    info['devices']['tests']['askey_ecnt']['lan']
                                dados_hgu['supported_tests']['topologia'] = \
                                    info['devices']['tests']['askey_ecnt']['topologia']
                                dados_hgu['supported_tests']['mapa_cobertura'] = \
                                    info['devices']['tests']['askey_ecnt']['mapa_cobertura']
                                dados_hgu['supported_tests']['voip'] = \
                                    info['devices']['tests']['askey_ecnt']['voip']
                                dados_hgu['supported_tests']['iptv'] = \
                                    info['devices']['tests']['askey_ecnt']['iptv']
                                dados_hgu['supported_tests']['jiga'] = \
                                    info['devices']['tests']['askey_ecnt']['jiga']
                                dados_hgu['supported_tests']['iot'] = \
                                    info['devices']['tests']['askey_ecnt']['iot']

                                ##--> Validação de firmware suportado
                                if dut_fmw in askey_ecnt_fw:
                                    dados_hgu['suporte_magic'] = 'OK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'
                                    dados_hgu['message'] = 'ready_to_test'

                                else:
                                    dados_hgu['status_info_hgu'] = 'NOK'
                                    dados_hgu['message'] = 'error_06'
                                    dados_hgu['suporte_magic'] = 'NOK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'
                            except:
                                dados_hgu['status_info_hgu'] = 'NOK'
                                dados_hgu['message'] = 'error_07'
                                dados_hgu['Result'] = 'OK'
                                dados_hgu['Exception'] = 'OK'

                        ##--> ANALISE MITRA BRCM
                        elif dut_model in mitra_brcm_model:
                            try:
                                ###Verificação de informações do HGU
                                hgu = cliMitraBrcm(pwd, ip_addr)

                                cmd = 'sys atsh'
                                interact.send(cmd)
                                interact.expect(prompt)
                                query = interact.current_output
                                device_info = hgu.version(query)
                                print(device_info)
                                dados_hgu['firmware'] = device_info['firmware']
                                dut_fmw = device_info['firmware']

                                ##Definição de serialNumber
                                dados_hgu['serialNumber'] = device_info['serialNumber']

                                ##Definição de macAddress
                                dados_hgu['macAddress'] = device_info['macAddress']
                                device_info['macAddress'] = device_info['macAddress']

                                ##--> ProductClass
                                dados_hgu['productClass'] = device_info['Model']

                                ##--> Vendor
                                dados_hgu['vendor'] = device_info['vendor']

                                ##--> Definição de região
                                dut_region_aux = device_info['Model']
                                dut_region_aux = dut_region_aux.split('-')

                                if len(dut_region_aux) > 2:
                                    dut_region = dut_region_aux[2]
                                    dados_hgu['regiao'] = dut_region
                                else:
                                    dados_hgu['regiao'] = 'N1'


                                ##--> Validação de firmware suportado
                                if dut_fmw in mitra_brcm_fw:
                                    dados_hgu['suporte_magic'] = 'OK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'
                                    dados_hgu['message'] = 'info_hgu_ok'

                                else:
                                    dados_hgu['status_info_hgu'] = 'NOK'
                                    dados_hgu['message'] = 'Firmware não suportado pelo Magic'
                                    dados_hgu['suporte_magic'] = 'NOK'
                                    dados_hgu['Result'] = 'OK'
                                    dados_hgu['Exception'] = 'OK'
                            except:
                                dados_hgu['status_info_hgu'] = 'NOK'
                                dados_hgu['message'] = 'Erro ao coletar info do firmware do HGU'
                                dados_hgu['Result'] = 'OK'
                                dados_hgu['Exception'] = 'OK'

                    else:
                        dados_hgu['status_info_hgu'] = 'NOK'
                        dados_hgu['message'] = 'Modelo não suportado pelo Magic'
                        dados_hgu['suporte_magic'] = 'NOK'
                        dados_hgu['Result'] = 'OK'
                        dados_hgu['Exception'] = 'OK'

                else:
                    dados_hgu['status_info_hgu'] = 'NOK'
                    dados_hgu['message'] = 'Erro ao coletar info HGU, SSH estabelecido'
                    dados_hgu['Result'] = 'NOK'
                    dados_hgu['Exception'] = 'NOK'

            else:
                if channel['exception'] == 'VERIFIQUE SENHA INSERIDA':
                    dados_hgu['message'] = 'Erro SSH, verifique a senha inserida'

                elif channel['exception'] == 'VERIFIQUE CABO DESCONETADO':
                    dados_hgu['message'] = 'Erro SSH, verifique conectividade com o HGU'
                else:
                    dados_hgu['message'] = 'Erro ao estabelecer conexão SSH com o HGU'

                dados_hgu['status_info_hgu'] = 'NOK'
                dados_hgu['Result'] = 'OK'
                dados_hgu['Exception'] = 'OK'

        else:
            dados_hgu['status_info_hgu'] = 'NOK'
            dados_hgu['connect_ip'] = 'NOK'
            dados_hgu['Result'] = 'OK'
            dados_hgu['Exception'] = 'OK'
            dados_hgu['message'] = 'Erro conectividade IP'

        time_end = datetime.now()
        delta = time_end - time_start
        print('STEP-EXECUTION_TIME (getInfoHgu):' + str(delta))

    except Exception as error:
        dados_hgu['status_info_hgu'] = 'NOK'
        dados_hgu['message'] = 'Houve um exceção ao tentar acessar o HGU'
        dados_hgu['Result'] = 'NOK'
        dados_hgu['Exception'] = str(error)

    finally:
        try:
            print('STEP-08: CLOSING SSH SESSION (getInfoHgu) --> ' + str(datetime.now()))
            print(dados_hgu)
            ssh.close()
            del hgu
            print('STEP-09: CLOSED SSH SESSION (getInfoHgu) --> ' + str(datetime.now()))
            print('STEP-10: END OF FUNCTION (getInfoHgu) --> ' + str(datetime.now()))
            print('\n\n')
        except:
            pass

    return dados_hgu