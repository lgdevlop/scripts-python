#coding: utf-8

#===================================================================================
# Script para monitoramento de quedas de conexão ADSL
# Monitora o modem ADSL2+ TP-LINK TD-8816 via Telnet
# O referido modem tem alguns comportamentos anormais quando o ADSL cai
# Logo não estranhe algumas checagem que parecem redundantes entre outros
#===================================================================================

import sys
import telnetlib
import time
import socket

host = "192.168.0.253"
password = "seu_password_aqui"
uptime = ""
uptime_antigo = []
uptime_atual = []
tempo_maximo_conectado = []
quantidade_quedas_adsl = 0
quantidade_voltou_ar_adsl = 0

def conecta_no_servidor():
    tn = telnetlib.Telnet(host)
    return tn

def autentica_no_servidor(tn):
    resposta = tn.read_until("Password: ")
    tn.write(password + "\n")

def obtem_resposta_do_servidor(tn):
    resposta = "Erro"
    try:
        resposta = tn.read_until("TP-LINK> ", 5)
    except EOFError:
        print "Aconteceu algum erro!"
    except socket.error:
        print "Erro na obtenção da resposta. Provavelmente o servidor fechou a conexão!"
        return "Erro"
    return resposta

def envia_comando_para_servidor(tn):
    # QUANDO A NET CAI, ELE FICA BOMBARDEANDO O MODEM COM ESTE COMANDO
    try:
        tn.write("show wan adsl uptime\n")
    except socket.error:
        print "Provavelmente o servidor fechou a conexão!"


def transforma_em_tempo(tempo_modem):
    horas = tempo_modem[tempo_modem.find(':')-2:tempo_modem.find(':')]
    minutos = tempo_modem[tempo_modem.find(':')+1:tempo_modem.find(':')+3]
    segundos = tempo_modem[tempo_modem.find(':')+4:tempo_modem.find(':')+6]
    print "Horas: ", horas
    print "Minutos: ", minutos
    print "Segundos: ", segundos
    tempo = [horas, minutos, segundos]
    return tempo

def modem_caiu():
    global quantidade_quedas_adsl
    global quantidade_voltou_ar_adsl
    global tempo_maximo_conectado
    global uptime

    if(quantidade_voltou_ar_adsl == 0) or (uptime_antigo[0] > uptime_atual[0]) or (uptime_antigo[0] == uptime_atual[0]) and (uptime_antigo[1] > uptime_atual[1]):
        quantidade_quedas_adsl = quantidade_quedas_adsl + 1
        quantidade_voltou_ar_adsl = 1

    calcula_uptime(uptime)
    print ""
    print "Caiu internet do Modem ADSL!"
    print "Tempo maximo conectado: ", tempo_maximo_conectado
    print "Tempo maximo conectado: %s:%s:%s" % (tempo_maximo_conectado[0], tempo_maximo_conectado[1], tempo_maximo_conectado[2])
    print "Tempo máximo funcionando com defasagem de dez segundos: %s:%s:%s" % (uptime_antigo[0], uptime_antigo[1], uptime_antigo[2])
    print "Tempo atual reportado pelo modem: %s:%s:%s" % (uptime_atual[0], uptime_atual[1], uptime_atual[2])
    print "Total de quedas ADSL até o momento: %d" % quantidade_quedas_adsl

def calcula_uptime(tempo_modem):
    global uptime_antigo
    global uptime_atual
    global tempo_maximo_conectado

    if not uptime_antigo:
        uptime_antigo = transforma_em_tempo(tempo_modem)
    else:
        uptime_antigo = uptime_atual
    uptime_atual = transforma_em_tempo(tempo_modem)
    if not tempo_maximo_conectado:
        tempo_maximo_conectado = uptime_atual
    elif(uptime_atual[0] > tempo_maximo_conectado[0]) or (uptime_atual[0] == tempo_maximo_conectado[0]) and (uptime_atual[1] > tempo_maximo_conectado[1]):
        tempo_maximo_conectado = uptime_atual

    print ""
    print "======================================================"
    print "UPTIME"
    print "quantidade_voltou_ar_adsl: ", quantidade_voltou_ar_adsl
    print "Tempo maximo conectado: ", tempo_maximo_conectado
    print "uptime_antigo: ", uptime_antigo
    print "uptime_atual: ", uptime_atual
    print "quantidade_quedas_adsl: ", quantidade_quedas_adsl
    print "======================================================"
    print ""

def inicio():
    global quantidade_voltou_ar_adsl
    tn = conecta_no_servidor()
    autentica_no_servidor(tn)
    n = 1
    while(n != 0):
        resposta = obtem_resposta_do_servidor(tn)
        if(resposta.find('ADSL') > 0):
            uptime = resposta[resposta.find(':')-2:resposta.rfind('\r\n')]
            print ""
            print "======================================================"
            print "Uptime: ", uptime
            calcula_uptime(uptime)
            print "======================================================"
            time.sleep(10)
            if(quantidade_voltou_ar_adsl == 1):
                quantidade_voltou_ar_adsl = 0
        elif(resposta == "Erro"):
            tn = conecta_no_servidor()
            autentica_no_servidor(tn)
        elif(resposta.find('adsl modem not up') > 0):
            print ""
            print "======================================================"
            print "ADSL MODEM NOT UP"
            print "quantidade_voltou_ar_adsl: ", quantidade_voltou_ar_adsl
            print "Tempo maximo conectado: ", tempo_maximo_conectado
            print "uptime_antigo: ", uptime_antigo
            print "uptime_atual: ", uptime_atual
            print "quantidade_quedas_adsl: ", quantidade_quedas_adsl
            print "======================================================"
            print ""

            print ""
            print "======================================================"
            print "CAIU MESMO"
            print "quantidade_voltou_ar_adsl: ", quantidade_voltou_ar_adsl
            print "Tempo maximo conectado: ", tempo_maximo_conectado
            print "Tempo máximo funcionando com defasagem de dez segundos: %s:%s:%s" % (uptime_antigo[0], uptime_antigo[1], uptime_antigo[2])
            print "Tempo atual reportado pelo modem: %s:%s:%s" % (uptime_atual[0], uptime_atual[1], uptime_atual[2])
            print "Total de quedas ADSL até o momento: %d" % quantidade_quedas_adsl
            print "======================================================"
            modem_caiu()
            if(quantidade_voltou_ar_adsl == 1):
                quantidade_voltou_ar_adsl = 0
            time.sleep(10)
        envia_comando_para_servidor(tn)

inicio()
