# Fake News Chatbot Assistant
## Overview
**Cek Fakta AI** is a specialized, intelligent chatbot and analytics platform designed to detect and combat hoax news and misinformation. Built with Django, this application leverages a Retrieval-Augmented Generation (RAG) architecture powered by localized Large Language Models (LLMs) via Ollama and a vector database (FAISS).

The platform solves the growing problem of digital misinformation by cross-referencing user queries against a curated knowledge base of fact-checked news. It is designed for journalists, researchers, and everyday users who need rapid, reliable validation of news claims. Key benefits include real-time fact-checking, comprehensive query analytics, automated topic categorization, and a privacy-centric approach utilizing local LLMs.

## Features

* **AI-Powered Fact Checking:** Utilizes a RAG pipeline (LangChain, FAISS, LLaMA 3.2) to fetch relevant factual context and generate accurate responses to news claims.
* **Automated Topic Classification:** Every user query is automatically categorized into specific domains (e.g., politics, health, economy, sports) using a zero-shot classification prompt with LLaMA 3.2.
* **Real-Time Analytics Dashboard:** An interactive dashboard (built with Chart.js) visualizing key performance indicators, 30-day query trends, hourly activity heatmaps, label distributions, and top keyword frequency.
* **Cloud-Synchronized Vector Store:** Automatically pulls pre-computed FAISS indexes (`index.faiss`, `index.pkl`) from an AWS S3 bucket on initialization.
* **Query Management Interface:** A dedicated admin-style view (`/show`) to track, monitor, and delete user queries and AI responses.
* **Modern UI/UX:** Responsive, Bootstrap 5-powered frontend featuring an elegant chat interface, typing indicators, and a persistent Dark/Light mode toggle.

## Tech Stack

* **Backend Framework:** Django 5.2, Python 3.x
* **AI & Machine Learning:** LangChain, Ollama (`llama3`, `llama3.2:3b`)
* **Vector Database:** FAISS (`faiss-cpu`)
* **Relational Database:** PostgreSQL (Hosted on Supabase)
* **Cloud Infrastructure:** Amazon Web Services (AWS S3 via `boto3`)
* **Frontend:** HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, Chart.js
* **Package Management:** `pip` (`requirement.txt`)

## Architecture Overview

The system follows a synchronous, monolithic Django architecture combined with external AI and cloud services.

```mermaid
graph TD;
    A[Client Browser] -->|HTTP POST / AJAX| B(Django Views)
    B -->|Save Query| C[(Supabase PostgreSQL)]
    B --> D(Classifier Service)
    D -->|Prompt| E[Ollama: LLaMA 3.2 3B]
    B --> F(RAG Service)
    F -->|Download Index| G[AWS S3: fake-news-uas]
    F -->|Embed Query| H[Ollama: LLaMA 3]
    F -->|Similarity Search| I[(Local FAISS Index)]
    F -->|Generate Answer| E
    B -->|JSON Response| A

```

## Repository Structure

```text
fake-news-chatbot/
├── .envcopy                    # Environment variables template
├── .gitignore                  # Git ignore rules
├── manage.py                   # Django management script
├── requirement.txt             # Python dependencies
├── project/                    # Main Django project configuration
│   ├── asgi.py
│   ├── settings.py             # Database, middleware, app settings
│   ├── urls.py                 # Core routing
│   └── wsgi.py
└── app/                        # Main application module
    ├── admin.py
    ├── apps.py
    ├── forms.py                # Django forms (UserQueryForm)
    ├── models.py               # Database schema (UserQuery)
    ├── tests.py
    ├── services/               # Core business logic & AI integration
    │   ├── analytics_service.py # Dashboard data aggregation
    │   ├── classifier.py       # Topic classification logic
    │   └── rag_service.py      # Vector search and answer generation
    ├── views/                  # HTTP request handlers
    │   ├── chatbot.py          # Chat & record management views
    │   └── dashboard.py        # Dashboard analytics view
    ├── static/                 # Static assets
    │   ├── css/                # Custom stylesheets (style.css, show.css)
    │   └── js/                 # Client-side scripts (script.js)
    └── templates/              # HTML templates
        ├── dashboard.html
        ├── index.html
        └── show.html

```

## Installation Instructions

### Prerequisites

1. **Python 3.x:** Ensure Python is installed.
2. **System Architecture:** Ensure your `x86_64` machine is updated, as `faiss-cpu` relies on specific C++ instruction sets native to this architecture.
3. **Ollama:** Install Ollama locally or on your host server. Pull the required models:
```bash
ollama run llama3.2:3b

```


4. **AWS CLI:** Configure your environment with AWS credentials that have read access to the S3 bucket (`fake-news-uas`).

### Setup Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd fake-news-chatbot

```


2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirement.txt

```


4. **Configure Environment Variables:**
Copy the `.envcopy` file to `.env` and populate the fields (see Configuration section).
5. **Run Database Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate

```


6. **Start the Development Server:**
```bash
python manage.py runserver

```


7. **Access the Application:** Open `http://localhost:8000` in your browser.

## Configuration

The application requires specific environment variables to connect to its remote database and establish security.

| Variable | Description | Required | Example |
| --- | --- | --- | --- |
| `SECRET_KEY` | The Django secret key used for cryptographic signing. | Yes | `django-insecure-xyz...` |
| `SUPABASE_PASSWORD` | Password for the Supabase PostgreSQL database (`postgres.krhlvjzmitfkgwckxahx`). | Yes | `super_secure_password` |
| `AWS_ACCESS_KEY_ID` | Implicitly required by `boto3` to fetch FAISS index. | Yes* | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Implicitly required by `boto3` to fetch FAISS index. | Yes* | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |

*(AWS credentials should be configured via `~/.aws/credentials` or standard system environment variables).*

## API Documentation

While primarily a Server-Side Rendered (SSR) application, the chatbot relies on a JSON-based endpoint for asynchronous message handling.

### `POST /`

Handles incoming user queries from the chatbot interface.

* **Content-Type:** `multipart/form-data`
* **Authentication:** Valid Django CSRF Token required (`X-CSRFToken` header).
* **Request Body:**
* `question` (string): The text of the user's news claim.


* **Success Response (200 OK):**
```json
{
    "success": true,
    "answer": "Berdasarkan konteks yang ditemukan, klaim tersebut adalah..."
}

```


* **Error Response (200 OK - Graceful Failure):**
```json
{
    "success": false,
    "error": "Error details here..."
}

```



## Database Design

The application uses PostgreSQL, utilizing Django's ORM.

### `UserQuery` Table (`app/models.py`)

Stores all interactions between the user and the system.

| Column | Type | Description |
| --- | --- | --- |
| `id` | `UUIDField` | Primary Key, auto-generated UUIDv4. |
| `question` | `TextField` | The initial news claim/query submitted. |
| `answer` | `TextField` | The generated response from the RAG pipeline. |
| `timestamp` | `DateTimeField` | Auto-populated on creation. |
| `retrieved_docs` | `JSONField` | Stores the chunked text and metadata retrieved from FAISS. |
| `label` | `CharField(50)` | The domain classification output (e.g., 'politics'). |

## Usage Examples

**Chatting with the Bot:**

1. Navigate to `/`.
2. Type a claim in the input field, e.g., *"Apakah benar ada gempa bumi hari ini?"*
3. The bot will display a typing indicator, route the request through the RAG pipeline, and return a validated answer based on the downloaded FAISS index.

**Viewing Analytics:**
Navigate to `/dashboard/`. The charts will automatically render:

* Total news processing metrics.
* A 30-day query trend line graph.
* Keyword horizontal bar chart (Indonesian and English stopwords are automatically filtered out).

**Managing Records:**
Navigate to `/show`. You can view a tabular list of all queries, read the retrieved context documents, and delete records via the `Delete` action button.
