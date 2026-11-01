import os
import shutil
import subprocess
from typing import List


def ensure_bin(name: str) -> bool:
    return shutil.which(name) is not None


def run_cmd(cmd: List[str]):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        print(result.stderr)
    return result


def download_video(url: str, output_dir: str) -> str:
    if not ensure_bin("yt-dlp"):
        raise RuntimeError("yt-dlp غير مثبت. استخدم: pip install yt-dlp")

    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--format", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        url,
    ]
    result = run_cmd(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"فشل في تحميل الفيديو: {result.stderr}")

    candidates = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.lower().endswith(".mp4"):
                candidates.append(os.path.join(root, file))

    if not candidates:
        raise FileNotFoundError("لم يتم العثور على ملف فيديو محمل.")

    return sorted(candidates)[-1]
