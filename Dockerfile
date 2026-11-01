FROM python:3.13-alpine

LABEL org.opencontainers.image.title="cheer-web"
LABEL org.opencontainers.image.description="Cheer-up message web server"

ENV PORT=5000 \
    APP_MODE=dev \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN adduser -D appuser
COPY app/ /app/
USER appuser

EXPOSE 5000
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:${PORT}/health || exit 1

CMD ["python", "server.py"]
