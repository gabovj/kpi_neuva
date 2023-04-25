Generador de KPI's
Generador de KPI's es una aplicación desarrollada en Python utilizando Streamlit y la API de GPT-3.5-turbo de OpenAI. Esta aplicación ayuda a los usuarios a obtener indicadores clave de rendimiento (KPI) personalizados para diferentes puestos de trabajo en una empresa.

Además, la aplicación interactúa con la API de ActiveCampaign para gestionar contactos. Busca si el correo electrónico del usuario ya existe en la base de datos de ActiveCampaign y, si no existe, crea un nuevo contacto con la información proporcionada. Luego, agrega el contacto a una lista específica en ActiveCampaign.

Características
Recopila información del usuario sobre la empresa, el puesto de trabajo y otros detalles relevantes.
Genera el propósito del puesto de trabajo y una lista de 5 KPI principales utilizando la API de GPT-3.5-turbo de OpenAI.
Interactúa con la API de ActiveCampaign para buscar, agregar o actualizar contactos.
Implementa una restricción de velocidad para limitar las solicitudes de la API de OpenAI a 5 solicitudes en 10 minutos por dirección IP.
Requisitos
Python 3.6 o superior
Streamlit
OpenAI
Requests
python-dotenv
Instalación
Clona este repositorio:
bash
Copy code
git clone https://github.com/your-username/generador-kpis.git
Cambia al directorio del proyecto:
bash
Copy code
cd generador-kpis
Instala las dependencias:
bash
Copy code
pip install -r requirements.txt
Crea un archivo .env en el directorio del proyecto y agrega tus claves de API para OpenAI y ActiveCampaign:
makefile
Copy code
OPENAI_API_KEY=tu_clave_api_openai
ACTIVE_CAMPAIGN_API=tu_clave_api_active_campaign
Uso
Para ejecutar la aplicación, utiliza el siguiente comando en el directorio del proyecto:

bash
Copy code
streamlit run app.py
Abre la dirección proporcionada en tu navegador para acceder a la aplicación.

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más información.
