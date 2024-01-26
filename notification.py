from win10toast import ToastNotifier

def notify(status: list) -> None:
    notification_msg = ""
    
    for estate_info in status:
        if estate_info[1]:
            notification_msg += f"{estate_info[0]}: Executado com sucesso!\n"
        else: 
            notification_msg += f"{estate_info[0]}: Erro na execução!\n"

    ToastNotifier().show_toast("Relatório de execução", notification_msg, duration=10)