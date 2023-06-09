FROM python:3.8

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade dill

CMD ["python3", "app.py"]
