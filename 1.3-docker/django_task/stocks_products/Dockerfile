FROM python:3.9

WORKDIR /stocks_products

COPY . /stocks_products

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD gunicorn stocks_products.wsgi -b 0.0.0.0:8000