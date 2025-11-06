# Doctor Assistant Chatbot

This project is a Doctor Assistant chatbot that can answer medical questions. It uses the Gemini 2.5 Flash language model through the LangChain library. The chatbot can be run in three different ways: as a command-line application, as a web application using Streamlit, or as an API using FastAPI.

## Features

-   **Multiple Interfaces:** Run the chatbot in the terminal, as a Streamlit web app, or as a FastAPI-powered API.
-   **Conversational Memory:** The chatbot remembers the context of the conversation for each user.
-   **Powered by Gemini 2.5 Flash:** Utilizes Google's powerful and efficient language model.
-   **Easy to Use:** Simple and intuitive interfaces for interacting with the chatbot.

## Prerequisites

-   Python 3.7+
-   An API key for the Gemini API.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/DoctorGPT.git
    cd DoctorGPT
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv doctor_gpt
    source doctor_gpt/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**

    Create a file named `.env` in the root directory of the project and add your Gemini API key to it:

    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

## Usage

You can run the Doctor Assistant chatbot in three different ways:

### 1. Terminal Application

To run the chatbot in your terminal, execute the following command:

```bash
python doctor_assistant_terminal.py
```

The application will prompt you for your name and age, and then you can start chatting with the assistant.

### 2. Streamlit Web Application

To run the chatbot as a web application, use the following command:

```bash
streamlit run streamlit_app.py
```

This will start a local web server, and you can interact with the chatbot in your browser.

### 3. FastAPI Application

To run the chatbot as an API, you need to use `uvicorn`:

```bash
uvicorn doctor_assistant_api:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can send POST requests to the `/chat` endpoint with a JSON payload containing the user's name, age, and message.

You can test the API using the `client_test.py` script:

```bash
python client_test.py
```

## Project Structure

-   `doctor_assistant_terminal.py`: The command-line interface for the chatbot.
-   `streamlit_app.py`: The Streamlit web application.
-   `doctor_assistant_api.py`: The FastAPI application.
-   `client_test.py`: A script to test the FastAPI endpoint.
-   `requirements.txt`: A list of the Python dependencies for the project.
-   `.env`: A file for storing environment variables (e.g., your Gemini API key).
-   `README.md`: This file.