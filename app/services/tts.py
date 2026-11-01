import shutil
import subprocess


def ensure_bin(name: str) -> bool:
    return shutil.which(name) is not None


def synthesize_arabic_tts(text: str, output_path: str):
    if ensure_bin("espeak-ng"):
        cmd = ["espeak-ng", "-v", "ar", "-w", output_path, text]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return

    if ensure_bin("espeak"):
        cmd = ["espeak", "-v", "ar", "-w", output_path, text]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return

    with open(output_path, "wb") as f:
        f.write(b"")
