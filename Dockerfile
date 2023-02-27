FROM python:latest

ENV OUTPUT_LOCATION="/data"

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

COPY ./scraper/ /src/scraper/
WORKDIR /src/scraper

RUN mkdir /data && \
    python -m pytest /src/scraper/tests/ --junitxml=/src/scraper/test_results.xml && \
    python /src/scraper/scraper.py

EXPOSE 8501

CMD ["streamlit", "run", "/src/scraper/visualization.py" ]
