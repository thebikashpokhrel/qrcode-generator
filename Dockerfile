FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN python -m venv projenv

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/qrcodes

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]