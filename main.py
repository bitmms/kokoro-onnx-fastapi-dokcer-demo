import os
import logging
import io
import uvicorn
from misaki import zh
import soundfile as sf
from misaki.zh import ZHG2P
from kokoro_onnx import Kokoro
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Body, Response


# 全局配置
kokoro: Kokoro
zhg2p: ZHG2P
BASE: str = os.path.dirname(__file__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


# 启动时加载模型
@asynccontextmanager
async def lifespan(_):
    global kokoro, zhg2p

    kokoro = Kokoro(
        model_path=os.path.join(BASE, "models/kokoro-v1.1-zh.onnx"),
        voices_path=os.path.join(BASE, "models/voices-v1.1-zh.bin"),
        vocab_config=os.path.join(BASE, "models/config.json")
    )
    logging.info("文本转语音模型 Kokoro 加载完成")

    zhg2p = zh.ZHG2P()
    logging.info("音素转换工具 ZHG2P 加载完成")

    # ======================
    # 【关键：启动预热】
    # ======================
    try:
        logging.info("服务预热中（第一次推理加载）...")
        phonemes, _ = zhg2p("预热测试")
        kokoro.create(phonemes, voice="zf_001", speed=1.0, is_phonemes=True)
        logging.info("预热完成！后续请求秒回")
    except:
        logging.warning("⚠预热失败，但不影响正常运行")

    yield
    logging.info("服务已关闭，服务已关闭，服务已关闭！")


app = FastAPI(lifespan=lifespan)


# 语音合成接口
@app.post("/generate-speech/")
def generate_speech_api(
        text: str = Body(..., description="必填：要转换为语音的文本"),
        voice: str = Body(default="zf_001", description="必填：使用的声音，例如 zf_001"),
        speed: float = Body(default=1.0, description="必填：语速，例如 1.0")
):
    # 模型是否就绪
    if not kokoro or not zhg2p:
        raise HTTPException(status_code=503, detail="服务未准备就绪")

    # 强校验 text 必须传
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="text 不能为空")

    try:
        logging.info(f"收到请求：text='{text}', voice='{voice}', speed='{speed}'")
        # 文本转音素
        phonemes, _ = zhg2p(text)
        # 生成语音
        samples, sr = kokoro.create(phonemes, voice=voice, speed=speed, is_phonemes=True)
        # 在内存中生成音频
        audio_stream = io.BytesIO()
        sf.write(audio_stream, samples, sr, format="WAV")
        audio_stream.seek(0)
        # 直接返回音频
        return Response(content=audio_stream.read(), media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 启动
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8210)
