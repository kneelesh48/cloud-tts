FROM python:3.12.3-bookworm

WORKDIR /app

RUN mkdir temp

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "home.py"]
