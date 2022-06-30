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
import time



class tests:
    
    def __init__(self):
        self.ip = []
        self.username = []
        self.password = []

    # 1
    def sequentialSwitchFiftyTimes(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "sequentialSwitchFiftyTimes", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 50 vezes o interruptor do dispositivo com intervalo de 2 segundos sequenciais", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.sequentialSwitchFiftyTimes_1(dados_entrada)



    # 2
    def twoSecondsSwitchTwentyTimes(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "twoSecondsSwitchTwentyTimes", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 20 vezes o interruptor do dispositivo com intervalo de 2 segundos", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.twoSecondsSwitchTwentyTimes_2(dados_entrada)


    # 3
    def ONTSwitchFiftyTimes(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "ONTSwitchFiftyTimes", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 50 vezes o interruptor da ONT sequencialmente", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.ONTSwitchFiftyTimes_3(dados_entrada)


    # 4
    def twoSecondsSwitchTwentyTimesONT(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "twoSecondsSwitchTwentyTimesONT", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 20 vezes o interruptor da ONT com intervalo de 2 segundos", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.twoSecondsSwitchTwentyTimesONT_4(dados_entrada)


    # 5
    def STBSwitchFiftyTimes(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "STBSwitchFiftyTimes", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 50 vezes o interruptor da STB sequencialmente", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.STBSwitchFiftyTimes_5(dados_entrada)


    # 6
    def twoSecondsSwitchTwentyTimesSTB(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "twoSecondsSwitchTwentyTimesSTB", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 20 vezes o interruptor da STB sequencialmente", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.twoSecondsSwitchTwentyTimesSTB_6(dados_entrada)


    # 7
    def reguaSwitchFiftyTimes(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "reguaSwitchFiftyTimes", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 50 vezes o interruptor da régua sequencialmente", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.reguaSwitchFiftyTimes_7(dados_entrada)


    # 8
    def twoSecondsSwitchTwentyTimesRegua(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "twoSecondsSwitchTwentyTimesRegua", 
            "Probe#": "XXXXXXX", 
            "Description": "Desligar 20 vezes o interruptor da régua sequencialmente", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.twoSecondsSwitchTwentyTimesRegua_8(dados_entrada)


    # 26
    def WPS2GHzFiveSeconds(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "WPS2GHzFiveSeconds", 
            "Probe#": "XXXXXXX", 
            "Description": "Pressionar por 5 segundos o botão WPS 2.4GHz para parear com o device", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.WPS2GHzFiveSeconds_26(dados_entrada)


    # 28
    def WPS5GHzFiveSeconds(self, ip_arduino, rele, model_name):
        dict_result = {
            "result": "failed",
            "Resultado_Probe": "NOK", 
            "ControllerName": "acs", 
            "ProbeName": "WPS5GHzFiveSeconds", 
            "Probe#": "XXXXXXX", 
            "Description": "Pressionar por 5 segundos o botão WPS 5GHz para parear com o device", 
            "obs": None}

        dados_entrada = {
            'ip_arduino': ip_arduino,
            'rele': rele,
        }

        hgu = HGUModelFactory.getHGU(
            probe='functionalProbe', 
            model_name=model_name, 
            dict_result=dict_result)

        return hgu.WPS5GHzFiveSeconds_28(dados_entrada)


    

