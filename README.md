# Listnr Report Recommender Bot

This project is a web application that recommends relevant tags for a given report. It uses a machine learning model to understand the content of the report and suggest the most appropriate categories.

## Features

- A simple web interface to submit reports for processing.
- An API endpoint (`/process`) for programmatic access.
- Utilizes Google's Generative AI for creating text embeddings.
- Uses FAISS (Facebook AI Similarity Search) for efficient similarity search.
- Easy to set up and run locally.
- Configured for deployment on Google App Engine.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project and add your Google API key:
    ```
    GOOGLE_API_KEY=your_google_api_key
    ```

5.  **Build the FAISS index:**
    You will need access to the Google Cloud Storage bucket `gs://lstnr-reports-data/AIS-feedback - final_reports_till_August24_2025.csv`. Make sure you have the necessary authentication set up (e.g., by running `gcloud auth application-default login`).
    Then, run the `embed.py` script to create the vector store:
    ```bash
    python embed.py
    ```
    This will create a `faiss_index` directory in your project.

6.  **Run the application:**
    ```bash
    python main.py
    ```
    The application will be available at `http://127.0.0.1:8080`.

## Usage

### Web Interface

1.  Open your web browser and navigate to `http://127.0.0.1:8080`.
2.  Enter the report text in the textarea.
3.  Click the "Submit" button.
4.  The recommended tags will be displayed in JSON format.

### API Endpoint

You can also send a POST request to the `/process` endpoint with a JSON payload:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"report": "your report text here"}' http://127.0.0.1:8080/process
```

The response will be a JSON object with the top 5 recommended tags.

## Deployment

This application is configured for deployment on Google App Engine. The `app.yaml` file contains the necessary configuration. You can deploy the application using the `gcloud` command-line tool:

```bash
gcloud app deploy
```

Make sure you have a Google Cloud project set up and the `gcloud` CLI configured correctly.
