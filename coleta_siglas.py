def coleta_siglas():
    import os

    dirs_imob = os.listdir("Imobiliarias")

    siglas = []

    for file in dirs_imob:
        if file.find("[P]") != -1: continue
        siglas.append(file.split("__")[0])

    return siglas