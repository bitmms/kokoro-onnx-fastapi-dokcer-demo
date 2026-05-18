> **基于 Kokoro 构建的中文 TTS 服务**，参考项目：https://github.com/kamjin3086/kokoro-onnx-fastapi
> * kokoro
> * fastapi
> * uv
> * docker



# 一、从源代码使用 uv 运行

```bash
git clone https://github.com/bitmms/kokoro-onnx-docker-demo.git
```

```bash
cd kokoro-onnx-docker-demo
```

```bash
wget https://github.com/bitmms/kokoro-onnx-docker-demo/releases/download/model/models.zip
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
git clone https://github.com/bitmms/kokoro-onnx-docker-demo.git
```

```bash
cd kokoro-onnx-docker-demo
```

```bash
wget https://github.com/bitmms/kokoro-onnx-docker-demo/releases/download/model/models.zip
```

```bash
unzip models.zip
```

```bash
docker build -t kokoro-onnx-fastapi-dokcer-demo .
```

```bash
docker run -d -p 8210:8210 kokoro-onnx-fastapi-dokcer-demo
```



# 三、从 Docker 镜像压缩包运行

```bash
docker load < kokoro-onnx-fastapi-dokcer-demo-latest.tar
```

```
docker run -d -p 8210:8210 kokoro-onnx-fastapi-dokcer-demo
```



# 四、从 DockerHub 运行

```bash
docker run -d -p 8210:8210 kokoro-onnx-fastapi-dokcer-demo
```

```bash
curl -X POST "http://127.0.0.1:8210/generate-speech/" \
     -H "Content-Type: application/json" \
     -d '{"text":"今天天气真好，我要自己上厕所", "voice":"zm_100", "speed": 1.0}' \
     --output ./test.wav
```
