import json
import os

##-->Leitura arquivo de default Parameters
def getDefaultParams():
    try:
        if os.name == 'nt':
            path = 'files/default_params.json'
        elif os.name == 'posix':
            path = '/home/automacao/Projects/automacao_b2c_backend/HGUmodels/models/SSHutils/files/default_params.json'

    except Exception as e:
        print(e)
        pass

    try:
        file_params = open(path, "r")
        params = json.load(file_params)
        file_params.close()

    except Exception as error:
        params = {
            'resultado': 'nok',
            'exception': 'nok'
        }

    return params