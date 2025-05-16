FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    python -m spacy download en_core_web_sm

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "main:app"]
