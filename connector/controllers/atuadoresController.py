from flask_restful import Resource
from flask import jsonify, request
import requests
from connector.controllers import configAtuadores

from daos.mongo_dao import MongoConnSigleton
from probes import atuadoresProbe
import HGUmodels.models.Atuadoresutils.utils
mongo_conn = MongoConnSigleton()


class atuadores(Resource):

    def post(self, method):

        print(method)


        if method == "twoSecondsSwitchTwentyTimes":
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            ip_arduino = configAtuadores.atuadores['arduino_01']['ip_arduino']

            rele = configAtuadores.atuadores['arduino_01']['HGU']['model'][modelo]['power']

            obj = atuadoresProbe.tests()
            result = obj.twoSecondsSwitchTwentyTimes(ip_arduino, rele, modelo)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == "ONTSwitchFiftyTimes":
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            ip_arduino = configAtuadores.atuadores['arduino_01']['ip_arduino']

            rele = configAtuadores.atuadores['arduino_01']['devices']['ONT']['power']

            obj = atuadoresProbe.tests()
            result = obj.ONTSwitchFiftyTimes(ip_arduino, rele, modelo)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == "twoSecondsSwitchTwentyTimesONT":
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            ip_arduino = configAtuadores.atuadores['arduino_01']['ip_arduino']

            rele = configAtuadores.atuadores['arduino_01']['devices']['ONT']['power']

            obj = atuadoresProbe.tests()
            result = obj.twoSecondsSwitchTwentyTimesONT(ip_arduino, rele, modelo)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == "STBSwitchFiftyTimes":
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            ip_arduino = configAtuadores.atuadores['arduino_01']['ip_arduino']

            rele = configAtuadores.atuadores['arduino_01']['devices']['STB']['power']

            obj = atuadoresProbe.tests()
            result = obj.STBSwitchFiftyTimes(ip_arduino, rele, modelo)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == "twoSecondsSwitchTwentyTimesSTB":
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            ip_arduino = configAtuadores.atuadores['arduino_01']['ip_arduino']

            rele = configAtuadores.atuadores['arduino_01']['devices']['ONT']['power']

            obj = atuadoresProbe.tests()
            result = obj.twoSecondsSwitchTwentyTimesSTB(ip_arduino, rele, modelo)
            print('\nresult:', result, '\n')
            test_result = result['result']
            ans = {'test_result': result}
            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)


        elif method == "arduinoReguaLigaDesliga":
            ip_arduino = request.json['ip_arduino']
            rele = request.json['rele']
            tempo_desligado = request.json['tempo_desligado']
            tempo_ligado = request.json['tempo_ligado']
            repeticoes = request.json['repeticoes']
            obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
            ans = obj.arduinoReguaLigaDesliga(ip_arduino,rele,tempo_desligado,tempo_ligado,repeticoes)
            return jsonify(ans)
            

        elif method == "arduinoPressionaSimultaneo":
            ip_arduino = request.json['ip_arduino']
            rele1 = request.json['rele1']
            rele2 = request.json['rele2']
            rele3 = request.json['rele3']
            tempo = request.json['tempo']

            obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
            ans = obj.arduinoPressionaSimultaneo(ip_arduino,rele1,rele2,rele3,tempo)
            
        elif method == "arduinoMedeFreqIntermitenciaLED":
            ip_arduino = request.json['ip_arduino']
            portaAnalogica = request.json['portaAnalogica']
            medirTempoMax = request.json['medirTempoMax']

            obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
            ans = obj.arduinoMedeFreqIntermitenciaLED(ip_arduino,portaAnalogica,medirTempoMax)
            
        elif method == "arduinoMedeTempoIntermitenciaLED":
            ip_arduino = request.json['ip_arduino']
            portaAnalogica = request.json['portaAnalogica']
            tempoEsperado = request.json['tempoEsperado']
            tempoTolerancia = request.json['tempoTolerancia']
            
            obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
            ans = obj.arduinoMedeTempoIntermitenciaLED(ip_arduino,portaAnalogica,tempoEsperado,tempoTolerancia)
            
        elif method == "reguaAPCLigaDesliga":
            # Objetivo: liga, desliga ou verifica status da régua de alimentação. Comando executado por tomada.
            # comando: liga, desliga, status
            # tomada da régua: 1 à 8
            
            ip_regua = request.json['ip_regua']
            tomada = request.json['tomada']
            comando = request.json['comando']
            
            obj = HGUmodels.models.Atuadoresutils.utils.atuadores()
            ans = obj.reguaAPCLigaDesliga(ip_regua,tomada,comando)

        else:
            return {"name_teste": "Doesnt Exist", "response": "none"}

        return jsonify(ans)