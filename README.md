# 🏠 AI Домашний Помощник — Минималистичный Голосовой Ассистент

**[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Лицензия](https://img.shields.io/badge/License-GPL3-green)](LICENSE)**

**Лёгкий | Мультиплатформенный**  
Ассистент активируется **только по имени**, работает с облачными и локальными нейросетями. Потребляет минимум ресурсов.

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDFoODNqZGJ4dW0ya3AwdGJ6Y2JmOGVkY2JmYzV6cjRnb2VqeWZ5biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.gif" width="400" alt="Демо">
</p>

---

## 🌟 Почему этот проект?

| Особенность        | Преимущество                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------- |
| **🔒 Приватность** | Обработка запросов начинается **только после активационной фразы** (звуковой сигнал)        |
| **☁️ Лёгкость**    | Работает с облачными (GPT-4o, Gemini) моделями избавляя от необходимсти иметь мощное железо |
| **🎭 Характеры**   | Добавьте свой (app/customAI/simple/characters.json) или используйте готовый                 |
| **⚡ Минимализм**  | Нацелен на работу через голосовое управление                                                |

---

## 🚀 Быстрый старт

### Установка (1 минута)

```bash
git clone https://github.com/NobidoNs/CustomAI.git
cd CustomAI
pip install -r requirements.txt
```

**Для Linux/macOS:**

```bash
sudo apt install ffmpeg  # Linux
brew install portaudio  # macOS
```

### Первый запуск

1. **Калибровка микрофона** (5 сек тишины!):
   ```bash
   python ambient.py
   ```
2. Запустите ассистента:
   ```bash
   python start.py
   ```
3. Скажите _«Джарвис»_ (прогремит сигнал) → задайте вопрос.

---

## ⚙️ Настройка

### 1. Выбор нейросети

В `devolp_config.json` укажите приоритет моделей:

```json
"AImodelPriority": ["gpt-4o", "phi-3", "gemini-1.5-flash"]
```

### 2. Голос и TTS

Доступные движки:

- **Google TTS** (онлайн)
- **Edge TTS** (Microsoft)
- **Vosk** (оффлайн)

Настройка:

```json
"TTS_engine": "edgeTTS",
"voice_speed": 1.2
```

### 3. Текстовый режим

Откройте `output.md` и пишите:

```markdown
!какая погода?
```

_(Ответ появится в том же файле)_

---

## 🎭 Примеры команд

| Действие        | Голосовая команда        | Текстовая команда   |
| --------------- | ------------------------ | ------------------- |
| Смена характера | _«Джарвис, будь добрым»_ | `!character добрый` |
| Очистка памяти  | _«Джарвис, забудь всё»_  | `!clear_context`    |
| Экспорт диалога | —                        | `!save_history`     |

---

## 📌 FAQ

**Q: Как сменить имя ассистента?**  
→ В `devolp_config.json` найдите `"activation_name"`.

**Q: Можно ли использовать без интернета?**  
→ Да! Выберите **Vosk + Llama 3** в настройках.

**Q: Почему нет GUI?**  
→ Проект заточен под голос/терминал для экономии ресурсов.

---

## 🛠️ Для разработчиков

### Добавление команд

Создайте плагин в `modules/`:

```python
from core import register_command

@register_command("моя_команда")
def custom_handler(text: str):
    return "Результат работы!"
```

💡 **Идеи или баги?** Открывайте [Issue](https://github.com/NobidoNs/CustomAI/issues)!
