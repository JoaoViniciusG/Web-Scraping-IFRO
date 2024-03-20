def coleta_siglas():
    import os

    dirs_imob = os.listdir("Imobiliarias")

    siglas = []

    for file in dirs_imob:
        siglas.append(file.split("__")[0])

    return siglas