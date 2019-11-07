FROM python:latest
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "/app/app.py"]
EXPOSE 8081
