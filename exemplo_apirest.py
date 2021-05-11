import requests
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta, datetime
import pandas as pd
import xlsxwriter
from getpass import getpass
import re
import pdb

def metodoGet(url, user, senha):
    # Será utilizado somente para a Planilha de Mudanças
    response = requests.request('GET', url, verify=False, auth=HTTPBasicAuth(user, senha))
    conteudoMember = response.json()['member']
    return conteudoMember
  
 # exemplo de funcao para construcao de dataframes
 def dfInc(conteudoMember):
    df = pd.DataFrame(conteudoMember)
    df = pd.concat([df['ticketid'], df['description'], df['relatedrecord.itau_tipomud'], df['relatedrecord.relatedrecwonum'], df['internalpriority']], axis=1)
    df = df.reindex(columns=['ticketid', 'description', 'relatedrecord.itau_tipomud', 'relatedrecord.relatedrecwonum','internalpriority'])
    df.columns = ['ID', 'Título', 'Tipo_de_Mudanca', 'ID_Mudanca', 'Prioridade Interna']
    return df
    
#exemplo para renomear planilha em excel de acordo com a data de execucao do codigo
today = str(date.today())
yesterday = str(date.today() - timedelta(days=1))
t1 = str(date.today() - timedelta(days=3))
t2 = str(date.today() + timedelta(days=3))
now = datetime.now()
time = (now.strftime("%Hh%M"))
nameExcel = 'Incidentes e Mudanças Relacionadas ' + today + ' ' + time + '.xlsx'
writer = pd.ExcelWriter(nameExcel, engine='xlsxwriter')

#url = ... => um endereco web deve ser atribuido pela url que foi analisada no postman previamente
#construcao do dataframe com os dados coletados pelo metodo get
conteudoMember = metodoGet1(url,user,senha)
dfinc1 = pd.DataFrame()
if conteudoMember:
    dfinc1 = dfInc(conteudoMember)
    
dfm = pd.DataFrame()
if conteudoMember:
    dfm = dfMud(conteudoMember)

dfinc1 = dfinc1[dfinc1['ID_Mudanca'].isna() == False]
dfinc2 = dfinc2[dfinc2['ID_Mudanca'].isna() == False]
dfinc3 = dfinc3[dfinc3['ID_Mudanca'].isna() == False]
dfinc4 = dfinc4[dfinc4['ID_Mudanca'].isna() == False]

# Realizando comparação entre as planilhas para filtrar somente as mudanças que possuem relação com os incidentes

mud_incid = pd.Series([])
mud_incid = mud_incid.append(dfinc1['ID_Mudanca'])
mud_incid = mud_incid.append(dfinc2['ID_Mudanca'])
mud_incid = mud_incid.append(dfinc3['ID_Mudanca'])
mud_incid = mud_incid.append(dfinc4['ID_Mudanca'])

# Comparação entre a série mud_incid e a coluna dfm['ID']

dfm = dfm[dfm['ID'].isin(mud_incid) == True]

# Salvando os dados na Planilha

dfinc1.to_excel(writer, sheet_name='Prioridade Crítica')
dfinc2.to_excel(writer, sheet_name='Prioridade Alta')
dfinc3.to_excel(writer, sheet_name='Prioridade Média')
dfinc4.to_excel(writer, sheet_name='Prioridade Baixa')
dfm.to_excel(writer, sheet_name='Mudanças')

writer.save()
    
    

    
    
    
