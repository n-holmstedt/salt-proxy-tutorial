FROM python:3.8.16-alpine3.17
RUN python -m pip install flask flask_httpauth werkzeug
WORKDIR /app
COPY ./app /app
CMD ["python3", "app.py"]