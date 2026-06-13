FROM python:3.11-slim

# Create a non-root user (mandatory for HF Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY --chown=user . .

EXPOSE 7860

# Run Streamlit on port 7860
CMD ["streamlit", "run", "src/ui/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
