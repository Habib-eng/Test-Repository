FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

RUN mkdir /media/documents

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

ENV DB_NAME=neuroparser
ENV DB_PASSWORD=neuroparser123
ENV DB_USER=root
ENV DB_HOST=127.0.0.1
ENV DB_PORT=3306

CMD [ "python", "manage.py", "runserver"]