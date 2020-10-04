FROM python:3.6-slim
RUN apt-get update && \
    pip install --upgrade pip && \
    apt-get install build-essential -y
COPY . /usr/app/
EXPOSE 8501
WORKDIR /usr/app/
RUN pip install -r requirements.txt
CMD streamlit run app.py