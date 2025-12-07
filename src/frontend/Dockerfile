# Copyright (c) 2025 Green Wave Team
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Build stage
FROM node:24-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build args
ARG VITE_API_URL
ARG VITE_WS_URL
ARG VITE_ORION_URL

# Set env vars for build
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_WS_URL=$VITE_WS_URL
ENV VITE_ORION_URL=$VITE_ORION_URL

# Build application
RUN npm install
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files to nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
