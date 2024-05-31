### Docker CLI commands :
docker build -t frontend-code-validation-service .      
docker run -d -p 8000:8080 frontend-code-validation-service

### To run locally: ###
pip install -r requirements. txt
uvicorn api:app

### Open Swagger UI ###
http://127.0.0.1:8000/docs<br>