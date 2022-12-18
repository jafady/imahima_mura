# ビルド環境
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN apk add --no-cache python3 make g++
RUN npm install -g npm@9.2.0
RUN npm install
RUN npx browserslist@latest --update-db
COPY . .
ARG VUE_APP_API_ENDPOINT_PROTOCOL
ARG VUE_APP_API_ENDPOINT_HOST
ARG VUE_APP_WEBSOCKET_ENDPOINT_PROTOCOL
ARG VUE_APP_WEBPUSH_APPSERVERKEY
ENV VUE_APP_API_ENDPOINT_PROTOCOL=${VUE_APP_API_ENDPOINT_PROTOCOL}
ENV VUE_APP_API_ENDPOINT_HOST=${VUE_APP_API_ENDPOINT_HOST}
ENV VUE_APP_WEBSOCKET_ENDPOINT_PROTOCOL=${VUE_APP_WEBSOCKET_ENDPOINT_PROTOCOL}
ENV VUE_APP_WEBPUSH_APPSERVERKEY=${VUE_APP_WEBPUSH_APPSERVERKEY}
ENV NODE_ENV=production
RUN npm run build

# 本番環境
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
ENV PORT=8080
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'