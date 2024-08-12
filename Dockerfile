FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# 复制 entrypoint.sh 并设置可执行权限
COPY init.sh /app/init.sh
RUN chmod +x /app/init.sh


CMD ["/app/init.sh"]