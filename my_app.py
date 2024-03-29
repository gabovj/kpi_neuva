import streamlit as st
import openai
import time
from datetime import datetime, timedelta
from session_state import SessionState
import requests
import os


# Access the API key
openai_api_key = st.secrets['OPENAI_API_KEY']
ac_api_key = st.secrets['ACTIVE_CAMPAIGN_API']


# Title of the app
st.title("Generador de KPI's")
# Company name input field
company_name = st.text_input("¿Cúal es el nombre de tu empresa?")
# Email input field
email = st.text_input("Ingresa tu email:")
# Name input field
name = st.text_input("Ingresa tu nombre:")
# Last Name input field
last_name = st.text_input("Ingresa tu apellido:")
# Position input field
position = st.text_input("¿Cúal es el nombre de tu posción de trabajo?")
# Company sector input field
company_sector = st.text_input("¿A que se dedica tu empresa?")
# management team size input field
company_size = st.selectbox("¿Cúal es el tamaño de tu equipo administrativo?",
                            ("1-5 personas", "6-15 personas", "21-70 personas", "71-250 personas", ">250 personas"))
# annual income input field
anual_income = st.selectbox("¿Cuantos años tiene operando tu empresa?",
                            ("1-3 años", "4-7 años", "8-10 años", ">10 años"))
# company years input field
company_age = st.selectbox("¿Cúal es ingreso anual de tu empresa?",
                           ("<1 MDD", "1-2 MDD", "2-5 MDD", "6-10 MDD", ">10 MDD"))
# Button
button = st.button("Generar KPIs")
# Set up your API key
openai.api_key = openai_api_key


def search_contact_in_active_campaign(email):
    """
    Busca si existe ya el correo electronico en AC
    """
    API_URL = f'https://neuva.api-us1.com/api/3/contacts?email={email}'
    headers = {
        "Api-Token": ac_api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(API_URL, headers=headers)
    return response.json()


def add_contact_to_active_campaign(name, last_name, email, size, years, income):
    """
    Agrega un nuevo contacto en AC
    """
    API_URL = 'https://neuva.api-us1.com/api/3/contact/sync'
    data = {
        "contact": {
            "email": email,
            "firstName": name,
            "lastName": last_name,
            "fieldValues": [
                {
                    "field": "9",
                    "value": size
                },
                {
                    "field": "10",
                    "value": years
                },
                {
                    "field": "11",
                    "value": income
                },
            ]
        }
    }
    headers = {
        "Api-Token": ac_api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, json=data, headers=headers)
    return response.status_code


def update_contactlist(contact_id):
    """
    Agrega un contacto a la lista NEUVA de AC
    """
    url = "https://neuva.api-us1.com/api/3/contactLists"
    payload = {"contactList": {
        "sourceid": 0,
        "list": 2,
        "contact": contact_id,
        "status": 1
    }}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Api-Token": ac_api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code


# Create a dictionary to store IP addresses with call count and timestamps
ip_counts = {}


def get_client_ip():
    response = requests.get("https://api.ipify.org?format=json")
    return response.json()["ip"]


# Get client IP address
if "ip_address" not in st.session_state:
    st.session_state.ip_address = get_client_ip()

ip_address = st.session_state.ip_address


def is_ip_allowed(ip):
    if ip not in ip_counts:
        ip_counts[ip] = {"count": 0, "timestamps": []}

    # Remove timestamps older than 10 minutes
    ip_counts[ip]["timestamps"] = [
        ts for ts in ip_counts[ip]["timestamps"] if ts >= datetime.now() - timedelta(minutes=10)
    ]

    # Check if the IP address has made 5 or more API calls within the last 10 minutes
    if len(ip_counts[ip]["timestamps"]) >= 5:
        return False

    return True


if not position or not company_name or not company_sector or not name or not email or not last_name:
    st.warning(
        "Por favor, completa todos los campos requeridos antes de generar KPIs.")
else:
    if button:
        if is_ip_allowed(ip_address):
            # Add timestamp to the IP address
            ip_counts[ip_address]["timestamps"].append(datetime.now())
            # Check if the contact already exists in ActiveCampaign
            search_result = search_contact_in_active_campaign(email)
            if search_result["contacts"]:
                result = 'already in db'
            else:
                # Add contact to ActiveCampaign
                list_id_neuva = 2
                active_campaign_response = add_contact_to_active_campaign(
                    name, last_name, email, company_size, company_age, anual_income)
                # get contact ID
                search_for_contact_id = search_contact_in_active_campaign(
                    email)
                contact_id = search_for_contact_id["contacts"][0]['id']
                active_campaign_update_contact = update_contactlist(contact_id)
                st.write(contact_id)
            with st.spinner(f'{name}, estamos generando tus KPIs...'):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un asesor de negocios."},
                        {"role": "user", "content": f"Describe en maximo 20 palabras el propósito de un {position} de una empresa que se dedica a {company_sector}"}
                    ]
                )

                response1_text = response['choices'][0]['message']['content']

                st.header('Propósito')

                # Display the purpose
                st.write(response1_text)

                response2 = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un asesor de negocios."},
                        {"role": "user", "content": f"Soy {name} y trabajo en {company_name} es una empresa que se dedica a {company_sector} y es de tamaño {company_size}, mi puesto de trabajo es {position}, redacta en forma de lista 5 Kpi's que mi puesto de trabajo debe tener"}
                    ]
                )

                response2_text = response2['choices'][0]['message']['content']
                metric_list = response2_text.split(
                    '\n\n')  # split by double line break

                st.header("Kpi's principales")

                # Display the KPIs
                for linea in metric_list:
                    if linea.startswith(('1.', '2.', '3.', '4.', '5.')):
                        st.write(linea)

                st.success('Listo!')
        else:
            st.error(
                "Has alcanzado el límite de 5 solicitudes en 10 minutos. Por favor, inténtalo de nuevo más tarde.")
