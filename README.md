> **基于 Kokoro 构建的中文 TTS 服务**，参考项目：https://github.com/kamjin3086/kokoro-onnx-fastapi
>
> * kokoro
> * fastapi
> * uv
> * docker



# 一、从源代码使用 uv 运行

```bash
git clone https://github.com/bitmms/kokoro-onnx-fastapi-docker-demo.git
```

```bash
cd kokoro-onnx-fastapi-docker-demo
```

```bash
wget https://github.com/bitmms/kokoro-onnx-fastapi-docker-demo/releases/download/model/models.zip
```

```bash
unzip models.zip
```

```bash
uv sync
```

```bash
uv run main.py
```



# 二、从源代码打包 Docker 镜像运行

```bash
git clone https://github.com/bitmms/kokoro-onnx-fastapi-docker-demo.git
```

```bash
cd kokoro-onnx-fastapi-docker-demo
```

```bash
wget https://github.com/bitmms/kokoro-onnx-fastapi-docker-demo/releases/download/model/models.zip
```

```bash
unzip models.zip
```

```bash
docker build -t kokoro-onnx-fastapi-docker-demo:v0.0.1 .
```

```bash
docker images
```

```bash
docker run -d \
  --name kokoro-onnx-fastapi-docker-demo \
  --restart unless-stopped \
  -p 8210:8210 \
  kokoro-onnx-fastapi-docker-demo:v0.0.1
```

```bash
docker ps -l
```

```bash
# docker exec -it 容器名称/容器ID /bin/bash
docker exec -it kokoro-onnx-fastapi-docker-demo /bin/bash
```



# 三、从 Docker 镜像压缩包运行

> 镜像导出为 tar 压缩包，便于后续使用

```bash
docker save kokoro-onnx-fastapi-docker-demo:v0.0.1 -o kokoro-onnx-fastapi-docker-demo-v0.0.1.tar
```

> 从 Docker 镜像压缩包运行

```bash
wget https://github.com/bitmms/kokoro-onnx-fastapi-docker-demo/releases/download/image/kokoro-onnx-fastapi-docker-demo-latest.tar
```

```bash
docker load < kokoro-onnx-fastapi-docker-demo-v0.0.1.tar
```

```bash
docker run -d \
  --name kokoro-onnx-fastapi-docker-demo \
  --restart unless-stopped \
  -p 8210:8210 \
  kokoro-onnx-fastapi-docker-demo:v0.0.1
```

```bash
docker exec -it kokoro-onnx-fastapi-docker-demo /bin/bash
```



# 四、从容器镜像仓库运行

> 这里以阿里云容器镜像管理服务为例

```bash
# 登录
docker login registry.cn-hangzhou.aliyuncs.com

# 给镜像打标签：要推送到阿里云镜像管理服务则必须要给镜像打阿里云专属的标签
# docker tag [imageId 或者 tag:version] registry.cn-hangzhou.aliyuncs.com/命名空间/镜像名称:version
docker tag kokoro-onnx-fastapi-docker-demo:v0.0.1 registry.cn-hangzhou.aliyuncs.com/bitm-aliyun-repo/kokoro-onnx-fastapi-docker-demo:v0.0.1

# 将镜像推送到 Docker 仓库
docker push registry.cn-hangzhou.aliyuncs.com/bitm-aliyun-repo/kokoro-onnx-fastapi-docker-demo:v0.0.1
```

> 从阿里云容器镜像管理服务拉取镜像并运行

```bash
docker pull registry.cn-hangzhou.aliyuncs.com/bitm-aliyun-repo/kokoro-onnx-fastapi-docker-demo:v0.0.1
```

```
docker tag registry.cn-hangzhou.aliyuncs.com/bitm-aliyun-repo/kokoro-onnx-fastapi-docker-demo:v0.0.1 kokoro-onnx-fastapi-docker-demo:v0.0.1
```

```bash
docker run -d \
  --name kokoro-onnx-fastapi-docker-demo \
  --restart unless-stopped \
  -p 8210:8210 \
  kokoro-onnx-fastapi-docker-demo:v0.0.1
```



# 五、测试
```bash
curl -X POST "http://127.0.0.1:8210/generate-speech/" \
     -H "Content-Type: application/json" \
     -d '{"text": "今天天气真好，请尽快撤离", "voice": "zm_100", "speed": 1.0}' \
     --output test.wav
```
