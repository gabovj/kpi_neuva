
# KPI Generator

KPI Generator is a Python application developed using Streamlit and OpenAI's GPT-3.5-turbo API. This application assists users in obtaining personalized Key Performance Indicators (KPIs) for various job positions within a company.

In addition, the application interacts with the ActiveCampaign API to manage contacts. It searches for the user's email in the ActiveCampaign database and, if not found, creates a new contact with the provided information. The contact is then added to a specific list in ActiveCampaign.

## Features

 - Collects user information about the company, job position, and other relevant details.
 - Generates the job position's purpose and a list of 5 main KPIs using OpenAI's GPT-3.5-turbo API.
 - Interacts with ActiveCampaign API to search, add, or update contacts.
 - Implements rate limiting to restrict OpenAI API requests to 5 requests per 10 minutes per IP address.
## Requirements

- Python 3.6 or higher
- Streamlit
- OpenAI
- Requests
- python-dotenv


## Installation

Clone this repository:

```bash
  git clone https://github.com/your-username/kpi-generator.git
```
Change to the project directory:

```bash
  cd kpi-generator
```
Install the dependencies:
```bash
  pip install -r requirements.txt
```
Create a .env file in the project directory and add your API keys for OpenAI and ActiveCampaign:
```bash
  OPENAI_API_KEY=your_openai_api_key
  ACTIVE_CAMPAIGN_API=your_active_campaign_api_key

```
    