from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Contacts, Message
from .forms import MessageForm, ContactsForm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from django.conf import settings
import time

def get_browser_from_user_agent(user_agent):
    if 'Chrome' in user_agent and not 'OPR' in user_agent:
        return 'chrome'
    elif 'Firefox' in user_agent:
        return 'firefox'
    elif 'Safari' in user_agent and not 'Chrome' in user_agent:
        return 'safari'
    elif 'Edge' in user_agent:
        return 'edge'
    elif 'OPR' in user_agent or 'Opera' in user_agent:
        return 'opera'
    else:
        return 'unknown'

def get_webdriver(request):
    user_agent = request.META['HTTP_USER_AGENT']
    browser = get_browser_from_user_agent(user_agent)
    
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=/path/to/your/chrome/profile')
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.profile = '/path/to/your/firefox/profile'
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    elif browser == 'safari':
        driver = webdriver.Safari()
    elif browser == 'opera':
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=/path/to/your/chrome/profile')
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError('Unsupported browser')
    
    return driver

def aguardar_elemento_presente(driver, by, valor):
    while len(driver.find_elements(by, valor)) < 1:
        time.sleep(1)

def conectar_whatsapp(driver):
    driver.get("https://web.whatsapp.com/")
    aguardar_elemento_presente(driver, By.ID, 'pane-side')
    print("Conecte seu WhatsApp com o QR code exibido.")
    time.sleep(15)  # Aguarda o tempo para o usuário fazer login e carregar o WhatsApp Web

def enviar_mensagem(driver, telefone, texto):
    driver.get(f"https://web.whatsapp.com/send?phone={telefone}")
    aguardar_elemento_presente(driver, By.ID, 'side')
    time.sleep(3)
    campo_mensagem = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    campo_mensagem.send_keys(texto)
    botao_enviar = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
    botao_enviar.click()
    time.sleep(2)  # Aguarda um pouco para garantir que a mensagem seja enviada

def enviar_mensagem_para_contatos(driver, texto, contatos):
    for contato in contatos:
        telefone = contato.phone
        enviar_mensagem(driver, telefone, texto)
        print(f"Mensagem enviada para {contato.full_name} ({telefone})")

def perfil_mensage(request):
    if request.method == 'POST':
        message_form = MessageForm(request.POST, request.FILES)
        contacts_form = ContactsForm(request.POST)
        if message_form.is_valid() and contacts_form.is_valid():
            message = message_form.save()
            contacts = contacts_form.cleaned_data['contacts']
            selected_neighborhoods = contacts_form.cleaned_data['neighborhoods']
            selected_city = contacts_form.cleaned_data['city']

            if selected_neighborhoods:
                contacts = contacts.filter(neighborhood__icontains=selected_neighborhoods)
            if selected_city:
                contacts = contacts.filter(city__icontains=selected_city)

            request.session['message_id'] = message.id
            request.session['contact_ids'] = [contact.id for contact in contacts]

            return redirect('enviar_whatsapp')
    else:
        message_form = MessageForm()
        contacts_form = ContactsForm()

    return render(request, 'perfil_mensage.html', {'message_form': message_form, 'contacts_form': contacts_form})

def enviar_whatsapp(request):
    message_id = request.session.get('message_id')
    contact_ids = request.session.get('contact_ids')

    if message_id and contact_ids:
        message = Message.objects.get(id=message_id)
        contacts = Contacts.objects.filter(id__in=contact_ids)

        driver = get_webdriver(request)
        conectar_whatsapp(driver)

        # Inicia o processo de envio e retorna uma resposta JSON com o status inicial
        response = {'status': 'starting'}

        def update_status(status):
            nonlocal response
            response['status'] = status
            return JsonResponse(response)

        try:
            enviar_mensagem_para_contatos(driver, message.text, contacts)
            update_status('completed')

        except Exception as e:
            update_status(f'error: {str(e)}')

        finally:
            driver.quit()
            del request.session['message_id']
            del request.session['contact_ids']

        return JsonResponse(response)

    return render(request, 'enviar_whatsapp.html')

