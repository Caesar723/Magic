FROM registry.cn-shanghai.aliyuncs.com/magic_fan_made/pythonmagic:latest

WORKDIR /app

COPY requirements-inference.txt /app/requirements-inference.txt
RUN --mount=type=cache,target=/root/.cache/pip python -m pip install pip==25.3 \
    && python -m pip install torch==2.7.1+cu126 torchvision==0.22.1+cu126 --index-url https://download.pytorch.org/whl/cu126 --extra-index-url https://pypi.org/simple \
    && python -m pip install -r /app/requirements-inference.txt \
    && python -c "import torch, onnxruntime, transformers, peft, onnx; from transformers.models.qwen3 import Qwen3Model; assert torch.version.cuda is not None; assert 'CUDAExecutionProvider' in onnxruntime.get_available_providers()"

COPY . /app/


# ARG TARGETPLATFORM
# RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then \
#         pip install torch==2.3.1+cpu  -f https://download.pytorch.org/whl/cpu/torch_stable.html; \
#     else \
#         pip install torch==2.3.1; \
#     fi
#     ##
#     # elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
#     #     pip install torch==2.3.1; \

# RUN pip install --no-cache-dir -r requirements.txt



COPY init.sh /src/init.sh
RUN chmod +x /src/init.sh

EXPOSE 443

CMD ["/src/init.sh"]
