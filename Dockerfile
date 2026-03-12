
FROM python:3.10.4-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema para Pillow (Wagtail) y otras extensiones C
RUN apk add --no-cache \
    gcc \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev \
    libjpeg

COPY requirements/base.txt ./
COPY requirements/prod.txt ./

RUN pip install -r prod.txt

COPY ./ ./

CMD ["sh", "entrypoint.sh"]
