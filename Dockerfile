FROM python:3.12
WORKDIR /code

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --no-cache-dir numpy==1.26.3

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
