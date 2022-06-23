from probes import cliProbe
from probes import tsharkProbe
import HGUmodels.models.Atuadoresutils.utils
from probes import opencvProbe
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.all import *
import os
from probes import networkProbe
import numpy as np
import time

class ErrorGetDhcpCondPool(Exception):
    pass

class iptv:
    def __init__(self):
        # Regua de energia (ip_re), emissor de infravermelho (ir_trans), switch HPE
        self.ip_re = '10.10.10.31'
        self.ip_irtrans = "10.10.10.32"
        self.ip_switch_hpe = "10.10.10.10"
        self.switch_hpe_user = "admin"
        self.switch_hpe_senha = "hpe@2021"
        self.switch_hpe_dest_mirror_port = "22"

        # definições plataforma IPTV
        self.dhcpOption60OP = "TEF_IPTV"
        self.dhcpOption60MR = "MSFT_IPTV"
        self.dnss_iptv = np.array(['177.16.30.67', '177.16.30.7'])

        # PODs e atuadores
        self.pod_stb_ip=[0,1,2,3]
        self.pod_stb_mac_eth=[0,1,2,3]
        self.pod_stb_casn=[0,1,2,3]
        self.pod_stb_modelo=[0,1,2,3]
        self.pod_stb_switch_port=[0,1,2,3]
        self.pod_hgu_ip=[0,1,2,3]
        self.pod_hgu_switch_hpe_vlan=[0,1,2,3]
        self.pod_hgu_senha=[0,1,2,3]
        self.pod_hgu_modelo=[0,1,2,3]
        self.pod_hgu_versao=[0,1,2,3]
        self.pod_hgu_switch_port=[0,1,2,3]
        self.pod_hgu_urlLANCfg=[0,1,2,3]

        # POD1=0, POD2=1, PODN=N-1.
        # STBs
        self.pod_stb_mac_eth[0] = "8c:5b:f0:e0:ab:16"
        self.pod_stb_ip[0] = "192.168.15.230"
        self.pod_stb_casn[0] = "2252696709"
        self.pod_stb_modelo[0] = "VIP5262"
        self.pod_stb_switch_port[0] = "2"
        self.pod_stb_mac_eth[1] = "e8:82:5b:12:7f:1c"
        self.pod_stb_ip[1] = "192.168.16.230"
        self.pod_stb_casn[1] = "2249208908"
        self.pod_stb_modelo[1] = "VIP4242H"
        self.pod_stb_switch_port[1] = "6"
        self.pod_stb_mac_eth[2] = "98:f7:d7:87:ee:5b"
        self.pod_stb_ip[2] = "192.168.17.230"
        self.pod_stb_casn[2] = "2249188044"
        self.pod_stb_modelo[2] = "VIP4242H"
        self.pod_stb_switch_port[2] = "10"
        self.pod_stb_mac_eth[3] = "8c:5b:f0:de:16:0c"
        self.pod_stb_ip[3] = "192.168.18.234"
        self.pod_stb_casn[3] = "2252266208"
        self.pod_stb_modelo[3] = "VIP4242H"
        self.pod_stb_switch_port[3] = "14"

        # HGUs
        self.pod_hgu_ip[0] = "192.168.15.1"
        self.pod_hgu_switch_hpe_vlan[0] = "15"
        self.pod_hgu_senha[0] = "6d298a86"
        self.pod_hgu_modelo[0] = ""
        self.pod_hgu_versao[0] = ""
        self.pod_hgu_switch_port[0] = "1"
        self.pod_hgu_urlLANCfg[0] = "lancfg2.html"
        self.pod_hgu_ip[1] = "192.168.16.1"
        self.pod_hgu_switch_hpe_vlan[1] = "16"
        self.pod_hgu_senha[1] = "b7ubtman"
        self.pod_hgu_modelo[1] = ""
        self.pod_hgu_versao[1] = ""
        self.pod_hgu_switch_port[1] = "5"
        self.pod_hgu_ip[2] = "192.168.17.1"
        self.pod_hgu_switch_hpe_vlan[2] = "17"
        self.pod_hgu_senha[2] = "ind95ams"
        self.pod_hgu_modelo[2] = ""
        self.pod_hgu_versao[2] = ""
        self.pod_hgu_switch_port[2] = "9"
        self.pod_hgu_ip[3] = "192.168.18.1"
        self.pod_hgu_switch_hpe_vlan[3] = "18"
        self.pod_hgu_senha[3] = "ee111e3a"
        self.pod_hgu_modelo[3] = ""
        self.pod_hgu_versao[3] = ""
        self.pod_hgu_switch_port[3] = "13"

    def checkSTBIPPool(self, cenario, stb):
        # test cases: 674, 675, 676
        ip_hgu = self.pod_hgu_ip[int(cenario) - 1]

        tempo_captura = 60

        try:
            ip_hgu = self.pod_hgu_ip[int(cenario)-1]
            username = "support"
            password = self.pod_hgu_senha[int(cenario)-1]
            pagina = self.pod_hgu_urlLANCfg[int(cenario)-1]
    
            obj = cliProbe.cli()
            #print(ip_hgu," ",username," ",password," ",pagina)
    
            filtro = "var dhcpCondSrvStart = '(.+?)';"
            ans = obj.execHGUHTTPGetFiltrar(ip_hgu, username, password, pagina, filtro)
            #print(str(ans))
            Resultado_Probe = ans["Resultado_Probe"]
    
            if (Resultado_Probe == "NOK"):
                Resposta = ans["Resposta"]
                raise ErrorGetDhcpCondPool
            else:
                iptvIPInicial = ans["Resposta"]
    
            time.sleep(2)
            filtro = "var dhcpCondSrvEnd = '(.+?)';"
            ans = obj.execHGUHTTPGetFiltrar(ip_hgu, username, password, pagina, filtro)
            #print(str(ans))
            Resultado_Probe = ans["Resultado_Probe"]
    
            if (Resultado_Probe == "NOK"):
                Resposta = ans["Resposta"]
                raise ErrorGetDhcpCondPool
            else:
                iptvIPFinal = ans["Resposta"]
    
            print("DHCP Pool condicional: " + iptvIPInicial + " " + iptvIPFinal)

            stb_porta_switch = self.pod_stb_switch_port[int(cenario)-1]

            print("Ativando port mirror no switch HPE.")
            objSwitchHPE = networkProbe.network()
            objSwitchHPE.portMirrorHPE(self.ip_switch_hpe,self.switch_hpe_user,self.switch_hpe_senha,stb_porta_switch,self.switch_hpe_dest_mirror_port,"ativar")
    
            obj = tsharkProbe.tsharkCapture()
    
            arq_captura = "cen"+str(cenario)+"_stb"+str(stb)+"_dhcp.pcap"
            ans = obj.captureCustom(str(tempo_captura), "captura", "D:\\ocv\\", arq_captura, "udp port 67")
    
            resultadoCaptura = ans["Resultado_Probe"]
    
            if ( resultadoCaptura != "OK"):
                print("Desativando port mirror no switch HPE.")
                objSwitchHPE.portMirrorHPE(self.ip_switch_hpe, self.switch_hpe_user, self.switch_hpe_senha,
                                           stb_porta_switch, self.switch_hpe_dest_mirror_port, "desativar")
                return {"Resultado_Probe": "NOK", "cenario": cenario, "stb": stb, "ControllerName": "iptv",
                        "ProbeName": "checkSTPIPPool", "Probe#": "XX",
                        "Description": "Verificar se STB pega IP do Pool correto por DHCP.",
                        "Resultado": "Erro na captura."}
    
            time.sleep(2)
            print("Captura iniciada")
    
            obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
            obj.reguaAPCLigaDesliga(self.ip_re, cenario, "desliga")
            print("STB desligado")
    
            time.sleep(1)
            obj.reguaAPCLigaDesliga(self.ip_re, cenario, "liga")
            print("STB ligado")

            print("Aguardando STB iniciar... (sleep " + str(tempo_captura) + "s)")
            time.sleep(tempo_captura)
            print("Desativando port mirror no switch HPE.")
            objSwitchHPE.portMirrorHPE(self.ip_switch_hpe, self.switch_hpe_user, self.switch_hpe_senha, stb_porta_switch, self.switch_hpe_dest_mirror_port, "desativar")

            arq_captura = "D:\\ocv\\cen" + str(cenario) + "_stb" + str(stb) + "_dhcp.pcap"
            stb_option60 = ""
            stb_ip = ""
            stb_mac = ""
            stb_dnss = []

            print ("Verificando captura...")

            pacotes_cnt = 0
            for (pkt_data, pkt_metadata,) in RawPcapReader(arq_captura):
                pacotes_cnt += 1
                ether_frame = Ether(pkt_data)
                ip_pkt = ether_frame[IP]

                if (ether_frame.haslayer(DHCP)):
                    #print(str(ether_frame[DHCP].options))
                    req_type = next(opt[1] for opt in ether_frame[DHCP].options if isinstance(opt, tuple) and opt[0] == 'message-type')

                    if (req_type == 1): # discovery
                        stb_option60 = self.dhcpOptionValue(ether_frame[DHCP],'vendor_class_id')[0].decode("UTF-8")
                        stb_mac = ether_frame.src

                    if (req_type == 5): # ack
                        stb_ip = ip_pkt.dst
                        stb_dnss = self.dhcpOptionValue(ether_frame[DHCP],'name_server')
                        stb_dnss = np.array(stb_dnss)
                        #stb_dnss = np.append(stb_dnss,["1.1.1.1"])

                    if (stb_ip != "" and stb_option60 != "" and stb_mac != "" and len(stb_dnss) > 0):
                        break

            if ( pacotes_cnt == 0 ):
                return {"Resultado_Probe": "NOK", "cenario": cenario, "stb": stb, "ControllerName": "iptv",
                        "ProbeName": "checkSTBIPPool", "Probe#": "XX",
                        "Description": "Verificar se STB pega IP do Pool correto por DHCP.", "Resultado": "Nenhum pacote capturado."}

            print("Captura verificada")
            print ("stb_ip: " + stb_ip )
            print ("stb_option60: " + str(stb_option60) )
            print ("stb_mac: " + str(stb_mac))
            print ("stb_dnss: " + str(stb_dnss))
            print ("iptv_dnss: " + str(self.dnss_iptv))

            comp = np.array_equal(stb_dnss,self.dnss_iptv)
            #print("comp:" + str(comp))

            falharam = ""

            if ( stb_option60 != self.dhcpOption60OP):
                falharam = "stb_option60"

            if ( comp == False ):
                falharam = "iptv_dnss " + falharam

            stb_ip_arr = stb_ip.split(".")
            iptvIPInicial_arr = iptvIPInicial.split(".")
            iptvIPFinal_arr = iptvIPFinal.split(".")

            if ((stb_ip_arr[0] != iptvIPInicial_arr[0] or stb_ip_arr[1] != iptvIPInicial_arr[1] or stb_ip_arr[2] != iptvIPInicial_arr[2]) or not (int(stb_ip_arr[3]) >= int(iptvIPInicial_arr[3]) and int(stb_ip_arr[3]) <= int(iptvIPFinal_arr[3]))):
                falharam = "ip_address " + falharam

            #os.remove(arq_captura)
            falharam = falharam.strip()
            #print("falharam:" + falharam)

            print("Teste finalizado")

            if ( falharam == "" ):
                return {"Resultado_Probe": "OK", "cenario": cenario, "stb": stb, "ControllerName": "iptv",
                        "ProbeName": "checkSTBIPPool", "Probe#": "XX", "stb_ip": stb_ip,
                        "stb_option60": stb_option60, "stb_mac": stb_mac, "stb_dnss": str(stb_dnss),
                        "Description": "Verificar se STB pega IP do Pool correto por DHCP.", "Resultado": "200_OK"}
            else:
                return {"Resultado_Probe": "NOK", "cenario": cenario, "stb": stb, "ControllerName": "iptv",
                        "ProbeName": "checkSTBIPPool", "Probe#": "XX", "stb_ip": stb_ip,
                        "stb_option60": stb_option60, "stb_mac": stb_mac, "stb_dnss": str(stb_dnss),
                        "Description": "Verificar se STB pega IP do Pool correto por DHCP.", "Resultado": "Falharam no teste: "+falharam}

        except ErrorGetDhcpCondPool:
            return {"Resultado_Probe": "NOK", "cenario": cenario, "stb": stb, "ControllerName": "iptv",
                    "ProbeName": "checkSTBIPPool", "Probe#": "XX",
                    "Description": "Verificar se STB pega IP do Pool correto por DHCP.", "Resultado": Resposta}
        except:
            return {"Resultado_Probe": "NOK", "cenario": cenario, "stb": stb, "ControllerName": "iptv",
                    "ProbeName": "checkSTBIPPool", "Probe#": "XX",
                    "Description": "Verificar se STB pega IP do Pool correto por DHCP.", "Resultado": "Erro durante a execucao do teste."}

    def dhcpOptionValue(self, payload, opcao):
        valor = next(opt for opt in payload.options if isinstance(opt, tuple) and opt[0] == opcao)

        list_op = list(valor)
        list_op.pop(0)
        valor = tuple(list_op)

        return valor

    def timeToService(self, cenario, elementoEmTeste, elementoId, evento, tempo_maximo):
        if (elementoEmTeste == "STB"):
            # coloca STB na VLAN do HGU
            vlan_stb = self.pod_hgu_switch_hpe_vlan[int(cenario)]

            obj = networkProbe.network()
            ans = obj.portChangeVLANHPE(self.ip_switch_hpe, self.switch_hpe_user, self.switch_hpe_senha, self.pod_stb_switch_port[int(elementoId)], vlan_stb)

            Resultado_Probe = ans["Resultado_Probe"]

            if (Resultado_Probe == "NOK"):
                return {"Resultado_Probe": "NOK", "elementoEmTeste": elementoEmTeste, "elementoId": elementoId,
                        "ControllerName": "iptv", "cenario": cenario, "tempo_maximo": tempo_maximo,
                        "ProbeName": "timeToService", "Probe#": "XX", "evento": evento,
                        "Description": "Mede tempo para o serviço voltar a funcionar mediante a um evemto (exemplo, queda de energia).",
                        "Resultado": "Não foi possível mudar a VLAN do cenário."}

            ocvObj = opencvProbe.opencv()

            if (evento == "bootEletricoSTB"):
                # reinicia STB eletricamente
                obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
                obj.reguaAPCLigaDesliga(self.ip_re, (int(elementoId) + 1), "desliga")
                print("STB " + elementoId + " desligado")

                time.sleep(1)
                obj.reguaAPCLigaDesliga(self.ip_re, (int(elementoId) + 1), "liga")
                print("STB " + elementoId + " ligado")
            elif (evento == "bootEletricoHGU"):
                resTela = ocvObj.posicionarGraphene(elementoId, True)

                if (resTela == False):
                    return {"Resultado_Probe": "NOK", "elementoEmTeste": elementoEmTeste, "elementoId": elementoId,
                            "ControllerName": "iptv", "cenario": cenario, "tempo_maximo": tempo_maximo,
                            "ProbeName": "timeToService", "Probe#": "XX", "evento": evento,
                            "Description": "Mede tempo para o serviço voltar a funcionar mediante a um evemto (exemplo, queda de energia).",
                            "Resultado": "Teste não iniciado. Serviço não está Ok no STB."}

                obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
                obj.reguaAPCLigaDesliga(self.ip_re, (int(cenario) + 5), "desliga")
                print("HGU " + cenario + " desligado")

                time.sleep(1)
                obj.reguaAPCLigaDesliga(self.ip_re, (int(cenario) + 5), "liga")
                print("HGU " + cenario + " ligado")
            else:
                return {"Resultado_Probe": "NOK", "elementoEmTeste": elementoEmTeste, "elementoId": elementoId,
                        "ControllerName": "iptv", "cenario": cenario, "tempo_maximo": tempo_maximo,
                        "ProbeName": "timeToService", "Probe#": "XX", "evento": evento,
                        "Description": "Mede tempo para o serviço voltar a funcionar mediante a um evemto (exemplo, queda de energia).",
                        "Resultado": "Evento não reconhecido."}

            # aguarda conteudo na tela
            resTela = ocvObj.aguardaTela(elementoId, [['componentes_destaques.png', "imagem", True],
                              ['tela_inicial_area_video_tot_l65x280_c33x640.png', "video", True],
                              ['color_bar_l90x150_c7x378.png', "imagem", False],
                              ['erro_gcn11.png', "imagem", False],
                              ['componentes_vivoplay_csd_l81x103_c490x576_fc(3)253x253b_253x253g_253x253r.png',
                               "mascara", True],
                              ['tela_inicial_area_video_dir_l133x263_c463x608.png', "telapreta", False],
                              ['erro_gcn11_2_l175x187_c384x454.png', "imagem", False]],
                              tempo_maximo)
            del ocvObj

            if (resTela == False):
                return {"Resultado_Probe": "NOK", "elementoEmTeste": elementoEmTeste, "elementoId": elementoId,
                        "ControllerName": "iptv", "ProbeName": "timeToService", "Probe#": "XX",
                        "evento": evento, "cenario": cenario, "tempo_maximo": tempo_maximo,
                        "Description": "Mede tempo para o serviço voltar a funcionar mediante a um evemto (exemplo, queda de energia).",
                        "Resultado": "Conteúdo/Serviço não voltou a funcionar dentro do tempo máximo."}

            return {"Resultado_Probe": "OK", "elementoEmTeste": elementoEmTeste, "elementoId": elementoId,
                        "ControllerName": "iptv", "ProbeName": "timeToService", "Probe#": "XX",
                        "evento": evento, "cenario": cenario, "tempo_maximo": tempo_maximo, "tempo_medido(s):": resTela,
                        "Description": "Mede tempo para o serviço voltar a funcionar mediante a um evemto (exemplo, queda de energia).",
                        "Resultado": "Ok."}

        else:
            return {"Resultado_Probe": "NOK", "elementoEmTeste": elementoEmTeste, "elementoId": elementoId, "ControllerName": "iptv",
                "ProbeName": "timeToService", "Probe#": "XX", "evento": evento, "cenario": cenario, "tempo_maximo": tempo_maximo,
                "Description": "Mede tempo para o serviço voltar a funcionar mediante a um evemto (exemplo, queda de energia).",
                "Resultado": "elementoEmTeste desconhecido."}