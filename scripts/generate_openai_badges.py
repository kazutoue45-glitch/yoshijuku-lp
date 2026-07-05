#!/usr/bin/env python3
import base64
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "public" / "images"
API_URL = "https://api.openai.com/v1/images/generations"


COMMON_STYLE = """
Japanese cram school campaign badge, premium luxury jewelry feel, transparent
background. Real photorealistic gold metal with multi-stop gradients, bright
specular highlights, deeper shadowed gold edges, double thin gold border,
small sparkle and star ornaments around the edges, laurel wreath on both left
and right sides, soft drop shadow, deep burgundy or deep brown Japanese text.

Exact Japanese text, highly legible and centered:
Top line: 新規入塾生限定
Main line: 初月授業料 1ヶ月無料

Do not add any other words, logos, watermarks, people, classrooms, or background
objects. Keep the background fully transparent PNG.
"""


BADGES = [
    {
        "path": OUT_DIR / "badge-medal.png",
        "api_size": "1024x1024",
        "final_size": (1024, 1024),
        "prompt": COMMON_STYLE
        + """
Variant: ornate round medal badge. Symmetrical circular gold medallion, most
ornate of the set, raised embossed rim, inner round plaque, detailed gold
laurel wreath hugging the left and right sides, luxury award-medal composition.
""",
    },
    {
        "path": OUT_DIR / "badge-ribbon.png",
        "api_size": "1536x1024",
        "final_size": (1536, 512),
        "prompt": COMMON_STYLE
        + """
Variant: wide horizontal ribbon badge. Long central gold plaque with elegant
banner-fold tails on both ends, premium metallic folds and bevels, laurel wreath
details near the left and right of the central text. Compose all important
content in the vertical center band so it remains perfect after cropping to a
wide 3:1 ribbon.
""",
    },
    {
        "path": OUT_DIR / "badge-mini.png",
        "api_size": "1024x1024",
        "final_size": (1024, 1024),
        "prompt": COMMON_STYLE
        + """
Variant: simpler round badge. Clean circular gold badge with restrained laurel
wreath on the left and right sides, less ornate than the medal version, refined
and readable at smaller landing-page sizes.
""",
    },
]


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def generate_image(prompt: str, size: str) -> bytes:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it and rerun this script."
        )

    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": size,
        "n": 1,
        "quality": "high",
        "background": "transparent",
        "output_format": "png",
    }

    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"OpenAI API request failed: {exc.reason}") from exc

    try:
        return base64.b64decode(data["data"][0]["b64_json"])
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected OpenAI response: {data}") from exc


def fit_to_size(path: Path, final_size: tuple[int, int]) -> None:
    with Image.open(path) as image:
        image = image.convert("RGBA")
        if image.size == final_size:
            image.save(path)
            return

        target_w, target_h = final_size
        src_w, src_h = image.size
        scale = max(target_w / src_w, target_h / src_h)
        resized = image.resize(
            (round(src_w * scale), round(src_h * scale)),
            Image.Resampling.LANCZOS,
        )

        left = max(0, (resized.width - target_w) // 2)
        top = max(0, (resized.height - target_h) // 2)
        cropped = resized.crop((left, top, left + target_w, top + target_h))
        cropped.save(path)


def main() -> int:
    load_dotenv()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for badge in BADGES:
        path = badge["path"]
        print(f"Generating {path.relative_to(ROOT)} ({badge['api_size']})...")
        image_bytes = generate_image(badge["prompt"], badge["api_size"])
        path.write_bytes(image_bytes)
        fit_to_size(path, badge["final_size"])

        with Image.open(path) as image:
            print(
                f"  saved {path.relative_to(ROOT)} "
                f"{image.size[0]}x{image.size[1]} "
                f"{path.stat().st_size:,} bytes"
            )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
