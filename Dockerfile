FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]