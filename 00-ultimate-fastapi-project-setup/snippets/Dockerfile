FROM python:3.12-slim AS builder

COPY ./snippets/requirements.txt requirements.txt
COPY ./snippets/requirements-dev.txt requirements-dev.txt

RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

ARG ENV
RUN if [ "$ENV" = "test" ]; then \
    pip install --user --no-cache-dir -r requirements-dev.txt; \
    fi;

FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

WORKDIR /code

COPY ./snippets /code/snippets
