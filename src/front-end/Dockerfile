FROM node:alpine

WORKDIR /app

COPY . /app

RUN npm install -n
RUN npm install -g @angular/cli

# CMD ["ng", "build", "--prod", "--base-href", "/test-app/"]

# EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]