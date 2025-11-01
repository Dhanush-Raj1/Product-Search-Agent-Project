FROM python:3.10-slim

WORKDIR /app 

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 8080 

#CMD gunicorn app:app --bind 0.0.0.0:$PORT 

# default timeout is 5s which is not enough and kills the web app as LLM + tools takes longer to respons.                                               
CMD gunicorn --bind 0.0.0.0:$PORT \
  --workers 2 --threads 2 \
  --timeout 300 --graceful-timeout 300 \
  --access-logfile - --error-logfile - --log-level info \
  app:app 
                                          

