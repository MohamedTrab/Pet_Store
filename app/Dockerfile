FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install pyjwt
RUN pip install fastapi uvicorn
RUN pip install fastapi[all]
RUN pip install flask
RUN pip install --upgrade python-jose
RUN pip install psycopg2-binary
RUN pip install passlib
RUN pip install sqlalchemy
RUN pip install bcrypt
RUN pip install pika
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
