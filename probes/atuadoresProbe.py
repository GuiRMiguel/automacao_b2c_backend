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


    # 2
    def twoSecondsSwitchTwentyTimes(self, ip_arduino, rele, model_name):
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
            "ProbeName": "setAccessClass", 
            "Probe#": "XXXXXXX", 
            "Description": "", 
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
            "ProbeName": "setAccessClass", 
            "Probe#": "XXXXXXX", 
            "Description": "", 
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

