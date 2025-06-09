import os

def salvar_arquivo_resultado(nome_arquivo_original, instrucoes_convertidas, pasta_saida=None):

    nome_saida = nome_arquivo_original.replace('.txt', '-RESULTADO.txt')
    
    caminho_saida = os.path.join(pasta_saida or '', nome_saida)

    try:
        with open(caminho_saida, 'w') as arquivo:
            for instrucao in instrucoes_convertidas:
                arquivo.write(instrucao + '\n')
        print(f"✔ Arquivo salvo com sucesso: {nome_saida}")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo {nome_saida}: {e}")
