FROM python:3.12.8

WORKDIR /app

COPY simple_app.py requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "simple_app.py"]
