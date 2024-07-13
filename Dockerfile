FROM seleniarm/standalone-chromium:latest

USER root

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip python3-venv

WORKDIR /app

COPY requirements.txt ./

RUN python3 -m venv /app/venv

RUN /bin/bash -c "source /app/venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

COPY ["src", "./src"]

EXPOSE 8080

CMD ["/app/venv/bin/python", "src/api.py"]