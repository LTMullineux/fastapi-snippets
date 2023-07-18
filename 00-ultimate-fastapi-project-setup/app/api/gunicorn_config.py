from multiprocessing import cpu_count
from os import environ

_gunicorn_port = int(environ.get("APP_PORT", 8000))
_gunicorn_host = environ.get("APP_HOST", "0.0.0.0")
bind = f"{_gunicorn_host}:{_gunicorn_port}"
workers = int(environ.get("GUNICORN_WORKERS", 2 * cpu_count() + 1))
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 600
timeout = 3600
reload = True
accesslog = "-"
errorlog = "-"
capture_output = True
