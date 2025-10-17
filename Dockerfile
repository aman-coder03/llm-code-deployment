FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /home/user/app

# Copy requirements first to leverage Docker cache
COPY --chown=user ./requirements.txt /home/user/app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /home/user/app/requirements.txt

# Copy application code
COPY --chown=user . /home/user/app

# Switch to non-root user
USER user

# Environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Expose port for uvicorn
EXPOSE 7860

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
