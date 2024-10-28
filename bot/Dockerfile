FROM python:3.11.7-slim

EXPOSE 8000

RUN mkdir /app 
  
ADD . /app   

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
  
CMD ["streamlit", "run", "Overview.py", "--server.port=8000", "--server.address=0.0.0.0"]   