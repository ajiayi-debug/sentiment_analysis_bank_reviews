FROM python:3.10.14

WORKDIR /DSA3101_group19

COPY backend/requirements.txt backend/
RUN pip install -r backend/requirements.txt

COPY backend/ backend/

COPY config.json .

COPY frontend/ frontend/

ENV FLASK_APP=backend/app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
