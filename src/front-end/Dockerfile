FROM node:alpine

WORKDIR /app

COPY . /app

RUN npm install -n --force
RUN npm install -g @angular/cli
# RUN ng build --prod

# Apromore environment
CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check", "--configuration=production"]
# Local environment
# CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
