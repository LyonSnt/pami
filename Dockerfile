FROM node:22-alpine AS assets

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY static/css/input.css ./static/css/input.css
COPY templates/ ./templates/
COPY apps/ ./apps/
RUN npm run tailwind


FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/ /app/requirements/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements/prod.txt

COPY . /app/
COPY --from=assets /app/static/css/output.css /app/static/css/output.css

RUN groupadd --gid 10001 appgroup \
    && useradd --uid 10001 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/media /app/staticfiles \
    && chmod +x /app/deploy/entrypoint.sh \
    && chown -R appuser:appgroup /app

USER appuser

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-"]
