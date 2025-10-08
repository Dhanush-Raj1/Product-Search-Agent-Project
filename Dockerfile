FROM python:3.10-slim

WORKDIR /app 

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 8080 

#CMD gunicorn app:app --bind 0.0.0.0:$PORT 

# default timeout is 5s which is not enough and kills the web app as LLM + tools takes longer to respons.                                               
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 300 --graceful-timeout 300 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 --access-logfile - --error-logfile - --log-level info
                                          # 2 CPU    # 2 threads   # 300s timout