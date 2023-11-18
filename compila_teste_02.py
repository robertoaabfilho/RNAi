import os

def compila():
    Covid_Path = "C:/Users/Lorena/OneDrive/Documentos/R/FASTAS_Teste/"  #Caminho para abrir o diretorio com os arquivos. MUDAR O DIRETORIO DESEJADO
    CovidFiles= os.listdir(Covid_Path)  #os. listdir() vai retornar um lista, puxando todos os arquivos que estão todos esses arquivos do diretório.
    # Ter uma pasta separada com os fastas para a leitura ser correta e eficiente.
    # Declarei a variavel CovidFiles para que o loop leia apenas o nome dos arquivos de verdade.

#não usar nome de variavel como "f". Mudei para "Arquivo".
    with open (Covid_Path +"TODAS_SEQS.fasta", "a") as f: # "Todas_seqs" é o arquivo que será criado para unificar.
        for Arquivo in CovidFiles:
            with open(Covid_Path + Arquivo, 'r') as g: #arquivo sendo aberto no modo leitura ('r') como variável 'g'. with open já fecha o arquivo então nao preciso dar close no arquivo.
                linhas_do_arq = g.readlines() # Covid_Path + Arquivo = diretório mais o arquivo. linhas_do_arq recebem os obj da lista da variavel g.
                for linhas in linhas_do_arq:    #linhas recebe as linhas da variavel linhas_do_arq para serem gravadas no novo arq. unificado.
                    f.write(linhas) #escreve as linhas no arquivo "TODAS_SEQS" em f.


compila()