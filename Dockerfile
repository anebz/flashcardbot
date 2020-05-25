FROM python:3.7

RUN mkdir /app
ADD . /app
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python /app/flashcardbot.py