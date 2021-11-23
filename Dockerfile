FROM python:3.9.4-slim-buster as base

WORKDIR /app
EXPOSE 5000
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false


FROM base as production
RUN poetry install --no-dev --no-root
COPY . /app/
ENTRYPOINT bash ./entrypoint.sh


FROM base as development
RUN poetry install
COPY . /app/    
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000


FROM base as test
RUN poetry install
# Get Chrome
RUN apt-get update && apt-get install curl unzip -y
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt install ./chrome.deb -y &&\
    rm ./chrome.deb
# Get ChromeDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver.zip &&\
    unzip ./chromedriver.zip
COPY . /app/

ENTRYPOINT [ "poetry", "run", "pytest" ]