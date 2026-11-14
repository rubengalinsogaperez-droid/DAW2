FROM node:22-alpine
# La versión queda grabada DENTRO de la imagen al construirla (docker compose build)
ARG VERSION=dev
ENV APP_VERSION=$VERSION
WORKDIR /app
COPY server.js .
EXPOSE 3000
CMD ["node", "server.js"]
