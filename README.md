# Wildberries Review Parser

## 📌 Описание
Wildberries Review Parser — это инструмент для автоматизированного сбора отзывов о товарах с маркетплейса [Wildberries](https://www.wildberries.ru). 
Парсер загружает страницы товаров, извлекает отзывы и сохраняет их в удобный формат Excel.

## 🚀 Установка
1. **Клонируйте репозиторий:**
   ```bash
   git clone git@github.com:progmat64/wildberries_parser_review.git
   ```
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

## 📌 Использование

1. Запустите скрипт `main.py`:
   ```bash
   python main.py
   ```
2. Введите артикулы товаров через запятую (например, `123456, 789012`).
3. После завершения работы результат будет сохранён в папке `results/` в файле `wb_reviews_<product_ids>_<timestamp>.xlsx`.

⚠ **Важно:** для работы парсера требуется установленный Google Chrome.  
⏳ **Обратите внимание** загрузка отзывов может занять некоторое время (несколько минут), так как сайт Wildberries загружает данные постепенно.

## 🛠 Стек
- **Python 3.8+**
- **Selenium**
- **BeautifulSoup4**
- **Pandas**

## 👨‍💻 Автор
Разработчик: **Александр Матвеев**  
Telegram: @alematv
