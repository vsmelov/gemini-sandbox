"""Тестовый запрос к Gemini Robotics ER через API-ключ из .env."""

import os
import sys

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (OSError, ValueError):
        pass

import warnings

from dotenv import load_dotenv

# Пакет помечен как deprecated в пользу google-genai; пока оставляем как в твоём примере.
warnings.simplefilter("ignore", FutureWarning)

import google.generativeai as genai

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
# В Generative Language API модель называется иначе, чем в старых сниппетах: см. robotics-overview.
ROBOTICS_ER_MODEL = os.environ.get(
    "GEMINI_ROBOTICS_ER_MODEL", "gemini-robotics-er-1.6-preview"
)
if not API_KEY:
    print(
        "Задай GEMINI_API_KEY (или GOOGLE_API_KEY) в файле .env — см. .env.example",
        file=sys.stderr,
    )
    sys.exit(1)

genai.configure(api_key=API_KEY)


def test_robotics_er_with_key() -> None:
    model = genai.GenerativeModel(ROBOTICS_ER_MODEL)

    prompt = """
    Рассчитай безопасную траекторию.
    Эффектор манипулятора находится в [x: 120, y: 50, z: 10].
    Цель (ручка корзины для варки пасты) на [x: 120, y: 55, z: -5].
    Учитывай, что на высоте z: 5 находится дозирующий модуль, который нельзя задеть.
    """

    print("Отправляю запрос через API ключ...")

    try:
        response = model.generate_content(prompt)
        print("\nОтвет модели:")
        print(response.text)
    except Exception as e:
        print(f"\nОшибка: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    test_robotics_er_with_key()
