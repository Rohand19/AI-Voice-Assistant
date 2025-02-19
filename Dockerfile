# Use official Python image as a base
FROM python:3.11

# Set working directory in the container
WORKDIR /app

# Copy project files to the container
COPY requirements.txt ./ 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose ports
EXPOSE 8000 8501

# Start FastAPI and Streamlit in parallel
CMD uvicorn main:app --host localhost --port 8000 & streamlit run app.py --server.port 8501 --server.address localhost
