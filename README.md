## Frontend Code Validation service
This API service validates HTML/CSS/JS code against selenium test scripts for our frontend-leetcode project


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