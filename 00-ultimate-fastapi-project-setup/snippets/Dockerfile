FROM python:3.10-slim AS builder

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

ARG ENV
RUN if [ "$ENV" = "test" ]; then \
    pip install --user --no-cache-dir -r requirements-dev.txt; \
    fi;

FROM python:3.10-slim AS production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

WORKDIR /snippets

COPY . /snippets
