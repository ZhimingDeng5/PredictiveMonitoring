FROM node:alpine

WORKDIR /app

COPY . /app

RUN npm install -n --force
RUN npm install -g @angular/cli
# RUN ng build --base-href /predictive/
RUN ng build

CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
