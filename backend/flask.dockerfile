FROM python:3.11.4

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["flask","--app", "run", "--debug", "run","--host=0.0.0.0","--port=4000"]