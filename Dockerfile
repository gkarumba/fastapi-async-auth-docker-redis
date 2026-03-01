FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    jq \
    tar \
    gcc \
    default-libmysqlclient-dev \
    libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# Install uv
RUN set -eux; \
    api="https://api.github.com/repos/astral-sh/uv/releases/latest"; \
    asset_url=$(curl -s "$api" | jq -r '.assets[] | select(.name|test("linux";"i")) | select(.name|test("x86_64|amd64";"i")) | .browser_download_url' | head -n1); \
    if [ -z "$asset_url" ]; then echo "uv release asset not found"; exit 1; fi; \
    curl -L "$asset_url" -o /tmp/uv.tar.gz; \
    mkdir -p /tmp/uv && tar -xzf /tmp/uv.tar.gz -C /tmp/uv; \
    uvbin=$(find /tmp/uv -type f -name "uv*" -perm /111 | head -n1); \
    install -m 0755 "$uvbin" /usr/local/bin/uv; \
    rm -rf /tmp/uv /tmp/uv.tar.gz

# Add wait-for-it script (correct way)
RUN curl -o /app/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /app/wait-for-it.sh

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock /app/

# Install dependencies
RUN uv sync --system --frozen

# Copy app
COPY . /app

# Add entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]