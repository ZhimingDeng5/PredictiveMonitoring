FROM node:alpine

WORKDIR /app

COPY . /app

RUN npm install -n --force
RUN npm install -g @angular/cli
# RUN ng build --prod

CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check", "--configuration=production"]
