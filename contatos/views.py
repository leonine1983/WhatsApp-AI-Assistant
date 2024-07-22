from django.shortcuts import render
from selenium import webdriver
from .models import Contacts

def send_msg(contato, msg):
    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com')

    # Aguardar o usuário  scanear o codigo
    input("Pressione Enter após scanear o código QR")
    search_box = driver.find_element()

    pass

# Create your views here.
"""
# enviar_mensagens.py
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import django
import os

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from contatos.models import Contato

def enviar_mensagem(contato, mensagem):
    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com')

    # Espere o usuário escanear o código QR
    input("Pressione Enter após escanear o código QR")

    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(contato.telefone)
    search_box.send_keys(Keys.ENTER)
    sleep(2)

    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')
    message_box.click()
    message_box.send_keys(mensagem)
    message_box.send_keys(Keys.ENTER)
    
    sleep(2)
    driver.quit()

if __name__ == '__main__':
    mensagem = "Olá, esta é uma mensagem de teste."
    contatos = Contato.objects.all()
    for contato in contatos:
        enviar_mensagem(contato, mensagem)


"""