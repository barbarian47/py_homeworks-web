FROM python:3.9.6-alpine

WORKDIR /stocks_products

COPY . /stocks_products

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /stocks_products/entrypoint.sh
RUN chmod +x /stocks_products/entrypoint.sh

ENTRYPOINT ["/stocks_products/entrypoint.sh"]