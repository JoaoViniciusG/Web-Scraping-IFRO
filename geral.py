from imports import findVendaAR, findVendaBZ, findVendaCD_IC, findVendaDR, findVendaFB_CF_SR_CR, findVendaGA_PD, findVendaVT,\
findVendaFT, findVendaME_CC, findVendaBC, findVendaAP, findVendaCH, findVendaJL, findVendaDC, findVendaEM, findVendaRM,\
findVendaJP, findVendaPC, findVendaWE, Parallel, delayed, service, options
from time import time
from notification import notify
from coleta_siglas import coleta_siglas

time_start = time()

#Execution status: [estate acronym: str, successfully executed: bool, exception: Exception (optional)]
exec_status = []
instances = coleta_siglas()

for def_file in instances:
    try:
        print(f"Executing {def_file}")
        response = eval(f"findVenda{def_file}(service, options)")
        print(f"{def_file} completed!") 
        exec_status.append([def_file, True])
        print(response)
    
    except Exception as exc: 
        print(f"Error in {def_file}\n", exc)
        exec_status.append([def_file, False])

time_final = time()
print(f"Demorou {time_final - time_start} segundos")

notify(exec_status)