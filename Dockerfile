FROM alpine:3.6

ENV NGINX_VERSION 1.12.2
ENV NGINX_VOD_MODULE_VERSION 1.20

EXPOSE 1935
EXPOSE 80

RUN apk add --no-cache wget ca-certificates build-base openssl openssl-dev zlib-dev linux-headers pcre-dev ffmpeg ffmpeg-dev

# Get nginx source.
RUN wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz \
  && tar zxf nginx-${NGINX_VERSION}.tar.gz \
  && rm nginx-${NGINX_VERSION}.tar.gz

# Get nginx vod module.
RUN wget https://github.com/kaltura/nginx-vod-module/archive/${NGINX_VOD_MODULE_VERSION}.tar.gz \
  && tar zxf ${NGINX_VOD_MODULE_VERSION}.tar.gz \
  && rm ${NGINX_VOD_MODULE_VERSION}.tar.gz

# Compile nginx with nginx-vod-module.
RUN cd nginx-${NGINX_VERSION} \
  && ./configure \
  --prefix=/usr/local/nginx \
  --add-module=../nginx-vod-module-${NGINX_VOD_MODULE_VERSION} \
  --conf-path=/usr/local/nginx/conf/nginx.conf \
  --with-file-aio \
  --error-log-path=/opt/nginx/logs/error.log \
  --http-log-path=/opt/nginx/logs/access.log \
  --with-threads \
  --with-cc-opt="-O3" \
  --with-debug
RUN cd nginx-${NGINX_VERSION} && make && make install

# Cleanup.
RUN rm -rf /var/cache/* /tmp/*

ENTRYPOINT ["/usr/local/nginx/sbin/nginx"]
CMD ["-g", "daemon off;"]