FROM python:3.11-alpine
RUN mkdir /appli
WORKDIR /appli
COPY . .
run pip install --upgrade pip
RUN pip install -e .
WORKDIR /appli/src/data_uploader
CMD ["python3","main.py"]

EXPOSE 5000

