import paramiko
from HGUmodels.models.SSHutils.services.general import sumHex, eh_ip, eh_macaddr, ProcuraVal
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException
from paramiko_expect import SSHClientInteraction
import socket
import time
import re
import json


class cliAskeyBrcm():

    def __init__(self, password, ip):
        self.user_support = 'support'
        self.password = password
        self.ip = ip


    ####Verificar Serial#######
    def getSerial(self, out_str):
        # Entrada: show serial
        ###STEP-00: JSON SAIDA
        device_serial = {
            'serial': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                if key.startswith('serial'):
                    list = key.split()
                    device_serial['serial'] = list[1]

        except Exception as error:
            device_serial['Result'] = 'NOK'
            device_serial['Exception'] = error

        return device_serial


    ######Listar dispositivos na tabela DHCP######
    def dhcp_table(self, out_str, fmw = ''):

        # Entrada: 'show map_info dhcp_table'

        raw_list = out_str.splitlines()

        qtde_eth = int(0)
        count_eth = int(0)
        qtde_4 = int(0)
        count_wifi24 = int(0)
        qtde_5 = int(0)
        count_wifi5 = int(0)
        count_bp_ap = int(0)
        count_bp_rep = int(0)
        count_hosts = int(0)

        tabela_host = {"qtde_hosts": "",
                       "qtde_eth": qtde_eth,
                       "qtde_wifi24": qtde_4,
                       "qtde_wifi5": qtde_5,
                       "interface": {},
                       "bp":{
                           'repeater': {},
                           'ap': {},
                       },
                       "Result": '',
                       "Exception": ''}
        pass_fmw = 'OK'

        try:

            # if fmw in ['S35', 'BR_SV_g000_R3505VWN1001_s35', 'BR_SV_g000_R3507VWN1001_s35', 'BR_SV_g000_R3505VWN1001_s36', 'BR_SV_g000_R3507VWN1001_s36']:
            if pass_fmw == 'OK':
                for key in raw_list:
                    list_tab = key.split('\t')
                    list_spa = key.split()

                    if len(list_spa) > 4:
                        if 'WiFi' in list_spa:
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ####CONTABILIZAR SE DEVICES EM 2.4GHz & 5GHz
                            tabela_host["interface"][count_iface]["radio"] = list_spa[5]
                            if list_spa[5] == '5':
                                count_wifi5 = count_wifi5 + 1
                            else:
                                count_wifi24 = count_wifi24 + 1

                            ###TRATAMENTO DE HOSTNAME E SSID PARA DIFERENTES SAIDAS

                            ###SOMENTE SSID SEM HOSTNAME (LEN 6)
                            if len(list_tab) == 6:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]

                            ###SSID & HOSTNAME (LEN 7)
                            elif len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÃO DA TABELA DE BPs NO MODO REPEATER
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_rep = count_bp_rep + 1
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['ipaddr'] = list_tab[0]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['macaddr'] = list_tab[1]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['dhcp_mode'] = list_tab[2]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['leasetime'] = list_tab[3]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['media'] = list_spa[4]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['hostname'] = list_tab[6]

                        elif 'Ethernet' in list_spa:
                            count_bp_ap = 0
                            count_eth = count_eth + 1
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ###TRATAMENTO DE HOSTNAME PARA DIFERENTES SAIDAS
                            if len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÂO DA TABELA DE BPs NO MODO AP
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_ap = count_bp_ap + 1
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }

                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['ipaddr'] = list_tab[0]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['macaddr'] = list_tab[1]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['dhcp_mode'] = list_tab[2]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['leasetime'] = list_tab[3]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['media'] = list_spa[4]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['hostname'] = list_tab[6]

                tabela_host['qtde_hosts'] = str(count_hosts)
                tabela_host['qtde_eth'] = str(count_eth)
                tabela_host['qtde_wifi24'] = str(count_wifi24)
                tabela_host['qtde_wifi5'] = str(count_wifi5)

                tabela_host['Result'] = 'OK'
                tabela_host['Exception'] = 'OK'

            elif fmw in ['S32_7', 'BR_SV_g000_R3507VWN1001_s35']:
                for key in raw_list:
                    list_tab = key.split('\t')
                    list_spa = key.split()

                    if len(list_spa) > 4:
                        if 'WiFi' in list_spa:
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ####CONTABILIZAR SE DEVICES EM 2.4GHz & 5GHz
                            tabela_host["interface"][count_iface]["radio"] = list_spa[5]
                            if list_spa[5] == '5':
                                count_wifi5 = count_wifi5 + 1
                            else:
                                count_wifi24 = count_wifi24 + 1

                            ###TRATAMENTO DE HOSTNAME E SSID PARA DIFERENTES SAIDAS

                            ###SOMENTE SSID SEM HOSTNAME (LEN 6)
                            if len(list_tab) == 6:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]

                            ###SSID & HOSTNAME (LEN 7)
                            elif len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÃO DA TABELA DE BPs NO MODO REPEATER
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_rep = count_bp_rep + 1
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['ipaddr'] = list_tab[0]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['macaddr'] = list_tab[1]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['dhcp_mode'] = list_tab[2]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['leasetime'] = list_tab[3]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['media'] = list_spa[4]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['hostname'] = list_tab[6]

                        elif 'Ethernet' in list_spa:
                            count_eth = count_eth + 1
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ###TRATAMENTO DE HOSTNAME PARA DIFERENTES SAIDAS
                            if len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÃO DA TABELA DE BPs NO MODO AP
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_ap = count_bp_ap + 1
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }

                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['ipaddr'] = list_tab[0]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['macaddr'] = list_tab[1]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['dhcp_mode'] = list_tab[2]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['leasetime'] = list_tab[3]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['media'] = list_spa[4]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['hostname'] = list_tab[6]

                tabela_host['qtde_hosts'] = str(count_hosts)
                tabela_host['qtde_eth'] = str(count_eth)
                tabela_host['qtde_wifi24'] = str(count_wifi24)
                tabela_host['qtde_wifi5'] = str(count_wifi5)

                tabela_host['Result'] = 'OK'
                tabela_host['Exception'] = 'OK'

        except Exception as error:
            tabela_host['Result'] = 'NOK'
            tabela_host['Exception'] = 'ERRO GERAÇÃO TABELA HOST ASKEY BRCM'

        return tabela_host


    ######Listar domínios e bssids criados######
    def roaming_bss(self, out_str, model='', firmware='', dhcp_table = {}):


        ####LISTA DE OUI DOS BASES PORTS EM PLANTA
        oui_bp_mitra = ['a4:33:d7', 'cc:ed:dc', 'd8:c6:78', '34:57:60', 'cc:d4:a1', '84:aa:9c']
        oui_bp_askey = ['94:91:7f', '1c:b0:44', '80:78:71']

        raw_list = out_str.splitlines()

        table_bssid = {"qty_domain": "",
                       "qty_baseport": "",
                       "qty_bssid_total": "",
                       "ssid-0000": '',
                       "ssid-aaaa": '',
                       "qty_bssid_2.4GHz": "",
                       "qty_bssid_5GHz": "",
                       "hgu": {
                           "fat_5G": "",
                           "fat_2G": ""
                       },
                       "base_port": {},
                       "bssid/domain":
                           {"BS": {},
                            'MAIN': {}
                            },
                       "bssids": {},
                       "Result": '',
                       "Exception": ''}

        try:

            pass_fmw = 'OK'

            # if firmware in ['S35', 'BR_SV_g000_R3505VWN1001_s35', 'BR_SV_g000_R3507VWN1001_s35', 'BR_SV_g000_R3505VWN1001_s36', 'BR_SV_g000_R3507VWN1001_s36', '']:
            if pass_fmw == 'OK':
                qty_bp = int(0)
                qty_domain = int(0)
                qty_bssid_total = int(0)
                qty_bssid_24 = int(0)
                qty_bssid_5 = int(0)

                count_bp = 0

                tag_domain_BS = False
                tag_domain_5 = False
                tag_domain_guest = False

                count_bssid_24 = 0
                count_bssid_5 = 0
                count_bssid_guest = 0

                count_domain_24 = 0
                count_domain_5_bs = 0
                count_domain_5_main = 0

                aux_basePort = {}
                mac_ref_table = []

                for key in raw_list:
                    list = key.split()
                    if len(list) > 5 and list[0].startswith('00'):
                        # print(list[1])
                        # index = list[0].strip('.')
                        index = list[1]
                        table_bssid["bssids"][index] = {"bssid": "",
                                                        "status": "",
                                                        "local": "",
                                                        "radio": "",
                                                        "channel": "",
                                                        "bandwidth": "",
                                                        "BSSTr": "",
                                                        "fat": "",
                                                        "domain": "",
                                                        "vendor": "",
                                                        "network": ""}

                        if list[3] == 'Yes':  # Indice 3 identifica o device a qual esta conectado o shell
                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['local'] = 'HGU'
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]
                            table_bssid["bssids"][index]['index_mac'] = 'HGU'

                            if list[10] == '0000' and list[4] == '2.4G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                table_bssid['ssid-0000'] = list[12]
                                table_bssid['hgu']['fat_2G'] = list[8]
                            elif list[10] == '0000' and list[4] == '5G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                            elif list[10] == 'aaaa':
                                table_bssid['bssids'][index]['network'] = 'Main_5G'
                                table_bssid['ssid-aaaa'] = list[12]
                                table_bssid['hgu']['fat_5G'] = list[8]
                            else:
                                table_bssid['bssids'][index]['network'] = 'Guest'


                        elif list[3] == 'No' and list[2] == 'UP':
                            mac_ref = list[9]

                            if mac_ref not in mac_ref_table:
                                count_bp = count_bp + 1
                                aux_basePort[mac_ref] = 'BP-' + str(count_bp)
                                table_bssid["bssids"][index]['local'] = "BP-" + str(count_bp)
                                mac_ref_table.append(mac_ref)

                                # -->Nova feature para identificação do MAC do BP
                                if list[10] != '':
                                    name_bp = 'BP-' + str(count_bp)
                                    mac_bp = mac_ref
                                    table_bssid['base_port'][name_bp] = mac_ref

                            else:
                                table_bssid["bssids"][index]['local'] = aux_basePort[mac_ref]

                            ####VALIDAR MODELO BP
                            oui = list[9][:8]

                            ###VALIDAR SE BP ASKEY
                            if oui in oui_bp_askey:  # Identificar modelo de base port Askey
                                table_bssid["bssids"][index]['vendor'] = "ASKEY"
                                if list[10].strip() == '0000' and list[4].strip() == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'


                            ###VALIDAR SE BP MITRA
                            elif oui in oui_bp_mitra:  # Identificar modelo de base port Mitra
                                table_bssid["bssids"][index]['vendor'] = "MITRA"
                                if list[10] == '0000' and list[4] == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'

                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]
                            table_bssid["bssids"][index]['index_mac'] = mac_ref

                        ###Verificar quantidade de Dominios

                        if list[10] == '0000' and list[2] == 'UP':
                            tag_domain_BS = True
                            if int(list[5]) < 14:
                                count_bssid_24 = count_bssid_24 + 1
                                count_domain_24 = count_domain_24 + 1
                            else:
                                count_bssid_5 = count_bssid_5 + 1
                                count_domain_5_bs = count_domain_5_bs + 1

                        elif list[10] == 'aaaa' and list[2] == 'UP':
                            tag_domain_5 = True
                            count_bssid_5 = count_bssid_5 + 1
                            count_domain_5_main = count_domain_5_main + 1

                        elif (list[10] != '0000' or list[10] != 'aaaa') and list[2] == 'UP':
                            tag_domain_guest = True
                            count_bssid_guest = count_bssid_guest + 1

                qty_bp = len(mac_ref_table)

                ###VERIFICAR QUANTIDADE DE DOMINIOS

                if tag_domain_BS and tag_domain_5 and tag_domain_guest:
                    table_bssid["qty_domain"] = str(3)
                elif tag_domain_BS and tag_domain_5 and tag_domain_guest == False:
                    table_bssid["qty_domain"] = str(2)

                table_bssid["qty_baseport"] = str(qty_bp)
                table_bssid['bssid/domain']['BS']['2_4GHz'] = str(count_domain_24)
                table_bssid['bssid/domain']['BS']['5GHz'] = str(count_domain_5_bs)
                table_bssid['bssid/domain']['MAIN']['5GHz'] = str(count_domain_5_main)
                table_bssid["qty_bssid_2.4GHz"] = str(count_domain_24)
                table_bssid["qty_bssid_5GHz"] = str(count_domain_5_bs + count_domain_5_main)
                table_bssid["qty_bssid_total"] = str(count_domain_5_bs + count_domain_5_main + count_domain_24)

                table_bssid['Result'] = 'OK'
                table_bssid['Exception'] = 'OK'

            elif firmware in ['S32_7']:

                list_bp = []
                count_bp = int(0)
                domain_5G = []
                domain_bp_5G = []
                domain_bp_2G = []
                list_domain = []
                domain_inv = []
                tag_main = int(0)
                tag_bs = int(0)
                tag_inv = int(0)
                mac_ref_table = []
                mac_hgu_table = []

                table_bssid = {"qty_domain": "",
                               "qty_baseport": "",
                               "qty_bssid_total": "",
                               "ssid-0000": '',
                               "ssid-aaaa": '',
                               "qty_bssid_2.4GHz": "",
                               "qty_bssid_5GHz": "",
                               "bssid/domain":
                                   {"BS": {},
                                    'MAIN': {}
                                    },
                               "bssids": {},
                               "Result": '',
                               "Exception": ''}


                ## STEP:0 IDENTIFICANDO O HGU

                for bp in dhcp_table['bp']:
                    for key in dhcp_table['bp'][bp]:
                        if bp == 'repeater':
                            # mac_bp = sumHex(dhcp_table['bp'][bp][key]['macaddr'], 1)
                            mac_bp = dhcp_table['bp'][bp][key]['macaddr']
                            list_bp.append(mac_bp.lower())
                        else:
                            mac_bp = dhcp_table['bp'][bp][key]['macaddr']
                            list_bp.append(mac_bp.lower())

                # STEP:0.1 LISTA DE BSSID
                for key in raw_list:
                    if key.startswith('bss'):
                        list = key.split(',')
                        for i in list:
                            list_bss = i.split()
                            list_domain.append(list_bss)
                            if list_bss[1] not in list_bp and list_bss[2] == 'aaaa':
                                bssid5_main = list_bss[1]
                                mac_hgu_table.append(bssid5_main)

                # STEP:0.1 IDENTIFICANDO REDE 2.5GHz BS
                bssid2_bs = sumHex(bssid5_main, -13)
                mac_hgu_table.append(bssid2_bs)

                # STEP:0.1 IDENTIFICANDO REDE 5 BS
                ref5G = bssid5_main.split(':')
                bssid5_bs = '06:' + ref5G[1] + ':' + ref5G[2] + ':' + ref5G[3] + ':' + ref5G[4] + ':' + ref5G[5]
                mac_hgu_table.append(bssid5_bs)

                for key in list_domain:
                    if key[1] in mac_hgu_table:
                        table_bssid['bssids'][key[1]] = {}
                        table_bssid['bssids'][key[1]]['bssid'] = key[1]
                        table_bssid['bssids'][key[1]]['status'] = 'UP'
                        table_bssid['bssids'][key[1]]['local'] = 'HGU'
                        table_bssid['bssids'][key[1]]['BSSTr'] = 'Yes'
                        table_bssid['bssids'][key[1]]['radio'] = key[3]
                        table_bssid['bssids'][key[1]]['domain'] = key[2]

                        if key[2] == 'aaaa':
                            table_bssid['bssids'][key[1]]['network'] = 'Main_5G'
                            table_bssid['bssids'][key[1]]['fat'] = '910'
                            table_bssid['bssids'][key[1]]['bandwidth'] = '20|40|80'

                        elif key[2] == '0000' and key[3] == '5G':
                            table_bssid['bssids'][key[1]]['network'] = 'BandSteering_5G'
                            table_bssid['bssids'][key[1]]['fat'] = '910'
                            table_bssid['bssids'][key[1]]['bandwidth'] = '20|40|80'

                        elif key[2] == '0000' and key[3] == '2.4G':
                            table_bssid['bssids'][key[1]]['network'] = 'BandSteering_2G'
                            table_bssid['bssids'][key[1]]['fat'] = '600'
                            table_bssid['bssids'][key[1]]['bandwidth'] = '20'

                    elif key[1] in list_bp:

                        ####VALIDAR MODELO BP
                        oui = key[1][:8]

                        if oui in oui_bp_askey:
                            count_bp = count_bp + 1
                            table_bssid['bssids'][key[1]] = {}
                            table_bssid['bssids'][key[1]]['bssid'] = key[1]
                            table_bssid["bssids"][key[1]]['local'] = "BP-" + str(count_bp)
                            table_bssid["bssids"][key[1]]['vendor'] = 'ASKEY'
                            table_bssid["bssids"][key[1]]['domain'] = 'aaaa'
                            table_bssid["bssids"][key[1]]['network'] = 'Main_5G'
                            table_bssid["bssids"][key[1]]['fat'] = '910'
                            table_bssid['bssids'][key[1]]['bandwidth'] = '20|40|80'
                            table_bssid['bssids'][key[1]]['radio'] = key[3]

                            bssid5_main = key[1]

                            ###BS_5G
                            ref5G = bssid5_main.split(':')
                            bssid5_bs = '86:' + ref5G[1] + ':' + ref5G[2] + ':' + ref5G[3] + ':' + ref5G[4] + ':' + \
                                        ref5G[5]
                            table_bssid['bssids'][bssid5_bs] = {}
                            table_bssid['bssids'][bssid5_bs]['bssid'] = bssid5_bs
                            table_bssid["bssids"][bssid5_bs]['vendor'] = 'ASKEY'
                            table_bssid["bssids"][bssid5_bs]['local'] = "BP-" + str(count_bp)
                            table_bssid["bssids"][bssid5_bs]['domain'] = '0000'
                            table_bssid["bssids"][bssid5_bs]['network'] = 'BandSteering_5G'
                            table_bssid["bssids"][bssid5_bs]['fat'] = '910'
                            table_bssid['bssids'][bssid5_bs]['bandwidth'] = '20|40|80'
                            table_bssid['bssids'][bssid5_bs]['radio'] = '5G'

                            ###BS_2.4G
                            ref_5G = sumHex(bssid5_main, 1)
                            ref_5G = ref_5G.split(':')
                            bssid2_bs = '96:' + ref_5G[1] + ':' + ref_5G[2] + ':' + ref_5G[3] + ':' + ref_5G[4] + ':' + \
                                        ref_5G[5]
                            table_bssid['bssids'][bssid2_bs] = {}
                            table_bssid['bssids'][bssid2_bs]['bssid'] = bssid2_bs
                            table_bssid["bssids"][bssid2_bs]['vendor'] = 'ASKEY'
                            table_bssid["bssids"][bssid2_bs]['local'] = "BP-" + str(count_bp)
                            table_bssid["bssids"][bssid2_bs]['domain'] = '0000'
                            table_bssid["bssids"][bssid2_bs]['network'] = 'BandSteering_2G'
                            table_bssid["bssids"][bssid2_bs]['fat'] = '600'
                            table_bssid['bssids'][bssid2_bs]['bandwidth'] = '20'
                            table_bssid['bssids'][bssid2_bs]['radio'] = '2.4G'

                        elif oui in oui_bp_mitra:
                            count_bp = count_bp + 1
                            table_bssid['bssids'][key[1]] = {}
                            table_bssid['bssids'][key[1]]['bssid'] = key[1]
                            table_bssid["bssids"][key[1]]['local'] = "BP-" + str(count_bp)
                            table_bssid["bssids"][key[1]]['vendor'] = 'MITRA'
                            table_bssid["bssids"][key[1]]['domain'] = 'aaaa'
                            table_bssid["bssids"][key[1]]['network'] = 'Main_5G'
                            table_bssid["bssids"][key[1]]['fat'] = '910'
                            table_bssid['bssids'][key[1]]['bandwidth'] = '20|40|80'
                            table_bssid['bssids'][key[1]]['radio'] = key[3]

                            bssid5_main = key[1]

                            ###BS_5G
                            ref5G = bssid5_main.split(':')
                            bssid5_bs = '06:' + ref5G[1] + ':' + ref5G[2] + ':' + ref5G[3] + ':' + ref5G[4] + ':' + \
                                        ref5G[5]
                            table_bssid['bssids'][bssid5_bs] = {}
                            table_bssid['bssids'][bssid5_bs]['bssid'] = bssid5_bs
                            table_bssid["bssids"][bssid5_bs]['vendor'] = 'MITRA'
                            table_bssid["bssids"][bssid5_bs]['local'] = "BP-" + str(count_bp)
                            table_bssid["bssids"][bssid5_bs]['domain'] = '0000'
                            table_bssid["bssids"][bssid5_bs]['network'] = 'BandSteering_5G'
                            table_bssid["bssids"][bssid5_bs]['fat'] = '910'
                            table_bssid['bssids'][bssid5_bs]['bandwidth'] = '20|40|80'
                            table_bssid['bssids'][bssid5_bs]['radio'] = '5G'

                            ###BS_2.4G
                            ref_5G = sumHex(bssid5_main, 1)
                            ref_5G = ref_5G.split(':')
                            bssid2_bs = '06:' + ref_5G[1] + ':' + ref_5G[2] + ':' + ref_5G[3] + ':' + ref_5G[4] + ':' + \
                                        ref_5G[5]
                            table_bssid['bssids'][bssid2_bs] = {}
                            table_bssid['bssids'][bssid2_bs]['bssid'] = bssid2_bs
                            table_bssid["bssids"][bssid2_bs]['vendor'] = 'MITRA'
                            table_bssid["bssids"][bssid2_bs]['local'] = "BP-" + str(count_bp)
                            table_bssid["bssids"][bssid2_bs]['domain'] = '0000'
                            table_bssid["bssids"][bssid2_bs]['network'] = 'BandSteering_2G'
                            table_bssid["bssids"][bssid2_bs]['fat'] = '600'
                            table_bssid['bssids'][bssid2_bs]['bandwidth'] = '20'
                            table_bssid['bssids'][bssid2_bs]['radio'] = '2.4G'

                table_bssid['qty_baseport'] = str(len(list_bp))

                table_bssid['Result'] = 'OK'
                table_bssid['Exception'] = 'OK'

        except Exception as error:

            table_bssid['Result'] = 'NOK'
            table_bssid['Exception'] = 'ERRO NA GERACAO DA TABELA_BSSID: ', error

        return table_bssid


    ######Listar detalhes das estacoes conectadas nos bssids WiFi######
    def roaming_assoc(self, out_str, model, firmware):

        raw_list = out_str.splitlines()
        count_host = int(0)

        table_sta_assoc = {}

        pass_fmw = 'OK'

        try:

            # if firmware in ['S35', 'BR_SV_g000_R3505VWN1001_s35', 'BR_SV_g000_R3507VWN1001_s35', 'BR_SV_g000_R3505VWN1001_s36', 'BR_SV_g000_R3507VWN1001_s36']:

            if pass_fmw == 'OK':
                #####RX and TX is about the HGU, instance rssi_rx is the power seen by the HGU sent by the station
                if model in ('RTF3507VW-N1', 'RTF3507VW-N2'):
                    for key in raw_list:
                        if key != '':
                            list = key.split()
                            if len(list[0]) > 1 and list[0].startswith('00'):
                                count_host = count_host + 1
                                index = list[0].strip('.')
                                table_sta_assoc[list[1]] = {
                                    "radio": "",
                                    "ss": "",
                                    "bw": "",
                                    "phyrate": "",
                                    "bsstr": "",
                                    "bssid": "",
                                    "domain": "",
                                    "rssi_rx": "",
                                    "max_phyrate_tx": "",
                                    "avg_phyrate_tx": "",
                                    "avg_phyrate_rx": "",
                                }
                                table_sta_assoc[list[1]]["radio"] = list[2]
                                table_sta_assoc[list[1]]["ss"] = list[3]
                                table_sta_assoc[list[1]]["bw"] = list[4]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                table_sta_assoc[list[1]]["bsstr"] = list[6]
                                table_sta_assoc[list[1]]["bssid"] = list[7]
                                table_sta_assoc[list[1]]["domain"] = list[8]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                phyrate = list[11].split('/')
                                tx = phyrate[0]
                                rx = phyrate[1]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = rx
                            else:
                                table_sta_assoc['qty_hosts'] = str(count_host)
                    table_sta_assoc['qty_hosts'] = str(count_host)
                    table_sta_assoc['Result'] = 'OK'
                    table_sta_assoc['Exception'] = 'OK'

                elif model in ('RTF3505VW-N1', 'RTF3505VW-N2'):
                    for key in raw_list:
                        list = key.split()
                        if len(list) > 5 and not list[0].startswith('Aiee'):
                            count_host = count_host + 1
                            index = list[0].strip('.')
                            table_sta_assoc[list[1]] = {
                                "radio": "",
                                "ss": "",
                                "bw": "",
                                "max_phyrate_hw": "",
                                "bsstr": "",
                                "bssid": "",
                                "domain": "",
                                "rssi_rx": "",
                                "max_phyrate_current": "",
                                "avg_phyrate_tx": "",
                                "avg_phyrate_rx": "",
                            }

                            table_sta_assoc[list[1]]["radio"] = list[2]
                            table_sta_assoc[list[1]]["ss"] = list[3]
                            table_sta_assoc[list[1]]["bw"] = list[4]
                            table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                            table_sta_assoc[list[1]]["bsstr"] = list[6]
                            table_sta_assoc[list[1]]["bssid"] = list[7]
                            table_sta_assoc[list[1]]["domain"] = list[8]
                            table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                            table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                            phyrate = list[11].split('/')
                            tx = phyrate[0]
                            rx = phyrate[1]
                            table_sta_assoc[list[1]]["avg_phyrate_tx"] = tx
                            table_sta_assoc[list[1]]["avg_phyrate_rx"] = rx

                        else:
                            table_sta_assoc['qty_hosts'] = str(count_host)

                    table_sta_assoc['qty_hosts'] = str(count_host)
                    table_sta_assoc['Result'] = 'OK'
                    table_sta_assoc['Exception'] = 'OK'

                else:
                    table_sta_assoc['qty_hosts'] = str(count_host)
                    table_sta_assoc['Result'] = 'NOK'
                    table_sta_assoc['Exception'] = 'MODELO NAO ENCONTRADO'

            elif firmware in ['S32_7']:
                if model in ('RTF3507VW-N1', 'RTF3507VW-N2'):
                    for key in raw_list:
                        if key.startswith('00'):
                            count_host = count_host + 1
                            list = key.split()
                            table_sta_assoc[list[1]] = {
                                "radio": "",
                                "ss": "",
                                "bw": "",
                                "max_phyrate_hw": "",
                                "bsstr": "",
                                "bssid": "",
                                "domain": "",
                                "rssi_rx": "",
                                "max_phyrate_current": "",
                                "avg_phyrate_tx": "",
                                "avg_phyrate_rx": "",
                            }

                            if len(list) > 13:
                                table_sta_assoc[list[1]]['radio'] = '2G|5G'
                                table_sta_assoc[list[1]]['ss'] = list[4]
                                table_sta_assoc[list[1]]["bw"] = list[5]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[6]
                                table_sta_assoc[list[1]]["bsstr"] = list[7]
                                table_sta_assoc[list[1]]["bssid"] = list[8]
                                table_sta_assoc[list[1]]["domain"] = list[9]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[10]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[11]
                                phyrate = list[12].split('/')
                                tx = phyrate[0]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[13]
                            else:
                                table_sta_assoc[list[1]]['radio'] = list[2]
                                table_sta_assoc[list[1]]['ss'] = list[3]
                                table_sta_assoc[list[1]]["bw"] = list[4]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                table_sta_assoc[list[1]]["bsstr"] = list[6]
                                table_sta_assoc[list[1]]["bssid"] = list[7]
                                table_sta_assoc[list[1]]["domain"] = list[8]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                phyrate = list[11].split('/')
                                tx = phyrate[0]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                        else:
                            table_sta_assoc['qty_hosts'] = str(count_host)

                    table_sta_assoc['qty_hosts'] = str(count_host)
                    table_sta_assoc['Result'] = 'OK'
                    table_sta_assoc['Exception'] = 'OK'

                elif model in ('RTF3505VW-N1', 'RTF3505VW-N2'):
                    for key in raw_list:
                        if key.startswith('00'):
                            count_host = count_host + 1
                            list = key.split()
                            table_sta_assoc[list[1]] = {
                                "radio": "",
                                "ss": "",
                                "bw": "",
                                "max_phyrate_hw": "",
                                "bsstr": "",
                                "bssid": "",
                                "domain": "",
                                "rssi_rx": "",
                                "max_phyrate_current": "",
                                "avg_phyrate_tx": "",
                                "avg_phyrate_rx": "",
                            }

                            if len(list) > 13:
                                table_sta_assoc[list[1]]['radio'] = '2G|5G'
                                table_sta_assoc[list[1]]['ss'] = list[4]
                                table_sta_assoc[list[1]]["bw"] = list[5]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[6]
                                table_sta_assoc[list[1]]["bsstr"] = list[7]
                                table_sta_assoc[list[1]]["bssid"] = list[8]
                                table_sta_assoc[list[1]]["domain"] = list[9]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[10]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[11]
                                phyrate = list[12].split('/')
                                tx = phyrate[0]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[13]
                            else:
                                table_sta_assoc[list[1]]['radio'] = list[2]
                                table_sta_assoc[list[1]]['ss'] = list[3]
                                table_sta_assoc[list[1]]["bw"] = list[4]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                table_sta_assoc[list[1]]["bsstr"] = list[6]
                                table_sta_assoc[list[1]]["bssid"] = list[7]
                                table_sta_assoc[list[1]]["domain"] = list[8]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                phyrate = list[11].split('/')
                                tx = phyrate[0]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                        else:
                            table_sta_assoc['qty_hosts'] = str(count_host)

                    table_sta_assoc['qty_hosts'] = str(count_host)
                    table_sta_assoc['Result'] = 'OK'
                    table_sta_assoc['Exception'] = 'OK'

                else:
                    table_sta_assoc['qty_hosts'] = str(count_host)
                    table_sta_assoc['Result'] = 'NOK'
                    table_sta_assoc['Exception'] = 'MODELO NAO ENCONTRADO'

            return table_sta_assoc

        except Exception as error:
            table_sta_assoc['Result'] = 'NOK'
            table_sta_assoc['Exception'] = 'ERRO GERAÇÃO TABELA DE ASSOC WIFI: ' + error

            return table_sta_assoc


    ######Listar detalhes do dipositivo######
    def version(self, out_str):

        ###Entrada: >version

        raw_list = out_str.splitlines()

        info_hgu = {'Model': '',
                    'Profile': '',
                    'Booted Partition': '',
                    'Partition 1 Version': '',
                    'Partition 2 Version': '',
                    'firmware': '',
                    'brcm_release': '',
                    'Result': 'NOK',
                    'Exception': ''}
        try:
            for key in raw_list:
                list = key.split(':')
                for step_01 in list:
                    if step_01 == 'RTF Model':
                        info_hgu['Model'] = 'RTF' + list[1].strip()

                    elif step_01 == 'RTF Profile':
                        info_hgu['Profile'] = list[1].strip()

                    elif step_01 == 'Booted Partition':
                        info_hgu['Booted Partition'] = list[1].strip()

                    elif step_01 == 'Partition 1 Version':
                        info_hgu['Partition 1 Version'] = list[1].strip()

                    elif step_01 == 'Partition 2 Version':
                        info_hgu['Partition 2 Version'] = list[1].strip()

                    elif step_01 == 'auxfs version':
                        info_hgu['firmware'] = list[1].strip()

                    elif step_01 == 'BRCM Release Version':
                        info_hgu['brcm_release'] = list[1].strip()

                info_hgu['Result'] = 'OK'
                info_hgu['Exception'] = 'OK'

        except Exception as error:
            info_hgu['Result'] = 'NOK'
            info_hgu['Exception'] = error

        return info_hgu


    ######Listar serial do dispositivos######
    def serial(self, out_str):

        ###Entrada: >show serial
        raw_list = out_str.splitlines()
        # print(raw_list)

        serial_hgu = {
            'Result': '',
            'Exception': ''
        }

        try:
            for key in raw_list:
                list = key.split()

                if list[0] == 'serial':
                    serial_hgu['serial'] = list[1]

            serial_hgu['Result'] = 'OK'
            serial_hgu['Exception'] = 'OK'

        except Exception as error:
            serial_hgu['Result'] = 'NOK'
            serial_hgu['Exception'] = 'ERRO AO GERAR SERIAL', error

        return serial_hgu


    ######Listar informações de NTP######
    def getNtpStatus(self, out_str):

        ###Entrada: >mdm getpv InternetGatewayDevice.Time.Status

        ntp_status = {
            'status': '',
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0].startswith('Param'):
                        status_ntp = list[1].split('=')
                        status_ntp = status_ntp[1]
                        ntp_status['status'] = status_ntp

            ntp_status['Result'] = 'OK'
            ntp_status['Exception'] = 'OK'

            return ntp_status

        except Exception as error:
            ntp_status['Result'] = 'NOK'
            ntp_status['Exception'] = error

            return ntp_status


    ######Listar informações de NTP######
    def getNtpServer1(self, out_str):

        ###Entrada: >mdm getpv InternetGatewayDevice.Time.NTPServer1

        ntp_server = {
            'server1': '',
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0].startswith('Param'):
                        status_ntp = list[1].split('=')
                        status_ntp = status_ntp[1]
                        ntp_server['server1'] = status_ntp

            ntp_server['Result'] = 'OK'
            ntp_server['Exception'] = 'OK'

            return ntp_server

        except Exception as error:
            ntp_server['Result'] = 'NOK'
            ntp_server['Exception'] = error

            return ntp_server


    ######Listar informações de NTP######
    def getNtpServer2(self, out_str):

        ###Entrada: >mdm getpv InternetGatewayDevice.Time.NTPServer1

        ntp_server = {
            'server2': '',
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0].startswith('Param'):
                        status_ntp = list[1].split('=')
                        status_ntp = status_ntp[1]
                        ntp_server['server2'] = status_ntp

            ntp_server['Result'] = 'OK'
            ntp_server['Exception'] = 'OK'

            return ntp_server

        except Exception as error:
            ntp_server['Result'] = 'NOK'
            ntp_server['Exception'] = error

            return ntp_server


    ######Listar informações de NTP######
    def getNtpServer3(self, out_str):

        ###Entrada: >mdm getpv InternetGatewayDevice.Time.NTPServer1

        ntp_server = {
            'server3': '',
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0].startswith('Param'):
                        server_ntp = list[1].split('=')
                        server_ntp =  server_ntp[1]
                        ntp_server['server3'] = server_ntp

            ntp_server['Result'] = 'OK'
            ntp_server['Exception'] = 'OK'

            return ntp_server

        except Exception as error:
            ntp_server['Result'] = 'NOK'
            ntp_server['Exception'] = error

            return ntp_server


    ######Listar informações de NTP######
    def getNtpServer4(self, out_str):

        ###Entrada: >mdm getpv InternetGatewayDevice.Time.NTPServer1

        ntp_server = {
            'server4': '',
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0].startswith('Param'):
                        server_ntp = list[1].split('=')
                        server_ntp = server_ntp[1]
                        ntp_server['server4'] = server_ntp

            ntp_server['Result'] = 'OK'
            ntp_server['Exception'] = 'OK'

            return ntp_server

        except Exception as error:
            ntp_server['Result'] = 'NOK'
            ntp_server['Exception'] = error

            return ntp_server


    ######Listar informações de NTP######
    def getNtpLocalTime(self, out_str):

        ###Entrada: >mdm getpv InternetGatewayDevice.Time.CurrentLocalTime

        ntp_local_time = {
            'local_time': '',
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0].startswith('Param'):
                        ntp_local = list[1].split('=')
                        ntp_local = ntp_local[1]
                        ntp_local_time['local_time'] = str(ntp_local)

            ntp_local_time['Result'] = 'OK'
            ntp_local_time['Exception'] = 'OK'

            return ntp_local_time

        except Exception as error:
            ntp_local_time['Result'] = 'NOK'
            ntp_local_time['Exception'] = error

            return ntp_local_time


    ######Listar informacoes WiFi 2.4GHz######
    def getWiFi2G(self, out_str):

        ###Entrada: >show wifi all

        raw_list = out_str.splitlines()

        del raw_list[0]
        infoWiFi2G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': ''
        },
            'Result': '',
            'Exception': ''}

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[1].startswith('bandwidth'):
                        infoWiFi2G['info']['bandwidth'] = list[2]
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi2G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi2G['info']['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi2G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        if len(list) == 3:
                            infoWiFi2G['info']['ssid'] = list[2]
                        else:
                            len_default = 3
                            plus_size = (len(list) - len_default) + 1
                            index = 2
                            ssid_name = ''
                            for i in range(plus_size):
                                index = index + i
                                if ssid_name != '':
                                    ssid_name = ssid_name + ' ' + list[index]
                                else:
                                    ssid_name = ssid_name + list[index]
                                index = 2

                            infoWiFi2G['info']['ssid'] = ssid_name

                    elif list[1].startswith('bssid'):
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi2G['info']['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi2G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi2G['info']['password'] = list[2]
                    elif list[1].startswith('channel_mode'):
                        infoWiFi2G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi2G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi2G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi2G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi2G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi2G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi2G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi2G['info']['region'] = list[2]
                    ###TRATAMETNO DO CANAL 2.4GHz
                    elif list[1].startswith('channel') and len(list) == 3:
                        infoWiFi2G['info']['channel'] = list[2]


            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = 'error'

            return infoWiFi2G


    ######Listar informacoes WiFi 5GHz######
    def getWiFi5G(self, out_str):

        ###Entrada: >show wifi_plus all
        ###Necessário tempo maior para retorno do SSH

        raw_list = out_str.splitlines()

        del raw_list[0]

        infoWiFi5G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': '',
            'qhop': '',
            'beamforming': '',
            'scs': '',
            'airfair': '',
            'maui': '',
            'mumimo': '',
            'wifi_plus0_status': '',
            'roaming': ''

        },
            'Result': '',
            'Exception': ''}

        infoWiFi5GMobile = {
            'bandwidth': '',
            'status': '',
            'ssid': '',
            'authentication': '',
            'channel': '',
            'scs': '',
            'roaming': '',
            'result': '',
            'exception': ''
        }

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[1].startswith('bandwidth'):
                        infoWiFi5G['info']['bandwidth'] = list[2]
                        infoWiFi5GMobile['bandwidth'] = list[2]
                        # print(list[2])
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi5G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi5G['info']['status'] = list[2]
                        infoWiFi5GMobile['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi5G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        if len(list) == 3:
                            infoWiFi5G['info']['ssid'] = list[2]
                            infoWiFi5GMobile['ssid'] = list[2]
                        else:
                            len_default = 3
                            plus_size = (len(list) - len_default) + 1
                            index = 2
                            ssid_name = ''
                            for i in range(plus_size):
                                index = index + i
                                if ssid_name != '':
                                    ssid_name = ssid_name + ' ' + list[index]
                                else:
                                    ssid_name = ssid_name + list[index]
                                index = 2

                            infoWiFi5G['info']['ssid'] = ssid_name
                            infoWiFi5GMobile['ssid'] = ssid_name

                    elif list[1].startswith('bssid'):
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi5G['info']['authentication'] = list[2]
                        infoWiFi5GMobile['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi5G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi5G['info']['password'] = list[2]
                    elif list[1].startswith('channel'):
                        infoWiFi5G['info']['channel'] = list[2]
                        infoWiFi5GMobile['channel'] = list[2]
                    elif list[1].startswith('mode'):
                        infoWiFi5G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi5G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi5G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi5G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi5G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi5G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi5G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi5G['info']['region'] = list[2]

                    elif list[1].startswith('qhop') and len(list) == 3:
                        if infoWiFi5G['info']['qhop'] == '':
                            infoWiFi5G['info']['qhop'] = list[2]
                    elif list[1].startswith('beamforming'):
                        infoWiFi5G['info']['beamforming'] = list[2]
                    elif list[1].startswith('scs'):
                        infoWiFi5G['info']['scs'] = list[2]
                        infoWiFi5GMobile['scs'] = list[2]
                    elif list[1].startswith('airfair'):
                        infoWiFi5G['info']['airfair'] = list[2]
                    elif list[1].startswith('maui'):
                        infoWiFi5G['info']['maui'] = list[2]
                    elif list[1].startswith('mumimo'):
                        infoWiFi5G['info']['mumimo'] = list[2]
                    elif list[0].startswith('wifi_plus0_status'):
                        infoWiFi5G['info']['wifi_plus0_status'] = list[1]
                    elif list[1].startswith('roaming'):
                        # print(list[1])
                        infoWiFi5G['info']['roaming'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            infoWiFi5GMobile['message'] = 'ok'
            infoWiFi5GMobile['result'] = 'ok'
            infoWiFi5GMobile['exception'] = 'ok'

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = str(error)
            infoWiFi5GMobile['message'] = 'nok'
            infoWiFi5GMobile['result'] = 'nok'
            infoWiFi5GMobile['exception'] = str(error)

        return infoWiFi5G


    ######Listar informacoes IP_Internet######
    def getIpWan(self, out_str):

        ###Entrada: >wan show

        raw_list = out_str.splitlines()

        del raw_list[0]
        del raw_list[0]
        del raw_list[0]
        del raw_list[0]

        infoIpInet = {
            'iface': {},
            'Result': '',
            'Exception': ''
        }

        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 10:
                    infoIpInet['iface'][list[1]] = {
                        'service_name': '',
                        'iface_name': '',
                        'protocol': '',
                        'pbit': '',
                        'vlan': '',
                        'igmp': '',
                        'status_v4': '',
                        'ipv4': '',
                        'uptime': '',
                        'status_v6': '',
                        'ipv6': ''
                    }

                    infoIpInet['iface'][list[1]]['service_name'] = list[1]
                    infoIpInet['iface'][list[1]]['iface_name'] = list[2]
                    infoIpInet['iface'][list[1]]['protocol'] = list[3]
                    infoIpInet['iface'][list[1]]['pbit'] = list[4]
                    infoIpInet['iface'][list[1]]['vlan'] = list[5]
                    infoIpInet['iface'][list[1]]['igmp'] = list[6]
                    infoIpInet['iface'][list[1]]['status_v4'] = list[10]
                    infoIpInet['iface'][list[1]]['ipv4'] = list[11]
                    infoIpInet['iface'][list[1]]['uptime'] = list[12]

                elif len(list) > 5 and not list[0].startswith('tCon.'):
                    infoIpInet['iface'][list[1]]['ipv6'] = list[5]
                    infoIpInet['iface'][list[1]]['status_v6'] = list[4]

            infoIpInet['Result'] = 'OK'
            infoIpInet['Exception'] = 'OK'

            return infoIpInet

        except Exception as error:
            infoIpInet['Result'] = 'NOK'
            infoIpInet['Exception'] = error

            return infoIpInet


    ######Listar informacoes Opticas HGU######
    def getOpticalInfo(self, out_str):

        ###Entrada: >show ont optics

        raw_list = out_str.splitlines()

        del raw_list[0]
        del raw_list[0]

        infoGpon = {'info':
                        {'vendor': '',
                        'model': '',
                        'type': '',
                        'class': '',
                        'ont_rx': '',
                        'ont_tx': ''},
                    'Result': '',
                    'Exception': ''
        }

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 0:
                    if list[0].startswith('ont_transceiver_vendor'):
                        infoGpon['info']['vendor'] = list[1]
                    elif list[0].startswith('ont_transceiver_model'):
                        infoGpon['info']['model'] = list[1]
                    elif list[0].startswith('ont_transceiver_type'):
                        infoGpon['info']['type'] = list[1]
                    elif list[0].startswith('ont_transceiver_class'):
                        infoGpon['info']['class'] = list[2]
                    elif list[0].startswith('ont_rx_power'):
                        infoGpon['info']['ont_rx'] = list[1]
                    elif list[0].startswith('ont_tx_power'):
                        infoGpon['info']['ont_tx'] = list[1]

            infoGpon['Result'] = 'OK'
            infoGpon['Exception'] = 'OK'

            return infoGpon

        except Exception as error:
            infoGpon['Result'] = 'NOK'
            infoGpon['Exception'] = error

            return infoGpon



                ###### Listar DNS IPv4 HGU ######


    ######Listar informacoes das rotas do HGU######
    def getRoutes(self, out_str):

        ###Entrada: >route show

        raw_list = out_str.splitlines()

        del raw_list[0]
        del raw_list[0]
        del raw_list[0]
        del raw_list[0]

        count_route_inet = 0
        count_route_voip = 0
        count_route_vod = 0
        count_route_lan = 0

        infoRoute = {'qty_routes_inet': '',
                     'qty_routes_voip': '',
                     'qty_routes_vod': '',
                     'qty_routes_lan': '',
                     'info': {},
                     'Result': '',
                     'Exception': ''
                    }

        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 3:
                    if re.match\
                            (r'(^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$)', list[0]) \
                            or list[0] == 'default':
                        index = list[7]
                        if index == 'br0':
                            count_route_lan = count_route_lan + 1
                            infoRoute['info'][index + '-' + str(count_route_lan)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_lan)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['iface'] = list[5]

                        elif index == 'ppp0.1':
                            count_route_inet = count_route_inet + 1
                            infoRoute['info'][index + '-' + str(count_route_inet)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_inet)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['iface'] = list[5]

                        elif index == 'veip0.2':
                            count_route_vod = count_route_vod + 1
                            infoRoute['info'][index + '-' + str(count_route_vod)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_vod)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['iface'] = list[5]


                        elif index == 'veip0.3':
                            count_route_voip = count_route_voip + 1
                            infoRoute['info'][index + '-' + str(count_route_voip)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_voip)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['iface'] = list[5]

            infoRoute['qty_routes_inet'] = str(count_route_inet)
            infoRoute['qty_routes_voip'] = str(count_route_voip)
            infoRoute['qty_routes_vod'] = str(count_route_vod)
            infoRoute['qty_routes_lan'] = str(count_route_lan)
            infoRoute['Result'] = 'OK'
            infoRoute['Exception'] = 'OK'

            return infoRoute

        except Exception as error:
            infoRoute['Result'] = 'NOK'
            infoRoute['Exception'] = error

            return infoRoute

            ###### Listar DNS IPv4 HGU ######


    ######Listar DNS IPv4 HGU######
    def getDnsIpv4Hgu(self, output_str):

        #Entrada: mdm getpv InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.DNSServers

        resultado = {'DNS_IPv4': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            c = 0
            aux = []
            for i in ans:
                # print('linha #' + str(c) + '  ' + i)
                if i.startswith('Param'):
                # if c == 1:
                #     print(i)
                    aux = i.replace('=', ';')
                    aux = aux.split(';')
                    aux = aux[1]
                    aux = aux.split(',')
                c = c + 1
            # print(aux)
            resultado['DNS_IPv4'] = aux
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ###### Listar DNS IPv6 HGU ######
    def getDnsIpv6Hgu(self, output_str):

        #mdm getpv InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.X_TELEFONICA-ES_IPv6DNSServers
        resultado = {'DNS_IPv6': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            c = 0
            for i in ans:
                # print('linha #' + str(c) + '  ' + i)
                if c == 1:
                    # print(i)
                    aux = i.replace('=', ';')
                    aux = aux.split(';')
                    aux = aux[1]
                    aux = aux.split(',')
                c = c + 1
            # print(aux)
            resultado['DNS_IPv6'] = aux
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ###### Listar DHCP SETTINGS HGU ######
    def getDhcpSettingsHgu(self, output_str):

        #Entrada: dhcpserver show

        resultado = {'LAN': {
            'DHCP Server': '',
            'IP Inicio': '',
            'IP Final': '',
            'DNS Server': '',
            'Lease Time': '',
            'Gateway': '',
            'Option 42': '',
            'WAN VoIP Options': {
                'WAN Interface': '',
                'Option 42': ''
            },
            'AlternativeRange-NAT/PATLines': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': '',
                'Option 42': '',
            },
            'AlternativeRange-NAT/PATLines - 2': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': ''
            },

        },
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            c = 0
            aux = []
            for i in ans:
                aux1 = re.sub(' +', '', i)
                # print('linha #' + str(c) + '  ' + aux1)
                aux1 = aux1.split(':')
                # print(aux1)
                aux.append(aux1)
                c = c + 1
            # print(aux)
            for j in aux[1:9]:
                # print(j)
                if j[0].startswith('dhcpserver'):
                    resultado['LAN']['DHCP Server'] = j[1]
                elif j[0].startswith('StartIPAddress'):
                    resultado['LAN']['IP Inicio'] = j[1]
                elif j[0].startswith('EndIPAddress'):
                    resultado['LAN']['IP Final'] = j[1]
                elif j[0].startswith('DNSServers'):
                    resultado['LAN']['DNS Server'] = j[1]
                elif j[0].startswith('LeaseTime'):
                    resultado['LAN']['Lease Time'] = j[1]
                elif j[0].startswith('Router'):
                    resultado['LAN']['Gateway'] = j[1]
                elif j[0].startswith('Option42'):
                    resultado['LAN']['Option 42'] = j[1]
            for j in aux[10:13]:
                # print(j)
                if j[0].startswith('WANinterfacename'):
                    resultado['LAN']['WAN VoIP Options']['WAN Interface'] = j[1]
                elif j[0].startswith('option42'):
                    resultado['LAN']['WAN VoIP Options']['Option 42'] = j[1]
            for j in aux[16:26]:
                # print(j)
                if j[0].startswith('StartIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Inicio'] = j[1]
                elif j[0].startswith('EndIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Final'] = j[1]
                elif j[0].startswith('DNSServers'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['DNS Servers'] = j[1]
                elif j[0].startswith('IPRouter'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['Gateway'] = j[1]
                elif j[0].startswith('VendorClassID'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['Vendor ClassID'] = j[1]
                elif j[0].startswith('UserClassID'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['User ClassID'] = j[1]
                elif j[0].startswith('LeaseTime'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['Lease Time'] = j[1]
                elif j[0].startswith('Option42'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['Option 42'] = j[1]
            for j in aux[29:36]:
                # print(j)
                if j[0].startswith('StartIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Inicio'] = j[1]
                elif j[0].startswith('EndIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Final'] = j[1]
                elif j[0].startswith('DNSServers'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['DNS Servers'] = j[1]
                elif j[0].startswith('IPRouter'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Gateway'] = j[1]
                elif j[0].startswith('VendorClassID'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Vendor ClassID'] = j[1]
                elif j[0].startswith('UserClassID'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['User ClassID'] = j[1]
                elif j[0].startswith('LeaseTime'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Lease Time'] = j[1]

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            # print(resultado)
            return resultado

        except AuthenticationException:
            return {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'Authentication failed'}

        except socket.timeout:
            return {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'Timeout de conexão'}

        except SSHException as sshException:
            return {'connection': 'channel_NOK', 'status': 'NOK', 'exception':
                'Unable to establish SSH connection'}


    ######Listar interfaces ETH utilizadas######
    def listEthIfaces(self, out_str):
        #Entrada: show map_info eth1_device information

        try:

            connect_lan = {'iface': '', 'ip_addr': 'not_connected', 'mac_addr': 'not_connected', 'Result': '',
                           'Exception': ''}

            raw_list = out_str.splitlines()

            for key in raw_list:
                sew = key.split()
                if sew[0].startswith('eth'):
                    iface = sew[0]
                    iface = iface.split('_')
                    iface = iface[0]
                    connect_lan['iface'] = iface
                elif not (sew[0].startswith('show') | sew[0].startswith('>') | \
                          sew[0].startswith('eth' + str(int) + '_device')):
                    if len(sew) > 1:
                        ip_addr = sew[0]
                        mac_addr = sew[1]
                    connect_lan['ip_addr'] = ip_addr
                    connect_lan['mac_addr'] = mac_addr

            connect_lan['Result'] = 'OK'
            connect_lan['Exception'] = 'OK'

            return connect_lan

        except Exception as error:
            connect_lan['Result'] = 'NOK'
            connect_lan['Exception'] = 'ERRO AO LISTAR INTERFACES LAN DO HGU: ', error

            return connect_lan


    ######Listar interfaces ETH utilizadas######
    def listEthIfaces2(self, out_str):

        #Entrada: show map_info eth1_device information

        try:

            connect_lan = {'iface': '',
                           'status': '',
                           'Result': '',
                           'Exception': ''
            }

            raw_list = out_str.splitlines()
            # print(raw_list)

            for key in raw_list:
                print(key)
                if key.startswith(' > ethctl'):
                    # print('key ====== ' + str(key))
                    sew = key.split()
                    print(sew)
                    connect_lan['iface'] = sew[2]
                # if sew[0].startswith('eth'):
                #     iface = sew[0]
                #     iface = iface.split(' ')
                #     iface = iface[2]
                #     connect_lan['iface'] = iface
                elif key.startswith('ethctl'):
                    sew = key.split()
                    print(sew)
                    connect_lan['iface'] = sew[1]
                elif key.startswith('Link'):
                    if key.endswith('up'):
                        connect_lan['status'] = 'up'
                    else:
                        connect_lan['status'] = 'down'
                # elif not (sew[0].startswith('show') | sew[0].startswith('>') | \
                #           sew[0].startswith('eth' + str(int) + '_device')):
                #     if len(sew) > 1:
                #         ip_addr = sew[0]
                #         mac_addr = sew[1]
                #     connect_lan['ip_addr'] = ip_addr
                #     connect_lan['mac_addr'] = mac_addr

            connect_lan['Result'] = 'OK'
            connect_lan['Exception'] = 'OK'
            # print('PASSOU AQUIIIIIIIIIIIII')
            # print(connect_lan)

            return connect_lan

        except Exception as error:
            connect_lan['Result'] = 'NOK'
            connect_lan['Exception'] = 'ERRO AO LISTAR INTERFACES LAN DO HGU: ', error

            return connect_lan


    ######Listar infor VoIP######
    def getInfoVoIP(self, out_str):

        ###Entrada: > voice show

        voipInfo = {
            'info': {
                'Voice_Profile': {
                    'ifName': '',
                    'ipAddr': '',
                    'ipVersion': '',
                    'manageProtocol': '',
                    'voiceProfile': '',
                    'profileState': '',
                    'local': '',
                    'dtmfMethod': '',
                    'hookFlashMethod': '',
                    'T38': '',
                    'V18': '',
                    'rtpDscpMark': '',
                    'rtpPortMin': '',
                    'rtpPortMax': '',
                    'sip': '',
                    'domain': '',
                    'port': '',
                    'transport': '',
                    'regExpires': '',
                    'regRetriveInterval': '',
                    'dscpMark': '',
                    'addrRegister': '',
                    'portRegister': '',
                    'addrProxy': '',
                    'portProxy': '',
                    'option120Addr': '',
                    'outboundProxyAddr': '',
                    'outboundProxyPort': '',
                    'uriConference': '',
                    'optionConference': ''
                },
                'Account':{
                'lineEnableState': '',
                'voipServiceStatus': '',
                'reverserPolarity': '',
                'callStatus': '',
                'physicalReference': '',
                'uri': '',
                'number': '',
                'authName': '',
                'authPwd': '',
                'txGain': '',
                'rxGain': '',
                'echoCancellation': '',
                'callWaiting': ''
                },
                'Codec': {
                    'codec-1': '',
                    'codec-2': '',
                    'codec-3': ''
                }
            },
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        del raw_list[0]
        del raw_list[0]
        del raw_list[0]
        del raw_list[0]

        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:

                    ###INFORMAÇÕES VOICE PROFILE
                    if list[0].startswith('BoundIfName'):
                        voipInfo['info']['Voice_Profile']['ifName'] = list[2]
                    elif list[0].startswith('BoundIPAddr'):
                        voipInfo['info']['Voice_Profile']['ipAddr'] = list[2]
                    elif list[0].startswith('IP'):
                        voipInfo['info']['Voice_Profile']['ipVersion'] = list[4]
                    elif list[0].startswith('Management'):
                        voipInfo['info']['Voice_Profile']['manageProtocol'] = list[3]
                    elif list[0].startswith('Associated'):
                        voipInfo['info']['Voice_Profile']['voiceProfile'] = list[3]
                    elif list[0].startswith('ProfileEnableState'):
                        voipInfo['info']['Voice_Profile']['profileState'] = list[2]
                    elif list[0].startswith('Locale'):
                        voipInfo['info']['Voice_Profile']['local'] = list[2]
                    elif list[0].startswith('DTMFMethod'):
                        voipInfo['info']['Voice_Profile']['dtmfMethod'] = list[2]
                    elif list[0].startswith('HookFlashMethod'):
                        voipInfo['info']['Voice_Profile']['hookFlashMethod'] = list[2]
                    elif list[0].startswith('T38'):
                        voipInfo['info']['Voice_Profile']['T38'] = list[2]
                    elif list[0].startswith('V18'):
                        voipInfo['info']['Voice_Profile']['V18'] = list[2]
                    elif list[0].startswith('RTPDSCPMark'):
                        voipInfo['info']['Voice_Profile']['rtpDscpMark'] = list[2]
                    elif list[0].startswith('RTPPortMin'):
                        voipInfo['info']['Voice_Profile']['rtpPortMin'] = list[2]
                    elif list[0].startswith('RTPPortMax'):
                        voipInfo['info']['Voice_Profile']['rtpPortMax'] = list[2]
                    elif list[0].startswith('Domain'):
                        voipInfo['info']['Voice_Profile']['domain'] = list[2]
                    elif list[0].startswith('Port'):
                        voipInfo['info']['Voice_Profile']['port'] = list[2]
                    elif list[0].startswith('Transport'):
                        voipInfo['info']['Voice_Profile']['transport'] = list[2]
                    elif list[0].startswith('RegExpires'):
                        voipInfo['info']['Voice_Profile']['regExpires'] = list[2]
                    elif list[0].startswith('RegRetryInterval'):
                        voipInfo['info']['Voice_Profile']['regRetriveInterval'] = list[2]
                    elif list[0].startswith('DSCPMark'):
                        voipInfo['info']['Voice_Profile']['dscpMark'] = list[2]
                    elif list[0].startswith('Registrar') and list[1].startswith('Addr'):
                        voipInfo['info']['Voice_Profile']['addrRegister'] = list[3]
                    elif list[0].startswith('Registrar') and list[1].startswith('Port'):
                        voipInfo['info']['Voice_Profile']['portRegister'] = list[3]
                    elif list[0].startswith('Proxy') and list[1].startswith('Addr'):
                        voipInfo['info']['Voice_Profile']['addrProxy'] = list[3]
                    elif list[0].startswith('Proxy') and list[1].startswith('Port'):
                        voipInfo['info']['Voice_Profile']['portProxy'] = list[3]
                    elif list[0].startswith('OutBoundProxy') and list[1].startswith('Addr'):
                        voipInfo['info']['Voice_Profile']['outboundProxyAddr'] = list[3]
                    elif list[0].startswith('OutBoundProxy') and list[1].startswith('Port'):
                        voipInfo['info']['Voice_Profile']['outboundProxyPort'] = list[3]
                    elif list[0].startswith('Conferencing') and list[1].startswith('URI'):
                        voipInfo['info']['Voice_Profile']['uriConference'] = list[3]
                    elif list[0].startswith('Conferencing') and list[1].startswith('Option'):
                        voipInfo['info']['Voice_Profile']['optionConference'] = list[3]

                    ###INFORMAÇÕES LINHA SIP
                    elif list[0].startswith('LineEnableState'):
                        voipInfo['info']['Account']['lineEnableState'] = list[2]
                    elif list[0].startswith('VoipServiceStatus'):
                        voipInfo['info']['Account']['voipServiceStatus'] = list[2]
                    elif list[0].startswith('PolarityReverseState'):
                        voipInfo['info']['Account']['reverserPolarity'] = list[2]
                    elif list[0].startswith('CallStatus'):
                        voipInfo['info']['Account']['callStatus'] = list[2]
                    elif list[0].startswith('Associated'):
                        voipInfo['info']['Account']['physicalReference'] = list[3]
                    elif list[0].startswith('URI'):
                        voipInfo['info']['Account']['uri'] = list[2]
                    elif list[0].startswith('TelNumber'):
                        voipInfo['info']['Account']['number'] = list[2]
                    elif list[0].startswith('AuthName'):
                        voipInfo['info']['Account']['authName'] = list[2]
                    elif list[0].startswith('AuthPwd'):
                        voipInfo['info']['Account']['authPwd'] = list[2]
                    elif list[0].startswith('TxGain'):
                        voipInfo['info']['Account']['txGain'] = list[2]
                    elif list[0].startswith('RxGain'):
                        voipInfo['info']['Account']['rxGain'] = list[2]
                    elif list[0].startswith('EchoCancellation'):
                        voipInfo['info']['Account']['echoCancellation'] = list[2]
                    elif list[0].startswith('CallWaiting'):
                        voipInfo['info']['Account']['callWaiting'] = list[2]

                    ###INFORMAÇÕES DSO CODECS
                    elif list[0].startswith('CodecList'):
                        voipInfo['info']['Codec']['codec-1'] = list[3]
                    elif list[0].startswith('(1)'):
                        voipInfo['info']['Codec']['codec-2'] = list[1]
                    elif list[0].startswith('(2)'):
                        voipInfo['info']['Codec']['codec-3'] = list[1]


            ###INFORMAÇÕES REDE GPON
            voipInfo['info']['Network'] = 'Vivo_1'



            voipInfo['Result'] = 'OK'
            voipInfo['Exception'] = 'OK'

            return voipInfo

        except Exception as error:
            voipInfo['Result'] = 'NOK'
            voipInfo['Exception'] = error

            return voipInfo


    def verifyPppoeSettings(self, output_str1, output_str2):
        resultado = {'PPPoE': {'username': {},
                               'password': {}
                               },
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str1.splitlines()
            c = 0
            for i in ans:
                # print('linha #' + str(c) + '  ' + i)
                if c == 1:
                    # print(i)
                    aux1 = i.replace('=', ';')
                    aux1 = aux1.split(';')
                    aux1 = aux1[1]
                    aux1 = aux1.split(',')

                c = c + 1
            # print(aux1)
            resultado['PPPoE']['username'] = aux1[0]
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

            ans = output_str2.splitlines()
            c = 0
            for i in ans:
                # print('linha #' + str(c) + '  ' + i)
                if c == 1:
                    # print(i)
                    aux2 = i.replace('=', ';')
                    aux2 = aux2.split(';')
                    aux2 = aux2[1]
                    aux2 = aux2.split(',')

                c = c + 1
            # print(aux2)
            resultado['PPPoE']['password'] = aux2[0]
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado

        ###### Executar Soft Reset ######


    def execSoftReset(self, output_str):
        resultado = {'PPPoE': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            c = 0
            for i in ans:
                print('linha #' + str(c) + '  ' + i)

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado

        ###### Executar Hard Reset ######


    def execHardReset(self, output_str):
        resultado = {'PPPoE': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            c = 0
            for i in ans:
                print('linha #' + str(c) + '  ' + i)

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado

        ###### Verificar Parametros ACS ######


    def verifyDefaultAcsSettings(self, output_str):
        ### Abrindo arquivo de Default Settings
        auxiliar_settings = open('files/auxiliar.json', 'r')
        auxiliar_settings = json.load(auxiliar_settings)
        resultado = {'ACS': {
            'Parametros': {
                'CWMP Habilitado': {},
                'URL': {},
                'Periodic Inform Interval': {},
                'CWMP Habilitado': {},
                'Porta': {}
            },
        },
            'Validation': {
                'Geral': {},
                'ACS URL': {},
                'ACS PORT': {},
                'ACS PERIORIC': {},
                'ACS HABILITADO': {},
            },
            'Result': {},
            'Exception': {}}
        try:
            ans = output_str.splitlines()
            c = 0
            for i in ans:
                print('linha #' + str(c) + '  ' + i)
                if c == 4:
                    aux = re.search(r'(?<=>).*?(?=<)', i).group(0)
                    # print(aux)
                    resultado['ACS']['Parametros']['CWMP Habilitado'] = aux
                if c == 5:
                    aux = re.search(r'(?<=>).*?(?=<)', i).group(0)
                    aux2 = re.search(r'([0-9]+)', i).group(0)
                    # print(aux)
                    # print(aux2)
                    resultado['ACS']['Parametros']['URL'] = aux
                    resultado['ACS']['Parametros']['Porta'] = int(aux2)
                if c == 5:
                    aux = re.search(r'(?<=>).*?(?=<)', i).group(0)
                    # print(aux)
                    resultado['ACS']['Parametros']['URL'] = aux
                if c == 10:
                    aux = re.search(r'(?<=>).*?(?=<)', i).group(0)
                    # print(aux)
                    resultado['ACS']['Parametros']['Periodic Inform Interval'] = int(aux)

                c = c + 1
            if resultado['ACS']['Parametros']['URL'] == auxiliar_settings['Info_Auxiliar']['ACS']['URL MANAGEMENT']:
                print('ok')
                valida1 = 'OK'
                resultado['Validation']['ACS URL'] = valida1
            else:
                print('NOK')
                valida1 = 'NOK'
                resultado['Validation']['ACS URL'] = valida1
            if resultado['ACS']['Parametros']['CWMP Habilitado'] == 'TRUE':
                print('ok')
                valida2 = 'OK'
                resultado['Validation']['ACS HABILITADO'] = valida2
            else:
                print('NOK')
                valida2 = 'NOK'
                resultado['Validation']['ACS HABILITADO'] = valida2
            if resultado['ACS']['Parametros']['Periodic Inform Interval'] == auxiliar_settings['Info_Auxiliar']['ACS'][
                'PERIODIC INFORM']:
                print('ok')
                valida3 = 'OK'
                resultado['Validation']['ACS PERIORIC'] = valida3
            else:
                print('NOK')
                valida3 = 'NOK'
                resultado['Validation']['ACS PERIORIC'] = valida3
            if resultado['ACS']['Parametros']['Porta'] == auxiliar_settings['Info_Auxiliar']['ACS']['PORT MANAGEMENT']:
                print('ok')
                valida4 = 'OK'
                resultado['Validation']['ACS PORT'] = valida4
            else:
                print('NOK')
                valida4 = 'NOK'
                resultado['Validation']['ACS PORT'] = valida4

            if (valida1 == 'OK' and valida2 == 'OK' and valida3 == 'OK' and valida4 == 'OK'):
                valida_final = 'OK'
                print('OK')
                resultado['Validation']['Geral'] = valida_final
            else:
                print('NOK')
                valida_final = 'NOK'
                resultado['Validation']['Geral'] = valida_final

            print(resultado)
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado
        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ######Listar dispositivos conectados no WiFi Plus######
    def wifiplus_table(self, out_str, fmw=''):
        #Entrada: show map_info wifi_plus station_info

        raw_list = out_str.splitlines()
        info_wifiplus = {'wifi_stations': {
                            },
                        'base_port': {

                        },
                        'qty_bp_rep': '',
                         'Results': '',
                         'Exception': ''}

        try:
            raw_list = out_str.splitlines()

            count_bp_rep = 0

            for key in raw_list:
                if re.match(r'(^[0-9]{2})', key):
                    list = key.split()

                    if len(list) == 2:
                        info_wifiplus['wifi_stations'][list[1]] = {
                            'ip_addr': '',
                            'mac_addr': '',
                            'ssid': '',
                            'hostname': '',
                            'rssi': ''
                        }
                        info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                        info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]

                    elif len(list) == 3:
                        info_wifiplus['wifi_stations'][list[1]] = {
                            'ip_addr': '',
                            'mac_addr': '',
                            'ssid': '',
                            'hostname': '',
                            'rssi': ''
                        }
                        info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                        info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                        info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[2]

                    elif len(list) > 3:
                        if 'BP2' in list:
                            if 'BP2' in list[2]:
                                count_bp_rep = count_bp_rep + 1
                                info_wifiplus['base_port'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                                info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                                info_wifiplus['base_port'][list[1]]['ssid'] = ''
                                info_wifiplus['base_port'][list[1]]['hostname'] = list[2] + '-' + list[3] + '-' + \
                                                                                  list[4]
                                info_wifiplus['base_port'][list[1]]['rssi'] = ''

                            else:
                                count_bp_rep = count_bp_rep + 1
                                info_wifiplus['base_port'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                                info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                                info_wifiplus['base_port'][list[1]]['ssid'] = list[2]
                                info_wifiplus['base_port'][list[1]]['hostname'] = list[3] + '-' + list[4] + '-' + list[5]
                                info_wifiplus['base_port'][list[1]]['rssi'] = list[len(list) - 1]

                        else:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                            info_wifiplus['wifi_stations'][list[1]]['ssid'] = list[2]
                            info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[3]
                            info_wifiplus['wifi_stations'][list[1]]['rssi'] = list[len(list) - 1]

            info_wifiplus['qty_bp_rep'] = count_bp_rep
            info_wifiplus['Results'] = 'OK'
            info_wifiplus['Exception'] = 'OK'

        except Exception as error:
            info_wifiplus['Results'] = 'NOK'
            info_wifiplus['Exception'] = 'ERRO NA GERACAO DA TABELA DE DEVICES WIFI 5G'

        return info_wifiplus

    ######Listar dispositivos conectados no WiFi Plus######
    def wifi_table(self, out_str):
        # Entrada: show map_info wifi station_info

        raw_list = out_str.splitlines()
        info_wifiplus = {'wifi_stations': {
        },
            'base_port': {

            },
            'Results': '',
            'Exception': ''}

        try:
            raw_list = out_str.splitlines()

            del raw_list[0]
            del raw_list[0]

            for key in raw_list:
                list = key.split()
                if len(list) > 2:
                    if 'BP2' in list:
                        info_wifiplus['base_port'][list[1]] = {
                            'ip_addr': '',
                            'mac_addr': '',
                            'ssid': '',
                            'type': ''
                        }
                        info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                        info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                        info_wifiplus['base_port'][list[1]]['ssid'] = list[2]
                        info_wifiplus['base_port'][list[1]]['type'] = list[3]

                    else:
                        info_wifiplus['wifi_stations'][list[1]] = {
                            'ip_addr': '',
                            'mac_addr': '',
                            'ssid': '',
                            'type': ''
                        }
                        info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                        info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                        info_wifiplus['wifi_stations'][list[1]]['ssid'] = list[2]
                        info_wifiplus['wifi_stations'][list[1]]['type'] = list[3]

            info_wifiplus['Results'] = 'OK'
            info_wifiplus['Exception'] = 'OK'

            return info_wifiplus

        except Exception as error:
            info_wifiplus['Results'] = 'NOK'
            info_wifiplus['Exception'] = error

            return info_wifiplus


    ######Listar modelo do dispositivo######
    def device_model(self, out_str):

        #Entrada: show device_model

        ###STEP-00: JSON SAIDA
        device_info = {
            'model': '',
            'region': '',
            'Result': 'NOK',
            'Exception': ''
        }

        ###Variveis auxiliares
        model = ''
        region = ''

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                if key.startswith('device'):
                    list = key.split()
                    model = list[2]
                    region = model.split('-')
                    region = region[1]
                    device_info['model'] = model
                    device_info['region'] = region
                    device_info['Result'] = 'OK'
                    device_info['Exception'] = 'OK'

                elif key.startswith('sshd'):
                    device_info['Result'] = 'NOK'
                    device_info['Exception'] = 'PROBLEMA MEMORIA HGU'


        except Exception as error:
            device_info['Result'] = 'NOK'
            device_info['Exception'] = error

        return device_info


    ######Configurar bssid 5G Main do dispositivos######
    def setBssid5(self, bssid):
        self.bssid5 = bssid


    ######Configurar bssid 2.4G Main do dispositivos######
    def setBssid2(self, bssid):
        self.bssid2 = bssid


    ###### Verificar Device Info com Info do MDM######
    def getDeviceInfo(self, out_str):
        resultado = {'Device Info': {
            'Fabricante': '',
            'OUI': '',
            'Model Name': '',
            'Product Class': '',
            'SerialNumber': '',
            'Hardware Version': '',
            'Firmware Version': '',
            'Serial GPON': ''
                               },
                     'Result': {},
                     'Exception': {}}
        try:
            c = 0
            aux_out = []
            for i in out_str:
                # print(i)
                ans = i.split('\r\n')
                # print(ans)
                for j in ans:
                    # print(j)
                    if j.startswith('Param'):
                        # print(j)
                        aux = j.split('=')
                        # print(aux)
                        aux_out.append(aux[1])
            # print(aux_out)
            fabricante = aux_out[0]
            OUI = aux_out[1]
            modelName = aux_out[2]
            productClass = aux_out[3]
            serialnumber = aux_out[4]
            hardwareVersion = aux_out[5]
            firmwareVersion = aux_out[6]
            gponSerial = aux_out[7]

            resultado['Device Info']['Fabricante'] = fabricante
            resultado['Device Info']['OUI'] = OUI
            resultado['Device Info']['Model Name'] = modelName
            resultado['Device Info']['Product Class'] = productClass
            resultado['Device Info']['SerialNumber'] = serialnumber
            resultado['Device Info']['Hardware Version'] = hardwareVersion
            resultado['Device Info']['Firmware Version'] = firmwareVersion
            resultado['Device Info']['Serial GPON'] = gponSerial
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ####Verificar Info Básicas do WiFi 2.4G
    def getWiFi2Gligth(self, out_str):

        ###Entrada: >show wifi

        raw_list = out_str.splitlines()

        # del raw_list[0]
        # del raw_list[0]

        infoWiFi2G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi0_status':
                        infoWiFi2G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi2G['info']['ssid'] = ssid_name

                    elif list[1] == 'bssid':
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi2G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi2G['info']['password'] = list[2]

            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = 'ERRO AO GERAR INFO BASICA 2.4GHz', error

            return infoWiFi2G

            ###### Verificar Device Info ######


    ####Verificar Info Básicas do WiFi 5G
    def getWiFi5Gligth(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus0_status':
                        infoWiFi5G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G['info']['ssid'] = ssid_name

                    elif list[1] == 'bssid':
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi5G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi5G['info']['password'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            return infoWiFi5G

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz'

            return infoWiFi5G


    def getWiFi5GligthBS(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name

                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'


        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS'

        return infoWiFi5G_BS


    ####Verificar status interface Internet
    def statusInet(self, out_str):

        ###Entrada: >show primary_diagnosis internet_service status

        status_inet = {
            'status': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                if key.startswith('internet_service'):
                    list = key.split(' ')
                    status_inet['status'] = list[2]

            status_inet['Result'] = 'OK'
            status_inet['Exception'] = 'OK'

        except Exception as error:
            status_inet['Result'] = 'NOK'
            status_inet['Exception'] = error

        return status_inet

    ###METODOS PARA DEFINIR ATRIBUTOS DO HGU

    ######Configurar firmware do dispositivos######
    def setFirmware(self, firmware):
        self.firmware = firmware
        return firmware


    ######Configurar serial do dispositivos######
    def setSerial(self, serial):
        self.serial = serial


    ######Configurar ProductClass do dispositivos######
    def setProductClass(self, product_class):
        self.product_class = product_class
        return product_class

        ###### Verificar PPPoE Settings ######


    ###### Verificar Device Info com Info do MDM######
    def verifyHguHardware(self, out_str):

        resultado = {
            'CPU': {
                'Used': '',
                'Free': ''
            },
            'MEMORIA': {
                'Used': '',
                'Free': ''
            },
            'TOP': {
                'Load average': {
                    '#1': '',
                    '#2': '',
                    '#3': ''
                },
                'Processos': {
                    '#1': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#2': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#3': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#4': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#5': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    }
                }
            },
            'VALIDATION': {
                'CPU': {},
                'MEMORIA': {},
                'GERAL': {}
            },
            'Result': {},
            'Exception': {}
        }
        try:

            print(out_str)
            list_cpu = out_str[0].split('\n')
            print(list_cpu)
            for i in list_cpu:
                if i.startswith('used'):
                    resultado['CPU']['Used'] = int(re.findall(r'(\d+)', i)[0])
                elif i.startswith('free'):
                    resultado['CPU']['Free'] = int(re.findall(r'(\d+)', i)[0])

            list_memory = out_str[1].split('\n')
            # print(list)
            for i in list_memory:
                if i.startswith('percentaje_used'):
                    resultado['MEMORIA']['Used'] = int(re.findall(r'(\d+)', i)[0])
                elif i.startswith('percentaje_free'):
                    resultado['MEMORIA']['Free'] = int(re.findall(r'(\d+)', i)[0])

            out_str[2] = re.sub('<', '', out_str[2])
            list_top = out_str[2].split('\n')
            # print(list)
            aux_out = []
            for i in list_top:
                # print(i)
                if i.startswith('Load average'):
                    aux = i.split(' ')
                    aux_out.append(aux)
            # print(aux_out[0][2])
            resultado['TOP']['Load average']['#1'] = float(aux_out[0][2])
            resultado['TOP']['Load average']['#2'] = float(aux_out[0][3])
            resultado['TOP']['Load average']['#3'] = float(aux_out[0][4])

            aux_out = []
            for i in list_top[4:]:
                # print(i.split())
                #     i = re.sub('  +', ' ', i)
                aux1 = i.split()
                aux_out.append(aux1)
            print(aux_out)
            resultado['TOP']['Processos']['#1']['PID'] = aux_out[1][0]
            resultado['TOP']['Processos']['#1']['PPID'] = aux_out[1][1]
            resultado['TOP']['Processos']['#1']['USER'] = aux_out[1][2]
            resultado['TOP']['Processos']['#1']['STAT'] = aux_out[1][3]
            resultado['TOP']['Processos']['#1']['VSZ'] = aux_out[1][4]
            resultado['TOP']['Processos']['#1']['%MEM'] = aux_out[1][5]
            resultado['TOP']['Processos']['#1']['%CPU'] = aux_out[1][7]
            resultado['TOP']['Processos']['#1']['COMMAND'] = aux_out[1][8:]

            resultado['TOP']['Processos']['#2']['PID'] = aux_out[2][0]
            resultado['TOP']['Processos']['#2']['PPID'] = aux_out[2][1]
            resultado['TOP']['Processos']['#2']['USER'] = aux_out[2][2]
            resultado['TOP']['Processos']['#2']['STAT'] = aux_out[2][3]
            resultado['TOP']['Processos']['#2']['VSZ'] = aux_out[2][4]
            resultado['TOP']['Processos']['#2']['%MEM'] = aux_out[2][5]
            resultado['TOP']['Processos']['#2']['%CPU'] = aux_out[2][7]
            resultado['TOP']['Processos']['#2']['COMMAND'] = aux_out[2][8:]

            resultado['TOP']['Processos']['#3']['PID'] = aux_out[3][0]
            resultado['TOP']['Processos']['#3']['PPID'] = aux_out[3][1]
            resultado['TOP']['Processos']['#3']['USER'] = aux_out[3][2]
            resultado['TOP']['Processos']['#3']['STAT'] = aux_out[3][3]
            resultado['TOP']['Processos']['#3']['VSZ'] = aux_out[3][4]
            resultado['TOP']['Processos']['#3']['%MEM'] = aux_out[3][5]
            resultado['TOP']['Processos']['#3']['%CPU'] = aux_out[3][7]
            resultado['TOP']['Processos']['#3']['COMMAND'] = aux_out[3][8:]

            resultado['TOP']['Processos']['#4']['PID'] = aux_out[4][0]
            resultado['TOP']['Processos']['#4']['PPID'] = aux_out[4][1]
            resultado['TOP']['Processos']['#4']['USER'] = aux_out[4][2]
            resultado['TOP']['Processos']['#4']['STAT'] = aux_out[4][3]
            resultado['TOP']['Processos']['#4']['VSZ'] = aux_out[4][4]
            resultado['TOP']['Processos']['#4']['%MEM'] = aux_out[4][5]
            resultado['TOP']['Processos']['#4']['%CPU'] = aux_out[4][7]
            resultado['TOP']['Processos']['#4']['COMMAND'] = aux_out[4][8:]

            resultado['TOP']['Processos']['#5']['PID'] = aux_out[5][0]
            resultado['TOP']['Processos']['#5']['PPID'] = aux_out[5][1]
            resultado['TOP']['Processos']['#5']['USER'] = aux_out[5][2]
            resultado['TOP']['Processos']['#5']['STAT'] = aux_out[5][3]
            resultado['TOP']['Processos']['#5']['VSZ'] = aux_out[5][4]
            resultado['TOP']['Processos']['#5']['%MEM'] = aux_out[5][5]
            resultado['TOP']['Processos']['#5']['%CPU'] = aux_out[5][7]
            resultado['TOP']['Processos']['#5']['COMMAND'] = aux_out[5][8:]

            ### VALIDATION
            if resultado['CPU']['Free'] >= 9:
                resultado['VALIDATION']['CPU'] = 'OK'
            else:
                resultado['VALIDATION']['CPU'] = 'NOK'
            if resultado['MEMORIA']['Free'] >= 8:
                resultado['VALIDATION']['MEMORIA'] = 'OK'
            else:
                resultado['VALIDATION']['MEMORIA'] = 'NOK'
            if resultado['VALIDATION']['CPU'] == 'OK' and resultado['VALIDATION']['MEMORIA'] == 'OK':
                resultado['VALIDATION']['GERAL'] = 'OK'
            else:
                resultado['VALIDATION']['GERAL'] = 'NOK'

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    def netinf(self, out_str, limiares, fmw = ''):
        resultado = {
            'testes': [],
            'Result': '',
            'Exception': '',
            'Description': ''
        }

        print("passou1" + str(out_str) + " " + str(limiares))
        raw_list = out_str.splitlines()

        try:
            receiver = ''
            transmitter = ''
            erro = ''
            falha_detectada = False

            limiar_per = limiares['per_max']
            limiar_potencia_minima = limiares['potencia_minima']
            limiar_taxa_minima = limiares['taxa_minima']
            limiar_enviar_pacotes = limiares['enviar_pacotes']

            testes = []

            for key in raw_list:
                if ("CERT statistics -" in key):
                    if (len(testes) > 0):
                        if (len(testes[len(testes) - 1]) > 2):
                            if (erro != ''):
                                falha_detectada = True
                                testes[len(testes) - 1].update({"Result": "NOK", "Description": str(erro)})
                            else:
                                testes[len(testes) - 1].update({"Result": "OK", "Description": "OK"})
                    erro = ''
                    transmitter = ProcuraVal('Transmitter: (.+?),',key)
                    receiver = ProcuraVal('Receiver: (.+?)$',key)
                    testes.append({"transmitter": transmitter, "receiver": receiver})
                    continue
                elif (receiver == '' and transmitter == ''):
                    continue
                elif ("Transmitted bytes:" in key):
                    transm_bytes = ProcuraVal('Transmitted bytes: (.+?)$', key)
                    testes[len(testes)-1].update({"Transmitted bytes": transm_bytes})
                elif ("Transmit errors:" in key):
                    transm_error = ProcuraVal('Transmit errors: (.+?)$', key)
                    testes[len(testes) - 1].update({"Transmit errors": transm_error})
                elif ("Received packets:" in key):
                    received_pkts = ProcuraVal('Received packets: (.+?)$', key)
                    testes[len(testes) - 1].update({"Received packets": received_pkts})
                elif ("Received bytes:" in key):
                    received_bytes = ProcuraVal('Received bytes: (.+?)$', key)
                    testes[len(testes) - 1].update({"Received bytes": received_bytes})
                elif ("Received missed sequence packets:" in key):
                    received_missed_seq_pkts = ProcuraVal('Received missed sequence packets: (.+?)$', key)
                    testes[len(testes) - 1].update({"Received missed sequence packets": received_missed_seq_pkts})
                elif ("Received out of sequence packets:" in key):
                    received_out_seq_pkts = ProcuraVal('Received out of sequence packets: (.+?)$', key)
                    testes[len(testes) - 1].update({"Received out of sequence packets": received_out_seq_pkts})
                elif ("Received bad FCS frames:" in key):
                    received_bad_fcs_frms = ProcuraVal('Received bad FCS frames: (.+?)$', key)
                    testes[len(testes) - 1].update({"Received bad FCS frames": received_bad_fcs_frms})
                elif ("Received bad HCS frames:" in key):
                    received_bad_hcs_frms = ProcuraVal('Received bad HCS frames: (.+?)$', key)
                    testes[len(testes) - 1].update({"Received bad HCS frames": received_bad_hcs_frms})
                elif ("Received error frames:" in key):
                    received_error_frames = ProcuraVal('Received error frames: (.+?)$', key)
                    testes[len(testes) - 1].update({"Received error frames": received_error_frames})
                elif ("PER:" in key):
                    per = ProcuraVal('PER: (.+?)$', key)
                    per_n = float(per)

                    if (per_n is False):
                        print ("per inválido:" + str(per) + " " + str(per_n))
                        erro = erro + "PER inválido,"
                    elif (per_n > limiar_per):
                        erro = erro + "taxa de erro (PER) acima de " + str(limiar_per) + ","
                    testes[len(testes) - 1].update({"PER": per})
                elif ("SNR (db):" in key):
                    snr = ProcuraVal('SNR \(db\): (.+?)$', key)
                    testes[len(testes) - 1].update({"SNR (db)": snr})
                elif ("Rate::" in key):
                    rate = ProcuraVal('Rate:: (.+?)$', key)

                    rate_n = float(ProcuraVal('^(.+?)Mbps', rate))

                    if (rate_n is False):
                        erro = erro + "Rate inválido,"
                    elif (rate_n < limiar_taxa_minima):
                        erro = erro + "taxa de transmissão abaixo de " + str(limiar_taxa_minima) + " Mbps,"
                    testes[len(testes) - 1].update({"Rate": rate})
                elif ("RX power:" in key):
                    rx_power = ProcuraVal('RX power: (.+?)$', key)

                    rx_power_n = float(rx_power.replace("dBm",""))

                    if (rx_power_n is False):
                        erro = erro + "RX power inválido,"
                    elif (rx_power_n < limiar_potencia_minima):
                        erro = erro + "potência de RX abaixo de " + str(limiar_potencia_minima) + " dBm,"

                    testes[len(testes) - 1].update({"RX power": rx_power})

            if (len(testes) > 0):
                if (len(testes[len(testes) - 1]) > 2):
                    if (erro != ''):
                        falha_detectada = True
                        testes[len(testes) - 1].update({"Result": "NOK", "Description": str(erro)})
                    else:
                        testes[len(testes) - 1].update({"Result": "OK", "Description": "OK"})

            if (len(testes) == 0):
                resultado['testes'] = testes
                resultado["Result"] = "OK"
                resultado["Exception"] = "OK"
                resultado["Description"] = "Nenhum STB foi detectado na rede HPNA durante os testes."
            elif (falha_detectada == True):
                resultado['testes'] = testes
                resultado["Result"] = "NOK"
                resultado["Exception"] = "NOK"
                resultado["Description"] = "O teste da rede HPNA (Netinf) obteve valores fora do recomendado."
            else:
                resultado['testes'] = testes
                resultado["Result"] = "OK"
                resultado["Exception"] = "OK"
                resultado["Description"] = "O teste da rede HPNA (Netinf) obteve valores dentro do recomendado."

        except Exception as e:
            print(e)
            resultado["Result"] = "NOK"
            resultado["Description"] = "Ocorreu um erro ao executar o teste da rede HPNA."
            resultado["Exception"] = str(e)

        return resultado


    def ip_porta(self, out_str, modelo, fmw = ''):
        # mapeamento IP para porta

        # Entrada: 'show map_info dhcp_table'

        raw_list = out_str.splitlines()

        ip_porta = {'Result': '', 'Exception': '', 'Descrption': ''}

        porta_map = {"wifi station_info": "wifi24",
                     "wifi_plus station_info": "wifi5",
                     "eth1_device information": "eth1",
                     "eth2_device information": "eth2",
                     "eth3_device information": "eth3",
                     "eth4_device information": "eth4"
                     }

        try:
            #if fmw in ['S35', 'BR_SV_g000_R3505VWN1001_s35', 'BR_SV_g000_R3507VWN1001_s35', 'BR_SV_g000_R3505VWN1001_s36', 'BR_SV_g000_R3507VWN1001_s36']:
            demarcadores_interface = ["wifi station_info","wifi_plus station_info","eth1_device information","eth2_device information","eth3_device information","eth4_device information"]
            demarcadores_invalidos = ["arp_table","dhcp_table"]

            key_atual = ""
            for key in raw_list:
                if (key in demarcadores_invalidos):
                    key_atual = ""
                elif (key in demarcadores_interface):
                    key_atual = key

                    demarcadores_interface.remove(key)
                elif (key_atual != ""):
                    disp = key.split()

                    if (disp[0] == '>'):
                        continue

                    if ('RTF3507' in modelo and porta_map[key_atual] == "eth4"):
                        porta = "hpna"
                    else:
                        porta = porta_map[key_atual]

                    try:
                        ip_porta[disp[0]]
                    except:
                        ip_porta[disp[0]]={}

                    ip_porta[disp[0]].update({"porta_hgu": porta, "mac": disp[1]})
            #else:
                # ip_porta['Result'] = 'NOK'
                # ip_porta['Description'] = 'Firmware do HGU não suportado.'
                # ip_porta['Exception'] = 'NOK'
        except Exception as e:
            ip_porta['Result'] = 'NOK'
            ip_porta['Description'] = 'Erro ao mapear IP para porta no HGU.'
            ip_porta['Exception'] = e

        if (ip_porta['Result'] != 'NOK'):
            ip_porta['Result'] = 'OK'
            ip_porta['Description'] = 'OK'
            ip_porta['Exception'] = 'OK'

        return ip_porta


    def lanhosts(self, out_str, so_iptv = False):
        hosts = []
        raw_list = out_str.splitlines()

        for item in raw_list:
            cols = item.split()

            try:
                ip=cols[1]
            except:
                continue

            if (eh_ip(ip) == True):
                try:
                    mac = cols[0]
                    vendorclass = cols[3]
                except:
                    continue

                if (vendorclass != "TEF_IPTV" and so_iptv == True):
                    continue

                hosts.append([mac,ip,vendorclass])

        return hosts


    ####Verificar status GPON PARCIAL
    def getOntParams(self, out_str):

        info_onu = {
            'onu_status': 'N/A',
            'slid': '',
            'serial_gpon': '',
            'Result': '',
            'Exception': ''
        }
        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                lista = key.split()
                if len(lista) > 1:
                    if lista[0].startswith('gponSerialNumber'):
                        info_onu['serial_gpon'] = lista[2]

                    elif lista[0].startswith('gponPassword'):
                        slid = lista[2].split('"')
                        info_onu['slid'] = slid[1]

            info_onu['Result'] = 'OK'
            info_onu['Exception'] = 'OK'

        except Exception as error:
            print(error)
            info_onu['Result'] = 'NOK'
            info_onu['Exception'] = 'NOK'

        return info_onu


    ####Verificar status GPON
    def getStatusOnt(self, out_str):

        status_onu = {
            'onu_status': '',
            'onu_status_description': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()
            for key in raw_list:
                lista = key.split()
                if len(lista) > 1:
                    if lista[0].startswith('ont_status'):
                        status_onu['onu_status'] = lista[1]
                        status = lista[1]
                        print(status)
                        if status == 'O5':
                            status_onu['onu_status_description'] = 'Operation'
                        elif status == 'O4':
                            status_onu['onu_status_description'] = 'Ranging'
                        elif status == 'O3' or status == 'O2':
                            status_onu['onu_status_description'] = 'SN Aquisition'
                        elif status == 'O1':
                            status_onu['onu_status_description'] = 'Syncronization'
                        elif status == 'O6':
                            status_onu['onu_status_description'] = 'Intermittent LODS'
                        elif status == 'O7':
                            status_onu['onu_status_description'] = 'Emergency Stop'
                        else:
                            status_onu['onu_status_description'] = 'Failure '

            status_onu['Result'] = 'OK'
            status_onu['Exception'] = 'OK'

        except Exception as error:
            print(error)
            status_onu['Result'] = 'NOK'
            status_onu['Exception'] = 'NOK'

        return status_onu


    ####Verificar status GPON
    def primaryDiag(self, out_str):

        status_initial = {
            'internet_service': '',
            'iptv_service': '',
            'voip': '',
            'sip_register': '',
            'register_number': '',
            'recv_optical': '',
            'trans_optical': '',
            'public_ip': '',
            'eth_1_tx': '',
            'eth_1_rx': '',
            'eth_2_tx': '',
            'eth_2_rx': '',
            'eth_3_tx': '',
            'eth_3_rx': '',
            'eth_4_tx': '',
            'eth_5_rx': '',
            'result': '',
            'exception': ''
        }

        try:
            raw_list = out_str.splitlines()
            print(raw_list)
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0].startswith('internet_service'):
                        status_initial['internet_service'] = list[2]
                    elif list[0].startswith('iptv_service'):
                        status_initial['iptv_service'] = list[2]
                    elif list[0].startswith('voip'):
                        status_initial['voip'] = list[2]
                    elif list[0].startswith('SIP'):
                        status_initial['sip_register'] = list[3]
                    elif list[0].startswith('registered'):
                        status_initial['register_number'] = list[2]
                    elif list[0].startswith('received_optical'):
                        status_initial['recv_optical'] = list[2]
                    elif list[0].startswith('transmitted_optical'):
                        status_initial['trans_optical'] = list[2]
                    elif list[0].startswith('public_IP'):

                        status_initial['public_ip'] = list[1]

            status_initial['result'] = 'ok'
            status_initial['exception'] = 'ok'

        except Exception as error:
            print(error)
            status_initial['result'] = 'nok'
            status_initial['exception'] = 'nok'

        return status_initial


    def getWiFi5GBS(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': '',
            'hide': '',
            'authentication': '',
            'encryption': '',
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name
                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'hide':
                        infoWiFi5G_BS['info']['hide'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'authentication':
                        infoWiFi5G_BS['info']['authentication'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'encryption':
                        infoWiFi5G_BS['info']['encryption'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'

        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS'

        return infoWiFi5G_BS


class cliMitraEcnt():

    def __init__(self, password, ip):
        self.user_support = 'support'
        self.password = password
        self.ip = ip

    ######Listar detalhes do dipositivo######
    def version(self, out_str):

        ##--> Entrada: sys atsh

        info_hgu = {'Model': '',
                    'Profile': '',
                    'Booted Partition': '',
                    'Partition 1 Version': '',
                    'Partition 2 Version': '',
                    'firmware': '',
                    'brcm_release': '',
                    'bootbase': '',
                    'serialNumber': '',
                    'macAddress': '',
                    'vendor': '',
                    'Result': '',
                    'Exception': ''}

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                list = key.split(':')
                if list[0].startswith('Product Model'):
                    info_hgu['Model'] = list[1].strip()

                elif list[0].startswith('FW'):
                    info_hgu['firmware'] = list[1].strip()

                elif list[0].startswith('Bootbase'):
                    info_hgu['bootbase'] = list[1].strip()

                elif list[0].startswith('First MAC'):
                    mac_aux = list[1].strip()
                    mac = ''
                    count = 0
                    for i in mac_aux:
                        if count != 2:
                            mac = mac + i
                            count = count + 1
                        else:
                            mac = mac + ':' + i
                            count = 1
                    info_hgu['macAddress'] = mac
                    info_hgu['serialNumber'] = list[1].strip()

                elif list[0].startswith('Vendor'):
                    info_hgu['vendor'] = list[1].strip()

            info_hgu['Result'] = 'OK'
            info_hgu['Exception'] = 'OK'

        except Exception as error:
            info_hgu['Result'] = 'NOK'
            info_hgu['Exception'] = error

        return info_hgu


    ######Listar dispositivos na tabela DHCP######
        ######Listar dispositivos na tabela DHCP######
    def dhcp_table(self, out_str, fmw='VBR_g5.9_1.11(WVK.0)b30'):

        # Entrada: 'show map_info dhcp_table'

        raw_list = out_str.splitlines()

        qtde_eth = int(0)
        count_eth = int(0)
        qtde_hpna = int(0)
        count_hpna = int(0)
        qtde_4 = int(0)
        count_wifi24 = int(0)
        qtde_5 = int(0)
        count_wifi5 = int(0)
        count_bp_ap = int(0)
        count_bp_rep = int(0)
        count_hosts = int(0)

        tabela_host = {"qtde_hosts": "",
                       "qtde_eth": qtde_eth,
                       "qtde_hpna": qtde_hpna,
                       "qtde_wifi24": qtde_4,
                       "qtde_wifi5": qtde_5,
                       "interface": {},
                       "bp": {
                           'repeater': {},
                           'ap': {},
                       },
                       "Result": '',
                       "Exception": ''}

        try:

            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Mitra Ecnt
            mitra_ecnt_model = devices['supported']['mitra_ecnt_model']
            mitra_ecnt_fw = devices['supported']['mitra_ecnt_fw']


            if fmw in mitra_ecnt_fw:
                for key in raw_list:
                    list_tab = key.split('\t')
                    list_spa = key.split()

                    if len(list_spa) > 4:
                        if 'WiFi' in list_spa:
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ####CONTABILIZAR SE DEVICES EM 2.4GHz & 5GHz
                            tabela_host["interface"][count_iface]["radio"] = list_spa[5]
                            if list_spa[5] == '5':
                                count_wifi5 = count_wifi5 + 1
                            else:
                                count_wifi24 = count_wifi24 + 1

                            ###TRATAMENTO DE HOSTNAME E SSID PARA DIFERENTES SAIDAS

                            ###SOMENTE SSID SEM HOSTNAME (LEN 6)
                            if len(list_tab) == 6:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]

                            ###SSID & HOSTNAME (LEN 7)
                            elif len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÃO DA TABELA DE BPs NO MODO REPEATER
                                if list_tab[6].startswith('BP2') or list_tab[6].startswith('XPORT'):
                                    print(list_tab)
                                    count_bp_rep = count_bp_rep + 1
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['ipaddr'] = list_tab[
                                        0]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['macaddr'] = list_tab[
                                        1]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['dhcp_mode'] = \
                                    list_tab[2]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['leasetime'] = \
                                    list_tab[3]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['media'] = list_spa[4]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['hostname'] = \
                                    list_tab[6]

                        elif 'Ethernet' in list_spa:
                            count_eth = count_eth + 1
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ###TRATAMENTO DE HOSTNAME PARA DIFERENTES SAIDAS
                            if len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÂO DA TABELA DE BPs NO MODO AP
                                if list_tab[6].startswith('BP2') or list_tab[6].startswith('XPORT'):
                                    print(list_tab)
                                    count_bp_ap = count_bp_ap + 1
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }

                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['ipaddr'] = list_tab[0]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['macaddr'] = list_tab[1]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['dhcp_mode'] = list_tab[2]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['leasetime'] = list_tab[3]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['media'] = list_spa[4]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['hostname'] = list_tab[6]
                        elif 'HPNA' in list_spa:
                            count_bp_ap = 0
                            count_hpna = count_hpna + 1
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                tabela_host['qtde_hosts'] = str(count_hosts)
                tabela_host['qtde_eth'] = str(count_eth)
                tabela_host['qtde_wifi24'] = str(count_wifi24)
                tabela_host['qtde_wifi5'] = str(count_wifi5)

                tabela_host['Result'] = 'OK'
                tabela_host['Exception'] = 'OK'


        except Exception as error:
            tabela_host['Result'] = 'NOK'
            tabela_host['Exception'] = 'ERRO GERAÇÃO TABELA HOST ASKEY BRCM', error

        return tabela_host


    ######Listar dispositivos conectados no WiFi Plus######
    def wifiplus_table(self, out_str, fmw='VBR_g5.9_1.11(WVK.0)b30'):
        # Entrada: show map_info wifi_plus station_info

        info_wifiplus = {
            'wifi_stations': {},
            'base_port': {},
            'qty_bp_rep': '',
            'Results': '',
            'Exception': ''}

        try:

            raw_list = out_str.splitlines()

            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Mitra Ecnt
            mitra_ecnt_model = devices['supported']['mitra_ecnt_model']
            mitra_ecnt_fw = devices['supported']['mitra_ecnt_fw']

            if fmw in mitra_ecnt_fw:

                count_bp_rep = 0

                for key in raw_list:
                    if re.match(r'(^[0-9]{2})', key):
                        list = key.split()

                        if len(list) == 2:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]

                        elif len(list) == 3:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                            info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[2]

                        elif len(list) > 3:
                            if 'BP2' in list:
                                if 'BP2' in list[2]:
                                    count_bp_rep = count_bp_rep + 1
                                    info_wifiplus['base_port'][list[1]] = {
                                        'ip_addr': '',
                                        'mac_addr': '',
                                        'ssid': '',
                                        'hostname': '',
                                        'rssi': ''
                                    }
                                    info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                                    info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                                    info_wifiplus['base_port'][list[1]]['ssid'] = ''
                                    info_wifiplus['base_port'][list[1]]['hostname'] = list[2] + '-' + list[
                                        3] + '-' + \
                                                                                      list[4]
                                    info_wifiplus['base_port'][list[1]]['rssi'] = ''

                                else:
                                    count_bp_rep = count_bp_rep + 1
                                    info_wifiplus['base_port'][list[1]] = {
                                        'ip_addr': '',
                                        'mac_addr': '',
                                        'ssid': '',
                                        'hostname': '',
                                        'rssi': ''
                                    }
                                    info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                                    info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                                    info_wifiplus['base_port'][list[1]]['ssid'] = list[2]
                                    info_wifiplus['base_port'][list[1]]['hostname'] = list[3] + '-' + list[
                                        4] + '-' + list[5]
                                    info_wifiplus['base_port'][list[1]]['rssi'] = list[len(list) - 1]

                            else:
                                info_wifiplus['wifi_stations'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                                info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                                info_wifiplus['wifi_stations'][list[1]]['ssid'] = list[2]
                                info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[3]
                                info_wifiplus['wifi_stations'][list[1]]['rssi'] = list[len(list) - 1]

                info_wifiplus['qty_bp_rep'] = count_bp_rep
                info_wifiplus['Results'] = 'OK'
                info_wifiplus['Exception'] = 'OK'

                return info_wifiplus

            elif fmw in ['S32_7']:

                count_bp_rep = 0

                for key in raw_list:
                    if re.match(r'(^[0-9]{2})', key):
                        list = key.split()
                        if len(list) == 2:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]

                        elif len(list) == 3:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                            info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[2]

                        elif len(list) > 3:
                            if 'BP2' in list:
                                count_bp_rep = count_bp_rep + 1
                                info_wifiplus['base_port'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                                info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                                info_wifiplus['base_port'][list[1]]['ssid'] = list[2]
                                info_wifiplus['base_port'][list[1]]['hostname'] = list[3] + '-' + list[4] + '-' + \
                                                                                  list[5]
                                info_wifiplus['base_port'][list[1]]['rssi'] = list[len(list) - 1]

                            else:
                                info_wifiplus['wifi_stations'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                                info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                                info_wifiplus['wifi_stations'][list[1]]['ssid'] = list[2]
                                info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[3]
                                info_wifiplus['wifi_stations'][list[1]]['rssi'] = list[len(list) - 1]

                    info_wifiplus['qty_bp_rep'] = count_bp_rep
                    info_wifiplus['Results'] = 'OK'
                    info_wifiplus['Exception'] = 'OK'

                return info_wifiplus

            else:
                info_wifiplus['Results'] = 'NOK'
                info_wifiplus['Exception'] = 'NAO ENCONTRADO FIRMWARE COMPATIVEL'

                return info_wifiplus

        except Exception as error:
            info_wifiplus['Results'] = 'NOK'
            info_wifiplus['Exception'] = 'ERRO NA GERACAO DA TABELA DE DEVICES WIFI 5G', error

            return info_wifiplus


    ######Listar informacoes WiFi 5GHz######
    def getWiFi5G(self, out_str):

        ###Entrada: >show wifi_plus all
        ###Necessário tempo maior para retorno do SSH

        raw_list = out_str.splitlines()
        del raw_list[0]

        infoWiFi5G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': '',
            'qhop': '',
            'beamforming': '',
            'scs': '',
            'airfair': '',
            'maui': '',
            'mumimo': '',
            'wifi_plus0_status': '',
            'roaming': ''

        },
            'Result': '',
            'Exception': ''}

        try:

            for key in raw_list:
                # print(key)
                list = key.split()
                # print(list)
                if len(list) > 1:
                    if list[1].startswith('bandwidth'):
                        infoWiFi5G['info']['bandwidth'] = list[2]
                        # print(list[2])
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi5G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi5G['info']['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi5G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        infoWiFi5G['info']['ssid'] = list[2]
                    elif list[1].startswith('bssid'):
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi5G['info']['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi5G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi5G['info']['password'] = list[2]
                    elif list[1].startswith('channel_mode'):
                        infoWiFi5G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('channel'):
                        if infoWiFi5G['info']['channel'] == '':
                            infoWiFi5G['info']['channel'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi5G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi5G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi5G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi5G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi5G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi5G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi5G['info']['region'] = list[2]

                    elif list[1].startswith('qhop') and len(list) == 3:
                        if infoWiFi5G['info']['qhop'] == '':
                            infoWiFi5G['info']['qhop'] = list[2]
                    elif list[1].startswith('beamforming'):
                        infoWiFi5G['info']['beamforming'] = list[2]
                    elif list[1].startswith('scs'):
                        infoWiFi5G['info']['scs'] = list[2]
                    elif list[1].startswith('airfair'):
                        infoWiFi5G['info']['airfair'] = list[2]
                    elif list[1].startswith('maui'):
                        infoWiFi5G['info']['maui'] = list[2]
                    elif list[1].startswith('mumimo'):
                        infoWiFi5G['info']['mumimo'] = list[2]
                    elif list[1].startswith('wifi_plus0_status'):
                        infoWiFi5G['info']['wifi_plus0_status'] = list[2]
                    elif list[1].startswith('roaming'):
                        # print(list[1])
                        infoWiFi5G['info']['roaming'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            return infoWiFi5G

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = error

            return infoWiFi5G


    ######Listar informacoes WiFi 2.4GHz######
    def getWiFi2G(self, out_str):

        ###Entrada: >show wifi all

        raw_list = out_str.splitlines()

        infoWiFi2G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': ''
        },
            'Result': '',
            'Exception': ''}

        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[1].startswith('bandwidth'):
                        infoWiFi2G['info']['bandwidth'] = list[2]
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi2G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi2G['info']['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi2G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        infoWiFi2G['info']['ssid'] = list[2]
                    elif list[1].startswith('bssid'):
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi2G['info']['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi2G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi2G['info']['password'] = list[2]
                    elif list[1].startswith('channel_mode'):
                        infoWiFi2G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi2G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi2G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi2G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi2G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi2G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi2G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi2G['info']['region'] = list[2]
                    ###TRATAMETNO DO CANAL 2.4GHz
                    elif list[1].startswith('channel') and len(list) == 3:
                        infoWiFi2G['info']['channel'] = list[2]

            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = error

            return infoWiFi2G


    ######Listar domínios e bssids criados######
    def roaming_bss(self, out_str, model='', firmware='VBR_g5.9_1.11(WVK.0)b30', dhcp_table={}):

        ####LISTA DE OUI DOS BASES PORTS EM PLANTA
        oui_bp_mitra = ['a4:33:d7', 'cc:ed:dc', 'd8:c6:78', '34:57:60', 'cc:d4:a1', '84:aa:9c']
        oui_bp_askey = ['94:91:7f', '1c:b0:44', '80:78:71']

        raw_list = out_str.splitlines()

        table_bssid = {"qty_domain": "",
                       "qty_baseport": "",
                       "qty_bssid_total": "",
                       "ssid-0000": '',
                       "ssid-aaaa": '',
                       "qty_bssid_2.4GHz": "",
                       "qty_bssid_5GHz": "",
                       "bssid/domain":
                           {"BS": {},
                            'MAIN': {}
                            },
                       "bssids": {},
                       "Result": '',
                       "Exception": ''}

        try:

            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Mitra Ecnt
            mitra_ecnt_model = devices['supported']['mitra_ecnt_model']
            mitra_ecnt_fw = devices['supported']['mitra_ecnt_fw']

            if firmware in mitra_ecnt_fw:

                qty_bp = int(0)
                qty_domain = int(0)
                qty_bssid_total = int(0)
                qty_bssid_24 = int(0)
                qty_bssid_5 = int(0)

                count_bp = 0

                tag_domain_BS = False
                tag_domain_5 = False
                tag_domain_guest = False

                count_bssid_24 = 0
                count_bssid_5 = 0
                count_bssid_guest = 0

                count_domain_24 = 0
                count_domain_5_bs = 0
                count_domain_5_main = 0

                aux_basePort = {}
                mac_ref_table = []

                for key in raw_list:
                    list = key.split()
                    if len(list) > 5 and list[0].startswith('00'):
                        # print(list)
                        # print(list[1])
                        # index = list[0].strip('.')
                        index = list[1]
                        table_bssid["bssids"][index] = {"bssid": "",
                                                        "status": "",
                                                        "local": "",
                                                        "radio": "",
                                                        "channel": "",
                                                        "bandwidth": "",
                                                        "BSSTr": "",
                                                        "fat": "",
                                                        "domain": "",
                                                        "vendor": "",
                                                        "network": ""}
                        #
                        if list[3] == 'Yes':  # Indice 3 identifica o device a qual esta conectado o shell
                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['local'] = 'HGU'
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]

                            if list[10] == '0000' and list[4] == '2.4G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                table_bssid['ssid-0000'] = ''
                            elif list[10] == '0000' and list[4] == '5G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                            elif list[10] == 'aaaa':
                                table_bssid['bssids'][index]['network'] = 'Main_5G'
                                table_bssid['ssid-aaaa'] = ''
                            else:
                                table_bssid['bssids'][index]['network'] = 'Guest'


                        elif list[3] == 'No' and list[2] == 'UP':
                            mac_ref = list[9]

                            if mac_ref not in mac_ref_table:
                                count_bp = count_bp + 1
                                aux_basePort[mac_ref] = 'BP-' + str(count_bp)
                                table_bssid["bssids"][index]['local'] = "BP-" + str(count_bp)
                                mac_ref_table.append(mac_ref)
                            else:
                                table_bssid["bssids"][index]['local'] = aux_basePort[mac_ref]

                            ####VALIDAR MODELO BP
                            oui = list[9][:8]

                            ###VALIDAR SE BP ASKEY
                            if oui in oui_bp_askey:  # Identificar modelo de base port Askey
                                table_bssid["bssids"][index]['vendor'] = "ASKEY"
                                if list[10].strip() == '0000' and list[4].strip() == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'


                            ###VALIDAR SE BP MITRA
                            elif oui in oui_bp_mitra:  # Identificar modelo de base port Mitra
                                table_bssid["bssids"][index]['vendor'] = "MITRA"
                                if list[10] == '0000' and list[4] == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'

                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]
                #
                        ###Verificar quantidade de Dominios

                        if list[10] == '0000' and list[2] == 'UP':
                            tag_domain_BS = True
                            if int(list[5]) < 14:
                                count_bssid_24 = count_bssid_24 + 1
                                count_domain_24 = count_domain_24 + 1
                            else:
                                count_bssid_5 = count_bssid_5 + 1
                                count_domain_5_bs = count_domain_5_bs + 1

                        elif list[10] == 'aaaa' and list[2] == 'UP':
                            tag_domain_5 = True
                            count_bssid_5 = count_bssid_5 + 1
                            count_domain_5_main = count_domain_5_main + 1

                        elif (list[10] != '0000' or list[10] != 'aaaa') and list[2] == 'UP':
                            tag_domain_guest = True
                            count_bssid_guest = count_bssid_guest + 1

                qty_bp = len(mac_ref_table)

                ###VERIFICAR QUANTIDADE DE DOMINIOS

                if tag_domain_BS and tag_domain_5 and tag_domain_guest:
                    table_bssid["qty_domain"] = str(3)
                elif tag_domain_BS and tag_domain_5 and tag_domain_guest == False:
                    table_bssid["qty_domain"] = str(2)

                table_bssid["qty_baseport"] = str(qty_bp)
                table_bssid['bssid/domain']['BS']['2_4GHz'] = str(count_domain_24)
                table_bssid['bssid/domain']['BS']['5GHz'] = str(count_domain_5_bs)
                table_bssid['bssid/domain']['MAIN']['5GHz'] = str(count_domain_5_main)
                table_bssid["qty_bssid_2.4GHz"] = str(count_domain_24)
                table_bssid["qty_bssid_5GHz"] = str(count_domain_5_bs + count_domain_5_main)
                table_bssid["qty_bssid_total"] = str(count_domain_5_bs + count_domain_5_main + count_domain_24)

                table_bssid['Result'] = 'OK'
                table_bssid['Exception'] = 'OK'

        except Exception as error:

            table_bssid['Result'] = 'NOK'
            table_bssid['Exception'] = 'ERRO NA GERACAO DA TABELA_BSSID: ', error


        return table_bssid


    ######Listar detalhes das estacoes conectadas nos bssids WiFi######
    def roaming_assoc(self, out_str, firmware='VBR_g5.9_1.11(WVK.0)b30'):

        raw_list = out_str.splitlines()
        count_host = int(0)

        table_sta_assoc = {}

        try:

            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Mitra Ecnt
            mitra_ecnt_model = devices['supported']['mitra_ecnt_model']
            mitra_ecnt_fw = devices['supported']['mitra_ecnt_fw']

            if firmware in mitra_ecnt_fw:
                #####RX and TX is about the HGU, instance rssi_rx is the power seen by the HGU sent by the station

                if firmware == 'VBR_g5.9_1.11(WVK.0)b32':
                    for key in raw_list:
                        if key != '':
                            list = key.split()
                            if len(list) > 5 and list[0].startswith('000'):
                                count_host = count_host + 1
                                index = list[0].strip('.')
                                table_sta_assoc[list[1]] = {
                                    "radio": "",
                                    "ss": "",
                                    "bw": "",
                                    "phyrate": "",
                                    "bsstr": "",
                                    "bssid": "",
                                    "domain": "",
                                    "rssi_rx": "",
                                    "max_phyrate_tx": "",
                                    "avg_phyrate_tx": "",
                                    "avg_phyrate_rx": "",
                                }

                                if len(list) <= 12:
                                    table_sta_assoc[list[1]]["radio"] = list[2]
                                    table_sta_assoc[list[1]]["ss"] = list[3]
                                    table_sta_assoc[list[1]]["bw"] = list[4]
                                    table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                    table_sta_assoc[list[1]]["bsstr"] = list[6]
                                    table_sta_assoc[list[1]]["bssid"] = list[7]
                                    table_sta_assoc[list[1]]["domain"] = list[8]
                                    table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                    table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                    avg_phy_rate_aux = list[11].split('/')
                                    avg_phy_rate_tx = avg_phy_rate_aux[0]
                                    avg_phy_rate_rx = avg_phy_rate_aux[1]
                                    table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                    table_sta_assoc[list[1]]["avg_phyrate_rx"] = avg_phy_rate_rx

                                elif len(list) >= 14:
                                    table_sta_assoc[list[1]]["radio"] = list[2] + '|' + list[3]
                                    table_sta_assoc[list[1]]["ss"] = list[4]
                                    table_sta_assoc[list[1]]["bw"] = list[5]
                                    table_sta_assoc[list[1]]["max_phyrate_hw"] = list[6]
                                    table_sta_assoc[list[1]]["bsstr"] = list[7]
                                    table_sta_assoc[list[1]]["bssid"] = list[8]
                                    table_sta_assoc[list[1]]["domain"] = list[9]
                                    table_sta_assoc[list[1]]["rssi_rx"] = list[10]
                                    table_sta_assoc[list[1]]["max_phyrate_current"] = list[11]
                                    avg_phy_rate_tx_aux = list[12].split('/')
                                    avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                    table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                    table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[13]

                                else:
                                    table_sta_assoc[list[1]]["radio"] = list[2]
                                    table_sta_assoc[list[1]]["ss"] = list[3]
                                    table_sta_assoc[list[1]]["bw"] = list[4]
                                    table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                    table_sta_assoc[list[1]]["bsstr"] = list[6]
                                    table_sta_assoc[list[1]]["bssid"] = list[7]
                                    table_sta_assoc[list[1]]["domain"] = list[8]
                                    table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                    table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                    avg_phy_rate_tx_aux = list[11].split('/')
                                    avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                    table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                    table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                            else:
                                table_sta_assoc['qty_hosts'] = str(count_host)

                else:
                    for key in raw_list:
                        if key != '':
                            list = key.split()
                            if len(list) > 5 and list[0].startswith('00'):
                                count_host = count_host + 1
                                index = list[0].strip('.')
                                table_sta_assoc[list[1]] = {
                                    "radio": "",
                                    "ss": "",
                                    "bw": "",
                                    "phyrate": "",
                                    "bsstr": "",
                                    "bssid": "",
                                    "domain": "",
                                    "rssi_rx": "",
                                    "max_phyrate_tx": "",
                                    "avg_phyrate_tx": "",
                                    "avg_phyrate_rx": "",
                                }

                                if len(list) <= 13:
                                    table_sta_assoc[list[1]]["radio"] = list[2]
                                    table_sta_assoc[list[1]]["ss"] = list[3]
                                    table_sta_assoc[list[1]]["bw"] = list[4]
                                    table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                    table_sta_assoc[list[1]]["bsstr"] = list[6]
                                    table_sta_assoc[list[1]]["bssid"] = list[7]
                                    table_sta_assoc[list[1]]["domain"] = list[8]
                                    table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                    table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                    avg_phy_rate_tx_aux = list[11].split('/')
                                    avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                    table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                    table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                                elif len(list) > 13:
                                    table_sta_assoc[list[1]]["radio"] = list[2] + '|' + list[3]
                                    table_sta_assoc[list[1]]["ss"] = list[4]
                                    table_sta_assoc[list[1]]["bw"] = list[5]
                                    table_sta_assoc[list[1]]["max_phyrate_hw"] = list[6]
                                    table_sta_assoc[list[1]]["bsstr"] = list[7]
                                    table_sta_assoc[list[1]]["bssid"] = list[8]
                                    table_sta_assoc[list[1]]["domain"] = list[9]
                                    table_sta_assoc[list[1]]["rssi_rx"] = list[10]
                                    table_sta_assoc[list[1]]["max_phyrate_current"] = list[11]
                                    avg_phy_rate_tx_aux = list[12].split('/')
                                    avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                    table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                    table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[13]

                                else:

                                    table_sta_assoc[list[1]]["radio"] = list[2]
                                    table_sta_assoc[list[1]]["ss"] = list[3]
                                    table_sta_assoc[list[1]]["bw"] = list[4]
                                    table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                    table_sta_assoc[list[1]]["bsstr"] = list[6]
                                    table_sta_assoc[list[1]]["bssid"] = list[7]
                                    table_sta_assoc[list[1]]["domain"] = list[8]
                                    table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                    table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                    avg_phy_rate_tx_aux = list[11].split('/')
                                    avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                    table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                    table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                            else:
                                table_sta_assoc['qty_hosts'] = str(count_host)

                table_sta_assoc['qty_hosts'] = str(count_host)
                table_sta_assoc['Result'] = 'OK'
                table_sta_assoc['Exception'] = 'OK'

        except Exception as error:
            print(error)
            table_sta_assoc['Result'] = 'NOK'
            table_sta_assoc['Exception'] = 'ERRO GERAÇÃO TABELA DE ASSOC WIFI'

        return table_sta_assoc


    ######Listar modelo do dispositivo######
    def device_model(self, out_str):

        # Entrada: show device_model

        ###STEP-00: JSON SAIDA
        device_info = {
            'model': '',
            'region': '',
            'Result': 'NOK',
            'Exception': 'NOK'
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                ###Exception para dispositivo Mitra ECNT
                if key.startswith('device_'):
                    list = key.split()
                    model = list[1]
                    region_aux = model.split('-')
                    if len(region_aux) > 2:
                        region = 'N2'
                    else:
                        region = 'N1'

                ###Utilizado para Askey BRCM
                elif key.startswith('device'):
                    list = key.split()
                    model = list[2]
                    region = model.split('-')
                    region = region[1]

            device_info['model'] = model
            device_info['region'] = region
            device_info['Result'] = 'OK'
            device_info['Exception'] = 'OK'

        except Exception as error:
            device_info['Result'] = 'NOK'
            device_info['Exception'] = error

        return device_info


    ######Listar interfaces ETH utilizadas######
    def listEthIfaces(self, out_str):

        # Entrada: show map_info eth1_device information

        try:

            connect_lan = {'iface': '', 'ip_addr': 'not_connected', 'mac_addr': 'not_connected', 'Result': '',
                           'Exception': ''}

            raw_list = out_str.splitlines()

            for key in raw_list:
                sew = key.split()
                if sew[0].startswith('eth'):
                    iface = sew[0]
                    iface = iface.split('_')
                    iface = iface[0]
                    connect_lan['iface'] = iface
                elif not (sew[0].startswith('show') | sew[0].startswith('>') | \
                          sew[0].startswith('eth' + str(int) + '_device')):
                    if len(sew) > 1:
                        ip_addr = sew[0]
                        mac_addr = sew[1]
                    connect_lan['ip_addr'] = ip_addr
                    connect_lan['mac_addr'] = mac_addr

            connect_lan['Result'] = 'OK'
            connect_lan['Exception'] = 'OK'

            return connect_lan

        except Exception as error:
            connect_lan['Result'] = 'NOK'
            connect_lan['Exception'] = 'ERRO AO LISTAR INTERFACES LAN DO HGU: ', error

            return connect_lan


    ###### Listar DHCP SETTINGS HGU ######
    def getDhcpSettingsHgu(self, output_str):
        # print(output_str)

        # Entrada: dhcpserver show

        resultado = {'LAN': {
            'DHCP Server': '',
            'IP Inicio': '',
            'IP Final': '',
            'DNS Server': '',
            'Lease Time': '',
            'Gateway': '',
            'Option 42': '',
            'WAN VoIP Options': {
                'WAN Interface': '',
                'Option 42': ''
            },
            'AlternativeRange-NAT/PATLines': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': '',
                'Option 42': '',
            },
            'AlternativeRange-NAT/PATLines - 2': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': ''
            },

        },
            'Result': {},
            'Exception': {}}
        try:
            output_str1 = output_str[0]
            output_str2 = output_str[1]
            output_str3 = output_str[2]
            ans = output_str2.splitlines()
            # print(ans)
            c = 0
            aux = []
            for i in ans:
                aux1 = re.sub(' +', '', i)
                # print('linha #' + str(c) + '  ' + aux1)
                aux1 = aux1.split(':')
                # print(aux1)
                aux.append(aux1)
                c = c + 1
            # print(aux)
            for j in aux[1:6]:
                # print(j)
                if j[0].startswith('dhcpserver'):
                    resultado['LAN']['DHCP Server'] = j[1]
                elif j[0].startswith('startipaddress'):
                    resultado['LAN']['IP Inicio'] = j[1]
                    aux = j[1].split('.')
                    resultado['LAN']['DNS Server'] = resultado['LAN']['Gateway'] = aux[0] + '.' + aux[1] + '.' + aux[2] + '.' + '1'

                elif j[0].startswith('poolsize'):
                    a = int(j[1])
                    b = int(resultado['LAN']['IP Inicio'][-1:])
                    c = str(a + b - 1)
                    resultado['LAN']['IP Final'] = resultado['LAN']['IP Inicio'][:-1] + c
                elif j[0].startswith('LeasedTime'):
                    resultado['LAN']['Lease Time'] = j[1]

            ans = output_str3.splitlines()
            # print(ans)
            c = 0
            aux = []
            for i in ans:
                aux1 = re.sub(' +', '', i)
                # print('linha #' + str(c) + '  ' + aux1)
                aux1 = aux1.split(':')
                # print(aux1)
                aux.append(aux1)
                c = c + 1
            # print(aux)
            for j in aux[7:13]:
                # print(j)
                if j[0].startswith('StartIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Inicio'] = j[1]
                elif j[0].startswith('EndIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Final'] = j[1]
                elif j[0].startswith('DNSServer'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['DNS Servers'] = j[1]
                elif j[0].startswith('GatewayAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['Gateway'] = j[1]
                    resultado['LAN']['Gateway'] = j[1]
                    resultado['LAN']['DNS Server'] = j[1]
                elif j[0].startswith('LeasedTime'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines']['Lease Time'] = j[1]
                    resultado['LAN']['Lease Time'] = j[1]
            for j in aux[42:48]:
                # print(j)
                if j[0].startswith('StartIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Inicio'] = j[1]
                elif j[0].startswith('EndIPAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Final'] = j[1]
                elif j[0].startswith('DNSServer'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['DNS Servers'] = j[1]
                elif j[0].startswith('GatewayAddress'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Gateway'] = j[1]
                elif j[0].startswith('LeasedTime'):
                    resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Lease Time'] = j[1]

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = 'ERRO AO CONSULTAR dhcpSettings'

        return resultado


    ######Listar informacoes Opticas HGU######
    def getOpticalInfo(self, out_str):
        ###Entrada: >show ont optics
        raw_list = out_str.splitlines()
        infoGpon = {'info':
                        {'vendor': '',
                         'model': '',
                         'type': '',
                         'class': '',
                         'ont_rx': '',
                         'ont_tx': ''},
                    'Result': '',
                    'Exception': ''
                    }
        try:
            c = 0
            for key in raw_list:
                print('linha #' + str(c) + '  ' + key)
                list = key.split()
                if len(list) > 0:
                    if list[0].startswith('ont_transceiver_vendor'):
                        infoGpon['info']['vendor'] = list[1]
                    elif list[0].startswith('ont_transceiver_model'):
                        infoGpon['info']['model'] = list[1]
                    elif list[0].startswith('ont_transceiver_type'):
                        infoGpon['info']['type'] = list[1]
                    elif list[0].startswith('ont_transceiver_class'):
                        infoGpon['info']['class'] = list[2]
                    elif list[0].startswith('ont_rx_power'):
                        infoGpon['info']['ont_rx'] = list[1]
                    elif list[0].startswith('ont_tx_power'):
                        infoGpon['info']['ont_tx'] = list[1]
                c = c + 1
            infoGpon['Result'] = 'OK'
            infoGpon['Exception'] = 'OK'
            return infoGpon
        except Exception as error:
            infoGpon['Result'] = 'NOK'
            infoGpon['Exception'] = error
            return infoGpon


    ######Listar informacoes das rotas do HGU######
    def getRoutes(self, out_str):

        ###Entrada: >route show

        raw_list = out_str.splitlines()

        count_route_inet = 0
        count_route_voip = 0
        count_route_vod = 0
        count_route_lan = 0

        infoRoute = {'qty_routes_inet': '',
                     'qty_routes_voip': '',
                     'qty_routes_vod': '',
                     'qty_routes_lan': '',
                     'info': {},
                     'Result': '',
                     'Exception': ''
                     }

        try:
            for key in raw_list:
                list = key.split()
                print(list)
                if len(list) > 3:
                    if re.match \
                                (
                                r'(^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$)',
                                list[0]) \
                            or list[0] == 'default':
                        index = list[7]
                        if index == 'br0':
                            count_route_lan = count_route_lan + 1
                            infoRoute['info'][index + '-' + str(count_route_lan)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_lan)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['iface'] = list[5]

                        elif index == 'ppp0':
                            count_route_inet = count_route_inet + 1
                            infoRoute['info'][index + '-' + str(count_route_inet)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_inet)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['iface'] = list[5]

                        elif index == 'nas1':
                            count_route_vod = count_route_vod + 1
                            infoRoute['info'][index + '-' + str(count_route_vod)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_vod)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['iface'] = list[5]


                        elif index == 'nas2':
                            count_route_voip = count_route_voip + 1
                            infoRoute['info'][index + '-' + str(count_route_voip)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_voip)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['iface'] = list[5]

            infoRoute['qty_routes_inet'] = str(count_route_inet)
            infoRoute['qty_routes_voip'] = str(count_route_voip)
            infoRoute['qty_routes_vod'] = str(count_route_vod)
            infoRoute['qty_routes_lan'] = str(count_route_lan)
            infoRoute['Result'] = 'OK'
            infoRoute['Exception'] = 'OK'

        except Exception as error:
            infoRoute['Result'] = 'NOK'
            infoRoute['Exception'] = error

        return infoRoute


    ####Verificar Credenciais PPPoE
    def verifyPppoeSettings(self, output_str):
        resultado = {'PPPoE': {'username': {},
                               'password': {}
                               },
                     'Result': {},
                     'Exception': {}}
        try:
            # print(output_str)
            for i in output_str:
                aux = i.splitlines()
                # print(aux)
                if aux[0].endswith('USERNAME'):
                    resultado['PPPoE']['username'] = aux[1]
                elif aux[0].endswith('PASSWORD'):
                    resultado['PPPoE']['password'] = aux[1]
            # ans = output_str.splitlines()
            # print(aux2)
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado
        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ######Listar DNS IPv4 HGU######
    def getDnsIpv4Hgu(self, output_str):

        # Entrada: sys ipinfo

        resultado = {'DNS_IPv4': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            # print(ans)
            aux_final = []
            for i in ans:
                if i.startswith('server'):
                    aux = re.search(r'(?<=server=).*?(?=@ppp)', i).group(0)
                    aux_final.append(aux)
            print(aux_final)
            print(aux_final[0:2])
            resultado['DNS_IPv4'] = aux_final[0:2]
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ######Listar DNS IPv4 HGU######
    def getDnsIpv6Hgu(self, output_str):

        # Entrada: sys ipinfo

        resultado = {'DNS_IPv6': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            # print(ans)
            aux_final = []
            for i in ans:
                if i.startswith('server'):
                    aux = re.search(r'(?<=server=).*?(?=@ppp)', i).group(0)
                    aux_final.append(aux)
            print(aux_final)
            print(aux_final[2:])
            resultado['DNS_IPv6'] = aux_final[2:]
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ######Listar informacoes IP_Internet######
    def getIpWan(self, out_str):
        print(out_str)
        print('tamanho out_str = ' + str(len(out_str)))
        ###Entrada: >wan show

        infoIpInet = {
            'iface': {
                'Voip_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Vod_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Multicast_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Internet_ppp_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                }
            },
            'Result': '',
            'Exception': ''
        }

        if len(out_str) == 4:
            try:
                for key in out_str:
                    if key == 'down':
                        infoIpInet['iface']['Internet_ppp_interface']['service_name'] = key
                    elif key == 'DISCONNECTED':
                        infoIpInet['iface']['Internet_ppp_interface']['status_v4'] = key
                        infoIpInet['iface']['Internet_ppp_interface']['status_v6'] = key
                    elif key == '10':
                        infoIpInet['iface']['Internet_ppp_interface']['vlan'] = key
                infoIpInet['Result'] = 'OK'
                infoIpInet['Exception'] = 'OK'

                return infoIpInet

            except Exception as error:
                infoIpInet['Result'] = 'NOK'
                infoIpInet['Exception'] = error

                return infoIpInet
        elif len(out_str) == 3:
            try:
                if out_str[0]:
                    infoIpInet['iface']['Internet_ppp_interface']['service_name'] = out_str[0]
                ipv4 = re.search(r'inet addr:(\S+)', out_str[1])
                if ipv4:
                    ipv4 = ipv4.group(1)
                    infoIpInet['iface']['Internet_ppp_interface']['status_v4'] = 'CONNECTED'
                    print(ipv4)
                ipv6 = re.search(
                    r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))',
                    out_str[1])
                if ipv6:
                    ipv6 = ipv6.group()
                    infoIpInet['iface']['Internet_ppp_interface']['status_v6'] = 'CONNECTED'
                    print(ipv6)
                if out_str[2]:
                    aux = out_str[2].split('\n')
                    # print(aux)
                    infoIpInet['iface']['Internet_ppp_interface']['vlan'] = aux[1]
                infoIpInet['Result'] = 'OK'
                infoIpInet['Exception'] = 'OK'

                return infoIpInet
            except Exception as error:
                infoIpInet['Result'] = 'NOK'
                infoIpInet['Exception'] = error

                return infoIpInet

    ####Verificar status interface Internet
    def statusInet(self, out_str):

        ###Entrada: >show primary_diagnosis internet_service status

        status_inet = {
            'status': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                if key.startswith('internet_service'):
                    list = key.split(' ')
                    status_inet['status'] = list[2]

            status_inet['Result'] = 'OK'
            status_inet['Exception'] = 'OK'

        except Exception as error:
            status_inet['Result'] = 'NOK'
            status_inet['Exception'] = error

        return status_inet


    ####Verificar status interface VoIP
    def getInfoVoIP(self, out_str):

        ###Entrada: > voice show

        voipInfo = {
            'info': {
                'Voice_Profile': {
                    'ifName': '',
                    'ipAddr': '',
                    'ipVersion': '',
                    'manageProtocol': '',
                    'voiceProfile': '',
                    'profileState': '',
                    'local': '',
                    'dtmfMethod': '',
                    'hookFlashMethod': '',
                    'T38': '',
                    'V18': '',
                    'rtpDscpMark': '',
                    'rtpPortMin': '',
                    'rtpPortMax': '',
                    'sip': '',
                    'domain': '',
                    'port': '',
                    'transport': '',
                    'regExpires': '',
                    'regRetriveInterval': '',
                    'dscpMark': '',
                    'addrRegister': '',
                    'portRegister': '',
                    'addrProxy': '',
                    'portProxy': '',
                    'option120Addr': '',
                    'outboundProxyAddr': '',
                    'outboundProxyPort': '',
                    'uriConference': '',
                    'optionConference': ''
                },
                'Account': {
                    'lineEnableState': '',
                    'voipServiceStatus': '',
                    'reverserPolarity': '',
                    'callStatus': '',
                    'physicalReference': '',
                    'uri': '',
                    'number': '',
                    'authName': '',
                    'authPwd': '',
                    'txGain': '',
                    'rxGain': '',
                    'echoCancellation': '',
                    'callWaiting': ''
                },
                'Codec': {
                    'codec-1': '',
                    'codec-2': '',
                    'codec-3': ''
                }
            },
            'Result': '',
            'Exception': ''
        }
        # print(out_str)
        voip_on = out_str[0].splitlines()
        aux = []
        for i in voip_on:
            aux1 = i.split('\r\n')
            aux.append(aux1)
        print(aux)
        if aux[1] != '':
            voip = 'OK'
        else:
            voip = 'NOK'
        # print(voip)
        out_str = out_str[1]
        raw_list = out_str.splitlines()
        # print(raw_list)

        try:
            if voip == 'OK':
                list_out = []
                c = 0
                for key in raw_list:
                    list = re.sub('  +', '', key)
                    list = list.split(':')
                    print('linha #' + str(c) + '  ' + str(list))
                    list_out.append(list)

                    c = c + 1
                print(list_out)
                for i in list_out:
                    print(i)
                    if len(list_out) > 1:
                        # print(list)
                        ###INFORMAÇÕES VOICE PROFILE
                        if i[0].startswith('BoundIfName'):
                            voipInfo['info']['Voice_Profile']['ifName'] = i[1]
                        elif i[0].startswith('IPAddress'):
                            voipInfo['info']['Voice_Profile']['ipAddr'] = i[1]
                        # elif i[0].startswith('IPAddress'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['ipVersion'] = i[4]
                        # elif i[0].startswith('Management'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['manageProtocol'] = i[3]
                        # elif i[0].startswith('Associated'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['voiceProfile'] = i[3]
                        elif i[0].startswith('ActivationStatus'):
                            voipInfo['info']['Voice_Profile']['profileState'] = i[1]
                            voipInfo['info']['Account']['lineEnableState'] = i[1]
                        elif i[0].startswith('Region (Locale)'):
                            voipInfo['info']['Voice_Profile']['local'] = i[1]
                        elif i[0].startswith('DTMFMethod'):
                            voipInfo['info']['Voice_Profile']['dtmfMethod'] = i[1]
                        # elif i[0].startswith('HookFlashMethod'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['hookFlashMethod'] = i[2]
                        elif i[0].startswith('T38'):
                            voipInfo['info']['Voice_Profile']['T38'] = i[1]
                        # elif i[0].startswith('V18'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['V18'] = i[2]
                        elif i[0].startswith('RTPDSCPMark'):
                            voipInfo['info']['Voice_Profile']['rtpDscpMark'] = i[1]
                        # elif i[0].startswith('RTPPortMin'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['rtpPortMin'] = i[2]
                        # elif i[0].startswith('RTPPortMax'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['rtpPortMax'] = i[2]
                        elif i[0].startswith('Domain'):
                            voipInfo['info']['Voice_Profile']['domain'] = i[1]
                        elif i[0].startswith('Port'):
                            voipInfo['info']['Voice_Profile']['port'] = i[1]
                        elif i[0].startswith('Transport'):
                            voipInfo['info']['Voice_Profile']['transport'] = i[1]
                        elif i[0].startswith('RegExpires'):
                            voipInfo['info']['Voice_Profile']['regExpires'] = i[1]
                        elif i[0].startswith('RegRetryInterval'):
                            voipInfo['info']['Voice_Profile']['regRetriveInterval'] = i[1]
                        elif i[0].startswith('DSCPMark'):
                            voipInfo['info']['Voice_Profile']['dscpMark'] = i[1]
                        elif i[0].startswith('Registrar Addr'):
                            voipInfo['info']['Voice_Profile']['addrRegister'] = i[1]
                        elif i[0].startswith('Registrar Port'):
                            voipInfo['info']['Voice_Profile']['portRegister'] = i[1]
                        elif i[0].startswith('Proxy Addr'):
                            voipInfo['info']['Voice_Profile']['addrProxy'] = i[1]
                        elif i[0].startswith('Proxy Port'):
                            voipInfo['info']['Voice_Profile']['portProxy'] = i[1]
                        elif i[0].startswith('OutBoundProxy Addr'):
                            voipInfo['info']['Voice_Profile']['outboundProxyAddr'] = i[1]
                        elif i[0].startswith('OutBoundProxy Port'):
                            voipInfo['info']['Voice_Profile']['outboundProxyPort'] = i[1]
                        # elif i[0].startswith('Conferencing') and i[1].startswith('URI'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['uriConference'] = i[3]
                        # elif i[0].startswith('Conferencing') and i[1].startswith('Option'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['optionConference'] = i[3]
                        #
                        # ###INFORMAÇÕES LINHA SIP
                        # elif i[0].startswith('ActivationStatus'):
                        #     print('PASSOU AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
                        #     voipInfo['info']['Account']['lineEnableState'] = i[1]
                        elif i[0].startswith('VoipServiceStatus'):
                            voipInfo['info']['Account']['voipServiceStatus'] = i[1]
                        # elif i[0].startswith('PolarityReverseState'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['reverserPolarity'] = i[2]
                        elif i[0].startswith('CallStatus'):
                            voipInfo['info']['Account']['callStatus'] = i[1]
                        # elif i[0].startswith('Associated'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['physicalReference'] = i[3]
                        elif i[0].startswith('URI'):
                            voipInfo['info']['Account']['uri'] = i[1]
                        elif i[0].startswith('Extension'):
                            voipInfo['info']['Account']['number'] = i[1]
                        elif i[0].startswith('AuthName'):
                            voipInfo['info']['Account']['authName'] = i[1]
                        elif i[0].startswith('AuthPwd'):
                            voipInfo['info']['Account']['authPwd'] = i[1]
                        elif i[0].startswith('TxGain'):
                            voipInfo['info']['Account']['txGain'] = i[1]
                        elif i[0].startswith('RxGain'):
                            voipInfo['info']['Account']['rxGain'] = i[1]
                        # elif i[0].startswith('EchoCancellation'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['echoCancellation'] = i[2]
                        elif i[0].startswith('CallWaiting'):
                            voipInfo['info']['Account']['callWaiting'] = i[1]
                        #
                        # ###INFORMAÇÕES DSO CODECS

                for i in list_out[64:69]:
                    print(i)
                    if i[1].startswith(' (0)'):
                        print(i)
                        voipInfo['info']['Codec']['codec-1'] = i[1][5:]
                    elif i[1].startswith(' (1)'):
                        voipInfo['info']['Codec']['codec-2'] = i[1][5:]
                    elif i[1].startswith(' (2)'):
                        voipInfo['info']['Codec']['codec-3'] = i[1][5:]

                ###INFORMAÇÕES REDE GPON
                # voipInfo['info']['Network'] = 'Vivo_1'

                voipInfo['Result'] = 'OK'
                voipInfo['Exception'] = 'OK'
                return voipInfo
            else:
                print('Sem linha VoIP')
                for key in raw_list:
                    list = re.sub('  +', '', key)
                    list = list.split(':')
                    # print(list)
                    if len(list) > 1:
                        # print(key)
                        ###INFORMAÇÕES VOICE PROFILE
                        if list[0].startswith('BoundIfName'):
                            voipInfo['info']['Voice_Profile']['ifName'] = list[1]
                        elif list[0].startswith('IPAddress'):
                            voipInfo['info']['Voice_Profile']['ipAddr'] = list[1]
                        # elif list[0].startswith('IPAddress'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['ipVersion'] = list[4]
                        # elif list[0].startswith('Management'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['manageProtocol'] = list[3]
                        # elif list[0].startswith('Associated'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['voiceProfile'] = list[3]
                        # elif list[0].startswith('ActivationStatus'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['profileState'] = list[1]
                        elif list[0].startswith('Region (Locale)'):
                            voipInfo['info']['Voice_Profile']['local'] = list[1]
                        elif list[0].startswith('DTMFMethod'):
                            voipInfo['info']['Voice_Profile']['dtmfMethod'] = list[1]
                        # elif list[0].startswith('HookFlashMethod'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['hookFlashMethod'] = list[2]
                        elif list[0].startswith('T38'):
                            voipInfo['info']['Voice_Profile']['T38'] = list[1]
                        # elif list[0].startswith('V18'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['V18'] = list[2]
                        elif list[0].startswith('RTPDSCPMark'):
                            voipInfo['info']['Voice_Profile']['rtpDscpMark'] = list[1]
                        # elif list[0].startswith('RTPPortMin'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['rtpPortMin'] = list[2]
                        # elif list[0].startswith('RTPPortMax'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['rtpPortMax'] = list[2]
                        elif list[0].startswith('Domain'):
                            voipInfo['info']['Voice_Profile']['domain'] = list[1]
                        elif list[0].startswith('Port'):
                            voipInfo['info']['Voice_Profile']['port'] = list[1]
                        elif list[0].startswith('Transport'):
                            voipInfo['info']['Voice_Profile']['transport'] = list[1]
                        elif list[0].startswith('RegExpires'):
                            voipInfo['info']['Voice_Profile']['regExpires'] = list[1]
                        elif list[0].startswith('RegRetryInterval'):
                            voipInfo['info']['Voice_Profile']['regRetriveInterval'] = list[1]
                        elif list[0].startswith('DSCPMark'):
                            voipInfo['info']['Voice_Profile']['dscpMark'] = list[1]
                        elif list[0].startswith('Registrar Addr'):
                            voipInfo['info']['Voice_Profile']['addrRegister'] = list[1]
                        elif list[0].startswith('Registrar Port'):
                            voipInfo['info']['Voice_Profile']['portRegister'] = list[1]
                        elif list[0].startswith('Proxy Addr'):
                            voipInfo['info']['Voice_Profile']['addrProxy'] = list[1]
                        elif list[0].startswith('Proxy Port'):
                            voipInfo['info']['Voice_Profile']['portProxy'] = list[1]
                        elif list[0].startswith('OutBoundProxy Addr'):
                            voipInfo['info']['Voice_Profile']['outboundProxyAddr'] = list[1]
                        elif list[0].startswith('OutBoundProxy Port'):
                            voipInfo['info']['Voice_Profile']['outboundProxyPort'] = list[1]
                        # elif list[0].startswith('Conferencing') and list[1].startswith('URI'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['uriConference'] = list[3]
                        # elif list[0].startswith('Conferencing') and list[1].startswith('Option'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Voice_Profile']['optionConference'] = list[3]
                        #
                        # ###INFORMAÇÕES LINHA SIP
                        # elif list[0].startswith('ActivationStatus'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['lineEnableState'] = list[1]
                        # elif list[0].startswith('VoipServiceStatus'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['voipServiceStatus'] = list[1]
                        # elif list[0].startswith('PolarityReverseState'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['reverserPolarity'] = list[2]
                        # elif list[0].startswith('CallStatus'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['callStatus'] = list[1]
                        # elif list[0].startswith('Associated'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['physicalReference'] = list[3]
                        # elif list[0].startswith('URI'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['uri'] = list[1]
                        # elif list[0].startswith('Extension'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['number'] = list[1]
                        # elif list[0].startswith('AuthName'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['authName'] = list[1]
                        # elif list[0].startswith('AuthPwd'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['authPwd'] = list[1]
                        # elif list[0].startswith('TxGain'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['txGain'] = list[1]
                        # elif list[0].startswith('RxGain'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['rxGain'] = list[1]
                        # elif list[0].startswith('EchoCancellation'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['echoCancellation'] = list[2]
                        # elif list[0].startswith('CallWaiting'):  #### NÃO RESPONDE ESSA INFO
                        #     voipInfo['info']['Account']['callWaiting'] = list[1]
                        #
                        # ###INFORMAÇÕES DSO CODECS
                        # elif list[0].startswith('CodecList'):
                        #     voipInfo['info']['Codec']['codec-1'] = list[3]
                        # elif list[0].startswith('(1)'):
                        #     voipInfo['info']['Codec']['codec-2'] = list[1]
                        # elif list[0].startswith('(2)'):
                        #     voipInfo['info']['Codec']['codec-3'] = list[1]

                ###INFORMAÇÕES REDE GPON
                # voipInfo['info']['Network'] = 'Vivo_1'

                voipInfo['Result'] = 'OK'
                voipInfo['Exception'] = 'OK'
                return voipInfo
        except Exception as error:
            voipInfo['Result'] = 'NOK'
            voipInfo['Exception'] = error

            return voipInfo


    ####Verificar Info Básicas do WiFi 2.4G
    def getWiFi2Gligth(self, out_str):

        ###Entrada: >show wifi

        raw_list = out_str.splitlines()

        del raw_list[0]
        del raw_list[0]

        infoWiFi2G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi0_status':
                        infoWiFi2G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        infoWiFi2G['info']['ssid'] = list[2]
                    elif list[1] == 'bssid':
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi2G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi2G['info']['password'] = list[2]

            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = 'ERRO AO GERAR INFO BASICA 2.4GHz', error

            return infoWiFi2G

        ###### Verificar Device Info ######


    ####Verificar Info Básicas do WiFi 5G
    def getWiFi5Gligth(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        del raw_list[0]
        del raw_list[0]

        infoWiFi5G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus0_status':
                        infoWiFi5G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        infoWiFi5G['info']['ssid'] = list[2]
                    elif list[1] == 'bssid':
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi5G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi5G['info']['password'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            return infoWiFi5G

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz', error

            return infoWiFi5G


    ###### Verificar Device Info com Info do MDM######
    def verifyHguHardware(self, out_str):
        resultado = {
            'CPU': {
                'Used': '',
                'Free': ''
            },
            'MEMORIA': {
                'Used': '',
                'Free': ''
            },
            'TOP': {
                'Load average': {
                    '#1': '',
                    '#2': '',
                    '#3': ''
                },
                'Processos': {
                    '#1': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#2': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#3': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#4': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#5': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    }
                }
            },
            'VALIDATION': {
                'CPU': {},
                'MEMORIA': {},
                'GERAL': {}
            },
            'Result': {},
            'Exception': {}
        }
        try:
            # print(out_str)
            list_cpu = out_str[0].split('\r\n')
            # print(list)
            for i in list_cpu:
                if i.startswith('used'):
                    resultado['CPU']['Used'] = int(re.findall(r'(\d+)', i)[0])
                elif i.startswith('free'):
                    resultado['CPU']['Free'] = int(re.findall(r'(\d+)', i)[0])

            list_memory = out_str[1].split('\r\n')
            # print(list)
            for i in list_memory:
                if i.startswith('percentaje_used'):
                    resultado['MEMORIA']['Used'] = int(re.findall(r'(\d+)', i)[0])
                elif i.startswith('percentaje_free'):
                    resultado['MEMORIA']['Free'] = int(re.findall(r'(\d+)', i)[0])

            out_str[2] = re.sub('<', '', out_str[2])
            list_top = out_str[2].split('\r\n')
            # print(list)
            aux_out = []
            for i in list_top:
                # print(i)
                if i.startswith('Load average'):
                    aux = i.split(' ')
                    aux_out.append(aux)
            # print(aux_out[0][2])
            resultado['TOP']['Load average']['#1'] = float(aux_out[0][2])
            resultado['TOP']['Load average']['#2'] = float(aux_out[0][3])
            resultado['TOP']['Load average']['#3'] = float(aux_out[0][4])

            aux_out = []
            for i in list_top[3:]:
                # print(i.split())
            #     i = re.sub('  +', ' ', i)
                aux1 = i.split()
                aux_out.append(aux1)
            # print(aux_out)
            resultado['TOP']['Processos']['#1']['PID'] = aux_out[1][0]
            resultado['TOP']['Processos']['#1']['PPID'] = aux_out[1][1]
            resultado['TOP']['Processos']['#1']['USER'] = aux_out[1][2]
            resultado['TOP']['Processos']['#1']['STAT'] = aux_out[1][3]
            resultado['TOP']['Processos']['#1']['VSZ'] = aux_out[1][4]
            resultado['TOP']['Processos']['#1']['%VSZ'] = aux_out[1][5]
            resultado['TOP']['Processos']['#1']['%CPU'] = aux_out[1][6]
            resultado['TOP']['Processos']['#1']['COMMAND'] = aux_out[1][7:]

            resultado['TOP']['Processos']['#2']['PID'] = aux_out[2][0]
            resultado['TOP']['Processos']['#2']['PPID'] = aux_out[2][1]
            resultado['TOP']['Processos']['#2']['USER'] = aux_out[2][2]
            resultado['TOP']['Processos']['#2']['STAT'] = aux_out[2][3]
            resultado['TOP']['Processos']['#2']['VSZ'] = aux_out[2][4]
            resultado['TOP']['Processos']['#2']['%VSZ'] = aux_out[2][5]
            resultado['TOP']['Processos']['#2']['%CPU'] = aux_out[2][6]
            resultado['TOP']['Processos']['#2']['COMMAND'] = aux_out[2][7:]

            resultado['TOP']['Processos']['#3']['PID'] = aux_out[3][0]
            resultado['TOP']['Processos']['#3']['PPID'] = aux_out[3][1]
            resultado['TOP']['Processos']['#3']['USER'] = aux_out[3][2]
            resultado['TOP']['Processos']['#3']['STAT'] = aux_out[3][3]
            resultado['TOP']['Processos']['#3']['VSZ'] = aux_out[3][4]
            resultado['TOP']['Processos']['#3']['%VSZ'] = aux_out[3][5]
            resultado['TOP']['Processos']['#3']['%CPU'] = aux_out[3][6]
            resultado['TOP']['Processos']['#3']['COMMAND'] = aux_out[3][7:]

            resultado['TOP']['Processos']['#4']['PID'] = aux_out[4][0]
            resultado['TOP']['Processos']['#4']['PPID'] = aux_out[4][1]
            resultado['TOP']['Processos']['#4']['USER'] = aux_out[4][2]
            resultado['TOP']['Processos']['#4']['STAT'] = aux_out[4][3]
            resultado['TOP']['Processos']['#4']['VSZ'] = aux_out[4][4]
            resultado['TOP']['Processos']['#4']['%VSZ'] = aux_out[4][5]
            resultado['TOP']['Processos']['#4']['%CPU'] = aux_out[4][6]
            resultado['TOP']['Processos']['#4']['COMMAND'] = aux_out[4][7:]

            resultado['TOP']['Processos']['#5']['PID'] = aux_out[5][0]
            resultado['TOP']['Processos']['#5']['PPID'] = aux_out[5][1]
            resultado['TOP']['Processos']['#5']['USER'] = aux_out[5][2]
            resultado['TOP']['Processos']['#5']['STAT'] = aux_out[5][3]
            resultado['TOP']['Processos']['#5']['VSZ'] = aux_out[5][4]
            resultado['TOP']['Processos']['#5']['%VSZ'] = aux_out[5][5]
            resultado['TOP']['Processos']['#5']['%CPU'] = aux_out[5][6]
            resultado['TOP']['Processos']['#5']['COMMAND'] = aux_out[5][7:]

            ### VALIDATION
            if resultado['CPU']['Free'] >= 50:
                resultado['VALIDATION']['CPU'] = 'OK'
            else:
                resultado['VALIDATION']['CPU'] = 'NOK'
            if resultado['MEMORIA']['Free'] >= 8:
                resultado['VALIDATION']['MEMORIA'] = 'OK'
            else:
                resultado['VALIDATION']['MEMORIA'] = 'NOK'
            if resultado['VALIDATION']['CPU'] == 'OK' and resultado['VALIDATION']['MEMORIA'] == 'OK':
                resultado['VALIDATION']['GERAL'] = 'OK'
            else:
                resultado['VALIDATION']['GERAL'] = 'NOK'

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ####Verificar Info Básicas do WiFi 2.4G
    def getWiFi2Gligth(self, out_str):

        ###Entrada: >show wifi

        raw_list = out_str.splitlines()
        print(raw_list)

        del raw_list[0]
        del raw_list[0]

        infoWiFi2G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                # print(list)
                if len(list) > 1:
                    if list[0] == 'wifi0_status':
                        infoWiFi2G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        infoWiFi2G['info']['ssid'] = list[2]
                    elif list[1] == 'bssid':
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi2G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi2G['info']['password'] = list[2]

            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = 'ERRO AO GERAR INFO BASICA 2.4GHz', error

            return infoWiFi2G


    def netinf(self, canal, limiares, fmw):
        resultado = {
            'testes': [],
            'Result': '',
            'Exception': '',
            'Description': ''
        }

        erro = ''
        falha_detectada = False

        testes = []

        limiar_per = limiares['per_max']
        limiar_potencia_minima = limiares['potencia_minima']
        limiar_taxa_minima = limiares['taxa_minima']

        try:
            with SSHClientInteraction(canal, timeout=5, display=False) as interact:
                # verifica o mac do HGU
                interact.expect('>')
                interact.send('ifconfig eth0')
                interact.expect('>')
                saida_cmd = interact.current_output_clean
                maceth = ProcuraVal(' HWaddr (.+?)\n', saida_cmd)

                # verifica o IP da LAN (gateway)
                interact.send('ifconfig br0')
                interact.expect('>')
                saida_cmd = interact.current_output_clean
                gateway = ProcuraVal('inet addr:(.+?) +Bcast', saida_cmd)
                #print(maceth + " " + gateway)

                # verifica opção para execução do Netinf
                interact.send('engDbgtef 1 ' + maceth)
                interact.expect('>')
                interact.send('sh')
                interact.expect('# ')
                interact.send('netinf')
                interact.expect('please select network interface: ')
                saida_cmd = interact.current_output_clean
                opcao_netinf = ProcuraVal('^(.+?)\) +' + gateway, saida_cmd)

                # executa netinf
                interact.send(opcao_netinf)
                print("# netinf - Selecionada a opção " + str(opcao_netinf) + ".")
                interact.timeout = 120
                interact.expect('# ')

                # analisa a saída
                saida_cmd = interact.current_output_clean
                raw_list = saida_cmd.splitlines()

                for linha in raw_list:
                    erro_pontual = ""
                    if linha.startswith("ETC"):
                        tokens = linha.split()

                        nos = tokens[5].split("-->")
                        transmitter = nos[0][:17]
                        receiver = nos[1][:17]

                        if (eh_macaddr(transmitter) == False or eh_macaddr(receiver) == False):
                            print("transmitter / receiver inválidos --> " + transmitter + " " + receiver)
                            continue

                        per = ProcuraVal(' per: +(.+?) +', linha)
                        snr = ProcuraVal(' snr +(.+?) +dB', linha)
                        rate = ProcuraVal(' rate: +(.+?) +Rx', linha)
                        rx_power = ProcuraVal(' Rx power: +(.+?)$', linha)

                        per_n = float(per.replace("%",""))
                        if (per_n is False):
                            print("per inválido:" + str(per) + " " + str(per_n))
                            erro_pontual += "PER inválido,"
                        elif (per_n > limiar_per):
                            erro_pontual += "taxa de erro (PER) acima de " + str(limiar_per) + ","

                        rate_n = float(ProcuraVal('^(.+?)Mbps', rate))
                        if (rate_n is False):
                            erro_pontual += "Rate inválido,"
                        elif (rate_n < limiar_taxa_minima):
                            erro_pontual += "taxa de transmissão abaixo de " + str(limiar_taxa_minima) + " Mbps,"

                        rx_power_n = float(rx_power.replace("dBm", ""))
                        #print("passou1 " + str(rx_power_n) + " " + str(limiar_potencia_minima))
                        if (rx_power_n is False):
                            erro_pontual += "RX power inválido,"
                        elif (rx_power_n < limiar_potencia_minima):
                            erro_pontual += "potência de RX abaixo de " + str(limiar_potencia_minima) + " dBm,"

                        Result = ""
                        Description = ""

                        if (erro_pontual != ''):
                            erro += erro_pontual
                            falha_detectada = True
                            Result = "NOK"
                            Description = str(erro_pontual)
                        else:
                            Result = "OK"
                            Description = "OK"

                        testes.append({
                            "transmitter": transmitter,
                            "receiver": receiver,
                            "PER": per,
                            "Rate": rate,
                            "SNR (db)": snr,
                            "RX power": rx_power,
                            "Result": Result,
                            "Description": Description
                        })

                if (len(testes) == 0):
                    resultado['testes'] = testes
                    resultado["Result"] = "OK"
                    resultado["Exception"] = "OK"
                    resultado["Description"] = "Nenhum STB foi detectado na rede HPNA durante os testes."
                elif (falha_detectada == True):
                    resultado['testes'] = testes
                    resultado["Result"] = "NOK"
                    resultado["Exception"] = "NOK"
                    resultado["Description"] = "O teste da rede HPNA (Netinf) obteve valores fora do recomendado."
                else:
                    resultado['testes'] = testes
                    resultado["Result"] = "OK"
                    resultado["Exception"] = "OK"
                    resultado["Description"] = "O teste da rede HPNA (Netinf) obteve valores dentro do recomendado."

        except Exception as e:
            resultado['testes'] = testes
            resultado['Result'] = "NOK"
            resultado['Exception'] = str(e)
            resultado['Description'] = "Erro ao executar o Netinf."

        return resultado


    def ip_porta(self, out_str, modelo, ip_oct_de, ip_oct_ate, fmw=''):
        # mapeamento IP para porta
        # Entrada: 'lanhosts show all'

        raw_list = out_str.splitlines()

        ip_porta = {'Result': '', 'Exception': '', 'Description': ''}

        try:
            #if fmw in ['BR_g5.8_1.11(WVK.0)b29','VBR_g5.8_1.11(WVK.0)b29']:
            for key in raw_list:
                if (key.startswith("lanhosts") or key.startswith("Bridge") or key.startswith("Active") or key.startswith(">") or key.strip() == ""):
                    continue
                else:
                    disp = key.split()
                    print(str(key) + " " + str(disp))

                    ip_disp = disp[2]
                    ip_disp_ult_oct = int(ip_disp.split(".")[3])

                    if (ip_disp_ult_oct < ip_oct_de or ip_disp_ult_oct > ip_oct_ate):
                        continue

                    porta_disp = disp[3]
                    porta = ""

                    if (porta_disp == "WiFi"):
                        porta = "wifi5"
                    elif (modelo.startswith('GPT-2731') == True):
                        if (porta_disp == "LAN1"):
                            porta = "hpna"
                        elif (porta_disp == "LAN2"):
                            porta = "eth1"
                        elif (porta_disp == "LAN3"):
                            porta = "eth2"
                        elif (porta_disp == "LAN4"):
                            porta = "eth3"
                    else:
                        if (porta_disp == "LAN1"):
                            porta = "eth1"
                        elif (porta_disp == "LAN2"):
                            porta = "eth2"
                        elif (porta_disp == "LAN3"):
                            porta = "eth3"
                        elif (porta_disp == "LAN4"):
                            porta = "eth4"

                    ip_porta[ip_disp]={}
                    ip_porta[ip_disp].update({"porta_hgu": porta, "mac": disp[1]})
            #else:
                # print("Firmware HGU:" + fmw)
                # ip_porta['Result'] = 'NOK'
                # ip_porta['Description'] = 'Firmware do HGU não suportado para teste de IPTV.'
                # ip_porta['Exception'] = 'NOK'
        except Exception as e:
            ip_porta['Result'] = 'NOK'
            ip_porta['Description'] = 'Erro ao mapear os IPs e portas do HGU.'
            ip_porta['Exception'] = e

        if (ip_porta['Result'] != 'NOK'):
            ip_porta['Result'] = 'OK'
            ip_porta['Description'] = 'OK'
            ip_porta['Exception'] = 'OK'

        return ip_porta


    ###### Listar DHCP CONDSETTINGS HGU ######
    def getDhcpCondSettingsHgu(self, output_str):

        # Entrada: dhcpcondserv show

        resultado = {
            'Enable': '',
            'Vendor Class ID Exclude': '',
            'Vendor Class ID mode': '',
            'Vendor Class ID': '',
            'Start IP Address': '',
            'End IP Address': '',
            'Subnet Mask': '',
            'DNS Server1': '',
            'DNS Server2': '',
            'Gateway Address': '',
            'Leased Time': '',
            '[v] 1.Option 240': {
                'value': '',
                'value64': ''
            },
            'Result': {},
            'Exception': {}
        }

        try:
            resultado['Enable'] = ProcuraVal('Enable: +(.+?)\n', output_str)
            resultado['Vendor Class ID Exclude'] = ProcuraVal('Vendor Class ID Exclude: +(.+?)\n', output_str)
            resultado['Vendor Class ID mode'] = ProcuraVal('Vendor Class ID mode: +(.+?)\n', output_str)
            resultado['Vendor Class ID'] = ProcuraVal('Vendor Class ID: +(.+?)\n', output_str)
            resultado['Start IP Address'] = ProcuraVal('Start IP Address: +(.+?)\n', output_str)
            resultado['End IP Address'] = ProcuraVal('End IP Address: +(.+?)\n', output_str)
            resultado['Subnet Mask'] = ProcuraVal('Subnet Mask: +(.+?)\n', output_str)
            resultado['DNS Server1'] = ProcuraVal('DNS Server1: +(.+?)\n', output_str)
            resultado['DNS Server2'] = ProcuraVal('DNS Server2: +(.+?)\n', output_str)
            resultado['Gateway Address'] = ProcuraVal('Gateway Address: +(.+?)\n', output_str)
            resultado['Leased Time'] = ProcuraVal('Leased Time: +(.+?)\n', output_str)
            resultado['[v] 1.Option 240']['value'] = ProcuraVal('Option 240:\r\n +value:(.+?)\n', output_str)
            resultado['[v] 1.Option 240']['value64'] = ProcuraVal('\n +value64: +(.+?)\n', output_str)

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = 'ERRO AO CONSULTAR dhcpCondSettings'

        return resultado


    ###### Listar INFO IFCONFIG ######
    def getIfconfig(self, output_str):

        # Entrada: ifconfig

        infoIface = {
            'interfaces': {
                'internet': {},
                'voip': {},
                'vod': {}
            },
            'Result': '',
            'Exception': ''
        }

        try:

            raw_data = output_str.splitlines()

            tag_ppp0 = False
            tag_vod = False
            tag_voip = False
            tag_ipv6 = True

            for k in raw_data:
                info = k.split()

                if 'ppp0' in info or tag_ppp0:
                    try:
                        tag_ppp0 = True
                        if len(info) == 0:
                            tag_ppp0 = False
                        else:
                            if 'inet' in info:
                                ipv4 = info[1].split(':')
                                ipv4 = ipv4[1]
                                infoIface['interfaces']['internet']['ipv4'] = ipv4
                            elif 'inet6' in info:
                                if tag_ipv6:
                                    infoIface['interfaces']['internet']['ipv6'] = info[2]
                                    tag_ipv6 = False
                            elif 'UP' in info:
                                infoIface['interfaces']['internet']['status'] = 'UP'
                    except:
                        pass

                elif 'nas1' in info or tag_voip:
                    try:
                        tag_voip = True
                        if len(info) == 0:
                            tag_voip = False
                        else:
                            if 'inet' in info:
                                print(info)
                                ipv4 = info[1].split(':')
                                ipv4 = ipv4[1]
                                infoIface['interfaces']['voip']['ipv4'] = ipv4
                            elif 'UP' in info:
                                infoIface['interfaces']['voip']['status'] = 'UP'
                    except:
                        pass

                elif 'nas2' in info or tag_vod:
                    try:
                        tag_vod = True
                        if len(info) == 0:
                            tag_vod = False
                        else:
                            if 'inet' in info:
                                print(info)
                                ipv4 = info[1].split(':')
                                ipv4 = ipv4[1]
                                infoIface['interfaces']['vod']['ipv4'] = ipv4
                            elif 'UP' in info:
                                infoIface['interfaces']['vod']['status'] = 'UP'
                    except:
                        pass

            infoIface['Result'] = 'OK'
            infoIface['Exception'] = 'OK'

        except Exception as error:
            infoIface['Result'] = 'NOK'
            infoIface['Exception'] = 'ERRO AO CONSULTAR dhcpCondSettings'
            print(error)

        return infoIface


    ####Verificar status interface OMCI
    def getStatusOnt(self, out_str):

        ###Entrada: >ponportstatus

        info_onu = {
            'onu_status': '',
            'slid': '',
            'serial_gpon': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            line = 0
            for key in raw_list:
            #     line = line + 1
                lista = key.split()
            #
                if len(lista) > 1:
                    if lista[1].strip().startswith('State'):
                        print(lista)
                        status = str(lista[2].strip())
                        if status == 'O5':
                            info_onu['onu_status'] = 'Operation'
                        elif status == 'O4':
                            info_onu['onu_status'] = 'Ranging'
                        elif status == 'O3' or status == 'O2':
                            info_onu['onu_status'] = 'SN Aquisition'
                        elif status == 'O1':
                            info_onu['onu_status'] = 'Syncronization'
                        elif status == 'O6':
                            info_onu['onu_status'] = 'Intermittent LODS'
                        elif status == 'O7':
                            info_onu['onu_status'] = 'Emergency Stop'
                        else:
                            info_onu['onu_status'] = 'Failure '

                    elif lista[0].strip().startswith('ASCII'):
                        info_onu['slid'] = lista[1].strip('\u0001')
            #
                    elif lista[0].startswith('SN'):
                        info_onu['serial_gpon'] = str(lista[1].strip())

            info_onu['Result'] = 'OK'
            info_onu['Exception'] = 'OK'

        except Exception as error:
            info_onu['Result'] = 'NOK'
            info_onu['Exception'] = error

        return info_onu


    def getWiFi5GligthBS(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()
        print(raw_list)

        # del raw_list[0]
        # del raw_list[0]

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        print(list)
                        plus_size = (len(list) - len_default) + 1
                        print(plus_size)
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name

                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'


        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS', error

        return infoWiFi5G_BS


    def getWiFi5GBS(self, out_str):

        print(out_str)

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': '',
            'hide': '',
            'authentication': '',
            'encryption': '',
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name
                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'hide':
                        infoWiFi5G_BS['info']['hide'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'authentication':
                        infoWiFi5G_BS['info']['authentication'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'encryption':
                        infoWiFi5G_BS['info']['encryption'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'

        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS'

        return infoWiFi5G_BS


class cliAskeyEcnt():
    def __init__(self, password, ip):
        self.user_support = 'support'
        self.password = password
        self.ip = ip

    ######Listar detalhes do dipositivo######
    def version(self, out_str):

        ##--> aspcm_util show_module_info

        info_hgu = {'Model': '',
                    'Profile': '',
                    'Booted Partition': '',
                    'Partition 1 Version': '',
                    'Partition 2 Version': '',
                    'firmware': '',
                    'brcm_release': '',
                    'bootbase': '',
                    'serialNumber': '',
                    'macAddress': '',
                    'vendor': '',
                    'Result': '',
                    'Exception': ''}

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                list = key.split('=')
                if list[0].startswith('hw_model_name'):
                    info_hgu['Model'] = list[1].strip()

                elif list[0].startswith('img_active'):
                    img_active = list[1].strip()

                elif list[0].startswith('tef_img_version_0'):
                    fw_ax_0 = list[1].strip()

                elif list[0].startswith('tef_img_version_1'):
                    fw_ax_1 = list[1].strip()

                elif list[0].startswith('ethaddr'):
                    mac = list[1].strip()
                    info_hgu['macAddress'] = mac

                    serial_aux = mac.split(':')
                    serial = ''
                    for i in serial_aux:
                        serial = serial + i

                    info_hgu['serialNumber'] = serial

                info_hgu['vendor'] = 'Askey'
            if img_active == '0':
                info_hgu['firmware'] = fw_ax_0
            else:
                info_hgu['firmware'] = fw_ax_1

            info_hgu['Result'] = 'OK'
            info_hgu['Exception'] = 'OK'

        except Exception as error:
            info_hgu['Result'] = 'NOK'
            info_hgu['Exception'] = error

        return info_hgu


    ######Listar dispositivos na tabela DHCP######
    def dhcp_table(self, out_str):

        # Entrada: 'show map_info dhcp_table'

        raw_list = out_str.splitlines()
        # print(raw_list)

        qtde_eth = int(0)
        count_eth = int(0)
        qtde_hpna = int(0)
        count_hpna = int(0)
        qtde_4 = int(0)
        count_wifi24 = int(0)
        qtde_5 = int(0)
        count_wifi5 = int(0)
        count_bp_ap = int(0)
        count_bp_rep = int(0)
        count_hosts = int(0)

        tabela_host = {"qtde_hosts": "",
                       "qtde_eth": qtde_eth,
                       "qtde_hpna": qtde_hpna,
                       "qtde_wifi24": qtde_4,
                       "qtde_wifi5": qtde_5,
                       "interface": {},
                       "bp": {
                           'repeater': {},
                           'ap': {},
                       },
                       "Result": '',
                       "Exception": ''}

        try:

            fmw = 'OK'

            if fmw == 'OK':
                for key in raw_list:
                    list_tab = key.split('\t')
                    list_spa = key.split()

                    if len(list_spa) > 4:

                        if 'WiFi' in list_spa:
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ####CONTABILIZAR SE DEVICES EM 2.4GHz & 5GHz
                            tabela_host["interface"][count_iface]["radio"] = list_spa[5]
                            if list_spa[5] == '5':
                                count_wifi5 = count_wifi5 + 1
                            else:
                                count_wifi24 = count_wifi24 + 1

                            ###TRATAMENTO DE HOSTNAME E SSID PARA DIFERENTES SAIDAS

                            ###SOMENTE SSID SEM HOSTNAME (LEN 6)
                            if len(list_tab) == 6:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]

                            ###SSID & HOSTNAME (LEN 7)
                            elif len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]

                                hostname_wifi = list_tab[6].rstrip('\x00')
                                hostname_wifi = list_tab[6].rstrip('\u0000')
                                tabela_host["interface"][count_iface]["hostname"] = hostname_wifi

                                ####CONSTRUÇÃO DA TABELA DE BPs NO MODO REPEATER
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_rep = count_bp_rep + 1
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['ipaddr'] = list_tab[
                                        0]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['macaddr'] = list_tab[
                                        1]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['dhcp_mode'] = \
                                        list_tab[2]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['leasetime'] = \
                                        list_tab[3]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['media'] = list_spa[4]

                                    hostname_rep = list_tab[6].rstrip('\x00')
                                    hostname_rep = list_tab[6].rstrip('\u0000')
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)][
                                        'hostname'] = hostname_rep

                        elif 'Ethernet' in list_spa:
                            count_bp_ap = 0
                            count_eth = count_eth + 1
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ###TRATAMENTO DE HOSTNAME PARA DIFERENTES SAIDAS
                            if len(list_tab) == 7:
                                hostname_7 = list_tab[6].rstrip('\x00')
                                hostname_7 = list_tab[6].rstrip('\u0000')
                                tabela_host["interface"][count_iface]["hostname"] = hostname_7

                                ####CONSTRUÇÂO DA TABELA DE BPs NO MODO AP
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_ap = count_bp_ap + 1
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }

                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['ipaddr'] = list_tab[0]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['macaddr'] = list_tab[1]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['dhcp_mode'] = list_tab[2]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['leasetime'] = list_tab[3]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['media'] = list_spa[4]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['hostname'] = list_tab[6]

                        # HPNA
                        elif 'HPNA' in list_spa:
                            count_hpna = count_hpna + 1
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]
                        # fim HPNA

                tabela_host['qtde_hosts'] = str(count_hosts)
                tabela_host['qtde_eth'] = str(count_eth)
                tabela_host['qtde_hpna'] = str(count_hpna)
                tabela_host['qtde_wifi24'] = str(count_wifi24)
                tabela_host['qtde_wifi5'] = str(count_wifi5)

                tabela_host['Result'] = 'OK'
                tabela_host['Exception'] = 'OK'

        except Exception as error:
            print(error)
            tabela_host['Result'] = 'NOK'
            tabela_host['Exception'] = 'ERRO GERAÇÃO TABELA HOST ASKEY ECNT'


        return tabela_host


    ######Listar dispositivos conectados no WiFi Plus######
    def wifiplus_table(self, out_str, fmw='BR_SV_g12.6_RTF_TEF001_V7.15_V015'):
        # Entrada: show map_info wifi_plus station_info

        info_wifiplus = {
            'wifi_stations': {},
            'base_port': {},
            'qty_bp_rep': '',
            'Results': '',
            'Exception': ''}

        try:

            raw_list = out_str.splitlines()

            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Askey Econet
            askey_ecnt_model = devices['supported']['askey_ecnt_model']
            askey_ecnt_fw = devices['supported']['askey_ecnt_fw']

            if fmw in askey_ecnt_fw:
                count_bp_rep = 0
                for key in raw_list:
                    if re.match(r'(^[0-9]{2})', key):
                        list = key.split('\t')
                        list_aux = []
                        for item in list:
                            item_aux = item.rstrip('\x00')
                            list_aux.append(item_aux)
                        if len(list) == 2:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list_aux[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list_aux[1]

                        elif len(list) == 3:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list_aux[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list_aux[1]
                            info_wifiplus['wifi_stations'][list[1]]['hostname'] = list_aux[2]

                        elif len(list) > 3:
                            if list_aux[3].startswith('BP2'):
                                count_bp_rep = count_bp_rep + 1
                                info_wifiplus['base_port'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['base_port'][list[1]]['ip_addr'] = list_aux[0]
                                info_wifiplus['base_port'][list[1]]['mac_addr'] = list_aux[1]
                                info_wifiplus['base_port'][list[1]]['ssid'] = list_aux[2]
                                info_wifiplus['base_port'][list[1]]['hostname'] = list_aux[3]
                                info_wifiplus['base_port'][list[1]]['rssi'] = list_aux[4]

                            else:
                                info_wifiplus['wifi_stations'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list_aux[0]
                                info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list_aux[1]
                                info_wifiplus['wifi_stations'][list[1]]['ssid'] = list_aux[2]
                                info_wifiplus['wifi_stations'][list[1]]['hostname'] = list_aux[3]
                                info_wifiplus['wifi_stations'][list[1]]['rssi'] = list_aux[4]

                info_wifiplus['qty_bp_rep'] = count_bp_rep
                info_wifiplus['Results'] = 'OK'
                info_wifiplus['Exception'] = 'OK'

                return info_wifiplus

            else:
                info_wifiplus['Results'] = 'NOK'
                info_wifiplus['Exception'] = 'NAO ENCONTRADO FIRMWARE COMPATIVEL'

                return info_wifiplus

        except Exception as error:
            info_wifiplus['Results'] = 'NOK'
            info_wifiplus['Exception'] = 'ERRO NA GERACAO DA TABELA DE DEVICES WIFI 5G', error

            return info_wifiplus


    ######Listar informacoes WiFi 5GHz######
    def getWiFi5G(self, out_str):

        ###Entrada: >show wifi_plus all
        ###Necessário tempo maior para retorno do SSH

        raw_list = out_str.splitlines()

        del raw_list[0]

        infoWiFi5G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': '',
            'qhop': '',
            'beamforming': '',
            'scs': '',
            'airfair': '',
            'maui': '',
            'mumimo': '',
            'wifi_plus0_status': '',
            'roaming': ''

        },
            'Result': '',
            'Exception': ''}

        try:

            for key in raw_list:
                list = key.split()
                # print(list)
                if len(list) > 1:
                    if list[1].startswith('bandwidth'):
                        infoWiFi5G['info']['bandwidth'] = list[2]
                        # print(list[2])
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi5G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi5G['info']['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi5G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        infoWiFi5G['info']['ssid'] = list[2]
                    elif list[1].startswith('bssid'):
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi5G['info']['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi5G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi5G['info']['password'] = list[2]
                    elif list[1].startswith('channel_mode'):
                        infoWiFi5G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('channel'):
                        if infoWiFi5G['info']['channel'] == '':
                            infoWiFi5G['info']['channel'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi5G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi5G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi5G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi5G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi5G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi5G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi5G['info']['region'] = list[2]
                    elif list[1].startswith('qhop') and len(list) == 3:
                        if infoWiFi5G['info']['qhop'] == '':
                            infoWiFi5G['info']['qhop'] = list[2]
                    elif list[1].startswith('beamforming'):
                        infoWiFi5G['info']['beamforming'] = list[2]
                    elif list[1].startswith('scs'):
                        infoWiFi5G['info']['scs'] = list[2]
                    elif list[1].startswith('airfair'):
                        infoWiFi5G['info']['airfair'] = list[2]
                    elif list[1].startswith('maui'):
                        infoWiFi5G['info']['maui'] = list[2]
                    elif list[1].startswith('mumimo'):
                        infoWiFi5G['info']['mumimo'] = list[2]
                    elif list[0].startswith('wifi_plus0_status'):
                        infoWiFi5G['info']['wifi_plus0_status'] = list[1]
                    elif list[1].startswith('roaming'):
                        infoWiFi5G['info']['roaming'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            return infoWiFi5G

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = error

            return infoWiFi5G


    ######Listar informacoes WiFi 2.4GHz######
    def getWiFi2G(self, out_str):

        ###Entrada: >show wifi all

        raw_list = out_str.splitlines()

        infoWiFi2G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': ''
        },
            'Result': '',
            'Exception': ''}

        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[1].startswith('bandwidth'):
                        infoWiFi2G['info']['bandwidth'] = list[2]
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi2G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi2G['info']['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi2G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        infoWiFi2G['info']['ssid'] = list[2]
                    elif list[1].startswith('bssid'):
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi2G['info']['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi2G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi2G['info']['password'] = list[2]
                    elif list[1].startswith('channel_mode'):
                        infoWiFi2G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi2G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi2G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi2G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi2G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi2G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi2G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi2G['info']['region'] = list[2]
                    ###TRATAMETNO DO CANAL 2.4GHz
                    elif list[1].startswith('channel') and len(list) == 3:
                        infoWiFi2G['info']['channel'] = list[2]

            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = error

            return infoWiFi2G


    ######Listar domínios e bssids criados######
    def roaming_bss(self, out_str, firmware, params):


        ####LISTA DE OUI DOS BASES PORTS EM PLANTA
        oui_bp_mitra = ['a4:33:d7', 'cc:ed:dc', 'd8:c6:78', '34:57:60', 'cc:d4:a1', '84:aa:9c']
        oui_bp_askey = ['94:91:7f', '1c:b0:44', '80:78:71']

        raw_list = out_str.splitlines()

        table_bssid = {"qty_domain": "",
                       "qty_baseport": "",
                       "qty_bssid_total": "",
                       "ssid-0000": '',
                       "ssid-aaaa": '',
                       "qty_bssid_2.4GHz": "",
                       "qty_bssid_5GHz": "",
                       "hgu": {
                           "fat_5G": "",
                           "fat_2G": ""
                       },
                       "base_port": {},
                       "bssid/domain":
                           {"BS": {},
                            'MAIN': {}
                            },
                       "bssids": {},
                       "Result": '',
                       "Exception": ''}

        try:
            ##--> Info devices Askey Econet
            askey_ecnt_model = params['devices']['supported']['askey_ecnt_model']
            askey_ecnt_fw = params['devices']['supported']['askey_ecnt_fw']

            firmware = 'OK'

            if firmware == 'OK':

                qty_bp = int(0)
                qty_domain = int(0)
                qty_bssid_total = int(0)
                qty_bssid_24 = int(0)
                qty_bssid_5 = int(0)

                count_bp = 0

                tag_domain_BS = False
                tag_domain_5 = False
                tag_domain_guest = False

                count_bssid_24 = 0
                count_bssid_5 = 0
                count_bssid_guest = 0

                count_domain_24 = 0
                count_domain_5_bs = 0
                count_domain_5_main = 0

                aux_basePort = {}
                mac_ref_table = []

                for key in raw_list:
                    list = key.split()
                    if len(list) > 5 and list[0].startswith('00'):
                        # print(list[1])
                        # index = list[0].strip('.')
                        index = list[1]
                        table_bssid["bssids"][index] = {"bssid": "",
                                                        "status": "",
                                                        "local": "",
                                                        "radio": "",
                                                        "channel": "",
                                                        "bandwidth": "",
                                                        "BSSTr": "",
                                                        "fat": "",
                                                        "domain": "",
                                                        "vendor": "",
                                                        "network": ""}
                        #
                        if list[3] == 'Yes':  # Indice 3 identifica o device a qual esta conectado o shell
                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['local'] = 'HGU'
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]

                            # -->Nova feature para identificação do MAC do BP
                            table_bssid["bssids"][index]['index_mac'] = 'HGU'

                            if list[10] == '0000' and list[4] == '2.4G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                table_bssid['ssid-0000'] = list[12]

                                # -->Nova feature para topologia mobile
                                table_bssid['hgu']['fat_2G'] = list[8]
                            elif list[10] == '0000' and list[4] == '5G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                            elif list[10] == 'aaaa':
                                table_bssid['bssids'][index]['network'] = 'Main_5G'
                                table_bssid['ssid-aaaa'] = list[12]

                                # -->Nova feature para topologia mobile
                                table_bssid['hgu']['fat_5G'] = list[8]
                            else:
                                table_bssid['bssids'][index]['network'] = 'Guest'


                        elif list[3] == 'No' and list[2] == 'UP':
                            mac_ref = list[9]

                            if mac_ref not in mac_ref_table:
                                count_bp = count_bp + 1
                                aux_basePort[mac_ref] = 'BP-' + str(count_bp)
                                table_bssid["bssids"][index]['local'] = "BP-" + str(count_bp)
                                mac_ref_table.append(mac_ref)

                                # -->Nova feature para identificação do MAC do BP
                                if list[10] != '':
                                    name_bp = 'BP-' + str(count_bp)
                                    mac_bp = mac_ref
                                    table_bssid['base_port'][name_bp] = mac_ref

                            else:
                                table_bssid["bssids"][index]['local'] = aux_basePort[mac_ref]

                            ####VALIDAR MODELO BP
                            oui = list[9][:8]

                            ###VALIDAR SE BP ASKEY
                            if oui in oui_bp_askey:  # Identificar modelo de base port Askey
                                table_bssid["bssids"][index]['vendor'] = "ASKEY"
                                if list[10].strip() == '0000' and list[4].strip() == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'


                            ###VALIDAR SE BP MITRA
                            elif oui in oui_bp_mitra:  # Identificar modelo de base port Mitra
                                table_bssid["bssids"][index]['vendor'] = "MITRA"
                                if list[10] == '0000' and list[4] == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'

                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]

                            # -->Nova feature para identificação do MAC do BP
                            table_bssid["bssids"][index]['index_mac'] = mac_ref
                        #
                        ###Verificar quantidade de Dominios

                        if list[10] == '0000' and list[2] == 'UP':
                            tag_domain_BS = True
                            if int(list[5]) < 14:
                                count_bssid_24 = count_bssid_24 + 1
                                count_domain_24 = count_domain_24 + 1
                            else:
                                count_bssid_5 = count_bssid_5 + 1
                                count_domain_5_bs = count_domain_5_bs + 1

                        elif list[10] == 'aaaa' and list[2] == 'UP':
                            tag_domain_5 = True
                            count_bssid_5 = count_bssid_5 + 1
                            count_domain_5_main = count_domain_5_main + 1

                        elif (list[10] != '0000' or list[10] != 'aaaa') and list[2] == 'UP':
                            tag_domain_guest = True
                            count_bssid_guest = count_bssid_guest + 1

                qty_bp = len(mac_ref_table)

                ###VERIFICAR QUANTIDADE DE DOMINIOS

                if tag_domain_BS and tag_domain_5 and tag_domain_guest:
                    table_bssid["qty_domain"] = str(3)
                elif tag_domain_BS and tag_domain_5 and tag_domain_guest == False:
                    table_bssid["qty_domain"] = str(2)

                table_bssid["qty_baseport"] = str(qty_bp)
                table_bssid['bssid/domain']['BS']['2_4GHz'] = str(count_domain_24)
                table_bssid['bssid/domain']['BS']['5GHz'] = str(count_domain_5_bs)
                table_bssid['bssid/domain']['MAIN']['5GHz'] = str(count_domain_5_main)
                table_bssid["qty_bssid_2.4GHz"] = str(count_domain_24)
                table_bssid["qty_bssid_5GHz"] = str(count_domain_5_bs + count_domain_5_main)
                table_bssid["qty_bssid_total"] = str(count_domain_5_bs + count_domain_5_main + count_domain_24)

                table_bssid['Result'] = 'OK'
                table_bssid['Exception'] = 'OK'

        except Exception as error:
            print(error)
            table_bssid['Result'] = 'NOK'
            table_bssid['Exception'] = 'ERRO NA GERACAO DA TABELA_BSSID'

        print(table_bssid)
        return table_bssid


    ######Listar detalhes das estacoes conectadas nos bssids WiFi######
    def roaming_assoc(self, out_str, firmware, params):

        raw_list = out_str.splitlines()
        count_host = int(0)

        table_sta_assoc = {}

        try:

            ##--> Info devices Askey Econet
            askey_ecnt_model = params['devices']['supported']['askey_ecnt_model']
            askey_ecnt_fw = params['devices']['supported']['askey_ecnt_fw']

            firmware = 'OK'
            if firmware == 'OK':
                #####RX and TX is about the HGU, instance rssi_rx is the power seen by the HGU sent by the station

                for key in raw_list:
                    if key != '':
                        list = key.split()
                        if len(list) > 6 and list[0].startswith('00'):
                            print(list)
                            count_host = count_host + 1
                            index = list[0].strip('.')
                            table_sta_assoc[list[1]] = {
                                "radio": "",
                                "ss": "",
                                "bw": "",
                                "phyrate": "",
                                "bsstr": "",
                                "bssid": "",
                                "domain": "",
                                "rssi_rx": "",
                                "max_phyrate_tx": "",
                                "avg_phyrate_tx": "",
                                "avg_phyrate_rx": "",
                            }

                            if len(list) == 14:
                                table_sta_assoc[list[1]]["radio"] = list[2]
                                table_sta_assoc[list[1]]["ss"] = list[3]
                                table_sta_assoc[list[1]]["bw"] = list[4]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                table_sta_assoc[list[1]]["bsstr"] = list[6]
                                table_sta_assoc[list[1]]["bssid"] = list[7]
                                table_sta_assoc[list[1]]["domain"] = list[8]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                avg_phy_rate_tx_aux = list[11].split('/')
                                avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                            elif len(list) == 15:
                                table_sta_assoc[list[1]]["radio"] = list[2] + '|' + list[3]
                                table_sta_assoc[list[1]]["ss"] = list[4]
                                table_sta_assoc[list[1]]["bw"] = list[5]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[6]
                                table_sta_assoc[list[1]]["bsstr"] = list[7]
                                table_sta_assoc[list[1]]["bssid"] = list[8]
                                table_sta_assoc[list[1]]["domain"] = list[9]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[10]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[11]
                                avg_phy_rate_tx_aux = list[12].split('/')
                                avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[13]

                            else:
                                table_sta_assoc[list[1]]["radio"] = list[2]
                                table_sta_assoc[list[1]]["ss"] = list[3]
                                table_sta_assoc[list[1]]["bw"] = list[4]
                                table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                                table_sta_assoc[list[1]]["bsstr"] = list[6]
                                table_sta_assoc[list[1]]["bssid"] = list[7]
                                table_sta_assoc[list[1]]["domain"] = list[8]
                                table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                                table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                                avg_phy_rate_tx_aux = list[11].split('/')
                                avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                                table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                                table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                        else:
                            table_sta_assoc['qty_hosts'] = str(count_host)

                table_sta_assoc['qty_hosts'] = str(count_host)
                table_sta_assoc['Result'] = 'OK'
                table_sta_assoc['Exception'] = 'OK'

        except Exception as error:
            print(error)
            table_sta_assoc['Result'] = 'NOK'
            table_sta_assoc['Exception'] = 'Exceção ao gerar tabela de device wifi conectados'

        print(table_sta_assoc)
        return table_sta_assoc


    ###### Listar DHCP SETTINGS HGU ######
    def getDhcpSettingsHgu_01(self, output_str):

        # Entrada: dhcpserver show

        resultado = {'LAN': {
            'DHCP Server': '',
            'IP Inicio': '',
            'IP Final': '',
            'DNS Server': '',
            'Lease Time': '',
            'Gateway': '',
            'Option 42': '',
            'WAN VoIP Options': {
                'WAN Interface': '',
                'Option 42': ''
            },
            'AlternativeRange-NAT/PATLines': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': '',
                'Option 42': '',
            },
            'AlternativeRange-NAT/PATLines - 2': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': ''
            },

        },
            'Result': {},
            'Exception': {}}
        try:
            ans = output_str.splitlines()
            print(ans)
            c = 0
            aux = []
            for i in ans:
                aux1 = re.sub(' +', ';', i)
                print('linha #' + str(c) + '  ' + aux1)
                aux1 = aux1.split(';')
                # print(aux1)
                aux.append(aux1)
                c = c + 1
            # print(aux[7][1])
            resultado['LAN']['DHCP Server'] = aux[6][2]
            resultado['LAN']['IP Inicio'] = aux[6][4]
            resultado['LAN']['IP Final'] = aux[6][5]
            resultado['LAN']['DNS Server'] = aux[6][7]
            resultado['LAN']['Lease Time'] = aux[6][9]
            resultado['LAN']['Gateway'] = aux[6][8]
            resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Inicio'] = aux[18][4]
            resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Final'] = aux[18][5]
            resultado['LAN']['AlternativeRange-NAT/PATLines']['DNS Servers'] = aux[18][7]
            resultado['LAN']['AlternativeRange-NAT/PATLines']['Gateway'] = aux[18][8]
            resultado['LAN']['AlternativeRange-NAT/PATLines']['Lease Time'] = aux[18][9]
            resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Inicio'] = aux[24][4]
            resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Final'] = aux[24][5]
            resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['DNS Servers'] = aux[24][7]
            resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Gateway'] = aux[24][8]
            resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Lease Time'] = aux[24][9]

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'


        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = 'NOK'
            print('Erro ao consulta ifomrações de DHCP Settings', error)

        return resultado

    ######Listar informacoes Opticas HGU######
    def getOpticalInfo(self, out_str):
        ###Entrada: >show ont optics
        out_str1 = out_str[0]
        # out_str2 = out_str[1]
        out_str3 = out_str[1]
        infoGpon = {'info':
                        {'vendor': '',
                         'model': '',
                         'type': '',
                         'class': '',
                         'ont_rx': '',
                         'ont_tx': ''},
                    'Result': '',
                    'Exception': ''
                    }
        # print('olaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        raw_list = out_str1.splitlines()
        # print(raw_list)
        try:
            c = 0
            for key in raw_list[1:17]:
                # print('linha #' + str(c) + '  ' + key)
                list = key.split(' = ')
                # print(list)
                if len(list) > 0:
                    if list[0].startswith('Rx power'):
                        # print(list[0], list[1])
                        infoGpon['info']['ont_rx'] = list[1].split(' ')[0]
                    elif list[0].startswith('Tx power'):
                        infoGpon['info']['ont_tx'] = list[1].split(' ')[0]
                c = c + 1
            raw_list = out_str3.splitlines()
            c = 0
            for key in raw_list:
                # print('linha #' + str(c) + '  ' + key)
                list = key.split('=')
                if len(list) > 0:
                    if list[0].startswith('BOSA_vendor'):
                        infoGpon['info']['vendor'] = list[1]
                    elif list[0].startswith('BOSA_type'):
                        infoGpon['info']['model'] = list[1]
                c = c + 1
                infoGpon['info']['type'] = 'GPON'
                infoGpon['info']['class'] = 'Class B'
                infoGpon['Result'] = 'OK'
                infoGpon['Exception'] = 'OK'

        except Exception as error:
            infoGpon['Result'] = 'NOK'
            infoGpon['Exception'] = error

        return infoGpon


    ####Verificar status interface Internet
    def statusInet(self, out_str):

        ###Entrada: >show primary_diagnosis internet_service status

        status_inet = {
            'status': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                if key.startswith('internet_service'):
                    list = key.split(' ')
                    status_inet['status'] = list[2]

            status_inet['Result'] = 'OK'
            status_inet['Exception'] = 'OK'

        except Exception as error:
            status_inet['Result'] = 'NOK'
            status_inet['Exception'] = error

        return status_inet


    ######Listar informacoes IP_Internet######
    def getIpWan(self, out_str, model=''):

        # print(out_str)
        print('tamanho out_str = ' + str(len(out_str)))

        ###Entrada: >wan show
        infoIpInet = {
            'iface': {
                'Voip_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Vod_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Multicast_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Internet_ppp_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                }
            },
            'Result': '',
            'Exception': ''
        }

        if len(out_str) == 3: ### VIVO 1 e ONLINE
            try:
                infoIpInet['iface']['Internet_ppp_interface']['service_name'] = out_str[0]

                aux = out_str[1].split('\n')
                infoIpInet['iface']['Internet_ppp_interface']['status_v4'] = aux[2]
                infoIpInet['iface']['Internet_ppp_interface']['status_v6'] = aux[2]

                aux = out_str[2].split('\n')
                infoIpInet['iface']['Internet_ppp_interface']['vlan'] = aux[1]

                infoIpInet['Result'] = 'OK'
                infoIpInet['Exception'] = 'OK'

                return infoIpInet

            except Exception as error:
                infoIpInet['Result'] = 'NOK'
                infoIpInet['Exception'] = error

                return infoIpInet

        if len(out_str) == 4:
            try:
                for key in out_str:
                    if key == 'down':
                        infoIpInet['iface']['Internet_ppp_interface']['service_name'] = key
                    elif key == 'DISCONNECTED':
                        infoIpInet['iface']['Internet_ppp_interface']['status_v4'] = key
                        infoIpInet['iface']['Internet_ppp_interface']['status_v6'] = key
                    elif key == '10':
                        infoIpInet['iface']['Internet_ppp_interface']['vlan'] = key
                infoIpInet['Result'] = 'OK'
                infoIpInet['Exception'] = 'OK'

                return infoIpInet

            except Exception as error:
                infoIpInet['Result'] = 'NOK'
                infoIpInet['Exception'] = error

                return infoIpInet




    ######Listar informacoes das rotas do HGU######
    def getRoutes(self, out_str):

        ###Entrada: >route show

        raw_list = out_str.splitlines()
        # print(raw_list)

        count_route_inet = 0
        count_route_voip = 0
        count_route_vod = 0
        count_route_lan = 0

        infoRoute = {'qty_routes_inet': '',
                     'qty_routes_voip': '',
                     'qty_routes_vod': '',
                     'qty_routes_lan': '',
                     'info': {},
                     'Result': '',
                     'Exception': ''
                     }

        try:
            for key in raw_list:
                list = key.split()
                # print(list)
                if len(list) > 3:
                    if re.match \
                                (
                                r'(^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$)',
                                list[0]) \
                            or list[0] == 'default':
                        index = list[7]
                        if index == 'rbr4.0':
                            count_route_lan = count_route_lan + 1
                            infoRoute['info'][index + '-' + str(count_route_lan)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_lan)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['iface'] = list[5]

                        elif index == 'ppp0':
                            count_route_inet = count_route_inet + 1
                            infoRoute['info'][index + '-' + str(count_route_inet)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_inet)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['iface'] = list[5]

                        elif index == 'rbr3.3':
                            count_route_vod = count_route_vod + 1
                            infoRoute['info'][index + '-' + str(count_route_vod)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_vod)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['iface'] = list[5]


                        elif index == 'rbr2.2':
                            count_route_voip = count_route_voip + 1
                            infoRoute['info'][index + '-' + str(count_route_voip)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_voip)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['iface'] = list[5]

            infoRoute['qty_routes_inet'] = str(count_route_inet)
            infoRoute['qty_routes_voip'] = str(count_route_voip)
            infoRoute['qty_routes_vod'] = str(count_route_vod)
            infoRoute['qty_routes_lan'] = str(count_route_lan)
            infoRoute['Result'] = 'OK'
            infoRoute['Exception'] = 'OK'


        except Exception as error:
            infoRoute['Result'] = 'NOK'
            infoRoute['Exception'] = error

        return infoRoute


    ####Verificar Credenciais PPPoE
    def verifyPppoeSettings(self, output_str):
        resultado = {'PPPoE': {'username': {},
                               'password': {}
                               },
                     'Result': {},
                     'Exception': {}}
        try:
            # print(output_str)
            for i in output_str:
                aux = i.splitlines()
                print(aux)
                if aux[0].startswith("rtm_util cfg igd 1 ppp_intf list | grep 'username'"):
                    resultado['PPPoE']['username'] = aux[1]
                elif aux[0].startswith("rtm_util cfg igd 1 ppp_intf list | grep 'password'"):
                    resultado['PPPoE']['password'] = aux[1]
            # ans = output_str.splitlines()
            # print(aux2)
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error

        return resultado


    #####Listar DNS IPv4 HGU######
    def getDnsIpv4Hgu(self, output_str):
        # Entrada: sys ipinfo
        resultado = {'DNS_IPv4': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            # print(ans)
            c = 0
            aux = []
            for i in ans:
                # print(i)
                aux1 = i.split(' = ')
                # print(aux1)
                if aux1[0] == 'ipcpv4_info.dns_addr[0]':
                    aux.append(aux1[1])
                elif aux1[0] == 'ipcpv4_info.dns_addr[1]':
                    aux.append(aux1[1])
            resultado['DNS_IPv4'] = aux
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ######Listar DNS IPv6 HGU######
    def getDnsIpv6Hgu(self, output_str):
        # Entrada: sys ipinfo
        resultado = {'DNS_IPv6': {},
                     'Result': {},
                     'Exception': {}}
        try:
            ans = output_str.splitlines()
            # print(ans)
            c = 0
            aux = []
            for i in ans:
                # print(i)
                aux1 = i.split(' = ')
                # print(aux1)
                if aux1[0] == 'svr.ipv6_addr':
                    aux.append(aux1[1])
            resultado['DNS_IPv6'] = aux
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ###### Listar DHCP SETTINGS HGU ######
    def getDhcpSettingsHgu(self, output_str):

        # Entrada: dhcpserver show

        resultado = {'LAN': {
            'DHCP Server': '',
            'IP Inicio': '',
            'IP Final': '',
            'DNS Server': '',
            'Lease Time': '',
            'Gateway': '',
            'Option 42': '',
            'WAN VoIP Options': {
                'WAN Interface': '',
                'Option 42': ''
            },
            'AlternativeRange-NAT/PATLines': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': '',
                'Option 42': '',
            },
            'AlternativeRange-NAT/PATLines - 2': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': ''
            },

        },
            'Result': {},
            'Exception': {}}
        try:
            ans = output_str.splitlines()
            tag_dns = ''
            dns_server = ''

            for key in ans:
                list = key.split(',')
                for key2 in list:
                    list_aux = key2.split()
                    if len(list_aux) > 3 and list_aux[0].startswith('0'):
                        resultado['LAN']['DHCP Server'] = list_aux[1]
                        resultado['LAN']['IP Inicio'] = list_aux[3]
                        resultado['LAN']['IP Final'] = list_aux[4]
                        resultado['LAN']['DNS Server'] = list_aux[6]
                        dns_server = list_aux[6]
                        tag_dns = 'index_0'

                    elif len(list_aux) > 3 and list_aux[0].startswith('2'):
                        resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Inicio'] = list_aux[3]
                        resultado['LAN']['AlternativeRange-NAT/PATLines']['IP Final'] = list_aux[4]
                        tag_dns = 'index_2'

                    elif len(list_aux) > 3 and list_aux[0].startswith('3'):
                        resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Inicio'] = list_aux[3]
                        resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['IP Final'] = list_aux[4]
                        tag_dns = 'index_3'

                    elif len(list_aux) == 3 and tag_dns == 'index_0':
                        resultado['LAN']['Lease Time'] = list_aux[2]
                        resultado['LAN']['Gateway'] = list_aux[1]
                        if dns_server == '0.0.0.0':
                            resultado['LAN']['DNS Server'] = list_aux[1]

                    elif len(list_aux) == 3 and tag_dns == 'index_2':
                        resultado['LAN']['AlternativeRange-NAT/PATLines']['Lease Time'] = list_aux[2]
                        resultado['LAN']['AlternativeRange-NAT/PATLines']['Gateway'] = list_aux[1]

                    elif len(list_aux) == 3 and tag_dns == 'index_3':
                        resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Lease Time'] = list_aux[2]
                        resultado['LAN']['AlternativeRange-NAT/PATLines - 2']['Gateway'] = list_aux[1]


            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = 'NOK'
            print('Erro ao consulta ifomrações de DHCP Settings', error)

        return resultado


    ######Listar infor VoIP######
    def getInfoVoIP(self, out_str):

        ###Entrada: > voice show

        voipInfo = {
            'info': {
                'Voice_Profile': {
                    'ifName': '',
                    'ipAddr': '',
                    'ipVersion': '',
                    'manageProtocol': '',
                    'voiceProfile': '',
                    'profileState': '',
                    'local': '',
                    'dtmfMethod': '',
                    'hookFlashMethod': '',
                    'T38': '',
                    'V18': '',
                    'rtpDscpMark': '',
                    'rtpPortMin': '',
                    'rtpPortMax': '',
                    'sip': '',
                    'domain': '',
                    'port': '',
                    'transport': '',
                    'regExpires': '',
                    'regRetriveInterval': '',
                    'dscpMark': '',
                    'addrRegister': '',
                    'portRegister': '',
                    'addrProxy': '',
                    'portProxy': '',
                    'option120Addr': '',
                    'outboundProxyAddr': '',
                    'outboundProxyPort': '',
                    'uriConference': '',
                    'optionConference': ''
                },
                'Account': {
                    'lineEnableState': '',
                    'voipServiceStatus': '',
                    'reverserPolarity': '',
                    'callStatus': '',
                    'physicalReference': '',
                    'uri': '',
                    'number': '',
                    'authName': '',
                    'authPwd': '',
                    'txGain': '',
                    'rxGain': '',
                    'echoCancellation': '',
                    'callWaiting': ''
                },
                'Codec': {
                    'codec-1': '',
                    'codec-2': '',
                    'codec-3': ''
                }
            },
            'Result': '',
            'Exception': ''
        }
        # print(out_str)

        try:
            aux = []
            for i in out_str:
                raw_list = i.split('\n')
                aux.append(raw_list)
            print(aux)
            c = 0
            for i in aux:
                print('linha #' + str(c) + '   ' + str(i))
                #print(i)
                c = c + 1
            ###INFORMAÇÕES VOICE PROFILE
            if aux[0][1].startswith('rbr'):
                voipInfo['info']['Voice_Profile']['ifName'] = aux[0][1]
            else:
                voipInfo['info']['Voice_Profile']['ifName'] = 'voip_iface'
            voipInfo['info']['Voice_Profile']['ipAddr'] = aux[1][1]
            voipInfo['info']['Voice_Profile']['ipVersion'] = 'IPv4'
            voipInfo['info']['Voice_Profile']['manageProtocol'] = ''
            voipInfo['info']['Voice_Profile']['voiceProfile'] = ''
            voipInfo['info']['Voice_Profile']['profileState'] = aux[2][2]
            voipInfo['info']['Voice_Profile']['local'] = aux[3][1]
            voipInfo['info']['Voice_Profile']['dtmfMethod'] = aux[4][1]
            voipInfo['info']['Voice_Profile']['hookFlashMethod'] = ''
            voipInfo['info']['Voice_Profile']['T38'] = aux[5][2]
            voipInfo['info']['Voice_Profile']['V18'] = ''
            voipInfo['info']['Voice_Profile']['rtpDscpMark'] = aux[6][2]
            voipInfo['info']['Voice_Profile']['rtpPortMin'] = aux[7][2]
            voipInfo['info']['Voice_Profile']['rtpPortMax'] = aux[8][2]
            voipInfo['info']['Voice_Profile']['domain'] = aux[9][2]
            voipInfo['info']['Voice_Profile']['port'] = aux[10][2]
            voipInfo['info']['Voice_Profile']['transport'] = aux[11][2]
            voipInfo['info']['Voice_Profile']['regExpires'] = aux[12][2]
            voipInfo['info']['Voice_Profile']['regRetriveInterval'] = aux[13][2]
            voipInfo['info']['Voice_Profile']['dscpMark'] = aux[14][2]
            voipInfo['info']['Voice_Profile']['addrRegister'] = aux[15][2]
            voipInfo['info']['Voice_Profile']['portRegister'] = aux[16][2]
            voipInfo['info']['Voice_Profile']['addrProxy'] = aux[17][2]
            voipInfo['info']['Voice_Profile']['portProxy'] = aux[18][2]
            voipInfo['info']['Voice_Profile']['outboundProxyAddr'] = aux[19][2]
            voipInfo['info']['Voice_Profile']['outboundProxyPort'] = aux[20][2]
            voipInfo['info']['Voice_Profile']['uriConference'] = aux[21][2]
            voipInfo['info']['Voice_Profile']['optionConference'] = ''
            #
            # ###INFORMAÇÕES LINHA SIP
            voipInfo['info']['Account']['lineEnableState'] = aux[22][2]
            voipInfo['info']['Account']['voipServiceStatus'] = aux[23][2]
            voipInfo['info']['Account']['reverserPolarity'] = aux[24][2]
            voipInfo['info']['Account']['callStatus'] = aux[25][2]
            voipInfo['info']['Account']['physicalReference'] = ''
            voipInfo['info']['Account']['uri'] = aux[26][2]
            voipInfo['info']['Account']['number'] = aux[27][2]
            voipInfo['info']['Account']['authName'] = aux[27][2]
            voipInfo['info']['Account']['authPwd'] = aux[28][2]
            voipInfo['info']['Account']['txGain'] = aux[29][1]
            voipInfo['info']['Account']['rxGain'] = aux[30][1]
            voipInfo['info']['Account']['echoCancellation'] = aux[31][2]
            voipInfo['info']['Account']['callWaiting'] = aux[32][2]
            #
            # ###INFORMAÇÕES DSO CODECS
            voipInfo['info']['Codec']['codec-1'] = aux[33][2]
            voipInfo['info']['Codec']['codec-2'] = aux[34][2]
            voipInfo['info']['Codec']['codec-3'] = aux[35][2]

            ###INFORMAÇÕES REDE GPON
            voipInfo['info']['Network'] = 'Vivo_1'

            voipInfo['Result'] = 'OK'
            voipInfo['Exception'] = 'OK'

        except Exception as error:
            voipInfo['Result'] = 'NOK'
            voipInfo['Exception'] = error



        return voipInfo


    ####Verificar status interface Internet
    def getRegion(self, out_str):

        ###Entrada: >show primary_diagnosis internet_service status

        info_region = {
            'region': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                if key.startswith('rtf_def_area'):
                    list = key.split('=')
                    if list[1] == '1':
                        info_region['region'] = 'N1'
                    elif list[1] == '2':
                        info_region['region'] = 'N2'
                    else:
                        info_region['region'] = ''

            info_region['Result'] = 'OK'
            info_region['Exception'] = 'OK'

        except Exception as error:
            info_region['Result'] = 'NOK'
            info_region['Exception'] = error

        return info_region


    ####Verificar status interface OMCI
    def getStatusOnt(self, out_str):

        ###Entrada: >show primary_diagnosis internet_service status

        info_onu = {
            'onu_status': '',
            'slid': '',
            'serial_gpon': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            line = 0
            for key in raw_list:
                line = line + 1
                lista = key.split()

                if len(lista) > 1:
                    if lista[1].strip().startswith('State'):
                        status = str(lista[2].strip())
                        print(type(status))
                        if status == 'O5':
                            info_onu['onu_status'] = 'Operation'
                        elif status == 'O4':
                            info_onu['onu_status'] = 'Ranging'
                        elif status == 'O3' or status == 'O2':
                            info_onu['onu_status'] = 'SN Aquisition'
                        elif status == 'O1':
                            info_onu['onu_status'] = 'Syncronization'
                        elif status == 'O6':
                            info_onu['onu_status'] = 'Intermittent LODS'
                        elif status == 'O7':
                            info_onu['onu_status'] = 'Emergency Stop'
                        else:
                            info_onu['onu_status'] = 'Failure '
                    elif lista[0].startswith('ASCII'):
                        slid = str(lista[1].strip())
                        print(lista[1])
                        info_onu['slid'] = slid

                    elif lista[0].startswith('SN'):
                        serial_gpon = str(lista[1].strip())
                        info_onu['serial_gpon'] = serial_gpon

            info_onu['Result'] = 'OK'
            info_onu['Exception'] = 'OK'

        except Exception as error:
            info_onu['Result'] = 'NOK'
            info_onu['Exception'] = error

        return info_onu


    ####Verificar status interface Internet
    def getProcess(self, out_str, name_process):

        ###Entrada: >show primary_diagnosis internet_service status

        info_process = {
            'process_status': '',
            'Result': '',
            'Exception': ''
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                list = key.split()
                if name_process in list:
                    info_process['process_status'] = 'OK'
                    break

            info_process['Result'] = 'OK'
            info_process['Exception'] = 'OK'

        except Exception as error:
            info_process['Result'] = 'NOK'
            info_process['Exception'] = error

        return info_process


    ###### Verificar Device Info com Info do MDM######
    def verifyHguHardware(self, out_str):
        resultado = {
            'CPU': {
                'Used': '',
                'Free': ''
            },
            'MEMORIA': {
                'Used': '',
                'Free': ''
            },
            'TOP': {
                'Load average': {
                    '#1': '',
                    '#2': '',
                    '#3': ''
                },
                'Processos': {
                    '#1': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#2': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#3': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#4': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#5': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    }
                }
            },
            'VALIDATION': {
                'CPU': {},
                'MEMORIA': {},
                'GERAL': {}
            },
            'Result': {},
            'Exception': {}
        }
        try:
            print(out_str)
            list_top = out_str.split('\r\n')
            print(list)
            for i in list_top:
                # print(i)
                if i.startswith('CPU'):
                    aux = i.split('%')
                    # print(aux)
                    for j in aux:
                        aux1 = j.split(' ')
                        print(aux1)
                        if aux1[1] == 'nice':
                            resultado['CPU']['Free'] = float(aux1[2])
                            print(resultado['CPU']['Free'])
                        if aux1[1] == 'usr':
                            if len(aux1) == 3:
                                resultado['CPU']['Used'] = float(aux1[2])
                                print(resultado['CPU']['Used'])
                            elif len(aux1) == 4:
                                resultado['CPU']['Used'] = float(aux1[3])
                                print(resultado['CPU']['Used'])
                elif i.startswith('Mem'):
                    # print(i)
                    aux = i.split()
                    # print(aux)
                    memoTotalBytes = int(aux[1].replace('K', ''))
                    # print(memoTotalBytes)
                    memoFreeBytes = int(aux[3].replace('K', ''))
                    # print(memoFreeBytes)
                    memoFree = (memoFreeBytes/memoTotalBytes)*100
                    # print(memoFree)
                    # resultado['CPU']['Used'] = int(re.findall(r'(\d+)%{1}', i)[0])
            resultado['MEMORIA']['Used'] = 100-round(memoFree, 2)
            resultado['MEMORIA']['Free'] = float(round(memoFree, 2))
            aux_out = []
            for i in list_top:
                # print(i)
                if i.startswith('Load average'):
                    aux = i.split(' ')
                    aux_out.append(aux)
            # print(aux_out[0][2])
            resultado['TOP']['Load average']['#1'] = float(aux_out[0][2])
            resultado['TOP']['Load average']['#2'] = float(aux_out[0][3])
            resultado['TOP']['Load average']['#3'] = float(aux_out[0][4])

            aux_out = []
            for i in list_top[5:]:
                # print(i.split())
                #     i = re.sub('  +', ' ', i)
                aux1 = i.split()
                aux_out.append(aux1)
            print(aux_out)
            resultado['TOP']['Processos']['#1']['PID'] = aux_out[0][0]
            resultado['TOP']['Processos']['#1']['PPID'] = aux_out[0][1]
            resultado['TOP']['Processos']['#1']['USER'] = aux_out[0][2]
            resultado['TOP']['Processos']['#1']['STAT'] = aux_out[0][3]
            resultado['TOP']['Processos']['#1']['VSZ'] = aux_out[0][4]
            resultado['TOP']['Processos']['#1']['%MEM'] = aux_out[0][5]
            resultado['TOP']['Processos']['#1']['%CPU'] = aux_out[0][6]
            resultado['TOP']['Processos']['#1']['COMMAND'] = aux_out[0][7:]

            resultado['TOP']['Processos']['#2']['PID'] = aux_out[1][0]
            resultado['TOP']['Processos']['#2']['PPID'] = aux_out[1][1]
            resultado['TOP']['Processos']['#2']['USER'] = aux_out[1][2]
            resultado['TOP']['Processos']['#2']['STAT'] = aux_out[1][3]
            resultado['TOP']['Processos']['#2']['VSZ'] = aux_out[1][4]
            resultado['TOP']['Processos']['#2']['%MEM'] = aux_out[1][5]
            resultado['TOP']['Processos']['#2']['%CPU'] = aux_out[1][6]
            resultado['TOP']['Processos']['#2']['COMMAND'] = aux_out[1][7:]

            resultado['TOP']['Processos']['#3']['PID'] = aux_out[2][0]
            resultado['TOP']['Processos']['#3']['PPID'] = aux_out[2][1]
            resultado['TOP']['Processos']['#3']['USER'] = aux_out[2][2]
            resultado['TOP']['Processos']['#3']['STAT'] = aux_out[2][3]
            resultado['TOP']['Processos']['#3']['VSZ'] = aux_out[2][4]
            resultado['TOP']['Processos']['#3']['%MEM'] = aux_out[2][5]
            resultado['TOP']['Processos']['#3']['%CPU'] = aux_out[2][6]
            resultado['TOP']['Processos']['#3']['COMMAND'] = aux_out[2][7:]

            resultado['TOP']['Processos']['#4']['PID'] = aux_out[3][0]
            resultado['TOP']['Processos']['#4']['PPID'] = aux_out[3][1]
            resultado['TOP']['Processos']['#4']['USER'] = aux_out[3][2]
            resultado['TOP']['Processos']['#4']['STAT'] = aux_out[3][3]
            resultado['TOP']['Processos']['#4']['VSZ'] = aux_out[3][4]
            resultado['TOP']['Processos']['#4']['%MEM'] = aux_out[3][5]
            resultado['TOP']['Processos']['#4']['%CPU'] = aux_out[3][6]
            resultado['TOP']['Processos']['#4']['COMMAND'] = aux_out[3][7:]

            resultado['TOP']['Processos']['#5']['PID'] = aux_out[4][0]
            resultado['TOP']['Processos']['#5']['PPID'] = aux_out[4][1]
            resultado['TOP']['Processos']['#5']['USER'] = aux_out[4][2]
            resultado['TOP']['Processos']['#5']['STAT'] = aux_out[4][3]
            resultado['TOP']['Processos']['#5']['VSZ'] = aux_out[4][4]
            resultado['TOP']['Processos']['#5']['%MEM'] = aux_out[4][5]
            resultado['TOP']['Processos']['#5']['%CPU'] = aux_out[4][6]
            resultado['TOP']['Processos']['#5']['COMMAND'] = aux_out[4][7:]

            ### VALIDATION
            if resultado['CPU']['Free'] >= 35:
                resultado['VALIDATION']['CPU'] = 'OK'
            else:
                resultado['VALIDATION']['CPU'] = 'NOK'
            if resultado['MEMORIA']['Free'] >= 8:
                resultado['VALIDATION']['MEMORIA'] = 'OK'
            else:
                resultado['VALIDATION']['MEMORIA'] = 'NOK'
            if resultado['VALIDATION']['CPU'] == 'OK' and resultado['VALIDATION']['MEMORIA'] == 'OK':
                resultado['VALIDATION']['GERAL'] = 'OK'
            else:
                resultado['VALIDATION']['GERAL'] = 'NOK'

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            print(resultado)
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ####Verificar Info Básicas do WiFi 2.4G
    def getWiFi2Gligth(self, out_str):

        ###Entrada: >show wifi

        raw_list = out_str.splitlines()


        infoWiFi2G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                # print(list)
                if len(list) > 1:
                    if list[0] == 'wifi0_status':
                        infoWiFi2G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        infoWiFi2G['info']['ssid'] = list[2]
                    elif list[1] == 'bssid':
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi2G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi2G['info']['password'] = list[2]

            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = 'ERRO AO GERAR INFO BASICA 2.4GHz', error

            return infoWiFi2G


    # ######Listar informacoes WiFi 5GHz######
    # def getWiFi5Gligth(self, out_str):
    #
    #     ###Entrada: >show wifi_plus all
    #     ###Necessário tempo maior para retorno do SSH
    #
    #     raw_list = out_str.splitlines()
    #
    #     del raw_list[0]
    #
    #     infoWiFi5G = {'info': {
    #         'bandwidth': '',
    #         'transmission_mode': '',
    #         'status': '',
    #         'hide': '',
    #         'ssid': '',
    #         'bssid': '',
    #         'authentication': '',
    #         'encryption': '',
    #         'password': '',
    #         'channel': '',
    #         'channel_mode': '',
    #         'gi': '',
    #         'dtim': '',
    #         'preamble': '',
    #         'wps': '',
    #         'wps_mode': '',
    #         'wmm': '',
    #         'region': '',
    #         'qhop': '',
    #         'beamforming': '',
    #         'scs': '',
    #         'airfair': '',
    #         'maui': '',
    #         'mumimo': '',
    #         'wifi_plus0_status': '',
    #         'roaming': ''
    #
    #     },
    #         'Result': '',
    #         'Exception': ''}
    #
    #     try:
    #
    #         for key in raw_list:
    #             list = key.split()
    #             # print(list)
    #             if len(list) > 1:
    #                 if list[1].startswith('bandwidth'):
    #                     infoWiFi5G['info']['bandwidth'] = list[2]
    #                     # print(list[2])
    #                 elif list[1].startswith('transmission_mode'):
    #                     infoWiFi5G['info']['transmission_mode'] = list[2]
    #                 elif list[1].startswith('status'):
    #                     infoWiFi5G['info']['status'] = list[2]
    #                 elif list[1].startswith('hide'):
    #                     infoWiFi5G['info']['hide'] = list[2]
    #                 elif list[1].startswith('ssid'):
    #                     infoWiFi5G['info']['ssid'] = list[2]
    #                 elif list[1].startswith('bssid'):
    #                     infoWiFi5G['info']['bssid'] = list[2]
    #                 elif list[1].startswith('authentication'):
    #                     infoWiFi5G['info']['authentication'] = list[2]
    #                 elif list[1].startswith('encryption'):
    #                     infoWiFi5G['info']['encryption'] = list[2]
    #                 elif list[1].startswith('password'):
    #                     infoWiFi5G['info']['password'] = list[2]
    #                 elif list[1].startswith('channel'):
    #                     infoWiFi5G['info']['channel'] = list[2]
    #                 elif list[1].startswith('mode'):
    #                     infoWiFi5G['info']['channel_mode'] = list[2]
    #                 elif list[1].startswith('gi'):
    #                     infoWiFi5G['info']['gi'] = list[2]
    #                 elif list[1].startswith('dtim'):
    #                     infoWiFi5G['info']['dtim'] = list[2]
    #                 elif list[1].startswith('preamble'):
    #                     infoWiFi5G['info']['preamble'] = list[2]
    #                 elif list[1].startswith('wps'):
    #                     infoWiFi5G['info']['wps'] = list[2]
    #                 elif list[1].startswith('wps_mode'):
    #                     infoWiFi5G['info']['wps_mode'] = list[2]
    #                 elif list[1].startswith('wmm'):
    #                     infoWiFi5G['info']['wmm'] = list[2]
    #                 elif list[1].startswith('region'):
    #                     infoWiFi5G['info']['region'] = list[2]
    #
    #                 elif list[1].startswith('qhop') and len(list) == 3:
    #                     if infoWiFi5G['info']['qhop'] == '':
    #                         infoWiFi5G['info']['qhop'] = list[2]
    #                 elif list[1].startswith('beamforming'):
    #                     infoWiFi5G['info']['beamforming'] = list[2]
    #                 elif list[1].startswith('scs'):
    #                     infoWiFi5G['info']['scs'] = list[2]
    #                 elif list[1].startswith('airfair'):
    #                     infoWiFi5G['info']['airfair'] = list[2]
    #                 elif list[1].startswith('maui'):
    #                     infoWiFi5G['info']['maui'] = list[2]
    #                 elif list[1].startswith('mumimo'):
    #                     infoWiFi5G['info']['mumimo'] = list[2]
    #                 elif list[0].startswith('wifi_plus0_status'):
    #                     infoWiFi5G['info']['wifi_plus0_status'] = list[1]
    #                 elif list[1].startswith('roaming'):
    #                     # print(list[1])
    #                     infoWiFi5G['info']['roaming'] = list[2]
    #
    #         infoWiFi5G['Result'] = 'OK'
    #         infoWiFi5G['Exception'] = 'OK'
    #
    #         return infoWiFi5G
    #
    #     except Exception as error:
    #         infoWiFi5G['Result'] = 'NOK'
    #         infoWiFi5G['Exception'] = error
    #
    #         return infoWiFi5G

        ####Verificar Info Básicas do WiFi 5G
    def getWiFi5Gligth(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus0_status':
                        infoWiFi5G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G['info']['ssid'] = ssid_name

                    elif list[1] == 'bssid':
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi5G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi5G['info']['password'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            return infoWiFi5G

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz'

            return infoWiFi5G


    ######Listar interfaces ETH utilizadas######
    def listEthIfaces(self, out_str):

        # Entrada: show map_info eth1_device information

        try:

            connect_lan = {'iface': '', 'ip_addr': 'not_connected', 'mac_addr': 'not_connected', 'Result': '',
                           'Exception': ''}

            raw_list = out_str.splitlines()

            for key in raw_list:
                sew = key.split()
                if sew[0].startswith('eth'):
                    iface = sew[0]
                    iface = iface.split('_')
                    iface = iface[0]
                    connect_lan['iface'] = iface
                elif not (sew[0].startswith('show') | sew[0].startswith('>') | \
                          sew[0].startswith('eth' + str(int) + '_device')):
                    if len(sew) > 1:
                        ip_addr = sew[0]
                        mac_addr = sew[1]
                    connect_lan['ip_addr'] = ip_addr
                    connect_lan['mac_addr'] = mac_addr

            connect_lan['Result'] = 'OK'
            connect_lan['Exception'] = 'OK'

            return connect_lan

        except Exception as error:
            connect_lan['Result'] = 'NOK'
            connect_lan['Exception'] = 'ERRO AO LISTAR INTERFACES LAN DO HGU: ', error

            return connect_lan


    ######Teste rede hpna (Netinf)
    def netinf(self, canal, limiares, fmw):
        resultado = {
            'testes': [],
            'Result': '',
            'Exception': '',
            'Description': ''
        }

        erro = ''
        falha_detectada = False

        testes = []

        limiar_per = limiares['per_max']
        limiar_potencia_minima = limiares['potencia_minima']
        limiar_taxa_minima = limiares['taxa_minima']

        try:
            with SSHClientInteraction(canal, timeout=5, display=False) as interact:
                # verifica o IP da LAN (gateway)
                interact.send('sh')
                interact.expect('~ # ')
                # interact.send('ifconfig rbr4.0')
                # interact.expect('~ #')
                # saida_cmd = interact.current_output_clean
                # gateway = ProcuraVal('inet addr:(.+?) +Bcast', saida_cmd)
                gateway = "192.168.0.1"
                # print(gateway)

                # verifica opção para execução do Netinf
                interact.send('netinf')
                interact.expect('please select network interface: ')
                saida_cmd = interact.current_output_clean
                opcao_netinf = ProcuraVal('^(.+?)\) +' + gateway, saida_cmd)

                # executa netinf
                interact.send(opcao_netinf)
                print("# netinf - Selecionada a opção " + str(opcao_netinf) + ".")
                interact.timeout = 120
                interact.expect('~ # ')

                # analisa a saída
                saida_cmd = interact.current_output_clean
                raw_list = saida_cmd.splitlines()

                for linha in raw_list:
                    erro_pontual = ""
                    if linha.startswith("ETC"):
                        tokens = linha.split()

                        nos = tokens[5].split("-->")
                        transmitter = nos[0][:17]
                        receiver = nos[1][:17]

                        if (eh_macaddr(transmitter) == False or eh_macaddr(receiver) == False):
                            print("transmitter / receiver inválidos --> " + transmitter + " " + receiver)
                            continue

                        per = ProcuraVal(' per: +(.+?) +', linha)
                        snr = ProcuraVal(' snr +(.+?)dB', linha)
                        rate = ProcuraVal(' rate: +(.+?) +Rx', linha)
                        rx_power = ProcuraVal(' Rx power: +(.+?)$', linha)

                        per_n = float(per.replace("%", ""))
                        if (per_n is False):
                            print("per inválido:" + str(per) + " " + str(per_n))
                            erro_pontual += "PER inválido,"
                        elif (per_n > limiar_per):
                            erro_pontual += "taxa de erro (PER) acima de " + str(limiar_per) + ","

                        rate_n = float(ProcuraVal('^(.+?)Mbps', rate))
                        if (rate_n is False):
                            erro_pontual += "Rate inválido,"
                        elif (rate_n < limiar_taxa_minima):
                            erro_pontual += "taxa de transmissão abaixo de " + str(limiar_taxa_minima) + " Mbps,"

                        rx_power_n = float(rx_power.replace("dBm", ""))
                        # print("passou1 " + str(rx_power_n) + " " + str(limiar_potencia_minima))
                        if (rx_power_n is False):
                            erro_pontual += "RX power inválido,"
                        elif (rx_power_n < limiar_potencia_minima):
                            erro_pontual += "potência de RX abaixo de " + str(limiar_potencia_minima) + " dBm,"

                        Result = ""
                        Description = ""

                        if (erro_pontual != ''):
                            erro += erro_pontual
                            falha_detectada = True
                            Result = "NOK"
                            Description = str(erro_pontual)
                        else:
                            Result = "OK"
                            Description = "OK"

                        testes.append({
                            "transmitter": transmitter,
                            "receiver": receiver,
                            "PER": per,
                            "Rate": rate,
                            "SNR (db)": snr,
                            "RX power": rx_power,
                            "Result": Result,
                            "Description": Description
                        })

                if (len(testes) == 0):
                    resultado['testes'] = testes
                    resultado["Result"] = "OK"
                    resultado["Exception"] = "OK"
                    resultado["Description"] = "Nenhum STB foi detectado na rede HPNA durante os testes."
                elif (falha_detectada == True):
                    resultado['testes'] = testes
                    resultado["Result"] = "NOK"
                    resultado["Exception"] = "NOK"
                    resultado["Description"] = "O teste da rede HPNA (Netinf) obteve valores fora do recomendado."
                else:
                    resultado['testes'] = testes
                    resultado["Result"] = "OK"
                    resultado["Exception"] = "OK"
                    resultado["Description"] = "O teste da rede HPNA (Netinf) obteve valores dentro do recomendado."

        except Exception as e:
            resultado['testes'] = testes
            resultado['Result'] = "NOK"
            resultado['Exception'] = str(e)
            resultado['Description'] = "Erro ao executar o Netinf."

        return resultado

        ###### Mapeia os IPs às portas físicas


    def ip_porta(self, out_str, modelo, fmw='BR_SV_g12.6_RTF_TEF001_V7.15_V015'):
        fmw='BR_SV_g12.6_RTF_TEF001_V7.15_V015' # remover essa linha
        # mapeamento IP para porta

        # Entrada: 'show map_info dhcp_table'

        raw_list = out_str.splitlines()

        ip_porta = {'Result': '', 'Exception': '', 'Description': ''}

        porta_map = {"wifi station_info": "wifi24",
                     "wifi_plus station_info": "wifi5",
                     "eth1_device information": "eth1",
                     "eth2_device information": "eth2",
                     "eth3_device information": "eth3",
                     "eth4_device information": "eth4",
                     "hpna information": "hpna"
                     }

        try:
            # if fmw in ['BR_SV_g12.6_RTF_TEF001_V7.15_V015']:
            demarcadores_interface = ["wifi station_info", "wifi_plus station_info", "eth1_device information",
                                      "eth2_device information", "eth3_device information",
                                      "eth4_device information", "hpna information"]
            demarcadores_invalidos = ["arp_table", "dhcp_table"]

            key_atual = ""
            for key in raw_list:
                if (key in demarcadores_invalidos):
                    key_atual = ""
                elif (key in demarcadores_interface):
                    key_atual = key

                    demarcadores_interface.remove(key)
                elif (key_atual != ""):
                    disp = key.split()

                    if (disp[0] == '>' or disp[0] == '0.0.0.0'):
                        continue

                    if ('RTF3507' in modelo and porta_map[key_atual] == "eth4"):
                        porta = "hpna"
                    else:
                        porta = porta_map[key_atual]

                    try:
                        ip_porta[disp[0]]
                    except:
                        ip_porta[disp[0]] = {}

                    ip_porta[disp[0]].update({"porta_hgu": porta, "mac": disp[1]})
            # else:
            #     ip_porta['Result'] = 'NOK'
            #     ip_porta['Exception'] = 'Firmware de HGU não suportado para teste IPTV. fmw:"' + fmw + '"'
        except Exception as e:
            ip_porta['Result'] = 'NOK'
            ip_porta['Exception'] = e

        if (ip_porta['Result'] != 'NOK'):
            ip_porta['Result'] = 'OK'
            ip_porta['Exception'] = 'OK'

        return ip_porta


    ####Verificar Info Básicas do WiFi 5G BS
    def getWiFi5GligthBS(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()
        print(raw_list)

        # del raw_list[0]
        # del raw_list[0]

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        print(list)
                        plus_size = (len(list) - len_default) + 1
                        print(plus_size)
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name

                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'


        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS', error

        return infoWiFi5G_BS


    def getWiFi5GBS(self, out_str):
        #Todo: Criar um IF para caso não tenha rodado anteriormente os comandos de wifi Main (gera erro de NoneType is not subscritable)
        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': '',
            'hide': '',
            'authentication': '',
            'encryption': '',
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name
                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'hide':
                        infoWiFi5G_BS['info']['hide'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'authentication':
                        infoWiFi5G_BS['info']['authentication'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'encryption':
                        infoWiFi5G_BS['info']['encryption'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'

        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS'

        return infoWiFi5G_BS


class cliMitraBrcm():
    def __init__(self, password, ip):
        self.user_support = 'support'
        self.password = password
        self.ip = ip


    def version(self, out_str):

        ##--> Entrada: sys atsh

        info_hgu = {'Model': '',
                    'Profile': '',
                    'Booted Partition': '',
                    'Partition 1 Version': '',
                    'Partition 2 Version': '',
                    'firmware': '',
                    'brcm_release': '',
                    'bootbase': '',
                    'serialNumber': '',
                    'macAddress': '',
                    'vendor': '',
                    'Result': '',
                    'Exception': ''}

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                list = key.split(':')
                if list[0].startswith('Product Model'):
                    info_hgu['Model'] = list[1].strip()

                elif list[0].startswith('MLD'):
                    info_hgu['firmware'] = list[1].strip()

                elif list[0].startswith('Bootbase'):
                    info_hgu['bootbase'] = list[1].strip()

                elif list[0].startswith('First MAC'):
                    mac_aux = list[1].strip()
                    mac = ''
                    count = 0
                    for i in mac_aux:
                        if count != 2:
                            mac = mac + i
                            count = count + 1
                        else:
                            mac = mac + ':' + i
                            count = 1
                    info_hgu['macAddress'] = mac
                    info_hgu['serialNumber'] = list[1].strip()

                elif list[0].startswith('Vendor'):
                    info_hgu['vendor'] = list[1].strip()

            info_hgu['Result'] = 'OK'
            info_hgu['Exception'] = 'OK'

        except Exception as error:
            info_hgu['Result'] = 'NOK'
            info_hgu['Exception'] = error

        return info_hgu


    ######Listar modelo do dispositivo######
    def device_model(self, out_str):

        # Entrada: show device_model

        ###STEP-00: JSON SAIDA
        device_info = {
            'model': '',
            'region': '',
            'Result': 'NOK',
            'Exception': 'NOK'
        }

        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                ###Exception para dispositivo Mitra ECNT
                if key.startswith('device_'):
                    list = key.split()
                    model = list[1]
                    region_aux = model.split('-')
                    if len(region_aux) > 2:
                        region = 'N2'
                    else:
                        region = 'N1'

                ###Utilizado para Askey BRCM
                elif key.startswith('device'):
                    list = key.split()
                    model = list[2]
                    region = model.split('-')
                    region = region[1]

                ###Utilizado para Mitra BRCM
                elif key.startswith('GPT'):
                    list = key.split()
                    model = list[0]
                    region = model.split('-')
                    region = region[2]

            device_info['model'] = model
            device_info['region'] = region
            device_info['Result'] = 'OK'
            device_info['Exception'] = 'OK'

        except Exception as error:
            device_info['Result'] = 'NOK'
            device_info['Exception'] = error

        return device_info


    ######Listar informacoes IP_Internet######
    def getIpWan(self, out_str):

        ###Entrada: >wan show
        out_str[0] = re.sub('\t', ';', out_str[0])
        print(out_str[1])
        raw_list = out_str[0].splitlines()

        infoIpInet = {
            'iface': {
                'Voip_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Vod_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Multicast_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Internet_ppp_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                }
            },
            'Result': '',
            'Exception': ''
        }

        try:
            for key in raw_list:
                # print(key)
                aux = key.split(';')
                print(aux)
                if len(aux) > 2:
                    if aux[2].startswith('VoIP'):
                        # print(aux[2])
                        infoIpInet['iface']['Voip_ip_interface']['service_name'] = aux[2]
                        infoIpInet['iface']['Voip_ip_interface']['iface_name'] = aux[4]
                        infoIpInet['iface']['Voip_ip_interface']['protocol'] = aux[6]
                        infoIpInet['iface']['Voip_ip_interface']['igmp'] = aux[7]
                        infoIpInet['iface']['Voip_ip_interface']['status_v4'] = aux[11]
                        infoIpInet['iface']['Voip_ip_interface']['ipv4'] = aux[12]
                    elif aux[2].startswith('Mediaroom'):
                        # print(aux[2])
                        infoIpInet['iface']['Vod_ip_interface']['service_name'] = aux[2]
                        infoIpInet['iface']['Vod_ip_interface']['iface_name'] = aux[3]
                        infoIpInet['iface']['Vod_ip_interface']['protocol'] = aux[5]
                        infoIpInet['iface']['Vod_ip_interface']['igmp'] = aux[6]
                        infoIpInet['iface']['Vod_ip_interface']['status_v4'] = aux[10]
                        infoIpInet['iface']['Vod_ip_interface']['ipv4'] = aux[11]
                    elif aux[2].startswith('Internet'):
                        # print(aux[2])
                        infoIpInet['iface']['Internet_ppp_interface']['service_name'] = aux[2]
                        infoIpInet['iface']['Internet_ppp_interface']['iface_name'] = aux[3]
                        infoIpInet['iface']['Internet_ppp_interface']['protocol'] = aux[5]
                        infoIpInet['iface']['Internet_ppp_interface']['igmp'] = aux[6]
                        infoIpInet['iface']['Internet_ppp_interface']['status_v4'] = aux[10]
                        infoIpInet['iface']['Internet_ppp_interface']['ipv4'] = aux[11]

            out_str[1] = out_str[1].split('\r\n')
            print(out_str[1])
            infoIpInet['iface']['Internet_ppp_interface']['ipv6'] = out_str[1][1]
            infoIpInet['Result'] = 'OK'
            infoIpInet['Exception'] = 'OK'

            return infoIpInet

        except Exception as error:
            infoIpInet['Result'] = 'NOK'
            infoIpInet['Exception'] = error

            return infoIpInet


    ######Listar informacoes das rotas do HGU######
    def getRoutes(self, out_str):

        ###Entrada: >route show

        raw_list = out_str.splitlines()

        count_route_inet = 0
        count_route_voip = 0
        count_route_vod = 0
        count_route_lan = 0

        infoRoute = {'qty_routes_inet': '',
                     'qty_routes_voip': '',
                     'qty_routes_vod': '',
                     'qty_routes_lan': '',
                     'info': {},
                     'Result': '',
                     'Exception': ''
                    }

        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 3:
                    if re.match\
                            (r'(^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$)', list[0]) \
                            or list[0] == 'default':
                        index = list[7]
                        if index == 'br0':
                            count_route_lan = count_route_lan + 1
                            infoRoute['info'][index + '-' + str(count_route_lan)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_lan)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_lan)]['iface'] = list[5]

                        elif index == 'ppp0.1':
                            count_route_inet = count_route_inet + 1
                            infoRoute['info'][index + '-' + str(count_route_inet)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_inet)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_inet)]['iface'] = list[5]

                        elif index == 'veip0.2':
                            count_route_vod = count_route_vod + 1
                            infoRoute['info'][index + '-' + str(count_route_vod)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_vod)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_vod)]['iface'] = list[5]


                        elif index == 'veip0.3':
                            count_route_voip = count_route_voip + 1
                            infoRoute['info'][index + '-' + str(count_route_voip)] = {
                                'destination': '',
                                'gateway': '',
                                'mask': '',
                                'flags': '',
                                'metric': '',
                                'iface': ''
                            }

                            infoRoute['info'][index + '-' + str(count_route_voip)]['destination'] = list[0]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['gateway'] = list[1]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['mask'] = list[2]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['flags'] = list[3]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['metric'] = list[4]
                            infoRoute['info'][index + '-' + str(count_route_voip)]['iface'] = list[5]

            infoRoute['qty_routes_inet'] = str(count_route_inet)
            infoRoute['qty_routes_voip'] = str(count_route_voip)
            infoRoute['qty_routes_vod'] = str(count_route_vod)
            infoRoute['qty_routes_lan'] = str(count_route_lan)
            infoRoute['Result'] = 'OK'
            infoRoute['Exception'] = 'OK'

            return infoRoute

        except Exception as error:
            infoRoute['Result'] = 'NOK'
            infoRoute['Exception'] = error

            return infoRoute

            ###### Listar DNS IPv4 HGU ######


    ######Listar dispositivos na tabela DHCP######
    def dhcp_table(self, out_str, fmw=''):

        # Entrada: 'show map_info dhcp_table'

        raw_list = out_str.splitlines()

        qtde_eth = int(0)
        count_eth = int(0)
        qtde_4 = int(0)
        count_wifi24 = int(0)
        qtde_5 = int(0)
        count_wifi5 = int(0)
        count_bp_ap = int(0)
        count_bp_rep = int(0)
        count_hosts = int(0)

        tabela_host = {"qtde_hosts": "",
                       "qtde_eth": qtde_eth,
                       "qtde_wifi24": qtde_4,
                       "qtde_wifi5": qtde_5,
                       "interface": {},
                       "bp": {
                           'repeater': {},
                           'ap': {},
                       },
                       "Result": '',
                       "Exception": ''}

        try:

            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Mitra Ecnt
            mitra_brcm_model = devices['supported']['mitra_brcm_model']
            mitra_brcm_fw = devices['supported']['mitra_brcm_fw']

            if fmw in mitra_brcm_fw:
                for key in raw_list:
                    list_tab = key.split('\t')
                    list_spa = key.split()

                    if len(list_spa) > 4:
                        if 'WiFi' in list_spa:
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ####CONTABILIZAR SE DEVICES EM 2.4GHz & 5GHz
                            tabela_host["interface"][count_iface]["radio"] = list_spa[5]
                            if list_spa[5] == '5':
                                count_wifi5 = count_wifi5 + 1
                            else:
                                count_wifi24 = count_wifi24 + 1

                            ###TRATAMENTO DE HOSTNAME E SSID PARA DIFERENTES SAIDAS

                            ###SOMENTE SSID SEM HOSTNAME (LEN 6)
                            if len(list_tab) == 6:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]

                            ###SSID & HOSTNAME (LEN 7)
                            elif len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["ssid_connect"] = list_tab[5]
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÃO DA TABELA DE BPs NO MODO REPEATER
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_rep = count_bp_rep + 1
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['ipaddr'] = list_tab[
                                        0]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['macaddr'] = list_tab[
                                        1]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['dhcp_mode'] = \
                                    list_tab[2]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['leasetime'] = \
                                    list_tab[3]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['media'] = list_spa[4]
                                    tabela_host['bp']['repeater']['rep-' + str(count_bp_rep)]['hostname'] = \
                                    list_tab[6]

                        elif 'Ethernet' in list_spa:
                            count_bp_ap = 0
                            count_eth = count_eth + 1
                            count_hosts = count_hosts + 1
                            count_iface = "host_" + str(count_hosts)

                            tabela_host["interface"][count_iface] = {"ipaddr": "",
                                                                     "macaddr": "",
                                                                     "dhcp_mode": "",
                                                                     "leasetime": "",
                                                                     "media": "",
                                                                     "radio": "",
                                                                     "ssid_connect": "",
                                                                     "hostname": ""}

                            tabela_host["interface"][count_iface]["ipaddr"] = list_tab[0]
                            tabela_host["interface"][count_iface]["macaddr"] = list_tab[1]
                            tabela_host["interface"][count_iface]["dhcp_mode"] = list_tab[2]
                            tabela_host["interface"][count_iface]["leasetime"] = list_tab[3]
                            tabela_host["interface"][count_iface]["media"] = list_spa[4]

                            ###TRATAMENTO DE HOSTNAME PARA DIFERENTES SAIDAS
                            if len(list_tab) == 7:
                                tabela_host["interface"][count_iface]["hostname"] = list_tab[6]

                                ####CONSTRUÇÂO DA TABELA DE BPs NO MODO AP
                                if list_tab[6].startswith('BP2 Mitrastar') or list_tab[6].startswith('BP2 Askey'):
                                    count_bp_ap = count_bp_ap + 1
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)] = {
                                        'ipaddr': '',
                                        'macaddr': '',
                                        'dhcp_mode': '',
                                        'leasetime': '',
                                        'media': '',
                                        'hostname': ''
                                    }

                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['ipaddr'] = list_tab[0]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['macaddr'] = list_tab[1]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['dhcp_mode'] = list_tab[2]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['leasetime'] = list_tab[3]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['media'] = list_spa[4]
                                    tabela_host['bp']['ap']['ap-' + str(count_bp_ap)]['hostname'] = list_tab[6]

                tabela_host['qtde_hosts'] = str(count_hosts)
                tabela_host['qtde_eth'] = str(count_eth)
                tabela_host['qtde_wifi24'] = str(count_wifi24)
                tabela_host['qtde_wifi5'] = str(count_wifi5)

                tabela_host['Result'] = 'OK'
                tabela_host['Exception'] = 'OK'


        except Exception as error:
            tabela_host['Result'] = 'NOK'
            tabela_host['Exception'] = 'ERRO GERAÇÃO TABELA HOST ASKEY BRCM', error

        return tabela_host


    ######Listar domínios e bssids criados######
    def roaming_bss(self, out_str, model='', firmware='VBR_g3.5_100VNZ0b33_1015', dhcp_table={}):

        ####LISTA DE OUI DOS BASES PORTS EM PLANTA
        oui_bp_mitra = ['a4:33:d7', 'cc:ed:dc', 'd8:c6:78', '34:57:60', 'cc:d4:a1', '84:aa:9c']
        oui_bp_askey = ['94:91:7f', '1c:b0:44', '80:78:71']

        raw_list = out_str.splitlines()

        table_bssid = {"qty_domain": "",
                       "qty_baseport": "",
                       "qty_bssid_total": "",
                       "ssid-0000": '',
                       "ssid-aaaa": '',
                       "qty_bssid_2.4GHz": "",
                       "qty_bssid_5GHz": "",
                       "bssid/domain":
                           {"BS": {},
                            'MAIN': {}
                            },
                       "bssids": {},
                       "Result": '',
                       "Exception": ''}

        try:

            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Mitra Ecnt
            mitra_brcm_model = devices['supported']['mitra_brcm_model']
            mitra_brcm_fw = devices['supported']['mitra_brcm_fw']

            if firmware in mitra_brcm_fw:

                qty_bp = int(0)
                qty_domain = int(0)
                qty_bssid_total = int(0)
                qty_bssid_24 = int(0)
                qty_bssid_5 = int(0)

                count_bp = 0

                tag_domain_BS = False
                tag_domain_5 = False
                tag_domain_guest = False

                count_bssid_24 = 0
                count_bssid_5 = 0
                count_bssid_guest = 0

                count_domain_24 = 0
                count_domain_5_bs = 0
                count_domain_5_main = 0

                aux_basePort = {}
                mac_ref_table = []

                for key in raw_list:
                    list = key.split()
                    if len(list) > 5 and list[0].startswith('00'):
                        # print(list)
                        # print(list[1])
                        # index = list[0].strip('.')
                        index = list[1]
                        table_bssid["bssids"][index] = {"bssid": "",
                                                        "status": "",
                                                        "local": "",
                                                        "radio": "",
                                                        "channel": "",
                                                        "bandwidth": "",
                                                        "BSSTr": "",
                                                        "fat": "",
                                                        "domain": "",
                                                        "vendor": "",
                                                        "network": ""}
                        #
                        if list[3] == 'Yes':  # Indice 3 identifica o device a qual esta conectado o shell
                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['local'] = 'HGU'
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]

                            if list[10] == '0000' and list[4] == '2.4G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                table_bssid['ssid-0000'] = ''
                            elif list[10] == '0000' and list[4] == '5G':
                                table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                            elif list[10] == 'aaaa':
                                table_bssid['bssids'][index]['network'] = 'Main_5G'
                                table_bssid['ssid-aaaa'] = ''
                            else:
                                table_bssid['bssids'][index]['network'] = 'Guest'


                        elif list[3] == 'No' and list[2] == 'UP':
                            mac_ref = list[9]

                            if mac_ref not in mac_ref_table:
                                count_bp = count_bp + 1
                                aux_basePort[mac_ref] = 'BP-' + str(count_bp)
                                table_bssid["bssids"][index]['local'] = "BP-" + str(count_bp)
                                mac_ref_table.append(mac_ref)
                            else:
                                table_bssid["bssids"][index]['local'] = aux_basePort[mac_ref]

                            ####VALIDAR MODELO BP
                            oui = list[9][:8]

                            ###VALIDAR SE BP ASKEY
                            if oui in oui_bp_askey:  # Identificar modelo de base port Askey
                                table_bssid["bssids"][index]['vendor'] = "ASKEY"
                                if list[10].strip() == '0000' and list[4].strip() == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'


                            ###VALIDAR SE BP MITRA
                            elif oui in oui_bp_mitra:  # Identificar modelo de base port Mitra
                                table_bssid["bssids"][index]['vendor'] = "MITRA"
                                if list[10] == '0000' and list[4] == '2.4G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_2G'
                                elif list[10] == '0000' and list[4] == '5G':
                                    table_bssid['bssids'][index]['network'] = 'BandSteering_5G'
                                elif list[10] == 'aaaa':
                                    table_bssid['bssids'][index]['network'] = 'Main_5G'
                                else:
                                    table_bssid['bssids'][index]['network'] = 'Guest'

                            table_bssid["bssids"][index]['bssid'] = list[1]
                            table_bssid["bssids"][index]['status'] = list[2]
                            table_bssid["bssids"][index]['radio'] = list[4]
                            table_bssid["bssids"][index]['channel'] = list[5]
                            table_bssid["bssids"][index]['bandwidth'] = list[6]
                            table_bssid["bssids"][index]['BSSTr'] = list[7]
                            table_bssid["bssids"][index]['fat'] = list[8]
                            table_bssid["bssids"][index]['domain'] = list[10]
                        #
                        ###Verificar quantidade de Dominios

                        if list[10] == '0000' and list[2] == 'UP':
                            tag_domain_BS = True
                            if int(list[5]) < 14:
                                count_bssid_24 = count_bssid_24 + 1
                                count_domain_24 = count_domain_24 + 1
                            else:
                                count_bssid_5 = count_bssid_5 + 1
                                count_domain_5_bs = count_domain_5_bs + 1

                        elif list[10] == 'aaaa' and list[2] == 'UP':
                            tag_domain_5 = True
                            count_bssid_5 = count_bssid_5 + 1
                            count_domain_5_main = count_domain_5_main + 1

                        elif (list[10] != '0000' or list[10] != 'aaaa') and list[2] == 'UP':
                            tag_domain_guest = True
                            count_bssid_guest = count_bssid_guest + 1

                qty_bp = len(mac_ref_table)

                ###VERIFICAR QUANTIDADE DE DOMINIOS

                if tag_domain_BS and tag_domain_5 and tag_domain_guest:
                    table_bssid["qty_domain"] = str(3)
                elif tag_domain_BS and tag_domain_5 and tag_domain_guest == False:
                    table_bssid["qty_domain"] = str(2)

                table_bssid["qty_baseport"] = str(qty_bp)
                table_bssid['bssid/domain']['BS']['2_4GHz'] = str(count_domain_24)
                table_bssid['bssid/domain']['BS']['5GHz'] = str(count_domain_5_bs)
                table_bssid['bssid/domain']['MAIN']['5GHz'] = str(count_domain_5_main)
                table_bssid["qty_bssid_2.4GHz"] = str(count_domain_24)
                table_bssid["qty_bssid_5GHz"] = str(count_domain_5_bs + count_domain_5_main)
                table_bssid["qty_bssid_total"] = str(count_domain_5_bs + count_domain_5_main + count_domain_24)

                table_bssid['Result'] = 'OK'
                table_bssid['Exception'] = 'OK'

        except Exception as error:

            table_bssid['Result'] = 'NOK'
            table_bssid['Exception'] = 'ERRO NA GERACAO DA TABELA_BSSID: ', error

        return table_bssid


    ######Listar detalhes das estacoes conectadas nos bssids WiFi######
    def roaming_assoc(self, out_str):

        raw_list = out_str.splitlines()
        print(raw_list)
        count_host = int(0)

        table_sta_assoc = {}

        try:
            ##--> File com informações dos modelos e firmware suportados
            file_devices = open("files/supported_devices.json", "r")
            devices = json.load(file_devices)
            file_devices.close()

            ##--> Info devices Mitra Ecnt
            mitra_brcm_model = devices['supported']['mitra_brcm_model']
            mitra_brcm_fw = devices['supported']['mitra_brcm_fw']

            # if firmware in mitra_brcm_fw:
            #     #####RX and TX is about the HGU, instance rssi_rx is the power seen by the HGU sent by the station

            for key in raw_list:
                if key != '':
                    list = key.split()
                    if len(list) > 6 and list[0].startswith('00'):
                        count_host = count_host + 1
                        index = list[0].strip('.')
                        table_sta_assoc[list[1]] = {
                            "radio": "",
                            "ss": "",
                            "bw": "",
                            "phyrate": "",
                            "bsstr": "",
                            "bssid": "",
                            "domain": "",
                            "rssi_rx": "",
                            "max_phyrate_tx": "",
                            "avg_phyrate_tx": "",
                            "avg_phyrate_rx": "",
                        }

                        ##Customização para MItra BRCM
                        if len(list) == 14:
                            table_sta_assoc[list[1]]["radio"] = list[2]
                            table_sta_assoc[list[1]]["ss"] = list[3]
                            table_sta_assoc[list[1]]["bw"] = list[4]
                            table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                            table_sta_assoc[list[1]]["bsstr"] = list[6]
                            table_sta_assoc[list[1]]["bssid"] = list[7]
                            table_sta_assoc[list[1]]["domain"] = list[8]
                            table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                            table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                            avg_phy_rate_tx_aux = list[11].split('/')
                            avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                            table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                            table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                        elif len(list) == 15:
                            table_sta_assoc[list[1]]["radio"] = list[2] + '|' + list[3]
                            table_sta_assoc[list[1]]["ss"] = list[4]
                            table_sta_assoc[list[1]]["bw"] = list[5]
                            table_sta_assoc[list[1]]["max_phyrate_hw"] = list[6]
                            table_sta_assoc[list[1]]["bsstr"] = list[7]
                            table_sta_assoc[list[1]]["bssid"] = list[8]
                            table_sta_assoc[list[1]]["domain"] = list[9]
                            table_sta_assoc[list[1]]["rssi_rx"] = list[10]
                            table_sta_assoc[list[1]]["max_phyrate_current"] = list[11]
                            avg_phy_rate_tx_aux = list[12].split('/')
                            avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                            table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                            table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[13]

                        else:

                            table_sta_assoc[list[1]]["radio"] = list[2]
                            table_sta_assoc[list[1]]["ss"] = list[3]
                            table_sta_assoc[list[1]]["bw"] = list[4]
                            table_sta_assoc[list[1]]["max_phyrate_hw"] = list[5]
                            table_sta_assoc[list[1]]["bsstr"] = list[6]
                            table_sta_assoc[list[1]]["bssid"] = list[7]
                            table_sta_assoc[list[1]]["domain"] = list[8]
                            table_sta_assoc[list[1]]["rssi_rx"] = list[9]
                            table_sta_assoc[list[1]]["max_phyrate_current"] = list[10]
                            avg_phy_rate_tx_aux = list[11].split('/')
                            avg_phy_rate_tx = avg_phy_rate_tx_aux[0]
                            table_sta_assoc[list[1]]["avg_phyrate_tx"] = avg_phy_rate_tx
                            table_sta_assoc[list[1]]["avg_phyrate_rx"] = list[12]

                    else:
                        table_sta_assoc['qty_hosts'] = str(count_host)

            table_sta_assoc['qty_hosts'] = str(count_host)
            table_sta_assoc['Result'] = 'OK'
            table_sta_assoc['Exception'] = 'OK'

        except Exception as error:
            table_sta_assoc['Result'] = 'NOK'
            table_sta_assoc['Exception'] = 'ERRO GERAÇÃO TABELA DE ASSOC WIFI: ' + error

        return table_sta_assoc


    ######Listar dispositivos conectados no WiFi Plus######
    def wifiplus_table(self, out_str, fmw=''):
        # Entrada: show map_info wifi_plus station_info

        raw_list = out_str.splitlines()
        print('SAIDA_WIFI---->', raw_list)
        info_wifiplus = {'wifi_stations': {
        },
            'base_port': {

            },
            'qty_bp_rep': '',
            'Results': '',
            'Exception': ''}

        try:

            raw_list = out_str.splitlines()
            print(raw_list)

            count_bp_rep = 0

            for key in raw_list:
                if re.match(r'(^[0-9]{2})', key):
                    list = key.split('\t')
                    print(list)

                    if len(list) == 2:
                        info_wifiplus['wifi_stations'][list[1]] = {
                            'ip_addr': '',
                            'mac_addr': '',
                            'ssid': '',
                            'hostname': '',
                            'rssi': ''
                        }
                        info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                        info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]

                    elif len(list) == 3:
                        info_wifiplus['wifi_stations'][list[1]] = {
                            'ip_addr': '',
                            'mac_addr': '',
                            'ssid': '',
                            'hostname': '',
                            'rssi': ''
                        }
                        info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                        info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                        info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[2]

                    elif len(list) > 3:
                        if 'BP2' in list:
                            if 'BP2' in list[2]:
                                count_bp_rep = count_bp_rep + 1
                                info_wifiplus['base_port'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                                info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                                info_wifiplus['base_port'][list[1]]['ssid'] = ''
                                info_wifiplus['base_port'][list[1]]['hostname'] = list[2] + '-' + list[3] + '-' + \
                                                                                  list[4]
                                info_wifiplus['base_port'][list[1]]['rssi'] = ''

                            else:
                                count_bp_rep = count_bp_rep + 1
                                info_wifiplus['base_port'][list[1]] = {
                                    'ip_addr': '',
                                    'mac_addr': '',
                                    'ssid': '',
                                    'hostname': '',
                                    'rssi': ''
                                }
                                info_wifiplus['base_port'][list[1]]['ip_addr'] = list[0]
                                info_wifiplus['base_port'][list[1]]['mac_addr'] = list[1]
                                info_wifiplus['base_port'][list[1]]['ssid'] = list[2]
                                info_wifiplus['base_port'][list[1]]['hostname'] = list[3] + '-' + list[4] + '-' + \
                                                                                  list[5]
                                info_wifiplus['base_port'][list[1]]['rssi'] = list[len(list) - 1]

                        else:
                            info_wifiplus['wifi_stations'][list[1]] = {
                                'ip_addr': '',
                                'mac_addr': '',
                                'ssid': '',
                                'hostname': '',
                                'rssi': ''
                            }
                            info_wifiplus['wifi_stations'][list[1]]['ip_addr'] = list[0]
                            info_wifiplus['wifi_stations'][list[1]]['mac_addr'] = list[1]
                            info_wifiplus['wifi_stations'][list[1]]['ssid'] = list[2]
                            info_wifiplus['wifi_stations'][list[1]]['hostname'] = list[3]
                            info_wifiplus['wifi_stations'][list[1]]['rssi'] = list[len(list) - 1]

            info_wifiplus['qty_bp_rep'] = count_bp_rep
            info_wifiplus['Results'] = 'OK'
            info_wifiplus['Exception'] = 'OK'


        except Exception as error:
            info_wifiplus['Results'] = 'NOK'
            info_wifiplus['Exception'] = 'ERRO NA GERACAO DA TABELA DE DEVICES WIFI 5G', error


        return info_wifiplus


    ######Listar informacoes WiFi 5GHz######
    def getWiFi5G(self, out_str):

        ###Entrada: >show wifi_plus all
        ###Necessário tempo maior para retorno do SSH

        raw_list = out_str.splitlines()

        print(raw_list)

        del raw_list[0]

        infoWiFi5G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': '',
            'qhop': '',
            'beamforming': '',
            'scs': '',
            'airfair': '',
            'maui': '',
            'mumimo': '',
            'wifi_plus0_status': '',
            'roaming': ''

        },
            'Result': '',
            'Exception': ''}

        try:

            for key in raw_list:
                list = key.split()
                # print(list)
                if len(list) > 1:
                    if list[1].startswith('bandwidth'):
                        infoWiFi5G['info']['bandwidth'] = list[2]
                        # print(list[2])
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi5G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi5G['info']['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi5G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        if len(list) == 3:
                            infoWiFi5G['info']['ssid'] = list[2]
                        else:
                            len_default = 3
                            plus_size = (len(list) - len_default) + 1
                            index = 2
                            ssid_name = ''
                            for i in range(plus_size):
                                index = index + i
                                if ssid_name != '':
                                    ssid_name = ssid_name + ' ' + list[index]
                                else:
                                    ssid_name = ssid_name + list[index]
                                index = 2

                            infoWiFi5G['info']['ssid'] = ssid_name

                    elif list[1].startswith('bssid'):
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi5G['info']['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi5G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi5G['info']['password'] = list[2]
                    elif list[1].startswith('channel_mode'):
                        infoWiFi5G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('channel'):
                        infoWiFi5G['info']['channel'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi5G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi5G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi5G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi5G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi5G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi5G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi5G['info']['region'] = list[2]

                    elif list[1].startswith('qhop') and len(list) == 3:
                        if infoWiFi5G['info']['qhop'] == '':
                            infoWiFi5G['info']['qhop'] = list[2]
                    elif list[1].startswith('beamforming'):
                        infoWiFi5G['info']['beamforming'] = list[2]
                    elif list[1].startswith('scs'):
                        infoWiFi5G['info']['scs'] = list[2]
                    elif list[1].startswith('airfair'):
                        infoWiFi5G['info']['airfair'] = list[2]
                    elif list[1].startswith('maui'):
                        infoWiFi5G['info']['maui'] = list[2]
                    elif list[1].startswith('mumimo'):
                        infoWiFi5G['info']['mumimo'] = list[2]
                    elif list[0].startswith('wifi_plus0_status'):
                        infoWiFi5G['info']['wifi_plus0_status'] = list[1]
                    elif list[1].startswith('roaming'):
                        # print(list[1])
                        infoWiFi5G['info']['roaming'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            return infoWiFi5G

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = error

            return infoWiFi5G


    ######Listar informacoes WiFi 2.4GHz######
    def getWiFi2G(self, out_str):

        ###Entrada: >show wifi all

        raw_list = out_str.splitlines()


        infoWiFi2G = {'info': {
            'bandwidth': '',
            'transmission_mode': '',
            'status': '',
            'hide': '',
            'ssid': '',
            'bssid': '',
            'authentication': '',
            'encryption': '',
            'password': '',
            'channel': '',
            'channel_mode': '',
            'gi': '',
            'dtim': '',
            'preamble': '',
            'wps': '',
            'wps_mode': '',
            'wmm': '',
            'region': ''
        },
            'Result': '',
            'Exception': ''}

        try:

            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    print(list[1])
                    if list[1].startswith('bandwidth'):
                        infoWiFi2G['info']['bandwidth'] = list[2]
                    elif list[1].startswith('transmission_mode'):
                        infoWiFi2G['info']['transmission_mode'] = list[2]
                    elif list[1].startswith('status'):
                        infoWiFi2G['info']['status'] = list[2]
                    elif list[1].startswith('hide'):
                        infoWiFi2G['info']['hide'] = list[2]
                    elif list[1].startswith('ssid'):
                        if len(list) == 3:
                            infoWiFi2G['info']['ssid'] = list[2]
                        else:
                            len_default = 3
                            plus_size = (len(list) - len_default) + 1
                            index = 2
                            ssid_name = ''
                            for i in range(plus_size):
                                index = index + i
                                if ssid_name != '':
                                    ssid_name = ssid_name + ' ' + list[index]
                                else:
                                    ssid_name = ssid_name + list[index]
                                index = 2

                            infoWiFi2G['info']['ssid'] = ssid_name
                    elif list[1].startswith('bssid'):
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1].startswith('channel_mode'):
                        infoWiFi2G['info']['channel_mode'] = list[2]
                    elif list[1].startswith('channel'):
                        if infoWiFi2G['info']['channel'] == '':
                            infoWiFi2G['info']['channel'] = list[2]
                    elif list[1].startswith('authentication'):
                        infoWiFi2G['info']['authentication'] = list[2]
                    elif list[1].startswith('encryption'):
                        infoWiFi2G['info']['encryption'] = list[2]
                    elif list[1].startswith('password'):
                        infoWiFi2G['info']['password'] = list[2]
                    elif list[1].startswith('gi'):
                        infoWiFi2G['info']['gi'] = list[2]
                    elif list[1].startswith('dtim'):
                        infoWiFi2G['info']['dtim'] = list[2]
                    elif list[1].startswith('preamble'):
                        infoWiFi2G['info']['preamble'] = list[2]
                    elif list[1].startswith('wps'):
                        infoWiFi2G['info']['wps'] = list[2]
                    elif list[1].startswith('wps_mode'):
                        infoWiFi2G['info']['wps_mode'] = list[2]
                    elif list[1].startswith('wmm'):
                        infoWiFi2G['info']['wmm'] = list[2]
                    elif list[1].startswith('region'):
                        infoWiFi2G['info']['region'] = list[2]
                    ###TRATAMETNO DO CANAL 2.4GHz


            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = error
            print(error)

        return infoWiFi2G


    #####Listar informacoes do DHCP LAN######
    def getDhcpSettingsHgu(self, output_str):
        # Entrada: dhcpserver show
        resultado = {'LAN': {
            'DHCP Server': '',
            'IP Inicio': '',
            'IP Final': '',
            'DNS Server': '',
            'Lease Time': '',
            'Gateway': '',
            'Option 42': '',
            'WAN VoIP Options': {
                'WAN Interface': '',
                'Option 42': ''
            },
            'AlternativeRange-NAT/PATLines': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': '',
                'Option 42': '',
            },
            'AlternativeRange-NAT/PATLines - 2': {
                'IP Inicio': '',
                'IP Final': '',
                'DNS Servers': '',
                'Gateway': '',
                'Vendor ClassID': '',
                'User ClassID': '',
                'Lease Time': ''
            },
        },
            'Result': {},
            'Exception': {}}
        try:
            raw_list = output_str.splitlines()
            # print('\n', raw_list)
            for i in raw_list:
                list = i.split()
                print('\n')
                print(list)
                if list[0].startswith('dhcpserver'):
                    print('OLAAA')
                    resultado['LAN']['DHCP Server'] = list[1]
                elif list[0].startswith('start'):
                    resultado['LAN']['IP Inicio'] = list[3]
                elif list[0].startswith('end'):
                    resultado['LAN']['IP Final'] = list[3]
                elif list[0].startswith('dnsserver'):
                    dnsServer = list[2]
                    resultado['LAN']['DNS Server'] = list[2]
                    # Workaroud para comando do Mitra BRCM Bug aberto
                    if dnsServer.startswith('192.168.1.1'):
                        resultado['LAN']['Gateway'] = '192.168.1.1'
                    elif dnsServer.startswith('192.168.15.1'):
                        resultado['LAN']['Gateway'] = '192.168.15.1'
                elif list[0].startswith('leased'):
                    try:
                        leaseTime = int(list[2]) * 3600
                    except:
                        leaseTime = '****'
                    resultado['LAN']['Lease Time'] = str(leaseTime)
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = 'NOK'
            print(error)

        return resultado


    ######Listar informacoes Opticas HGU######
    def getOpticalInfo(self, out_str):
        ###Entrada: >show ont optics
        # print(out_str)
        infoGpon = {'info':
                        {'vendor': '',
                         'model': '',
                         'type': '',
                         'class': '',
                         'ont_rx': '',
                         'ont_tx': ''},
                    'Result': '',
                    'Exception': ''
                    }
        # print('olaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        raw_list = out_str.splitlines()
        # print(raw_list)
        try:
            c = 0
            for key in raw_list:
                # print('linha #' + str(c) + '  ' + key)
                list = key.split(' ')
                # print(list)
                if len(list) > 0:
                    if list[0].startswith('ont_rx_power'):
                        # print(list[0], list[1])
                        infoGpon['info']['ont_rx'] = list[1]
                    elif list[0].startswith('ont_tx_power'):
                        infoGpon['info']['ont_tx'] = list[1]
                    elif list[0].startswith('ont_transceiver_vendor'):
                        infoGpon['info']['vendor'] = list[1]
                    elif list[0].startswith('ont_transceiver_model'):
                        infoGpon['info']['model'] = list[1]
                c = c + 1
                infoGpon['info']['type'] = 'GPON'
                infoGpon['info']['class'] = 'Class B'
                infoGpon['Result'] = 'OK'
                infoGpon['Exception'] = 'OK'

        except Exception as error:
            infoGpon['Result'] = 'NOK'
            infoGpon['Exception'] = error

        return infoGpon


    ####Verificar status interface Internet
    def statusInet(self, out_str):

        ###Entrada: >show primary_diagnosis internet_service status

        status_inet = {
            'status': '',
            'Result': '',
            'Exception': ''
        }
        print(out_str)
        try:
            raw_list = out_str.splitlines()

            for key in raw_list:
                if key.startswith('internet_service'):
                    list = key.split(' ')
                    status_inet['status'] = list[2]

            status_inet['Result'] = 'OK'
            status_inet['Exception'] = 'OK'

        except Exception as error:
            status_inet['Result'] = 'NOK'
            status_inet['Exception'] = error

        return status_inet


    ######Listar informacoes IP_Internet######
    def getIpWan(self, out_str):
        # print(out_str)
        print('tamanho de out = ', len(out_str))
        infoIpInet = {
            'iface': {
                'Voip_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Vod_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Multicast_ip_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                },
                'Internet_ppp_interface': {
                    'service_name': '',
                    'iface_name': '',
                    'protocol': '',
                    'pbit': '',
                    'vlan': '',
                    'igmp': '',
                    'status_v4': '',
                    'ipv4': '',
                    'uptime': '',
                    'status_v6': '',
                    'ipv6': '',
                }
            },
            'Result': '',
            'Exception': ''
        }
        if out_str[0]:
            raw_list = out_str[0].splitlines()

            del raw_list[0]
            del raw_list[0]
            del raw_list[0]


            try:
                for key in raw_list:
                    # print(key)
                    list = key.split()
                    # print('list = ', list)
                    if len(list) > 9 and list[2].startswith('VoIP'):

                        infoIpInet['iface']['Voip_ip_interface']['service_name'] = list[2]
                        infoIpInet['iface']['Voip_ip_interface']['iface_name'] = list[3]
                        infoIpInet['iface']['Voip_ip_interface']['protocol'] = list[4]
                        infoIpInet['iface']['Voip_ip_interface']['igmp'] = list[5]
                        infoIpInet['iface']['Voip_ip_interface']['status_v4'] = list[9]
                        infoIpInet['iface']['Voip_ip_interface']['ipv4'] = list[10]
                    elif len(list) > 9 and list[2].startswith('Mediaroom'):

                        infoIpInet['iface']['Vod_ip_interface']['service_name'] = list[2]
                        infoIpInet['iface']['Vod_ip_interface']['iface_name'] = list[3]
                        infoIpInet['iface']['Vod_ip_interface']['protocol'] = list[4]
                        infoIpInet['iface']['Vod_ip_interface']['igmp'] = list[5]
                        infoIpInet['iface']['Vod_ip_interface']['status_v4'] = list[9]
                        infoIpInet['iface']['Vod_ip_interface']['ipv4'] = list[10]
                    elif len(list) > 9 and list[2].startswith('Internet'):


                        infoIpInet['iface']['Internet_ppp_interface']['service_name'] = list[2]
                        infoIpInet['iface']['Internet_ppp_interface']['iface_name'] = list[3]
                        infoIpInet['iface']['Internet_ppp_interface']['protocol'] = list[4]
                        infoIpInet['iface']['Internet_ppp_interface']['igmp'] = list[5]
                        infoIpInet['iface']['Internet_ppp_interface']['status_v4'] = list[9]
                        infoIpInet['iface']['Internet_ppp_interface']['ipv4'] = list[10]


                    # elif len(list) > 5 and not list[0].startswith('tCon.'):
                    #     infoIpInet['iface'][list[1]]['ipv6'] = list[5]
                    #     infoIpInet['iface'][list[1]]['status_v6'] = list[4]
                    # print(infoIpInet)
                    # print('list[1] = ', list[1])
            except Exception as e:
                print(e)
        if out_str[1] != '':
            try:
                ipv6 = re.search(
                        r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))',
                        out_str[1])
                if ipv6:
                    ipv6 = ipv6.group()
                    infoIpInet['iface']['Internet_ppp_interface']['status_v6'] = 'Connected'
                    infoIpInet['iface']['Internet_ppp_interface']['ipv6'] = ipv6

                    # print(infoIpInet)
            except Exception as e:
                print(e)
                infoIpInet['Result'] = 'NOK'
                infoIpInet['Exception'] = 'NOK'
        if out_str[2] != '':
            infoIpInet['iface']['Internet_ppp_interface']['vlan'] = out_str[2]

        infoIpInet['Result'] = 'OK'
        infoIpInet['Exception'] = 'OK'



        return infoIpInet


    ####Verificar status GPON
    def getStatusOnt(self, out_str):

        status_onu = {
            'onu_status': '',
            'onu_status_description': '',
            'slid': '',
            'Result': '',
            'Exception': ''
            }

        try:
            raw_list = out_str.splitlines()
            for key in raw_list:
                lista = key.split()
                if len(lista) > 1:
                    if lista[0].startswith('ont_status'):
                        status_onu['onu_status'] = lista[1]
                        status = lista[1]
                        print(status)
                        if status == 'O5':
                            status_onu['onu_status_description'] = 'Operation'
                        elif status == 'O4':
                            status_onu['onu_status_description'] = 'Ranging'
                        elif status == 'O3' or status == 'O2':
                            status_onu['onu_status_description'] = 'SN Aquisition'
                        elif status == 'O1':
                            status_onu['onu_status_description'] = 'Syncronization'
                        elif status == 'O6':
                            status_onu['onu_status_description'] = 'Intermittent LODS'
                        elif status == 'O7':
                            status_onu['onu_status_description'] = 'Emergency Stop'
                        else:
                            status_onu['onu_status_description'] = 'Failure '

                    elif lista[0].startswith('ploam_password'):
                        status_onu['slid'] = lista[1]

            status_onu['Result'] = 'OK'
            status_onu['Exception'] = 'OK'

        except Exception as error:
            print(error)
            status_onu['Result'] = 'NOK'
            status_onu['Exception'] = 'NOK'

        return status_onu


    ####Verificar informações de PPPoE
    def verifyPppoeSettings(self, output_str):
        resultado = {'PPPoE': {'username': {},
                               'password': {}
                               },
                     'Result': {},
                     'Exception': {}}
        try:

            resultado['PPPoE']['username'] = 'cliente@cliente'
            resultado['PPPoE']['password'] = 'cliente'
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'

            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado

        ###### Executar Soft Reset ######


    ######Listar DNS IPv4 HGU######
    def getDnsIpv4Hgu(self, output_str):

        # Entrada: mdm getpv InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.DNSServers

        resultado = {'DNS_IPv4': {},
                     'Result': {},
                     'Exception': {}}
        # print(output_str)
        try:
            ans = output_str.splitlines()
            c = 0
            aux = []
            for i in ans:
                # print('linha #' + str(c) + '  ' + i)
                aux1 = i.split(' = ')
                aux.append(aux1)
                c = c + 1
            # print(aux)
            dns_out = []
            for i in aux:
                if i[0].startswith('Primary'):
                    dns_out.append(i[1])
                elif i[0].startswith('Secondary'):
                    dns_out.append(i[1])
            resultado['DNS_IPv4'] = dns_out
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            print(error)
            return resultado


    #####Listar informacoes Opticas HGU######
    def getSerialGpon(self, out_str):
        ###Entrada: >show ont optics
        # print(out_str)
        infoSerialGpon = {
                    'serial': '',
                    'Result': '',
                    'Exception': ''
                    }
        # print('olaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        raw_list = out_str.splitlines()
        print(raw_list)
        try:

            for key in raw_list:
                print(key)
                if key.startswith('MST'):
                    infoSerialGpon['serial'] = key

            infoSerialGpon['Result'] = 'OK'
            infoSerialGpon['Exception'] = 'OK'

        except Exception as error:
            infoSerialGpon['Result'] = 'NOK'
            infoSerialGpon['Exception'] = error

        return infoSerialGpon


    ###### Listar INFO IFCONFIG ######
    def getIfconfig(self, output_str, network=''):

        # Entrada: ifconfig

        infoIface = {
            'interfaces': {
                'network': '',
                'internet': {},
                'voip': {},
                'mediaroom': {},
                'vod': {}
            },
            'Result': '',
            'Exception': ''
        }

        try:

            raw_data = output_str.splitlines()

            tag_ppp0 = False
            tag_vod = False
            tag_voip = False
            tag_ipv6 = True

            for k in raw_data:
                info = k.split()

                if 'ppp0.1' in info or tag_ppp0:
                    try:
                        tag_ppp0 = True
                        if len(info) == 0:
                            tag_ppp0 = False
                        else:
                            if 'inet' in info:
                                ipv4 = info[1].split(':')
                                ipv4 = ipv4[1]
                                infoIface['interfaces']['internet']['ipv4'] = ipv4
                            elif 'inet6' in info:
                                if tag_ipv6:
                                    infoIface['interfaces']['internet']['ipv6'] = info[2]
                                    tag_ipv6 = False
                            elif 'UP' in info:
                                infoIface['interfaces']['internet']['status'] = 'UP'
                    except:
                        pass

                elif 'veip0.2' in info or tag_voip:
                    try:
                        tag_voip = True
                        if len(info) == 0:
                            tag_voip = False
                        else:
                            if 'inet' in info:
                                print(info)
                                ipv4 = info[1].split(':')
                                ipv4 = ipv4[1]
                                infoIface['interfaces']['voip']['ipv4'] = ipv4
                            elif 'UP' in info:
                                infoIface['interfaces']['voip']['status'] = 'UP'
                    except:
                        pass

                elif 'veip0.3' in info or tag_vod:
                    try:
                        tag_vod = True
                        if len(info) == 0:
                            tag_vod = False
                        else:
                            if 'inet' in info:
                                print(info)
                                ipv4 = info[1].split(':')
                                ipv4 = ipv4[1]
                                infoIface['interfaces']['mediaroom']['ipv4'] = ipv4
                            elif 'UP' in info:
                                infoIface['interfaces']['mediaroom']['status'] = 'UP'
                    except:
                        pass

            infoIface['interfaces']['network'] = network
            infoIface['Result'] = 'OK'
            infoIface['Exception'] = 'OK'

        except Exception as error:
            infoIface['Result'] = 'NOK'
            infoIface['Exception'] = 'ERRO AO CONSULTAR dhcpCondSettings'
            print(error)

        return infoIface


    ###### Listar DNS IPv6 HGU ######
    def getDnsIpv6Hgu(self, output_str):
        # print(output_str)
        # mdm getpv InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.X_TELEFONICA-ES_IPv6DNSServers
        resultado = {'DNS_IPv6': {},
                     'Result': {},
                     'Exception': {}}

        try:
            # print('tamanho out = ', len(output_str))
            # print('tipo out = ', type(output_str))
            output_str = output_str[0].replace(';', ',')
            aux = output_str.split(',')
            # print('aux = ', aux)
            dns_v6 = []
            dns_v6.append(aux[6])
            dns_v6.append(aux[7])
            resultado['DNS_IPv6'] = dns_v6
            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
        except Exception as e:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = 'NOK'
        return resultado


    ######Listar interfaces ETH utilizadas######
    def listEthIfaces(self, out_str):
        # Entrada: show map_info eth1_device information

        try:

            connect_lan = {'iface': '', 'ip_addr': 'not_connected', 'mac_addr': 'not_connected', 'Result': '',
                           'Exception': ''}

            raw_list = out_str.splitlines()

            for key in raw_list:
                sew = key.split()
                if sew[0].startswith('eth'):
                    iface = sew[0]
                    iface = iface.split('_')
                    iface = iface[0]
                    connect_lan['iface'] = iface
                elif not (sew[0].startswith('show') | sew[0].startswith('>') | \
                          sew[0].startswith('eth' + str(int) + '_device')):
                    if len(sew) > 1:
                        ip_addr = sew[0]
                        mac_addr = sew[1]
                    connect_lan['ip_addr'] = ip_addr
                    connect_lan['mac_addr'] = mac_addr.upper()

            connect_lan['Result'] = 'OK'
            connect_lan['Exception'] = 'OK'

            return connect_lan

        except Exception as error:
            connect_lan['Result'] = 'NOK'
            connect_lan['Exception'] = 'ERRO AO LISTAR INTERFACES LAN DO HGU: ', error

            return connect_lan


    ######Listar infor VoIP######
    def getInfoVoIP(self, out_str):

        ###Entrada: > voice show

        voipInfo = {
            'info': {
                'Voice_Profile': {
                    'ifName': '',
                    'ipAddr': '',
                    'ipVersion': '',
                    'manageProtocol': '',
                    'voiceProfile': '',
                    'profileState': '',
                    'local': '',
                    'dtmfMethod': '',
                    'hookFlashMethod': '',
                    'T38': '',
                    'V18': '',
                    'rtpDscpMark': '',
                    'rtpPortMin': '',
                    'rtpPortMax': '',
                    'sip': '',
                    'domain': '',
                    'port': '',
                    'transport': '',
                    'regExpires': '',
                    'regRetriveInterval': '',
                    'dscpMark': '',
                    'addrRegister': '',
                    'portRegister': '',
                    'addrProxy': '',
                    'portProxy': '',
                    'option120Addr': '',
                    'outboundProxyAddr': '',
                    'outboundProxyPort': '',
                    'uriConference': '',
                    'optionConference': ''
                },
                'Account': {
                    'lineEnableState': '',
                    'voipServiceStatus': '',
                    'reverserPolarity': '',
                    'callStatus': '',
                    'physicalReference': '',
                    'uri': '',
                    'number': '',
                    'authName': '',
                    'authPwd': '',
                    'txGain': '',
                    'rxGain': '',
                    'echoCancellation': '',
                    'callWaiting': ''
                },
                'Codec': {
                    'codec-1': '',
                    'codec-2': '',
                    'codec-3': ''
                }
            },
            'Result': '',
            'Exception': ''
        }

        raw_list = out_str.splitlines()

        try:
            for key in raw_list:
                list = key.split()
                tag = 'OK'
                if len(list) > 0:
                    print(list)
                    # ###INFORMAÇÕES VOICE PROFILE
                    if list[0].startswith('BoundIfList'):
                        voipInfo['info']['Voice_Profile']['ifName'] = list[2]
                    elif list[0].startswith('IP'):
                        voipInfo['info']['Voice_Profile']['ipAddr'] = list[3]
                    # elif list[0].startswith('IP'):
                    #     voipInfo['info']['Voice_Profile']['ipVersion'] = list[4]
                    elif list[0].startswith('Management'):
                        voipInfo['info']['Voice_Profile']['manageProtocol'] = list[3]
                    elif list[0].startswith('Associated'):
                        voipInfo['info']['Voice_Profile']['voiceProfile'] = list[3]
                    elif list[0].startswith('ProfileEnableState'):
                        voipInfo['info']['Voice_Profile']['profileState'] = list[2]
                    elif list[0].startswith('Locale'):
                        voipInfo['info']['Voice_Profile']['local'] = list[2]
                    elif list[0].startswith('DTMFMethod'):
                        voipInfo['info']['Voice_Profile']['dtmfMethod'] = list[2]
                    elif list[0].startswith('HookFlashMethod'):
                        voipInfo['info']['Voice_Profile']['hookFlashMethod'] = list[2]
                    elif list[0].startswith('T38'):
                        voipInfo['info']['Voice_Profile']['T38'] = list[2]
                    elif list[0].startswith('V18'):
                        voipInfo['info']['Voice_Profile']['V18'] = list[2]
                    elif list[0].startswith('RTPDSCPMark'):
                        voipInfo['info']['Voice_Profile']['rtpDscpMark'] = list[2]
                    elif list[0].startswith('RTPPortMin'):
                        voipInfo['info']['Voice_Profile']['rtpPortMin'] = list[2]
                    elif list[0].startswith('RTPPortMax'):
                        voipInfo['info']['Voice_Profile']['rtpPortMax'] = list[2]
                    elif list[0].startswith('Domain'):
                        if len(list) == 2:
                            voipInfo['info']['Voice_Profile']['domain'] = ''
                        else:
                            voipInfo['info']['Voice_Profile']['domain'] = list[2]
                    elif list[0].startswith('Port'):
                        voipInfo['info']['Voice_Profile']['port'] = list[2]
                    elif list[0].startswith('Transport'):
                        voipInfo['info']['Voice_Profile']['transport'] = list[2]
                    elif list[0].startswith('RegExpires'):
                        voipInfo['info']['Voice_Profile']['regExpires'] = list[2]
                    elif list[0].startswith('RegRetryInterval'):
                        voipInfo['info']['Voice_Profile']['regRetriveInterval'] = list[2]
                    elif list[0].startswith('DSCPMark'):
                        voipInfo['info']['Voice_Profile']['dscpMark'] = list[2]
                    elif list[0].startswith('Registrar') and list[1].startswith('Addr'):
                        if len(list) == 3:
                            voipInfo['info']['Voice_Profile']['addrRegister'] = ''
                        else:
                            voipInfo['info']['Voice_Profile']['addrRegister'] = list[3]

                    elif list[0].startswith('Registrar') and list[1].startswith('Port'):
                        if len(list) == 3:
                            voipInfo['info']['Voice_Profile']['portRegister'] = 'not_configured'
                        else:
                            voipInfo['info']['Voice_Profile']['portRegister'] = list[3]

                    elif list[0].startswith('Proxy') and list[1].startswith('Addr'):
                        if len(list) == 3:
                            voipInfo['info']['Voice_Profile']['addrProxy'] = 'not_configured'
                        else:
                            voipInfo['info']['Voice_Profile']['addrProxy'] = list[3]

                    elif list[0].startswith('Proxy') and list[1].startswith('Port'):
                        if len(list) == 3:
                            voipInfo['info']['Voice_Profile']['portProxy'] = 'not_configured'
                        else:
                            voipInfo['info']['Voice_Profile']['portProxy'] = list[3]

                    elif list[0].startswith('OutBoundProxy') and list[1].startswith('Addr'):
                        if len(list) == 3:
                            voipInfo['info']['Voice_Profile']['outboundProxyAddr'] = 'not_configured'
                        else:
                            voipInfo['info']['Voice_Profile']['outboundProxyAddr'] = list[3]

                    elif list[0].startswith('OutBoundProxy') and list[1].startswith('Port'):
                        if len(list) == 3:
                            voipInfo['info']['Voice_Profile']['outboundProxyPort'] = 'not_configured'
                        else:
                            voipInfo['info']['Voice_Profile']['outboundProxyAddr'] = list[3]

                    elif list[0].startswith('Conferencing') and list[1].startswith('URI'):
                        if len(list) == 2:
                            voipInfo['info']['Voice_Profile']['uriConference'] = 'not_configured'
                        else:
                            voipInfo['info']['Voice_Profile']['uriConference'] = list[3]

                    elif list[0].startswith('Conferencing') and list[1].startswith('Option'):
                        if len(list) == 2:
                            voipInfo['info']['Voice_Profile']['optionConference'] = 'not_configured'
                        else:
                            voipInfo['info']['Voice_Profile']['optionConference'] = list[3]
                    #
                    # ###INFORMAÇÕES LINHA SIP
                    elif list[0].startswith('ActivationStatus'):
                        voipInfo['info']['Account']['lineEnableState'] = list[2]
                    elif list[0].startswith('VoipServiceStatus'):
                        voipInfo['info']['Account']['voipServiceStatus'] = list[2]
                    # elif list[0].startswith('PolarityReverseState'):
                    #     voipInfo['info']['Account']['reverserPolarity'] = list[2]

                    elif list[0].startswith('CallStatus'):
                        voipInfo['info']['Account']['callStatus'] = list[2]
                    elif list[0].startswith('Associated'):
                        voipInfo['info']['Account']['physicalReference'] = list[3]
                    elif list[0].startswith('URI'):
                        if len(list) == 2:
                            voipInfo['info']['Account']['uri'] = 'not_configured'
                        else:
                            voipInfo['info']['Account']['uri'] = list[2]

                    elif list[0].startswith('Extension'):
                        if len(list) ==2:
                            voipInfo['info']['Account']['number'] = 'not_configured'
                        else:
                            voipInfo['info']['Account']['number'] = list[2]

                    elif list[0].startswith('AuthName'):
                        if len(list) == 2:
                            voipInfo['info']['Account']['authName'] = 'not_configured'
                        else:
                            voipInfo['info']['Account']['authName'] = list[2]

                    elif list[0].startswith('AuthPwd'):
                        if len(list) == 2:
                            voipInfo['info']['Account']['authPwd'] = 'not_configured'
                        else:
                            voipInfo['info']['Account']['authPwd'] = list[2]
                    # elif list[0].startswith('TxGain'):
                    #     voipInfo['info']['Account']['txGain'] = list[2]
                    # elif list[0].startswith('RxGain'):
                    #     voipInfo['info']['Account']['rxGain'] = list[2]
                    # elif list[0].startswith('EchoCancellation'):
                    #     voipInfo['info']['Account']['echoCancellation'] = list[2]
                    # elif list[0].startswith('CallWaiting'):
                    #     voipInfo['info']['Account']['callWaiting'] = list[2]
                    #
                    ###INFORMAÇÕES DSO CODECS
                    elif list[0].startswith('CodecList'):
                        voipInfo['info']['Codec']['codec-1'] = list[3]
                    elif list[0].startswith('(1)'):
                        voipInfo['info']['Codec']['codec-2'] = list[1]
                    elif list[0].startswith('(2)'):
                        voipInfo['info']['Codec']['codec-3'] = list[1]

            ###INFORMAÇÕES REDE GPON
            voipInfo['info']['Network'] = 'Vivo_1'

            voipInfo['Result'] = 'OK'
            voipInfo['Exception'] = 'OK'

        except Exception as error:
            voipInfo['Result'] = 'NOK'
            voipInfo['Exception'] = error
            print(error)

        return voipInfo


    ###### Verificar Device Info com Info do MDM######
    def verifyHguHardware(self, out_str):
        resultado = {
            'CPU': {
                'Used': '',
                'Free': ''
            },
            'MEMORIA': {
                'Used': '',
                'Free': ''
            },
            'TOP': {
                'Load average': {
                    '#1': '',
                    '#2': '',
                    '#3': ''
                },
                'Processos': {
                    '#1': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#2': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#3': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#4': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    },
                    '#5': {
                        'PID': '',
                        'PPID': '',
                        'USER': '',
                        'STAT': '',
                        'VSZ': '',
                        '%MEM': '',
                        '%CPU': '',
                        'COMMAND': ''
                    }
                }
            },
            'VALIDATION': {
                'CPU': {},
                'MEMORIA': {},
                'GERAL': {}
            },
            'Result': {},
            'Exception': {}
        }
        try:
            # print(out_str)
            list_cpu = out_str[0].split('\n')
            # print(list)
            for i in list_cpu:
                if i.startswith('used'):
                    resultado['CPU']['Used'] = int(re.findall(r'(\d+)', i)[0])
                elif i.startswith('free'):
                    resultado['CPU']['Free'] = int(re.findall(r'(\d+)', i)[0])

            list_memory = out_str[1].split('\n')
            # print(list)
            for i in list_memory:
                if i.startswith('percentaje_used'):
                    resultado['MEMORIA']['Used'] = int(re.findall(r'(\d+)', i)[0])
                elif i.startswith('percentaje_free'):
                    resultado['MEMORIA']['Free'] = int(re.findall(r'(\d+)', i)[0])

            out_str[2] = re.sub('<', '', out_str[2])
            list_top = out_str[2].split('\n')
            # print(list)
            aux_out = []
            for i in list_top:
                # print(i)
                if i.startswith('Load average'):
                    aux = i.split(' ')
                    aux_out.append(aux)
            # print(aux_out[0][2])
            resultado['TOP']['Load average']['#1'] = float(aux_out[0][2])
            resultado['TOP']['Load average']['#2'] = float(aux_out[0][3])
            resultado['TOP']['Load average']['#3'] = float(aux_out[0][4])

            aux_out = []
            for i in list_top[3:]:
                # print(i.split())
            #     i = re.sub('  +', ' ', i)
                aux1 = i.split()
                aux_out.append(aux1)
            # print(aux_out)
            resultado['TOP']['Processos']['#1']['PID'] = aux_out[1][0]
            resultado['TOP']['Processos']['#1']['PPID'] = aux_out[1][1]
            resultado['TOP']['Processos']['#1']['USER'] = aux_out[1][2]
            resultado['TOP']['Processos']['#1']['STAT'] = aux_out[1][3]
            resultado['TOP']['Processos']['#1']['VSZ'] = aux_out[1][4]
            resultado['TOP']['Processos']['#1']['%VSZ'] = aux_out[1][5]
            resultado['TOP']['Processos']['#1']['%CPU'] = aux_out[1][6]
            resultado['TOP']['Processos']['#1']['COMMAND'] = aux_out[1][7:]

            resultado['TOP']['Processos']['#2']['PID'] = aux_out[2][0]
            resultado['TOP']['Processos']['#2']['PPID'] = aux_out[2][1]
            resultado['TOP']['Processos']['#2']['USER'] = aux_out[2][2]
            resultado['TOP']['Processos']['#2']['STAT'] = aux_out[2][3]
            resultado['TOP']['Processos']['#2']['VSZ'] = aux_out[2][4]
            resultado['TOP']['Processos']['#2']['%VSZ'] = aux_out[2][5]
            resultado['TOP']['Processos']['#2']['%CPU'] = aux_out[2][6]
            resultado['TOP']['Processos']['#2']['COMMAND'] = aux_out[2][7:]

            resultado['TOP']['Processos']['#3']['PID'] = aux_out[3][0]
            resultado['TOP']['Processos']['#3']['PPID'] = aux_out[3][1]
            resultado['TOP']['Processos']['#3']['USER'] = aux_out[3][2]
            resultado['TOP']['Processos']['#3']['STAT'] = aux_out[3][3]
            resultado['TOP']['Processos']['#3']['VSZ'] = aux_out[3][4]
            resultado['TOP']['Processos']['#3']['%VSZ'] = aux_out[3][5]
            resultado['TOP']['Processos']['#3']['%CPU'] = aux_out[3][6]
            resultado['TOP']['Processos']['#3']['COMMAND'] = aux_out[3][7:]

            resultado['TOP']['Processos']['#4']['PID'] = aux_out[4][0]
            resultado['TOP']['Processos']['#4']['PPID'] = aux_out[4][1]
            resultado['TOP']['Processos']['#4']['USER'] = aux_out[4][2]
            resultado['TOP']['Processos']['#4']['STAT'] = aux_out[4][3]
            resultado['TOP']['Processos']['#4']['VSZ'] = aux_out[4][4]
            resultado['TOP']['Processos']['#4']['%VSZ'] = aux_out[4][5]
            resultado['TOP']['Processos']['#4']['%CPU'] = aux_out[4][6]
            resultado['TOP']['Processos']['#4']['COMMAND'] = aux_out[4][7:]

            resultado['TOP']['Processos']['#5']['PID'] = aux_out[5][0]
            resultado['TOP']['Processos']['#5']['PPID'] = aux_out[5][1]
            resultado['TOP']['Processos']['#5']['USER'] = aux_out[5][2]
            resultado['TOP']['Processos']['#5']['STAT'] = aux_out[5][3]
            resultado['TOP']['Processos']['#5']['VSZ'] = aux_out[5][4]
            resultado['TOP']['Processos']['#5']['%VSZ'] = aux_out[5][5]
            resultado['TOP']['Processos']['#5']['%CPU'] = aux_out[5][6]
            resultado['TOP']['Processos']['#5']['COMMAND'] = aux_out[5][7:]

            ### VALIDATION
            if resultado['CPU']['Free'] >= 50:
                resultado['VALIDATION']['CPU'] = 'OK'
            else:
                resultado['VALIDATION']['CPU'] = 'NOK'
            if resultado['MEMORIA']['Free'] >= 8:
                resultado['VALIDATION']['MEMORIA'] = 'OK'
            else:
                resultado['VALIDATION']['MEMORIA'] = 'NOK'
            if resultado['VALIDATION']['CPU'] == 'OK' and resultado['VALIDATION']['MEMORIA'] == 'OK':
                resultado['VALIDATION']['GERAL'] = 'OK'
            else:
                resultado['VALIDATION']['GERAL'] = 'NOK'

            resultado['Result'] = 'OK'
            resultado['Exception'] = 'OK'
            return resultado

        except Exception as error:
            resultado['Result'] = 'NOK'
            resultado['Exception'] = error
            return resultado


    ####Verificar Info Básicas do WiFi 2.4G
    def getWiFi2Gligth(self, out_str):

        ###Entrada: >show wifi

        raw_list = out_str.splitlines()
        print(raw_list)


        infoWiFi2G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                # print(list)
                if len(list) > 1:
                    if list[0] == 'wifi0_status':
                        infoWiFi2G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        infoWiFi2G['info']['ssid'] = list[2]
                    elif list[1] == 'bssid':
                        infoWiFi2G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi2G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi2G['info']['password'] = list[2]

            infoWiFi2G['Result'] = 'OK'
            infoWiFi2G['Exception'] = 'OK'

            return infoWiFi2G

        except Exception as error:
            infoWiFi2G['Result'] = 'NOK'
            infoWiFi2G['Exception'] = 'ERRO AO GERAR INFO BASICA 2.4GHz', error

            return infoWiFi2G


    ####Verificar Info Básicas do WiFi 5G
    def getWiFi5Gligth(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G = {'info': {
            'status': '',
            'ssid': '',
            'bssid': '',
            'channel': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus0_status':
                        infoWiFi5G['info']['status'] = list[1]
                    elif list[1] == 'ssid':
                        infoWiFi5G['info']['ssid'] = list[2]
                    elif list[1] == 'bssid':
                        infoWiFi5G['info']['bssid'] = list[2]
                    elif list[1] == 'channel':
                        infoWiFi5G['info']['channel'] = list[2]
                    elif list[1] == 'password':
                        infoWiFi5G['info']['password'] = list[2]

            infoWiFi5G['Result'] = 'OK'
            infoWiFi5G['Exception'] = 'OK'

            return infoWiFi5G

        except Exception as error:
            infoWiFi5G['Result'] = 'NOK'
            infoWiFi5G['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz', error

            return infoWiFi5G


    def getWiFi5GligthBS(self, out_str):

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()
        print(raw_list)

        # del raw_list[0]
        # del raw_list[0]

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': ''
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        print(list)
                        plus_size = (len(list) - len_default) + 1
                        print(plus_size)
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name

                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'


        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS', error

        return infoWiFi5G_BS


    def ip_porta(self, out_str, modelo, fmw=''):
        # mapeamento IP para porta

        ##--> File com informações dos modelos e firmware suportados
        file_devices = open("files/supported_devices.json", "r")
        devices = json.load(file_devices)
        file_devices.close()

        ##--> Info devices Mitra Ecnt
        mitra_brcm_model = devices['supported']['mitra_brcm_model']
        mitra_brcm_fw = devices['supported']['mitra_brcm_fw']

        # Entrada: 'show map_info dhcp_table'

        raw_list = out_str.splitlines()

        ip_porta = {'Result': '', 'Exception': '', 'Descrption': ''}

        porta_map = {"wifi station_info": "wifi24",
                     "wifi_plus station_info": "wifi5",
                     "eth1_device information": "eth1",
                     "eth2_device information": "eth2",
                     "eth3_device information": "eth3",
                     "eth4_device information": "eth4"
                     }

        try:
            if fmw in mitra_brcm_fw:
                demarcadores_interface = ["wifi station_info", "wifi_plus station_info", "eth1_device information",
                                          "eth2_device information", "eth3_device information",
                                          "eth4_device information"]
                demarcadores_invalidos = ["arp_table", "dhcp_table"]

                key_atual = ""
                for key in raw_list:
                    if (key in demarcadores_invalidos):
                        key_atual = ""
                    elif (key in demarcadores_interface):
                        key_atual = key

                        demarcadores_interface.remove(key)
                    elif (key_atual != ""):
                        disp = key.split()

                        if (disp[0] == '>'):
                            continue

                        if ('RTF3507' in modelo and porta_map[key_atual] == "eth4"):
                            porta = "hpna"
                        else:
                            porta = porta_map[key_atual]

                        try:
                            ip_porta[disp[0]]
                        except:
                            ip_porta[disp[0]] = {}

                        ip_porta[disp[0]].update({"porta_hgu": porta, "mac": disp[1]})
            else:
                ip_porta['Result'] = 'NOK'
                ip_porta['Description'] = 'Firmware do HGU não suportado.'
                ip_porta['Exception'] = 'NOK'
        except Exception as e:
            ip_porta['Result'] = 'NOK'
            ip_porta['Description'] = 'Erro ao mapear IP para porta no HGU.'
            ip_porta['Exception'] = e

        if (ip_porta['Result'] != 'NOK'):
            ip_porta['Result'] = 'OK'
            ip_porta['Description'] = 'OK'
            ip_porta['Exception'] = 'OK'

        return ip_porta


    def lanhosts(self, out_str, so_iptv = False):
        hosts = []
        raw_list = out_str.splitlines()

        for item in raw_list:
            cols = item.split()
            print(cols, '1')

            if len(cols) > 3:
                try:
                    ip=cols[2]
                except:
                    continue

                if (eh_ip(ip) == True):
                    try:
                        mac = cols[1]
                        # vendorclass = cols[3]
                        ip_stb = ip.split('.')
                        last_oct = int(ip_stb[3])
                    except:
                        continue

                    # if (vendorclass != "TEF_IPTV" and so_iptv == True):
                    #     continue
                    if (last_oct < 200 and so_iptv == True):
                        continue

                    hosts.append([mac,ip])

        return hosts



    def getWiFi5GBS(self, out_str):

        print(out_str)

        ###Entrada: >show wifi_plus

        raw_list = out_str.splitlines()

        infoWiFi5G_BS = {'info': {
            'status': '',
            'ssid': '',
            'password': '',
            'hide': '',
            'authentication': '',
            'encryption': '',
        },
            'Result': '',
            'Exception': ''
        }
        try:
            for key in raw_list:
                list = key.split()
                if len(list) > 1:
                    if list[0] == 'wifi_plus1' and list[1] == 'status':
                        infoWiFi5G_BS['info']['status'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'ssid':
                        len_default = 3
                        plus_size = (len(list) - len_default) + 1
                        index = 2
                        ssid_name = ''
                        for i in range(plus_size):
                            index = index + i
                            if ssid_name != '':
                                ssid_name = ssid_name + ' ' + list[index]
                            else:
                                ssid_name = ssid_name + list[index]
                            index = 2
                            infoWiFi5G_BS['info']['ssid'] = ssid_name
                    elif list[0] == 'wifi_plus1' and list[1] == 'password':
                        infoWiFi5G_BS['info']['password'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'hide':
                        infoWiFi5G_BS['info']['hide'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'authentication':
                        infoWiFi5G_BS['info']['authentication'] = list[2]
                    elif list[0] == 'wifi_plus1' and list[1] == 'encryption':
                        infoWiFi5G_BS['info']['encryption'] = list[2]

            infoWiFi5G_BS['Result'] = 'OK'
            infoWiFi5G_BS['Exception'] = 'OK'

        except Exception as error:
            infoWiFi5G_BS['Result'] = 'NOK'
            infoWiFi5G_BS['Exception'] = 'ERRO AO GERAR INFO BASICA 5GHz_BS'

        return infoWiFi5G_BS


###Classe utilizada para comandas universais
class cliHgu():
    def __init__(self, password, ip):
        self.user_support = 'support'
        self.password = password
        self.ip = ip

    ######Listar modelo do dispositivo######
    def device_model(self, out_str):

            # Entrada: show device_model

            ###STEP-00: JSON SAIDA
            device_info = {
                'model': '',
                'region': '',
                'Result': 'NOK',
                'Exception': 'NOK'
            }

            try:
                raw_list = out_str.splitlines()

                for key in raw_list:
                    ###Exception para dispositivo Mitra ECNT
                    if key.startswith('device_'):
                        list = key.split()
                        model = list[1]
                        region_aux = model.split('-')
                        if len(region_aux) > 2:
                            region = 'N2'
                        else:
                            region = 'N1'

                    ###Utilizado para Askey BRCM
                    elif key.startswith('device'):
                        list = key.split()
                        model = list[2]
                        region = model.split('-')
                        region = region[1]

                    ###Utilizado para Askey ECNT
                    elif key.startswith(' RTF') or key.startswith('RTF'):
                        model = key
                        region = ''

                    ###Utilizado para Mitra BRCM
                    elif key.startswith('GPT'):
                        list = key.split()
                        model = list[0]
                        region = model.split('-')
                        region = region[2]

                device_info['model'] = model
                device_info['region'] = region
                device_info['Result'] = 'OK'
                device_info['Exception'] = 'OK'

            except Exception as error:
                device_info['Result'] = 'NOK'
                device_info['Exception'] = error
                print(error)

            return device_info
