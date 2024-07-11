### Docker CLI commands :
docker build -t frontend-code-validation-service .      
docker run -d -p 8000:8080 frontend-code-validation-service

### To run locally: ###
```
python3 -m venv env
pip install -r requirements.txt
source env/bin/activate
python src/api.py
```

### Open Swagger UI ###
http://127.0.0.1:5000/docs<br>