## Frontend Code Validation service
Production Endpoint: https://frontendcodevalidationservice-cyz3lynf7q-uc.a.run.app/

This API service validates HTML/CSS/JS code against selenium test scripts for our frontend-leetcode project: [Frontend Racers](https://frontend-leetcode.vercel.app/)


### Docker CLI commands :
```
docker build -t frontend-code-validation-service .      
docker run -d -p 5050:8080 frontend-code-validation-service
```
> host port: 5050

### To run locally: ###
```
python3 -m venv env
pip install -r requirements.txt
source env/bin/activate
python src/api.py
```

>host port: 8080

### Open Swagger UI ###
http://\<api-endpoint\>/docs