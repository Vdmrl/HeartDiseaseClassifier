# Heart Disease Detector

## Description

The Heart Disease Detector is a web application that utilizes a trained AST transformer for classifying heart auscultation sounds, enabling early detection of heart conditions. Built with FastAPI, Streamlit, RabbitMQ, and PostgreSQL, it provides an efficient and interactive platform for healthcare professionals.

## Preparing environment and docker

+ Change .env.example name to .env.prod

+ Change .env.prod data to your configuration

## Running server

### Using Docker compose

+ Run services

    ```shell
    docker-compose up
    ```

+ Bring services down

    ```shell
    docker-compose down
    ```

go to the local host address: http://127.0.0.1:8501/

for backend documentation: http://127.0.0.1:8000/docs 
