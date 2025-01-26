FROM python:3.11.9-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]