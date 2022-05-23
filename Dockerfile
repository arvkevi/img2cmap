FROM python:3.10-slim
LABEL authors="arvkevi@gmail.com"

EXPOSE 8501

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install streamlit
RUN pip install -e .

ENTRYPOINT [ "streamlit", "run"]
CMD ["/app/streamlit/app.py"]
