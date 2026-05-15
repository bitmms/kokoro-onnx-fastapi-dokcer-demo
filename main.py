import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse
import soundfile as sf
from misaki import zh
from kokoro_onnx import Kokoro

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

kokoro_model: Kokoro = None
g2p_converter = None


@app.post("/generate-speech/")
async def generate_speech_api(
        text: str = Body(..., description="要转换为语音的文本"),
        voice: str = Body(..., description="使用的声音模型，例如 'zf_001'"),
        filename: str = Body(None, description="生成的语音文件名（不含路径和后缀，默认为临时文件）"),
        speed: float = Body(1.0, description="语音速度，支持小数，默认为1.0")
):
    if not kokoro_model or not g2p_converter:
        raise HTTPException(status_code=503, detail="模型服务尚未准备好，请稍后再试或检查启动日志。")
    try:
        logging.info(f"收到请求：text='{text}', voice='{voice}', filename='{filename}', speed='{speed}'")
        phonemes, _ = g2p_converter(text)
        samples, sample_rate = kokoro_model.create(phonemes, voice=voice, speed=speed, is_phonemes=True)

        audio_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_audio")
        output_path = os.path.join(audio_output_dir, f"{filename}.wav")

        sf.write(output_path, samples, sample_rate)
        logging.info(f"语音文件已生成: {output_path}")
        return FileResponse(output_path, media_type='audio/wav', filename=os.path.basename(output_path))
    except Exception as e:
        logging.exception(f"语音合成失败: {e}")
        raise HTTPException(status_code=500, detail=f"语音合成失败: {str(e)}")


if __name__ == "__main__":
    kokoro_model = Kokoro("./models/kokoro-v1.1-zh.onnx", "./models/voices-v1.1-zh.bin", vocab_config="./models/config.json")
    g2p_converter = zh.ZHG2P(version="1.1")
    logging.info("模型在 __main__ 中加载成功 (用于直接运行测试)。")
    uvicorn.run(app, host="0.0.0.0", port=8210)
