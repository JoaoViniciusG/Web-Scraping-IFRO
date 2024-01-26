from imports import findVendaAR, findVendaBZ, findVendaCD_IC, findVendaDR, findVendaFB_CF_SR, findVendaGA_PD, findVendaVT, findVendaFT, findVendaME, Parallel, delayed, service, options
from time import time
from notification import notify

time_start = time()

#Execution status: [estate acronym: str, successfully executed: bool, exception: Exception (optional)]
exec_status = []
instances_errors = ["AR()", "VT()", "BZ()", "CD_IC()", "FB_CF_SR()", "FT()", "ME()"]

def AR() -> list: return findVendaAR(service, options)
def GA_PD() -> list: return findVendaGA_PD(service, options)
def VT() -> list: return findVendaVT(service, options)
def BZ() -> list: return findVendaBZ(service, options)
def CD_IC() -> list: return findVendaCD_IC(service, options)
def DR() -> list: return findVendaDR(service, options)
def FB_CF_SR() -> list: return findVendaFB_CF_SR(service, options)
def FT() -> list: return findVendaFT(service, options)
def ME() -> list: return findVendaME(service, options)

def execute_scripts(def_file):
    try:
        print(f"Executing {def_file[:-2]}")
        response = eval(def_file)
        print(f"{def_file[:-2]} completed!")
        instances_errors.remove(def_file)
        exec_status.append([def_file[:-2], True])
        return response
    
    except Exception as exc: 
        print(f"Error in {def_file}\n", exc)
        exec_status.append([def_file[:-2], False])

    

Parallel(n_jobs=1, prefer="threads")(delayed(execute_scripts)(def_file) for def_file in instances_errors)

time_final = time()
print(f"Demorou {time_final - time_start} segundos")

notify(exec_status)