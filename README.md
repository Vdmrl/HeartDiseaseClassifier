# Heart Disease Detector

## Description

The Heart Disease Detector is a web application that utilizes a trained AST transformer for classifying heart auscultation sounds, enabling early detection of heart conditions. Built with FastAPI, Streamlit, RabbitMQ, and PostgreSQL, it provides an efficient and interactive platform for healthcare professionals.

### Using python virtual machine

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.

2. Install requirements:

    ```shell
    python3 -m pip install --user -r requirements.txt
    ```
   
3. Run pytest
    ```shell
    pytest
    ```

4. Run server using gunicorn:

    ```shell
    uvicorn main:app --reload
    ```

go to the local host address: http://127.0.0.1:8000/
