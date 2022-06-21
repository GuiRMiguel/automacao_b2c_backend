from flask_restful import Resource
from probes import atuadoresProbe
from flask import jsonify, request
import requests
from connector.controllers import configAtuadores
from connector.controllers import configRele

from daos.mongo_dao import MongoConnSigleton

mongo_conn = MongoConnSigleton()


class atuadores(Resource):

    def post(self, method):

        obj = atuadoresProbe.atuadores()
        print(method)

        if method == "arduinoReguaLigaDesliga":
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            selectRele = configRele.models[modelo]['power']

            ip_arduino = configAtuadores.reles[selectRele]['ip_arduino']
            rele = configAtuadores.reles[selectRele]['rele']
            tempo_desligado = configAtuadores.reles[selectRele]['tempo_desligado']
            tempo_ligado = configAtuadores.reles[selectRele]['tempo_ligado']
            repeticoes = configAtuadores.reles[selectRele]['repeticoes']

            result = obj.arduinoReguaLigaDesliga(ip_arduino,rele,tempo_desligado,tempo_ligado,repeticoes, modelo)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == "twoSecondsSwitchTwentyTimes":
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            selectRele = configRele.models[modelo]['power']

            ip_arduino = configAtuadores.reles[selectRele]['ip_arduino']
            rele = configAtuadores.reles[selectRele]['rele']
            tempo_desligado = configAtuadores.reles[selectRele]['tempo_desligado']
            tempo_ligado = configAtuadores.reles[selectRele]['tempo_ligado']
            repeticoes = configAtuadores.reles[selectRele]['repeticoes']

            result = obj.twoSecondsSwitchTwentyTimes(ip_arduino, rele, tempo_desligado, tempo_ligado, repeticoes, modelo)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)
            

        elif method == "arduinoPressionaSimultaneo":
            ip_arduino = request.json['ip_arduino']
            rele1 = request.json['rele1']
            rele2 = request.json['rele2']
            rele3 = request.json['rele3']
            tempo = request.json['tempo']
            
            ans = obj.arduinoPressionaSimultaneo(ip_arduino,rele1,rele2,rele3,tempo)
            
        elif method == "arduinoMedeFreqIntermitenciaLED":
            ip_arduino = request.json['ip_arduino']
            portaAnalogica = request.json['portaAnalogica']
            medirTempoMax = request.json['medirTempoMax']
            
            ans = obj.arduinoMedeFreqIntermitenciaLED(ip_arduino,portaAnalogica,medirTempoMax)
            
        elif method == "arduinoMedeTempoIntermitenciaLED":
            ip_arduino = request.json['ip_arduino']
            portaAnalogica = request.json['portaAnalogica']
            tempoEsperado = request.json['tempoEsperado']
            tempoTolerancia = request.json['tempoTolerancia']
            
            ans = obj.arduinoMedeTempoIntermitenciaLED(ip_arduino,portaAnalogica,tempoEsperado,tempoTolerancia)
            
        elif method == "reguaAPCLigaDesliga":
            # Objetivo: liga, desliga ou verifica status da régua de alimentação. Comando executado por tomada.
            # comando: liga, desliga, status
            # tomada da régua: 1 à 8
            
            ip_regua = request.json['ip_regua']
            tomada = request.json['tomada']
            comando = request.json['comando']
            
            ans = obj.reguaAPCLigaDesliga(ip_regua,tomada,comando)

        else:
            return {"name_teste": "Doesnt Exist", "response": "none"}

        return jsonify(ans)