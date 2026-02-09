# Build Stage
FROM oven/bun:1.3.4-alpine AS build
WORKDIR /app
COPY ../../frontend /app
RUN ["bun","install"]
RUN ["bun","run","build"]

# Production Stage
FROM nginx:stable-alpine AS production
RUN rm /etc/nginx/conf.d/default.conf
COPY ./infra/config/default.conf /etc/nginx/conf.d
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]