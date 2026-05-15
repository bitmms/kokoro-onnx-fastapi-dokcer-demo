> **基于 Kokoro 构建的中文 TTS 服务**，参考项目：https://github.com/kamjin3086/kokoro-onnx-fastapi
> * kokoro
> * fastapi
> * uv
> * docker

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
docker run -p 8210:8210 kokoro-onnx-fastapi-dokcer-demo:latest
```

```bash
curl -X POST "http://127.0.0.1:8210/generate-speech/" \
     -H "Content-Type: application/json" \
     -d '{"text":"今天天气真好，我要自己上厕所", "voice":"zm_100", "filename":"ttsfile", "speed": 1.0}' \
     --output ./test.wav
```