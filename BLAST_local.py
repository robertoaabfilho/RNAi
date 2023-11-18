# -*- coding: utf-8 -*-

print('\nInstalando todas as bibliotecas relacionadas\n')
import os
from tkinter import filedialog
from tkinter import filedialog as dlg
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import date
import time
import lxml
#from lxml import etree
from Bio.Seq import Seq
from Bio.Seq import MutableSeq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO 
from Bio import AlignIO
import Bio.Align.Applications
from Bio.Align import AlignInfo
from Bio.Align.Applications import MuscleCommandline
from Bio.Blast.Applications import *
from Bio.Blast import NCBIXML

print('\nSelecione o arquivo .fas')
seq = askopenfilename()
print('\n',seq)

print('\nSelecione o banco de referência')
db = askopenfilename()
print('\n',db)

data_atual = date.today()

result = 'blast'+'.'+str(data_atual)+'.xml'

comando = NcbiblastnCommandline(query=seq, subject=db, outfmt=6, out=result, evalue=0.00000000001)
NCBI_cline = str(comando)#transforma a linha de comando em string
os.system(NCBI_cline)#cola a string no terminal e roda

print('BLAST finalizado!')