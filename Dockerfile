FROM python:3.11

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /usr/src/app/
COPY . .
CMD [ "pytest" ]
