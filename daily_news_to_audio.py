import datetime
import requests
from apikey import OPENAI_API_KEY


PROMPT = """Din prompt här (din nyhetsstruktur med källkrav, ELI5, konsekvenser, ekonomi osv)."""

def openai_responses(prompt: str) -> str:
    # Skapar text med Responses API (rekommenderad för nya projekt). :contentReference[oaicite:1]{index=1}
    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": "gpt-4o-mini",
            "input": prompt,
        },
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    # Plocka ut text (fält kan variera mellan SDK/format, så håll koll vid behov)
    return data["output"][0]["content"][0]["text"]

def openai_tts(text: str, out_path: str):
    # Text till tal via Audio API /audio/speech. :contentReference[oaicite:2]{index=2}
    r = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": "gpt-4o-mini-tts",
            "voice": "marin",
            "input": text,
            "format": "mp3",
        },
        timeout=120,
    )
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)

def main():
    today = datetime.date.today().isoformat()
    text = openai_responses(PROMPT)
    mp3_path = f"daily_news_{today}.mp3"
    openai_tts(text, mp3_path)
    print(f"Saved {mp3_path}")

    # TODO: steg 3. Skicka filen till dig (Telegram/Drive/Email)
    # Exempel: ladda upp till S3/Drive eller posta till en webhook.

if __name__ == "__main__":
    main()
