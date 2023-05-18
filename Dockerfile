FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
# EXPOSE $PORT
ENTRYPOINT [ "python" ]
CMD ["app.py"]