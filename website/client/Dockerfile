# Frontend image: Vite build → nginx static serve.
#
# Two stages so the final image is small (no Node, no node_modules).
# nginx also proxies /api/* and /healthz to the backend container, so
# the browser only sees one origin and CORS is moot at runtime.

# ---------- Stage 1: build ----------
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# ---------- Stage 2: serve ----------
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80