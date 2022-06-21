from probes import iptvProbe
import pathlib
import requests
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from io import BytesIO
import pandas as pd
import zeep
import json
from json import JSONEncoder
from HGUmodels.factory import HGUModelFactory
from webdriver.webdriver import WebDriver


class atuadores:

    def __init__(self):
        self.ip = []
        self.username = []
        self.password = []


    def twoSecondsSwitchTwentyTimes(self, ip_arduino, rele, tempo_desligado, tempo_ligado, repeticoes, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "setAccessClass", 
            "Probe#": "XXXXXXX", 
            "Description": "", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
            'tempo_desligado': tempo_desligado,
            'tempo_ligado': tempo_ligado,
            'repeticoes': repeticoes
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.twoSecondsSwitchTwentyTimes_2(dados_entrada)


    def arduinoReguaLigaDesliga(self, ip_arduino, rele, tempo_desligado, tempo_ligado, repeticoes):
        try:
            url = 'http://' + ip_arduino + "/_ligaDesliga_" + str(rele) + '_' + str(tempo_ligado) + '_' + str(
                tempo_desligado) + '_' + str(repeticoes)
            requests.get(url, timeout=30)
            return {"Resultado_Probe": "OK", "ControllerName": "atuadores", "ProbeName": "arduinoReguaLigaDesliga", "Probe#": "XX",
                    "Description": "Acionar equipamento via rele", "URL": url, "Resultado": "200_OK"}
        except:
            return {"Resultado_Probe": "NOK", "ControllerName": "atuadores", "ProbeName": "arduinoReguaLigaDesliga", "Probe#": "XX",
                    "Description": "Acionar equipamento via rele", "URL": url, "Resultado": "Erro no envio do comando para o arduino."}

    def arduinoPressionaSimultaneo(self, ip_arduino, rele1, rele2, rele3, tempo):
        # Para hard reset, por exemplo.
        try:
            url = 'http://' + ip_arduino + "/_pressSimult_" + str(rele1) + '_' + str(rele2) + '_' + str(rele3) + '_' + str(tempo)
            requests.get(url, timeout=5)

            return {"Resultado_Probe": "OK", "ControllerName": "atuadores", "ProbeName": "arduinoPressionaSimultaneo", "Probe#": "XX",
                    "Description": "Acionar até três botôes simultaneamente.", "URL": url, "Resultado": "200_OK"}

        except:
            return {"Resultado_Probe": "NOK", "ControllerName": "atuadores", "ProbeName": "arduinoPressionaSimultaneo", "Probe#": "XX",
                    "Description": "Acionar até três botôes simultaneamente.", "URL": url, "Resultado": "Erro no envio do comando para o arduino."}

    def arduinoMedeFreqIntermitenciaLED(self, ip_arduino,portaAnalogica,medirTempoMax):
        # Verifica a frequencia que o LED está alternando (entre aceso e apagado).
        # medirTempoMax = Tempo maximo de medição
        # retorna media dos tempos. Se LED não estiver intermitente, retorna erro.

        try:
            url = 'http://' + ip_arduino + "/_medeLuzFreqIntermit_" + str(portaAnalogica) + '_' + str(medirTempoMax)
            resposta = requests.get(url, timeout=60)
            resultado = resposta.content.decode()

            cmd_status, cmd_detalhe = resultado.split(",")
            mediaTempoOn, mediaTempoOff = cmd_detalhe.split("/")

            mediaTempoOn = mediaTempoOn.strip()
            mediaTempoOff = mediaTempoOff.strip()

            return {"Resultado_Probe": cmd_status, "ControllerName": "atuadores", "ProbeName": "arduinoMedeFreqIntermitenciaLED", "Probe#": "XX",
                    "Description": "Mede a frequência em que o LED está alternando.", "URL": url, "mediaTempoOn": mediaTempoOn, "mediaTempoOff": mediaTempoOff, "Resultado": "200_OK"}
        except:
            return {"Resultado_Probe": "NOK", "ControllerName": "atuadores", "ProbeName": "arduinoMedeFreqIntermitenciaLED", "Probe#": "XX",
                    "Description": "Mede a frequência em que o LED está alternando.", "URL": url, "Resultado": "Erro no envio do comando para o arduino."}

    def arduinoMedeTempoIntermitenciaLED(self, ip_arduino,portaAnalogica,tempoEsperado,tempoTolerancia):
        # Verifica o tempo que o LED permanece alternando (entre aceso e apagado).
        # tempoEsperado = Quanto tempo o LED tem que ficar alternando, em segundos
        # tempoTolerancia = Tempo, em segundos, de tolerancia para mais e para menos em relação ao tempo esperado.

        try:
            url = 'http://' + ip_arduino + "/_medeLuzTempoIntermit_" + str(portaAnalogica) + '_' + str(tempoEsperado) + '_' + str(tempoTolerancia)

            resposta = requests.get(url, timeout=180)
            resultado = resposta.content.decode()

            cmd_status, cmd_detalhe = resultado.split(",")
            cmd_status = cmd_status.strip()
            cmd_detalhe = cmd_detalhe.strip()

            if cmd_status == "OK":
                Resultado_Probe_Detalhe = "Tempo de intermitência Ok."
                TempoIntermitencia = cmd_detalhe
            elif cmd_status == "NOK":
                Resultado_Probe_Detalhe = cmd_detalhe
                TempoIntermitencia = ""

            return {"Resultado_Probe": cmd_status, "Resultado_Probe_Detalhe": Resultado_Probe_Detalhe, "TempoIntermitencia": TempoIntermitencia, "ControllerName": "atuadores", "ProbeName": "arduinoMedeTempoIntermitenciaLED", "Probe#": "XX",
                    "Description": "Mede o tempo que o LED permanece intermitente (piscando)", "URL": url, "Resultado": "200_OK"}
        except:
            return {"Resultado_Probe": "NOK", "Resultado_Probe_Detalhe": "", "TempoIntermitencia": "", "ControllerName": "atuadores", "ProbeName": "arduinoMedeTempoIntermitenciaLED", "Probe#": "XX",
                    "Description": "Mede o tempo que o LED permanece intermitente (piscando)", "URL": url, "Resultado": "Erro no envio do comando para o arduino."}

    def reguaAPCLigaDesliga(self, ip_regua, tomada, comando):
        # Comandos relativos à regua da APC, utilizada no cenário IPTV (mesmo modelo da utilizada no Witbe)
        # comandos: liga, desliga e status da toma (se ligada ou desligada)
        # IP régua: 10.10.10.31

        porta_udp = 161
        status_tomada=""

        try:
            if comando == "liga":
                errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
                    cmdgen.CommunityData('private', 'private', 1),
                    cmdgen.UdpTransportTarget((ip_regua, porta_udp)),
                    ((1, 3, 6, 1, 4, 1, 318, 1, 1, 4, 4, 2, 1, 3, tomada), rfc1902.Integer("1")))
            elif comando == "desliga":
                errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
                    cmdgen.CommunityData('private', 'private', 1),
                    cmdgen.UdpTransportTarget((ip_regua, porta_udp)),
                    ((1, 3, 6, 1, 4, 1, 318, 1, 1, 4, 4, 2, 1, 3, tomada), rfc1902.Integer("2")))
            elif comando == "status":
                outlet_state = {1: 'ON', 2: 'OFF', 4: 'UNKNOWN'}
                outlets = dict(zip(range(1, 9), [4] * 8))

                errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                    cmdgen.CommunityData('my-agent', 'public', 0),
                    cmdgen.UdpTransportTarget((ip_regua, porta_udp)),
                    (1, 3, 6, 1, 4, 1, 318, 1, 1, 4, 4, 2, 1, 3, tomada))
                outlets[tomada] = varBinds[0][1]
                status_tomada = outlet_state[varBinds[0][1]]

            return {"Resultado_Probe": "OK", "tomada": tomada, "comando": comando, "status_tomada": status_tomada, "ControllerName": "atuadores", "ProbeName": "reguaAPCLigaDesliga", "Probe#": "XX",
                    "Description": "Atua na régua elétrica.", "Resultado": "200_OK"}
        except:
            return {"Resultado_Probe": "NOK", "tomada": tomada, "comando": comando, "status_tomada": status_tomada, "ControllerName": "atuadores", "ProbeName": "reguaAPCLigaDesliga", "Probe#": "XX",
                    "Description": "Atua na régua elétrica.", "Resultado": "Erro no envio do comando para a régua APC."}


    def irtransComando(self, stbID, comando):
        # print(comando,led)
        iptvObj = iptvProbe.iptv()

        led = int(stbID) + 1
        #b_obj = BytesIO()
        url_irtrans = "http://" + iptvObj.ip_irtrans + "/send.htm?remote=vivobrasil&command=" + comando + "&led=" + str(led)
        resposta = requests.get(url_irtrans, timeout=180)
        #crl = pycurl.Curl()
        #crl.setopt(crl.URL, url_irtrans)
        #crl.setopt(crl.WRITEDATA, b_obj)
        #crl.perform()
        #crl.close()


    def irtransTrocaCanal(self, stbID, canal):
        if canal == "proximo":
            self.irtransComando(stbID, "next_channel")
        elif canal == "anterior":
            self.irtransComando(stbID, "prev_channel")
        else:
            for n in canal:
                self.irtransComando(stbID, "b" + n)
                time.sleep(0.7)
            if (len(canal) < 3):
                self.irtransComando(stbID, "ok_button")
        time.sleep(0.05)
        print("irtransTrocaCanal() - STB:" + str(stbID) + ") - canal:" + canal + ")")