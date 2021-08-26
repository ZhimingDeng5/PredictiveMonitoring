FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install -y libgomp1

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r nirdizati-training-backend/requirements.txt

CMD ["python", "main.py"]