FROM python:3.11

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8501

ENV PYTHONPATH=/app

ENTRYPOINT ["streamlit","run"]

CMD ["pages/classifier.py"]