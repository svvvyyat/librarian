import json
import ollama

model = "gemma2:2b"
def analyze_text(text):
    text = text[:5000]
    prompt = f"""
    Ти — професійний бібліотекар та аналітик даних.
    Текст для аналізу:
    ----------------
    {text}
    ----------------

    Твоє завдання — створити метадані для пошукової системи.
    Вимоги до відповіді (JSON):
    1. "description": Короткий опис змісту українською мовою (2-3 речення).
    2. "keywords": Список ключових слів та фраз для пошуку українською.
    ВАЖЛИВО: Не обмежуй кількість тегів. Випиши ВСІ важливі терміни, імена, дати або назви, які зустрічаються в тексті і можуть бути корисні для пошуку. 
    Якщо документ складний — дай більше тегів. Якщо простий — менше.
    ВІДПОВІДАЙ ВИКЛЮЧНО В ТАКОМУ JSON ФОРМАТІ:
    {{
        "description": "Опис документа",
        "keywords": ["слово1", "слово2", "складний термін", "ім'я автора", ...]
    }}
    """
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}],format='json')
        answer = response.get("message", {}).get("content", "")
        json_answer = answer.replace("```json", "").replace("```", "").strip()
        return json.loads(json_answer)

    except json.JSONDecodeError:
        print("Некоректний формат відповіді AI")
        return {"summary": "Помилка обробки AI.", "keywords": []}
    
    except Exception as e:
        print(f"Помилка обробки: {e}")
        return {"summary": "Помилка обробки.", "keywords": []}