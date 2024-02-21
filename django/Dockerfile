# Dockerfile for Cisco Configurator 2.0

FROM python:3

COPY django/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000

ENTRYPOINT ["python", "django/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
