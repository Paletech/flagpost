FROM node:12 AS builder

ADD package.json /package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install

WORKDIR /app
ADD . /app

EXPOSE 8000
EXPOSE 35729

RUN ls -la

ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["start"]

FROM nginx:1.17

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build/ /usr/share/nginx/html

WORKDIR /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]