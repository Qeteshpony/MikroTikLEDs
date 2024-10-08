FROM python:3.11-alpine
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY *.py ./
CMD ["python3", "-u", "./main.py"]
