FROM python:3.12.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uvicorn[standard]

COPY . .

EXPOSE 8080

CMD ["uvicorn", "src.college_parser.main:router", "--host", "0.0.0.0", "--port", "8080"]
