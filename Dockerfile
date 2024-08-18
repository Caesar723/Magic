FROM registry.cn-shanghai.aliyuncs.com/magic_fan_made/python3.9

WORKDIR /app

COPY . /app/


ARG TARGETPLATFORM
RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then \
        pip install torch==2.3.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html; \
    elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
        pip install torch==2.3.1; \
    else \
        pip install torch; \
    fi

RUN pip install --no-cache-dir -r requirements.txt



COPY init.sh /src/init.sh
RUN chmod +x /src/init.sh

EXPOSE 8000

CMD ["/src/init.sh"]