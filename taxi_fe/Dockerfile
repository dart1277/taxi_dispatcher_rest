FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

FROM nginx:1.28-alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/
EXPOSE 8080
# run as root for demo purposes only, DO NOT RUN nginx like this in PROD !!
CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]

# docker build -t taxi_fe .
# docker run -p 8080:8080 --rm --name taxi_fe taxi_fe