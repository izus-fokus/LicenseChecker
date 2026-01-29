# build stage
FROM node:lts-alpine AS build-stage
WORKDIR /app
COPY . /app
RUN rm -fr /app/node_modules
RUN rm -fr /app/dist
RUN npm install -g npm@latest
RUN npm install --force
RUN npm run build

# production stage
FROM registry.suse.com/suse/nginx AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
