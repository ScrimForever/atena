FROM python:3.11
LABEL authors = "thiago.salgado.monteiro@gmail.com"
WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./src /src

CMD ["uvicorn", "startapp:app", "--host", "0.0.0.0", "--port", "8888"]