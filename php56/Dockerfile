ARG PHP_VERSION
FROM php:${PHP_VERSION}-fpm

ARG PHP_XDEBUG
ARG PHP_SWOOLE
ARG PHP_REDIS
ARG REPLACE_SOURCE_LIST

RUN mkdir -p /run/php

RUN mkdir -p /data/logs
RUN chmod -R 777 /data/logs
#RUN mkdir -p /data/logs/shopapi.smartisan.com
#RUN chmod -R 777 /data/logs/shopapi.smartisan.com
#RUN mkdir -p /data/logs/couponapi.smartisan.com
#RUN chmod -R 777 /data/logs/couponapi.smartisan.com


#COPY -a /usr/local/etc/php/php.ini /usr/local/etc/php/php.ini

COPY ./sources.list /etc/apt/sources.list.tmp
RUN if [ "${REPLACE_SOURCE_LIST}" = "true" ]; then \
    mv /etc/apt/sources.list.tmp /etc/apt/sources.list; else \
    rm -rf /etc/apt/sources.list.tmp; fi

RUN apt update

# Install extensions from source
COPY ./extensions /tmp/extensions
RUN chmod +x /tmp/extensions/install.sh \
    && /tmp/extensions/install.sh \
    && rm -rf /tmp/extensions

# More extensions
# 1. soap requires libxml2-dev.
# 2. xml, xmlrpc, wddx require libxml2-dev and libxslt-dev.
# 3. Line `&& :\` do nothing just for better reading.

#ADD https://git.archlinux.org/svntogit/packages.git/plain/trunk/freetype.patch?h=packages/php /tmp/freetype.patch
#RUN docker-php-source extract; \
#  cd /usr/src/php; \
#  patch -p1 -i /tmp/freetype.patch; \
#  rm /tmp/freetype.patch
#
#RUN docker-php-ext-configure gd --with-gd --with-freetype-dir


RUN apt-get update && apt-get install -y \
    git \
    libjpeg62-turbo-dev \
    libpng-dev \
    iputils-ping \
    libwebp-dev \
    vim-gtk \
&& docker-php-ext-configure gd  --with-jpeg-dir=/usr/include/ \
&& docker-php-ext-install -j$(nproc) gd \
    && docker-php-ext-install zip \
    && docker-php-ext-install pdo_mysql \
    && docker-php-ext-install opcache \
    && docker-php-ext-install mysqli \
    && apt install -y libxml2-dev \
    && apt install -y libxslt-dev \
    && apt install -y freetype2-demos \
    && docker-php-ext-install soap \
    && docker-php-ext-install sockets


