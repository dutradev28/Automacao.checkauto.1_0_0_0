import pyautogui
import time
import telebot
import os
import configparser
from datetime import datetime
import pygetwindow as gw

# Função para criar o arquivo config.ini com valores padrão
def criar_arquivo_config(caminho_arquivo):
    config = configparser.ConfigParser()
    config["Telegram"] = {
        "bot_token": "SEU_BOT_TOKEN",
        "chat_id": "SEU_CHAT_ID"
    }
    config["Capturas"] = {
        "caminho_pasta": "CAMINHO_DA_PASTA_PARA_CAPTURAS",
        "intervalo_captura": "3600",
        "mensagem": "SUA_MENSAGEM_AQUI",
        "capturar_tela_inteira": "True",
        "nome_executavel": "NOME_EXECUTAVEL_A_SER_CAPTURADO"
    }
    with open(caminho_arquivo, "w") as config_file:
        config.write(config_file)

# Função para ler o arquivo de configuração e obter os valores das opções
def ler_arquivo_config(caminho_arquivo):
    config = configparser.ConfigParser()
    if not os.path.exists(caminho_arquivo):
        criar_arquivo_config(caminho_arquivo)

    config.read(caminho_arquivo)

    bot_token = config.get("Telegram", "bot_token")
    chat_id = config.get("Telegram", "chat_id")
    caminho_pasta = config.get("Capturas", "caminho_pasta")
    intervalo_captura = int(config.get("Capturas", "intervalo_captura"))
    utf8_mensagem = config.get("Capturas", "mensagem").encode("utf-8")
    capturar_tela_inteira = config.getboolean("Capturas", "capturar_tela_inteira")
    nome_executavel = config.get("Capturas", "nome_executavel")

    return bot_token, chat_id, caminho_pasta, intervalo_captura, utf8_mensagem, capturar_tela_inteira, nome_executavel

# Função para capturar a janela especificada e enviar a captura pelo bot
def capture_window_and_send(bot, chat_id, caminho_pasta, nome_executavel, utf8_mensagem):
    try:
        while True:  # Executa indefinidamente em primeiro plano
            # Encontra a janela do programa pelo nome do executável
            janelas_programa = gw.getWindowsWithTitle(nome_executavel)
            if not janelas_programa:
                print(f"Janela '{nome_executavel}' não encontrada.")
                # Aguarda 1 minuto antes de tentar novamente
                time.sleep(60)
                continue

            # Seleciona a primeira janela encontrada
            janela_programa = janelas_programa[0]
            janela_programa.activate()
                        
            # Captura a tela da janela
            screenshot = pyautogui.screenshot(region=(janela_programa.left, janela_programa.top, janela_programa.width, janela_programa.height))

            # Salva a captura de tela com um nome único, usando a data e hora atual
            nome_arquivo = "screenshot_{}.png".format(time.strftime("%Y%m%d_%H%M%S"))
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            screenshot.save(caminho_completo)

            # Envia a mensagem de texto com caracteres especiais (UTF-8)
            bot.send_message(chat_id=chat_id, text=utf8_mensagem)

            # Envia a captura de tela para o bot no Telegram
            with open(caminho_completo, "rb") as photo:
                bot.send_photo(chat_id=chat_id, photo=photo)

            # Exibe uma mensagem na tela de que a captura foi realizada com sucesso
            print("Captura realizada com sucesso! Data e hora: {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

            # Intervalo de captura definido no arquivo de configuração (em segundos)
            time.sleep(intervalo_captura)
    except Exception as e:
        # Em caso de erro, exibe uma mensagem de erro na tela
        print("Erro ao capturar e enviar a screenshot:", str(e))

# Função para capturar a tela inteira e enviar a captura pelo bot
def capture_full_screen_and_send(bot, chat_id, caminho_pasta, utf8_mensagem):
    try:
        while True:  # Executa indefinidamente em primeiro plano
            # Aguardar 60 segundos antes de tirar o print
            time.sleep(60)
            
            # Captura a tela inteira
            screenshot = pyautogui.screenshot()

            # Salva a captura de tela com um nome único, usando a data e hora atual
            nome_arquivo = "screenshot_{}.png".format(time.strftime("%Y%m%d_%H%M%S"))
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            screenshot.save(caminho_completo)

            # Envia a mensagem de texto com caracteres especiais (UTF-8)
            bot.send_message(chat_id=chat_id, text=utf8_mensagem)

            # Envia a captura de tela para o bot no Telegram
            with open(caminho_completo, "rb") as photo:
                bot.send_photo(chat_id=chat_id, photo=photo)

            # Exibe uma mensagem na tela de que a captura foi realizada com sucesso
            print("Captura realizada com sucesso! Data e hora: {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

            # Intervalo de captura definido no arquivo de configuração (em segundos)
            time.sleep(intervalo_captura)
    except Exception as e:
        # Em caso de erro, exibe uma mensagem de erro na tela
        print("Erro ao capturar e enviar a screenshot:", str(e))

if __name__ == "__main__":
    # Lê as configurações do arquivo config.ini
    CONFIG_FILE = "config.ini"
    bot_token, chat_id, caminho_pasta, intervalo_captura, utf8_mensagem, capturar_tela_inteira, nome_executavel = ler_arquivo_config(CONFIG_FILE)

    # Inicializa o bot do Telegram
    bot = telebot.TeleBot(bot_token)

    if capturar_tela_inteira:
        capture_full_screen_and_send(bot, chat_id, caminho_pasta, utf8_mensagem)
    else:
        capture_window_and_send(bot, chat_id, caminho_pasta, nome_executavel, utf8_mensagem)
