from imports import findVendaAR, findVendaBZ, findVendaCD_IC, findVendaDR, findVendaFB_CF_SR_CR, findVendaGA_PD, findVendaVT,\
findVendaFT, findVendaME_CC, findVendaBC, findVendaCH, findVendaDC, findVendaEM, findVendaRM, findVendaPC, service, options
from coleta_siglas import coleta_siglas
import pandas as pd

#Execution status: [estate acronym: str, successfully executed: bool, exception: Exception (optional)]
exec_status = []
#instances = coleta_siglas()
instances = ["GA_PD"]

columns = ["Url", "Área Total", "Área Construída", "Dormitórios", "Suítes", "Banheiros", "Garagem", "Bairro", "Valor", "Tipo do Imóvel", "Tipo de Negócio", "Descrição"]

for def_file in instances:
    #Executar o arquivo:
    print(f"Executando {def_file}")

    try:
        response = eval(f"findVenda{def_file}(service, options)")
    except Exception as exc: 
        print(f"Erro em {def_file}\n", exc)
        exec_status.append([def_file, False])
        continue

    #Finalização:
    print(f"{def_file} completo!") 
    exec_status.append([def_file, True])
    
    #Tratamento:
    list_res = []

    for f in range(len(response[0])):
        list_res.append([n[f] for n in response])

    #Salvar:
    table_info = pd.DataFrame(list_res)

    table_info.columns = columns
    table_info.to_excel(f"Planilhas/list_{def_file}.xlsx", index=False)