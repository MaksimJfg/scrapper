FROM python:3.10-slim

WORKDIR /app/app

COPY requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]