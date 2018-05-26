import os
import sys
import subprocess
import shlex
import codecs
import io

#===================================================================================
# Script para criação de lista de reprodução no formato m3u8
# de arquivos mp4, incluindo arquivos de subdiretorios da pasta raiz
# informada como parametro de execucao deste script
#===================================================================================

def criaM3u8(arquivos, diretorio):
    y = 0
    while(y < len(arquivos)):
        if(arquivos[y].rfind('.mp4') != -1):
            tempoVideo = obtemTempoVideo(diretorio + "\\" + arquivos[y])
            linha = "#EXTINF:" + tempoVideo + "," + arquivos[y] + "\n"
            linha = linha.decode('cp1252')
            f.write(linha)
            linha = diretorio + "\\" + arquivos[y] + "\n"
            linha = linha.decode('cp1252')
            f.write(linha)
        y = y + 1

# Obtem lista de subdiretorios
def listaSubDiretorio(diretorio):
    diretorios = []
    y = 0
    for conteudo in os.listdir(diretorio):
        temp = os.path.join(diretorio, conteudo)
        if os.path.isdir(temp):
            diretorios.append(temp)
    while(y < len(diretorios)):
        listaArquivos(diretorios[y])
        listaSubDiretorio(diretorios[y])
        y = y + 1

# Obtem a lista de arquivos
def listaArquivos(diretorio):
    arquivos = []
    y = 0
    print ""
    print "================================================="
    print diretorio
    for conteudo in os.listdir(diretorio):
        temp = os.path.join(diretorio, conteudo)
        if os.path.isfile(temp):
            arquivos.append(conteudo)
    while(y < len(arquivos)):
        print "\t", arquivos[y]
        y = y + 1
    print "================================================="
    criaM3u8(arquivos, diretorio)


def obtemTempoVideo(arquivo):
    cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 '
    args = shlex.split(cmd)
    args.append(arquivo)
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    fim = ffprobe_output.rfind('.')
    outpput = ffprobe_output[0:fim]
    return outpput.encode('utf-8')

def checa_argumentos():
    if((len(sys.argv) > 2) or (len(sys.argv) < 2)):
        print "Erro! Parametros incorretos!"
        print "Favor checar os parametros passados"
        print "Modo de uso: python CriaPlaylistM3u8.py caminho_da_pasta_raiz_onde_estao_os_arquivos_a_serem_listados"
    else:
        listaArquivos(sys.argv[1])
        listaSubDiretorio(sys.argv[1])

f = io.open(sys.argv[1] + "\\ReproduzTodoCurso.m3u8",'w',encoding='utf8')

f.write(u'#EXTM3U\n')
checa_argumentos()
f.close()
