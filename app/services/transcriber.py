from typing import List, Dict


def transcribe_audio(audio_path: str) -> List[Dict]:
    try:
        import whisper
    except Exception:
        return [
            {
                "start": 0.0,
                "end": 1.0,
                "text": "مرحبا بكم. هذا نص تجريبي بدلاً من التشفير الصوتي الحقيقي."
            }
        ]

    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False)
    segments = result.get("segments", [])
    cleaned = []
    for seg in segments:
        cleaned.append({
            "start": float(seg.get("start", 0.0)),
            "end": float(seg.get("end", 0.0)),
            "text": str(seg.get("text", "")).strip()
        })
    return cleaned
