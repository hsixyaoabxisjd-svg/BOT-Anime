import os
import time
from celery import Celery
from app.config import REDIS_URL, WORK_DIR
from app.services.downloader import download_video
from app.services.transcriber import transcribe_audio
from app.services.translator import translate_segments
from app.services.tts import synthesize_arabic_tts
from app.services.renderer import merge_video_audio

celery = Celery(
    "anime_dubber",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

@celery.task
def process_video_task(user_id: int, source_value: str, source_type: str = "url"):
    print(f"Processing job: user_id={user_id}, source_type={source_type}")

    job_dir = os.path.join(str(WORK_DIR), f"job_{user_id}_{int(time.time())}")
    os.makedirs(job_dir, exist_ok=True)

    try:
        if source_type == "url":
            video_path = download_video(source_value, job_dir)
        else:
            raise NotImplementedError("معالجة الملفات المباشرة تحتاج تنفيذ إضافي.")

        audio_path = os.path.join(job_dir, "audio.wav")
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            audio_path,
        ]
        result = __import__("subprocess").run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"فشل استخراج الصوت: {result.stderr}")

        segments = transcribe_audio(audio_path)
        translated_segments = translate_segments(segments)

        arabic_text = " ".join(seg.get("translated_text", "") for seg in translated_segments)
        arabic_audio_path = os.path.join(job_dir, "arabic_output.wav")
        synthesize_arabic_tts(arabic_text, arabic_audio_path)

        final_output = os.path.join(job_dir, "final_dubbed.mp4")
        merge_video_audio(video_path, arabic_audio_path, final_output)

        return {
            "status": "success",
            "user_id": user_id,
            "output_path": final_output,
            "segments": translated_segments,
        }

    except Exception as e:
        return {
            "status": "failed",
            "user_id": user_id,
            "error": str(e),
        }
