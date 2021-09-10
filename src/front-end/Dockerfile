FROM node:alpine

WORKDIR /app

COPY . /app

RUN npm install -n
RUN npm install -g @angular/cli
RUN ng build --base-href /predictive/

CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]