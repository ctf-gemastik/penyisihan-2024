FROM php:8.2-fpm-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache nginx curl-dev

RUN docker-php-ext-install curl

RUN curl -sS https://getcomposer.org/installer | php && \
    mv composer.phar /usr/local/bin/composer

COPY ./src/site.conf /etc/nginx/http.d/default.conf
COPY ./src/php.ini /usr/local/etc/php/php.ini
COPY ./src/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

COPY ./src/flag.txt /.Th1sIsYourPr1z3

WORKDIR /opt/app
COPY ./src/app/ .
RUN chmod -R 777 /opt/app
RUN find . -type f -exec chmod 755 {} \;

ENV COMPOSER_ALLOW_SUPERUSER=1
RUN composer install

EXPOSE 80

CMD [ "/docker-entrypoint.sh" ]

