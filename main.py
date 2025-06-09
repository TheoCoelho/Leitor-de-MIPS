# main.py
from reader import ler_arquivos
from writer import salvar_arquivo_resultado

registradores = {
    '00000': '$zero', '00001': '$at', '00010': '$v0', '00011': '$v1',
    '00100': '$a0',   '00101': '$a1', '00110': '$a2', '00111': '$a3',
    '01000': '$t0',   '01001': '$t1', '01010': '$t2', '01011': '$t3',
    '01100': '$t4',   '01101': '$t5', '01110': '$t6', '01111': '$t7',
    '10000': '$s0',   '10001': '$s1', '10010': '$s2', '10011': '$s3',
    '10100': '$s4',   '10101': '$s5', '10110': '$s6', '10111': '$s7'
}

            
def tip_opcode(bin_instrucao):
    
    opcode = bin_instrucao[:6]
    if opcode == '000000':
        return 'R'
    elif opcode in ['000010', '000011']:
        return 'J'
    else:
        return 'I'
    
dados = ler_arquivos()

# Mostra os arquivos e conteúdos

            
def bin_to_int(bin_str):
    return int(bin_str, 2)

def get_mnemonico(instrucao):
    instrucao = instrucao.strip().replace(" ", "")
    opcode = instrucao[:6]
    tipo = tip_opcode(instrucao)

    match tipo:
        case 'R':
            funct = instrucao[26:32]
            match funct:
                case '100000': return 'add'
                case '100010': return 'sub'
                case '100100': return 'and'
                case '100101': return 'or'
                case '100110': return 'xor'
                case '000000': return 'sll'
                case '000010': return 'srl'
                case '001000': return 'jr'
                case _: return 'funct R desconhecido'
        case 'I':
            match opcode:
                case '100011': return 'lw'
                case '101011': return 'sw'
                case '001000': return 'addi'
                case '001100': return 'andi'
                case '001101': return 'ori'
                case '001110': return 'xori'
                case '001111': return 'lui'
                case '000100': return 'beq'
                case '000101': return 'bne'
                case '000110': return 'blez'
                case '000111': return 'bgtz'
                case _: return 'opcode I desconhecido'
        case 'J':
            match opcode:
                case '000010': return 'j'
                case '000011': return 'jal'
                case _: return 'opcode J desconhecido'
        case _:
            return 'Tipo desconhecido'

def decodificar_instrucao(instrucao):
    instrucao = instrucao.strip().replace(" ", "")
    tipo = tip_opcode(instrucao)
    opcode = instrucao[:6]

    if tipo == 'R':
        rs = instrucao[6:11]
        rt = instrucao[11:16]
        rd = instrucao[16:21]
        shamt = instrucao[21:26]
        funct = instrucao[26:32]

        nome = get_mnemonico(instrucao)

        match nome:
            case 'add' | 'sub' | 'and' | 'or' | 'xor':
                return f"{nome} {registradores.get(rd)}, {registradores.get(rs)}, {registradores.get(rt)}"
            case 'sll' | 'srl':
                return f"{nome} {registradores.get(rd)}, {registradores.get(rt)}, {int(shamt, 2)}"
            case 'jr':
                return f"{nome} {registradores.get(rs)}"
            case _:
                return nome  # fallback para instrução não reconhecida

    elif tipo == 'I':
        rs = instrucao[6:11]
        rt = instrucao[11:16]
        imm = instrucao[16:32]
        nome = get_mnemonico(instrucao)
        imm_valor = int(imm, 2)

        match nome:
            case 'lw' | 'sw':
                return f"{nome} {registradores.get(rt)}, {imm_valor}({registradores.get(rs)})"
            case 'addi' | 'andi' | 'ori' | 'xori':
                return f"{nome} {registradores.get(rt)}, {registradores.get(rs)}, {imm_valor}"
            case 'lui':
                return f"{nome} {registradores.get(rt)}, {imm_valor}"
            case 'beq' | 'bne':
                return f"{nome} {registradores.get(rs)}, {registradores.get(rt)}, offset:{imm_valor}"
            case 'blez' | 'bgtz':
                return f"{nome} {registradores.get(rs)}, offset:{imm_valor}"
            case _:
                return nome

    elif tipo == 'J':
        nome = get_mnemonico(instrucao)
        addr = instrucao[6:]
        endereco = int(addr, 2) << 2
        return f"{nome} {endereco}"

    return 'Instrução inválida'


for nome_arquivo, linhas in dados.items():
    instrucoes_convertidas = []
    for linha in linhas:
        binario = linha.strip().replace(" ", "")
        if binario:
            instrucao_formatada = decodificar_instrucao(binario)
            instrucoes_convertidas.append(instrucao_formatada)

    salvar_arquivo_resultado(nome_arquivo, instrucoes_convertidas, pasta_saida="teste")
