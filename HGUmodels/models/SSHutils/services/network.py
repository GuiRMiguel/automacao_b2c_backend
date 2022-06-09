import datetime
import time
import paramiko
from paramiko_expect import SSHClientInteraction
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException
import socket
from multiping import MultiPing
import speedtest
import platform
import sys
import os
from subprocess import Popen, PIPE
import re
import traceback
from paramiko_expect import SSHClientInteraction
# from geoip import geolite2
import logging
# from ip2geotools.databases.noncommercial import DbIpCity
import platform
import sys
import os
from subprocess import Popen, PIPE
import re
import traceback
import dns.resolver
from datetime import datetime
import io
from ping3 import verbose_ping
# import vlc
import ntplib
from time import ctime
import struct
# logger = paramiko.util.logging.getLogger()
# logging.basicConfig(level=logging.DEBUG)

###Método para estabelecer um canal SSH com o HGU
def connectSSH(ip, username, password):

    result = {
        'connection': '',
        'status': '',
        'exception': ''
    }

    try:

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=username, password=password, timeout=5, allow_agent=False,
                    look_for_keys=False, banner_timeout=10)

        channel = ssh.invoke_shell()
        result['ssh'] = ssh
        result['connection'] = channel
        result['status'] = 'OK'
        result['exception'] = ''

    except AuthenticationException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE SENHA INSERIDA'}

    except socket.timeout as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE CABO DESCONETADO' }

    except SSHException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': error}

    except BadHostKeyException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE HOST SERVER KEY'}

    except Exception as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': error}

    finally:
        try:
            if result['status'] == 'NOK':
                ssh.close()
                channel.transport.close()
                channel.close()
        except:
            pass

    return result


###Método para enviar e recebre comandos enviados ao HGU
def send_and_get_command(channel, cmd, sleep):
    try:

        bufsize = 65000
        if not cmd.endswith("\n"):
            cmd += "\n"
        # channel.send(cmd)
        channel.send(cmd)
        output = ''
        results = ''
        # print(channel.send_ready())
        # results = get_command_results(channel)
        time.sleep(sleep)
        results = channel.recv(bufsize)
        results = results.decode('unicode_escape')




    except Exception as error:
        print(error)
        results = 'EXCEPTION-CMD_NOT_SENT'

    return results


###Executação de ping para IP específico
def ping(ip, num_ping=15):
    try:

        ans_ping = {
            'Success_OK': '',
            'Success_NOK': '',
            'Resultado': '',
            'Exception': ''}

        i = 0
        success = 0
        success_nok = 0
        while i <= num_ping:
            time.sleep(0.1)

            ping = MultiPing([ip])
            ping.send()

            responses, no_responses = ping.receive(1)
            # print(responses)

            if responses != {}:
                success = success + 1
            else:
                success_nok = success_nok + 1
                ans_ping['Resultado'] = 'NOK'
                ans_ping['Exception'] = 'SEM CONECTIVIDADE'
            i = i + 1
        if success >= 2:
            ans_ping['Success_OK'] = success
            ans_ping['Success_NOK'] = success_nok
            ans_ping['Resultado'] = 'OK'
            ans_ping['Exception'] = 'OK'
        else:
            ans_ping['Success_OK'] = success
            ans_ping['Success_NOK'] = success_nok
            ans_ping['Resultado'] = 'NOK'
            ans_ping['Exception'] = 'NOK'
        return ans_ping

    except Exception as error:

        ans_ping['Resultado'] = 'NOK'
        ans_ping['Exception'] = 'NOK'
        print(str(error))
        return ans_ping


###Método otimizado para estabelecer/testar uma conexão SSH com o HGU
def checkSSH(ip, username, password):

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=username, password=password, timeout=5, allow_agent=False,
                    look_for_keys=False)

        channel = ssh.invoke_shell()

        transport = ssh.get_transport()
        status = transport.is_active()

        #Fechando conexão ssh para não impactar outras sessões.
        time.sleep(1)
        channel.transport.close()

        if status:
            return {'connection': 'channel_OK', 'status': 'OK', 'exception': '' }
        else:
            return {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'Transport Failed' }

    except AuthenticationException:
        return {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'Authentication failed'}

    except socket.timeout:
        return {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'Timeout de conexão' }

    except SSHException as sshException:
        return {'connection': 'channel_NOK', 'status': 'NOK', 'exception':
                'Unable to establish SSH connection'}

    except BadHostKeyException as badHostKeyException:
        return {'connection': 'channel_NOK', 'status': 'NOK', 'exception':
                'Unable to verify servers host key' }


###Método para execução de speed test
def speedTest(veloc_min, flag_server=True, num_servidores=2):
    resultSpeedTest = {
        'info': {
            'download': '',
            'upload': '',
            'ping': '',
            'latency': '',
            'ip_client': '',
            'ip_isp': '',
            'server_name': '',
            'perda': '',
        },
        'Result': '',
        'Exception': ''
    }

    os_info = platform.system()

    if os_info != 'Windows':
        try:
            servers = [16438]
            # servers = []
            # threads = None
            threads = 10
            s = speedtest.Speedtest()
            # print(s.get_servers())
            # s.get_servers(servers)
            s.get_best_server()
            # print(s.get_servers(servers))
            s.download(threads=threads)
            s.upload(threads=threads)
            s.results.share()
            res = s.results.dict()
            # print(res)

            resultSpeedTest['info']['download'] = str(round(int(res['download'])/1000000, 2)) + ' [Mbps]'
            resultSpeedTest['info']['upload'] = str(round(int(res['upload'])/1000000, 2)) + ' [Mbps]'
            resultSpeedTest['info']['ping'] = str(res['ping'])
            resultSpeedTest['info']['latency'] = str(res['server'].get('latency'))
            resultSpeedTest['info']['server_name'] = res['server'].get('name')
            resultSpeedTest['info']['ip_client'] = res['client'].get('ip')
            resultSpeedTest['info']['ip_isp'] = res['client'].get('isp')

            resultSpeedTest['Result'] = 'OK'
            resultSpeedTest['Exception'] = 'OK'

            return resultSpeedTest

        except Exception as error:
            resultSpeedTest['Result'] = 'NOK'
            print(error)
            resultSpeedTest['Exception'] = 'Não foi possível executar Speed Test'

            return resultSpeedTest
    else:
        try:
            servidores = []

            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
                #application_path = application_path + '\\files\\bin\\'
                os.chdir(application_path)
            else:
                application_path = os.path.dirname(os.path.realpath(__file__))
                application_path = application_path.replace("\\services", "")
                #application_path = application_path + '\\files\\bin\\'

            print("application_path: " + application_path)
            application_path = application_path + "\\"
            process = Popen([application_path + "speedtest.exe", "--accept-license", "--accept-gdpr", "-L"], stdout=PIPE, stderr=PIPE)

            (output, err) = process.communicate()
            exit_code = process.wait()
            output = output.decode()

            try:
                err = err.decode() # "cp1251"
            except:
                pass

            if (err != ""):
                traceback.print_exc()
                resultSpeedTest['Result'] = 'NOK'
                resultSpeedTest['Exception'] = "Erro ao obter a lista de servidores do speedtest."

                print (str(resultSpeedTest) + " \n " + str(err))
                return resultSpeedTest

            print(output)

            servidores_arr = output.split("\r\n")

            if flag_server == True:
                servidores.append(['16438', 'SPPD', 'São Paulo', 'Brasil'])

            #print ("num_servidores:" + str(num_servidores) + " flag_server:" + str(flag_server))

            for i in range(len(servidores_arr)):
                server = servidores_arr[i].split("  ")

                if (server[0] == False or server[0] == "" or server[0].startswith("Close") or server[0].startswith("ID") or server[0].startswith("===")):
                    continue

                #print("add servidor(" + str(i) + "): " + server[0] + " " + server[1])
                server[0] = server[0].strip()
                servidores.append([server[0],server[1]])

            if (num_servidores > len(servidores)):
                num_servidores = len(servidores)

            print ("num_servidores:" + str(num_servidores) + " len(servidores):" + str(len(servidores)) + " flag_server:" + str(flag_server))
            output = ""
            taxa_download = 0.0
            server_name = ""
            server_id = ""

            output = [""] * num_servidores
            err = [""] * num_servidores
            melhor_veloc = 0.0
            melhor_veloc_id = -1

            for i in range(num_servidores):
                server_id = servidores[i][0]
                server_name = servidores[i][1]

                print("Executando:" + str(application_path) + " \speedtest.exe" + " --accept-license" + " -s " + server_id)
                process = Popen([application_path + "\speedtest.exe", "--accept-license", "--accept-gdpr", "-s", server_id], stdout=PIPE, stderr=PIPE)
                (output[i], err[i]) = process.communicate()
                exit_code = process.wait()
                output[i] = output[i].decode()
                try:
                    err[i] = err[i].decode()
                except:
                    err[i] = str(err[i])

                print("output speedtest.exe:\n" + str(output[i]) + "\n" + str(err[i]))

                taxa_download = ProcuraVal('Download: +(.+?) +Mbps', output[i])
                print("velocidade servidor (" + str(i) + "):" + server_name + " id:" + server_id + " veloc down:" + str(taxa_download))

                if (taxa_download == False):
                    continue
                elif (float(taxa_download) >= veloc_min):
                    melhor_veloc_id = i
                    print("velocidade Ok")
                    break
                else:
                    if (float(taxa_download) > melhor_veloc):
                        melhor_veloc = float(taxa_download)
                        melhor_veloc_id = i
                    print("velocidade NOK")

            if (melhor_veloc_id != -1):
                server_name = ProcuraVal('Server: +(.+?)\r\n', output[melhor_veloc_id])
                taxa_download = ProcuraVal('Download: +(.+?) +Mbps', output[melhor_veloc_id])
                taxa_upload = ProcuraVal('Upload: +(.+?) +Mbps', output[melhor_veloc_id])
                latencia = ProcuraVal('Latency: +(.+?) +\(', output[melhor_veloc_id])
                perda = ProcuraVal('Packet Loss: +(.+?)\r\n', output[melhor_veloc_id])
                resultado = ProcuraVal('Result URL: +(.+?)\r\n', output[melhor_veloc_id])

                resultSpeedTest['info']['download'] = taxa_download + ' [Mbps]'
                resultSpeedTest['info']['upload'] = str(taxa_upload) + ' [Mbps]'
                resultSpeedTest['info']['ping'] = ''
                resultSpeedTest['info']['latency'] = latencia
                resultSpeedTest['info']['server_name'] = server_name
                resultSpeedTest['info']['ip_client'] = ''
                resultSpeedTest['info']['ip_isp'] = ''
                resultSpeedTest['info']['perda'] = perda
                resultSpeedTest['info']['link_result'] = resultado

                resultSpeedTest['Result'] = 'OK'
                resultSpeedTest['Exception'] = 'OK'
            else:
                resultSpeedTest['Result'] = 'NOK'
                print(err[0])
                resultSpeedTest['Exception'] = 'Não foi possível executar Speed Test'

            print(str(resultSpeedTest))

            return resultSpeedTest

        except Exception as error:
            traceback.print_exc()
            resultSpeedTest['Result'] = 'NOK'
            print(error)
            resultSpeedTest['Exception'] = 'Não foi possível executar Speed Test'

            return resultSpeedTest


def ProcuraVal(procurar, texto):
    retorno = re.search(procurar, texto)

    if retorno:
        retorno = retorno.group(1)
        return retorno.strip()

    return False;


# ###Método para verificar lozalização pelo IP da interface WAN
# def geoLocation():
#     ip = '189.101.204.78'
#
#     location = {'info': {
#                         'ip_address': '',
#                         'city': '',
#                         'region': '',
#                         'country': ''
#                     },
#                 'Result': '',
#                 'Exception': ''}
#
#     try:
#         response = DbIpCity.get(ip, api_key='free')
#         location['info']['ip_address'] = response.ip_address
#         location['info']['city'] = response.city
#         location['info']['region'] = response.region
#         location['info']['country'] = response.country
#
#         location['Result'] = 'OK'
#         location['Exception'] = 'OK'
#
#         return location
#
#     except Exception as error:
#         location['Result'] = 'NOK'
#         location['Exception'] = error
#
#         return location


###Método em desenvolvimento para controle de reposta SSH
def get_command_results(channel):
    print('Em teste')
    try:
        interval = 0.1
        maxseconds = 10
        maxcount = maxseconds / interval
        bufsize = 65000
        # input_idx = 0
        # timeout_flag = False
        # start = datetime.datetime.now()
        # start_secs = time.mktime(start.timetuple())
        output = ''
        channel.setblocking(0)
        while True:
            print(channel.recv_ready())
            if channel.recv_ready():
                data = channel.recv(bufsize).decode('utf-8')
                output += data
                print(output)

            if channel.exit_status_ready():
                break

        time.sleep(0.200)
        data = channel.recv(bufsize).decode('utf-8')

        if channel.recv_ready():
            data = channel.recv(bufsize)
            output += data.decode('utf-8')

        return data

    except Exception as error:

        print(error)
        data = 'NOK-GET'
        return data

    # input_idx = 0
    # timeout_flag = False
    # start = datetime.datetime.now()
    # start_secs = time.mktime(start.timetuple())
    # output = ''
    # channel.setblocking(0)
    # while True:
    #     if channel.recv_ready():
    #         data = channel.recv(bufsize).decode('utf-8')
    #         output += data
    #
    #     if channel.exit_status_ready():
    #         break
    #
    #     # Timeout check
    #     now = datetime.datetime.now()
    #     now_secs = time.mktime(now.timetuple())
    #     et_secs = now_secs - start_secs
    #     if et_secs > maxseconds:
    #         timeout_flag = True
    #         break
    #
    #     # rbuffer = output.rstrip(' ')
    #     # if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'):  ## got a Cisco command prompt
    #     #     break
    #
    #     time.sleep(0.200)
    #
    # if channel.recv_ready():
    #     data = channel.recv(bufsize)
    # #     output += data.decode('utf-8')

    return output


###Método para verificar status conexão SSH
def ssh_isalive(channel):
    status_ssh = {
        'status': '',
        'Result': '',
        'Exception': '',
        'Description': ''
    }
    try:
        transport = channel.get_transport()
        if transport.is_active():
            status_ssh['status'] = 'connected'
            status_ssh['Result'] = 'OK'
            status_ssh['Exception'] = 'OK'
            status_ssh['Description'] = 'Connection ssh alive'
        else:
            status_ssh['status'] = 'not_connected'
            status_ssh['Result'] = 'OK'
            status_ssh['Exception'] = 'OK'
            status_ssh['Description'] = 'Connection ssh lost'

    except Exception as error:
        status_ssh['Result'] = 'NOK'
        status_ssh['Exception'] = error
        status_ssh['Description'] = 'Error to verify ssh connection'

    return status_ssh


###Método para estabelecer um canal SSH com o HGU
def connectSSHE(ip, username, password):
    result = {
        'connection': '',
        'status': '',
        'exception': ''
    }

    try:

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=username, password=password, timeout=5, allow_agent=False,
                    look_for_keys=False, banner_timeout=10)
        channel = SSHClientInteraction(ssh, timeout=10, display=False)
        # channel = ssh.invoke_shell()
        result['ssh'] = ssh
        result['connection'] = channel
        result['status'] = 'OK'
        result['exception'] = ''

    except AuthenticationException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE SENHA INSERIDA'}

    except socket.timeout as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE CABO DESCONETADO' }

    except SSHException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': error}

    except BadHostKeyException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE HOST SERVER KEY'}

    except Exception as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': error}

    finally:
        try:
            if result['status'] == 'NOK':
                ssh.close()
                channel.transport.close()
                channel.close()
        except:
            pass

    return result


# def play_video_vlc(endereco,tempo=30, limiar_perda=10):
#     # MRL exemplo: rtp://239.128.2.48:5001
#     mrl = "rtp://@" + str(endereco)
#
#     result = {
#         'media_stats': {},
#         'limiar_lost_pictures': limiar_perda,
#         'mrl': mrl,
#         'status': '',
#         'exception': ''
#     }
#
#     try:
#         instance = vlc.Instance()
#         media = instance.media_new(mrl)
#         media_player = instance.media_player_new()
#
#         media_player.set_media(media)
#         media_player.video_set_scale(0.6)
#         media_player.play()
#
#         mstats = vlc.MediaStats()
#         media.get_stats(mstats)
#         demux_read_bytes = 0
#
#         tempo_buffer = 5
#
#         tini = time.time()
#
#         # tempo do buffer, não contar
#         while ((time.time() - tini) <= (tempo_buffer)):
#             media.get_stats(mstats)
#             demux_read_bytes = mstats.demux_read_bytes
#
#         if (demux_read_bytes > 0):
#             del mstats
#             mstats = vlc.MediaStats()
#
#             while ((time.time() - tini) <= (tempo+tempo_buffer)):
#                 pass
#
#             tfim = time.time()
#
#             media.get_stats(mstats)
#
#             result['media_stats'].update({
#                 'tempo_ini_uts': int(tini),
#                 'tempo_fim_uts': int(tfim),
#                 'tempo_reproducao': int(tfim-tini),
#                 'read_bytes': mstats.read_bytes,
#                 'decoded_video': mstats.decoded_video,
#                 'input_bitrate': mstats.input_bitrate,
#                 'demux_read_bytes': mstats.demux_read_bytes,
#                 'demux_bitrate': mstats.demux_bitrate,
#                 'demux_corrupted': mstats.demux_corrupted,
#                 'demux_discontinuity': mstats.demux_discontinuity,
#                 'lost_pictures': mstats.lost_pictures,
#                 'lost_abuffers': mstats.lost_abuffers
#             })
#
#             if (int(mstats.lost_pictures) > int(limiar_perda)):
#                 result['status'] = "NOK"
#                 result['exception'] = "Perda de quadros acima do limiar de " + str(limiar_perda) +"."
#             elif (mstats.demux_read_bytes == 0):
#                 result['status'] = "NOK"
#                 result['exception'] = "Não há fluxo de multicast/RTP neste canal."
#             else:
#                 result['status'] = "OK"
#                 result['exception'] = "OK"
#         else:
#             result['status'] = "NOK"
#             result['exception'] = "Não há fluxo de multicast/RTP neste canal."
#     except Exception as error:
#         result['connection'] = "NOK"
#         result['status'] = "Erro ao reproduzir vídeo."
#         result['exception'] = str(error)
#
#     try:
#         media_player.stop()
#     except:
#         pass
#
#     return result


def recebe_multicast(grupo, porta, media_tempo_br, tempo_max_mult=5):
    # media_tempo_br --> X - calcular bitrate na média de X segundos
    # tempo_max_mult --> se média calcular bitrate for 2 segundos, e tempo_max_mult=5, tempo total do teste será 10 segundos
    # retorna array --> [ultimo bitrate, min_bitrate, max_bitrate]

    result_multicast = {}

    try:
        tempo_join = -1
        join_ini = -1
        join_fim = -1

        addrinfo = socket.getaddrinfo(grupo, None)[0]
        s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(3)
        s.bind(('', porta))
        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])

        join_ini = time.time()

        if addrinfo[0] == socket.AF_INET:  # IPv4
            mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        else:
            mreq = group_bin + struct.pack('@I', 0)
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        tempo_ini = time.time()
        tempo_rot = time.time()
        tempo_media_s = media_tempo_br
        max_br = 0
        min_br = -1
        bitrate = 0
        recebido = 0
        falhou = False

        while (time.time() - tempo_ini < (tempo_max_mult * tempo_media_s)):
            if ((time.time() - tempo_rot) > tempo_media_s):
                tempo_rot = time.time()

                bitrate = recebido / tempo_media_s * 8

                if (bitrate > max_br):
                    max_br = bitrate

                if (min_br == -1):
                    min_br = bitrate
                elif (bitrate < min_br):
                    min_br = bitrate

                variacao_porc = (max_br - min_br) / min_br * 100
                print(grupo + ":" + str(porta) + " --> bitrate:" + str(bitrate) + " max:" + str(max_br) + " " + " min:" + str(min_br) + " " + str(variacao_porc) + "%")

                recebido = 0
            try:
                data, sender = s.recvfrom(1500)
                if (join_fim == -1):
                    join_fim = time.time()
                    tempo_join = join_fim - join_ini
            except:
                print("grupo:" + grupo + ":" + str(porta) + " indisponível!")
                falhou = True
                break

            recebido = recebido + len(data)

        s.close()

        variacao_porc = (max_br - min_br) / min_br * 100

        result_multicast['bitrate'] = bitrate
        result_multicast['min_br'] = min_br
        result_multicast['max_br'] = max_br
        result_multicast['variacao_porc'] = variacao_porc
        result_multicast['tempo_join'] = tempo_join

        if (falhou == True):
            result_multicast['Result'] = 'NOK'
            result_multicast['Exception'] = 'OK'
            result_multicast['Description'] = 'Grupo de multicast indisponível.'
        else:
            result_multicast['Result'] = 'OK'
            result_multicast['Exception'] = 'OK'
            result_multicast['Description'] = 'OK'
    except Exception as erro:
        result_multicast['Result'] = 'NOK'
        result_multicast['Exception'] = str(erro)
        result_multicast['Description'] = 'Exceção ocorrida durante o teste de multicast.'

    #print (result_multicast)
    return result_multicast


###DNS resolver
def nslookup(server, url):
    resolv = dns.resolver.Resolver()
    resolv.nameservers = [server]

    tini = datetime.now()
    resp = resolv.resolve(url, 'A')
    tend = datetime.now()

    resp = [ns.to_text() for ns in resp][0]
    tempo_resposta = tend - tini

    return [resp,(tempo_resposta.microseconds/1000)]


###Método para estabelecer um canal SSH com o HGU (mesmo que o connectSSH, mas sem invoke_shell())
def connectSSH2(ip, username, password):

    result = {
        'connection': '',
        'status': '',
        'exception': ''
    }

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=username, password=password, timeout=5, allow_agent=False,
                    look_for_keys=False, banner_timeout=10)

        channel = ssh
        result['ssh'] = ssh
        result['connection'] = channel
        result['status'] = 'OK'
        result['exception'] = ''

    except AuthenticationException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE SENHA INSERIDA'}

    except socket.timeout as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE CABO DESCONETADO' }

    except SSHException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': error}

    except BadHostKeyException as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': 'VERIFIQUE HOST SERVER KEY'}

    except Exception as error:
        result = {'connection': 'channel_NOK', 'status': 'NOK', 'exception': error}

    finally:
        try:
            if result['status'] == 'NOK':
                ssh.close()
                channel.transport.close()
                channel.close()
        except:
            pass

    return result


###envia comando e aguarda fim execucao
def get_command_output(channel, cmd, wait_text):
    try:
        if not cmd.endswith("\n"):
            cmd += "\n"
        channel.send(cmd)

        outdata = ""
        errdata = ""

        found = False

        print("Executando:" + cmd.strip())
        while True:
            while channel.recv_ready():
                chunk = channel.recv(1000).decode()
                print(chunk, end="", flush=True)
                outdata += chunk

            while channel.recv_stderr_ready():
                errdata += channel.recv_stderr(1000)

            if ("In wrong state, sampleState" in outdata):
                print("Erro: In wrong state, sampleState - resetando HPNA.")
                channel.send("hpna reset \n")

                time.sleep(5)

                channel.send(cmd)

                outdata = ""
                errdata = ""
                continue

            if (wait_text in outdata):
                break

            if (channel.exit_status_ready()):
                break

            #time.sleep(0.001)
        print("Fim da execucao de: " + cmd.strip())
        return outdata

    except Exception as error:
        print(error)
        results = 'EXCEPTION-CMD_NOT_SENT'

    return results


### Ping parametrizado
def ping2(host, pacotes=4, timeout=0.5):
    # teste de ping ICMP
    status_ping = {
        'taxa_sucesso_porc': '',
        'media_latencia_ms': '',
        'Result': '',
        'Exception': '',
        'Description': ''
    }

    try:
        # 1º ping com 1 pacote para evitar falhas/timeout no próximo devido ao ARP
        verbose_ping(host, count=1)

        sys.stdout = variavel = io.StringIO()
        verbose_ping(host, count=pacotes, timeout=1)
        sys.stdout = sys.__stdout__

        saida = variavel.getvalue().split("\n")

        taxa_sucesso = 0
        media_latencia = ''
        pacotes_respondidos = 0
        soma_latencia = 0

        for linha in saida:
            print(linha)
            linha = linha.split()

            try:
                soma_latencia = soma_latencia + float(linha[3].replace("ms",""))
                pacotes_respondidos += 1
            except:
                pass

        taxa_sucesso = round(pacotes_respondidos / pacotes * 100)

        if (pacotes_respondidos > 0):
            media_latencia = round(soma_latencia/pacotes_respondidos,2)

    except Exception as erro:
        status_ping['media_latencia_ms'] = media_latencia
        status_ping['taxa_sucesso_porc'] = taxa_sucesso
        status_ping['Result'] = 'NOK'
        status_ping['Exception'] = str(erro)
        status_ping['Description'] = 'Erro na execução do ping.'

    if (status_ping['Result'] != "NOK"):
        status_ping['media_latencia_ms'] = media_latencia
        status_ping['taxa_sucesso_porc'] = taxa_sucesso
        status_ping['Result'] = 'OK'
        status_ping['Exception'] = "OK"
        status_ping['Description'] = 'Ping executado sem erros.'

    return status_ping


def ntp_test(servidor, porta = 123):
    result = {
        'hora': '',
        'Result': '',
        'Exception': '',
        'Description': ''
    }
    try:
        c = ntplib.NTPClient()
        response = c.request(servidor, port=porta)

        if (response):
            result['hora'] = ctime(response.tx_time)
            result['Result'] = "OK"
            result['Exception'] = "OK"
            result['Description'] = "OK"

    except Exception as e:
        result['Result'] = "NOK"
        result['Exception'] = str(e)
        result['Description'] = "Erro no teste de NTP"
        return result

    return result


###DNS resolver
def nslookup_mobile(server, url, version):

    dns_ans = {
        "name_servers": [],
        "time_ans": "",
        "result": "",
        "exception": ""
    }

    try:
        res = dns.resolver.Resolver(configure=False)
        res.nameservers = [server]
        tini = datetime.now()
        result = res.query(url, version)
        tend = datetime.now()

        for ns in result:
            dns_ans['name_servers'].append(ns.to_text())

        tempo_resposta = tend - tini
        dns_ans['time_ans'] = tempo_resposta.microseconds/1000

        dns_ans['result'] = 'ok'
        dns_ans['exception'] = 'ok'

    except:

        dns_ans['result'] = 'nok'
        dns_ans['exception'] = 'nok'

    print(dns_ans)
    return dns_ans




