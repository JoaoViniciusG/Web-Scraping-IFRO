def findCep(cep: str) -> list[bool, str]:
    import requests
    import json

    res = requests.get(f"https://viacep.com.br/ws/{cep}/json/")

    try: 
        if res.status_code != 200 or res.json()["erro"] == True: return [False, ""]
    except: pass

    return [True, res.json()["bairro"]]