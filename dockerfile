FROM python:3.9-buster

WORKDIR /playground

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "-u", "main.py"]