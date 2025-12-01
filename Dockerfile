# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first to leverage cache
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
# --no-dev: Exclude development dependencies (like pytest)
# --frozen: Ensure uv.lock matches pyproject.toml
RUN uv sync --frozen --no-dev --no-install-project

# Copy the rest of the application code
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

# Final runtime image
FROM python:3.12-slim-bookworm

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --from=builder /app/src /app/src

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "service.api:app", "--host", "0.0.0.0", "--port", "8000"]
