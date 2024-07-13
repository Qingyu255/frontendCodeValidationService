FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ["src", "./src"]

EXPOSE 5000

CMD ["python", "src/api.py"]