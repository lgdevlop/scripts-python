from ffmpy import FFmpeg
import os
import sys
import time

#===================================================================================
# Script para conversão de vídeo aulas em mp4 para x265 usando 
# ffmpeg compilado para suportar o referido codec
# Chegando a economizar até 80% de espaço em comparação aos arquivos mp4
# Encoda os arquivos da pastar raíz e de seus subdiretórios
# Necessita a instalação do Wrapper ffmpy
# pip install ffmpy
#===================================================================================

def encoda_arquivos(caminho_completo_arquivo_a_encodar, caminho_completo_arquivo_encodado, arquivos):
    comando = '-y -c:v libx265 -preset veryfast -crf 28 -c:a libopus -b:a 48k -vbr on -compression_level 10 -frame_duration 60 -application audio -metadata title="' + arquivos[0:arquivos.rfind('.')] + '"'
    ff = FFmpeg(
        inputs={caminho_completo_arquivo_a_encodar: None},
        outputs={caminho_completo_arquivo_encodado: comando}
    )
    print ""
    print "========================"
    print "ENCODAR ARQUIVO"
    print ""
    print ff.cmd
    print ""
    print "========================"
    ff.run()

def encontra_arquivos_para_encodar(arquivos, diretorio):
    contador = 0
    if(len(arquivos) == 1):
        print "Arquivo: ", arquivos[0]
        if(arquivos[0].rfind('.mp4') != -1):
            caminho_completo_arquivo_a_encodar = diretorio + "\\" + arquivos[0]
            caminho_completo_arquivo_encodado = diretorio + "\\" + arquivos[0][0:arquivos[0].rfind('.')] + ".mkv"
            encoda_arquivos(caminho_completo_arquivo_a_encodar, caminho_completo_arquivo_encodado, arquivos[0])
        return
    else:
        y = 0
        z = 0
        while(y < len(arquivos)):
            fim = arquivos[y].rfind('.')
            arquivo_sem_extensao_atual = arquivos[y][0:fim]
            while(z < len(arquivos)):
                fim = arquivos[z].rfind('.')
                arquivo_sem_extensao_novo = arquivos[z][0:fim]
                if (arquivo_sem_extensao_atual == arquivo_sem_extensao_novo):
                    contador = contador + 1
                z = z + 1
            if (contador == 1):
                if(arquivos[y].rfind('.mp4') != -1):
                    caminho_completo_arquivo_a_encodar = diretorio + "\\" + arquivos[y]
                    caminho_completo_arquivo_encodado = diretorio + "\\" + arquivo_sem_extensao_atual + ".mkv"
                    encoda_arquivos(caminho_completo_arquivo_a_encodar, caminho_completo_arquivo_encodado, arquivos[y])
            contador = 0
            y = y + 1
            z = 0

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

def listaArquivos(diretorio):
    arquivos = []
    y = 0
    for conteudo in os.listdir(diretorio):
        temp = os.path.join(diretorio, conteudo)
        if os.path.isfile(temp):
            arquivos.append(conteudo)
    while(y < len(arquivos)):
        y = y + 1
    encontra_arquivos_para_encodar(arquivos, diretorio)

def geraLista(pasta_raiz):
    listaArquivos(pasta_raiz)
    listaSubDiretorio(pasta_raiz)

def checa_argumentos():
    if((len(sys.argv) > 2) or (len(sys.argv) < 2)):
        print "Erro! Parametros incorretos!"
        print "Favor checar os parametros passados"
        print "Modo de uso: python ConverteMp4ParaX265.py caminho_da_pasta_raiz_onde_estao_os_arquivos_a_serem_encodados"
    else:
        geraLista(sys.argv[1])

checa_argumentos()
