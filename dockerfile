# Multi-stage build for production-grade SaaS application
# Reduces final image size by ~70% and improves security
# 
# ARCHITECTURAL DECISIONS:
# 1. Multi-stage build: separate builder and runtime stages
# 2. Alpine base: smallest/most secure image (5MB base)
# 3. No root execution: runs as unprivileged user
# 4. Production dependencies only: no dev tools in final image
# 5. Proper signal handling: can gracefully shutdown
# 6. Health check endpoint: for orchestration liveness probes

# ============================================================
# STAGE 1: Builder - Compile dependencies
# ============================================================
FROM python:3.12-alpine as builder

LABEL maintainer="DevOps Team"
LABEL description="SaaS Subscription Billing Platform - Builder Stage"

# Install build dependencies
# These are only needed for compilation, removed in final image
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    linux-headers \
    g++ \
    make

# Create virtual environment in builder
RUN python -m venv /opt/venv

# Set PATH to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip/setuptools/wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install dependencies
COPY requirements.txt /tmp/

# Install Python dependencies
# Using --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r /tmp/requirements.txt


# ============================================================
# STAGE 2: Runtime - Final production image
# ============================================================
FROM python:3.12-alpine

LABEL maintainer="DevOps Team"
LABEL description="SaaS Subscription Billing Platform - Runtime"

# Environment variables (optimization + debugging)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOME=/app

# Install only runtime dependencies (not build tools)
RUN apk add --no-cache \
    postgresql-libs \
    curl \
    libmagic \
    ca-certificates \
    tini

# Create unprivileged user for security
# Never run containers as root in production
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Create application directory
WORKDIR ${APP_HOME}

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser . ${APP_HOME}

# Create necessary directories
RUN mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/media ${APP_HOME}/logs && \
    chown -R appuser:appuser ${APP_HOME}

# Collect static files (Django)
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Switch to non-root user
USER appuser

# Health check endpoint
# Docker will periodically call this to check container health
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Use tini as PID 1 (proper signal handling)
# Ensures graceful shutdown and zombie process cleanup
ENTRYPOINT ["/sbin/tini", "--"]

# Default command uses gunicorn (production server)
# Individual docker-compose services override this with their own command
CMD ["gunicorn", \
     "--workers=4", \
     "--worker-class=sync", \
     "--worker-tmp-dir=/dev/shm", \
     "--bind=0.0.0.0:8000", \
     "--timeout=120", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "--log-level=info", \
     "config.wsgi:application"]

# Expose port (for documentation; actual mapping in docker-compose)
EXPOSE 8000