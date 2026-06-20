FROM python:3.12.10

WORKDIR app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "run:router", "--host", "0.0.0.0", "--port", "8080"]
