FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .

# Set non-root user for security
RUN groupadd -r dracor && useradd -r -g dracor dracor
USER dracor

# Expose the MCP server port
EXPOSE 8008

# Add healthcheck to ensure the application is running properly
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8008/health || exit 1

# Set environment variable to choose implementation (default or fastmcp)
ENV IMPLEMENTATION=default

# Use entrypoint script to choose implementation
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"] 