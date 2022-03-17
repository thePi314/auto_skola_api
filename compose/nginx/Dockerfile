FROM debian:stretch
RUN echo exit 0 > /usr/sbin/policy-rc.d
RUN apt-get update && apt-get install -y nginx nginx-extras
CMD ["nginx", "-g", "daemon off;"]
