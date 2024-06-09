FROM python:3.11.9

WORKDIR /backend

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "4000"]