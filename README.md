### Docker CLI commands :
docker build -t frontend-code-validation-service .      
docker run -d -p 8000:8080 frontend-code-validation-service

### To run locally: ###
uvicorn api:app