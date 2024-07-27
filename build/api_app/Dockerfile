FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bzip2 \
    g++ \
    git \
    graphviz \
    libgl1-mesa-glx \
    libhdf5-dev \
    openmpi-bin \
    wget \
    python3-tk && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=iloveai
ENV POSTGRES_ADDRESS=postgres-container
ENV POSTGRES_DB=postgres

COPY . .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Minimize image size 
RUN (apt-get autoremove -y; \
    apt-get autoclean -y)

EXPOSE 8000
ENTRYPOINT ["python", "app.py"]
