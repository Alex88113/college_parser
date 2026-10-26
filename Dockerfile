FROM python:3.13-alpine AS builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && pip install --no-cache-dir --prefix=/install "uvicorn[standard]"


FROM python:3.13-alpine

WORKDIR /app


COPY --from=builder /install /usr/local

RUN addgroup -S app && adduser -S app -G app

COPY --chown=app:app . .

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://127.0.0.1:8000/docs > /dev/null || exit 1

CMD ["uvicorn", "src.college_parser.main:app", "--host", "0.0.0.0", "--port", "8000"]
