FROM python:latest
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple
CMD ["python", "/app/app.py"]
EXPOSE 8081
