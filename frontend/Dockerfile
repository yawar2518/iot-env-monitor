# =============================================================
# IoT Environmental Monitoring — React Frontend (Development)
# Runs Vite dev server with hot module replacement.
# In production this is replaced by an nginx static file server.
# =============================================================

FROM node:20-alpine

WORKDIR /app

# Copy package files first for dependency layer caching
# node_modules rebuild only when package.json changes
COPY package*.json ./

# Install dependencies if package.json exists,
# otherwise just prepare the directory for volume mount
RUN if [ -f package.json ]; then npm install; fi

# Copy source code
COPY . .

EXPOSE 5173

# Vite must bind to 0.0.0.0 inside Docker
# otherwise it only listens on localhost inside the container
# and is unreachable from your browser on the host machine
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]