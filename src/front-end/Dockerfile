FROM node:alpine

WORKDIR /app

COPY package.json /app/package.json

RUN npm install
RUN npm install -g @angular/cli

COPY . /app

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0"]