FROM python:3.14
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
COPY web .
WORKDIR /app/src
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w 4", "flsite:app"]
