FROM python:3.10-slim
LABEL authors="arvkevi@gmail.com"

EXPOSE 8501

WORKDIR /app
COPY . /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc g++ libffi-dev 
RUN pip install --upgrade pip
RUN pip install .[streamlit]

ENTRYPOINT [ "streamlit", "run"]
CMD ["/app/streamlit/app.py"]
