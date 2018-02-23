FROM nikolaik/python-nodejs
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install -r requirements.txt
RUN cd bicycleparking && npm install && npm install --dev && npm run build
CMD python manage.py migrate && python manage.py runserver
