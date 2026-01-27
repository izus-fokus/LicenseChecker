# 
FROM python:3.13.11-alpine3.23

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir -r /code/requirements.txt

# 
COPY . /code
WORKDIR /code/api
EXPOSE 8000

ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--host" ,"0.0.0.0" ,"--port", "8000"]
