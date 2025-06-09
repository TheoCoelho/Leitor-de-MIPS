# reader.py
import os

def ler_arquivos():
    pasta = r'C:\Users\coelh\Desktop\Trabalho I - Arquitetura de Computadores\teste'
    dados = {}  # dicionário: nome_arquivo → lista de linhas

    for i in range(1, 11):
        nome_arquivo = f'TESTE-{i:02d}.txt'
        caminho = os.path.join(pasta, nome_arquivo)

        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                linhas = f.read().splitlines()  # remove '\n' e salva como lista
                dados[nome_arquivo] = linhas

    return dados
