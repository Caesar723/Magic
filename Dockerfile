FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


COPY init.sh /src/init.sh
RUN chmod +x /src/init.sh


CMD ["/src/init.sh"]