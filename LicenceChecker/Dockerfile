# 
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code
WORKDIR /code/api
EXPOSE 80

ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--host" ,"0.0.0.0" ,"--port", "80"]
