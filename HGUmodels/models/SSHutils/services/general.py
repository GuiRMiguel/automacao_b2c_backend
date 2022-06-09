import json
import re

def sumHex(mac, sumNumber):
    number = mac.replace(':', '')
    hex_string = '0x' + number.replace(':', '')
    # hex_string = '0xf'
    an_integer = int(hex_string, 16) + sumNumber
    hex_value = hex(an_integer)
    new_value = hex_value.replace('0x', '')

    bssid = ''
    count = 0

    for i in new_value:
        bssid = bssid + i
        count = count +1
        if count == 2:
            bssid = bssid + ':'
            count = 0

    bssid = bssid.strip(':')

    return bssid


def jsonFile(file):
    file_path = 'files/jsonFiles/'
    file_extension = '.json'
    file_name = 'print'

    file_name_full = file_path + file_name + file_extension

    with open(file_name_full, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)


# se for MAC Address, retorna True
def eh_macaddr(texto):
    mac_re = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$"

    return (bool(re.match(mac_re, texto.lower())))


# se for IP, retorna True
def eh_ip(texto):
    ip_re = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    return (bool(re.match(ip_re,texto)))


def ProcuraVal(procurar, texto):
    retorno = re.search(procurar, texto)

    if retorno:
        retorno = retorno.group(1)
        return retorno.strip()

    return False


#Convert Hex fto Ascii
def hexToAscii(input_text):

    print(input_text)
    bytes_input_hex = bytes.fromhex(input_text)
    ascii_string = bytes_input_hex.decode('ASCII')
    print(ascii_string)

    return ascii_string


def macToSerial(serial):

    mac = ''
    count = 0
    for i in serial:
        mac = mac + i
        count = count +1
        if count == 2:
            mac = mac + ':'
            count = 0

    mac = mac.strip(':')

    return mac


