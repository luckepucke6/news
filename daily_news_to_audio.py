import datetime
import requests
import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


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
    send_to_telegram(mp3_path)
    print(f"Sent {mp3_path} to Telegram")


def send_to_telegram(mp3_path: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendAudio"
    with open(mp3_path, "rb") as audio:
        requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID},
            files={"audio": audio},
            timeout=120,
        )



if __name__ == "__main__":
    main()
