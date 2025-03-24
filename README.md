# Heart Disease Classifier

## Description

The Heart Disease Classifier is a web application that utilizes a trained Audio Spectrogram Transformer for classifying heart auscultation sounds, enabling early detection of heart conditions. Built with FastAPI, Streamlit, RabbitMQ, Celery, Redis, PostgreSQL and Docker, it provides an efficient and interactive platform for healthcare professionals.

### Main features:
+ Asynchronous API built with FastAPI and auto-generated Swagger documentation
+ Scalable model worker leveraging Celery and RabbitMQ for asynchronous audio classification
+ Dataset collection and preprocessing pipeline for robust training and validation
+ Trained Audio Spectrogram Transformer model and uploaded it to Hugging Face
+ High-performance caching implemented with Redis
+ Secure user authentication and management with JWT bearer tokens
+ Interaction with the database using SQLalchemy and async driver asyncpg
+ Migrations using Alembic
+ Logging with Python JSON logger
+ Sentry integration
+ Monitoring with Prometheus and Grafana dashboards
+ Reverse proxy configuration using Nginx
+ Linters with GitHub CI
+ Fully containerized application

## Preparing environment

+ Change .env.example name to .env.prod

+ Change .env.prod data to your configuration

## Running server

### Using Docker compose

+ Run services

    ```shell
    docker-compose up --build
    ```

+ Bring services down

    ```shell
    docker-compose down
    ```

Web-application local host address: http://127.0.0.1:8501/

Backend documentation: http://127.0.0.1:8000/docs

Monitoring Grafana: http://localhost:3000/ (admin, admin)

RabbitMQ Management UI: http://localhost:15672/ (user, pass)
