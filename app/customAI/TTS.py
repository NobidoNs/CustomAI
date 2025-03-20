from g4f.client import Client
from app.utils.wright import wright

client = Client()

def process_text_with_ai(input_text):
    """
    Обрабатывает текст через ИИ, удаляет программный код и возвращает краткий пересказ.
    """

    # Формируем запрос к модели
    messages = [
        {"role": "system", "content": "Ты опытный помощник, который обрабатывает текст. Есть текст и ты должен дать его перессказ, минимум своих мыслей. Представь, что ты разговаривеешь с человеком и должен донести мысль кратко и понятно. Твоя задача: удалить программный код и вернуть краткий пересказ текста на русском языке. Не комментируй задание"},
        {"role": "system", "content": input_text}
    ]

    try:
        # Отправляем запрос к модели
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.4,
        )
        processed_text = response.choices[0].message.content.strip()
        return processed_text
    except Exception as e:
        wright(f"Ошибка обработки текста через ИИ: {e}", log=True)
        return input_text