import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_reviews_selenium(product_id):
    url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-direct-composition")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cookies__btn")))
            cookie_btn.click()
        except Exception:
            pass

        try:
            reviews_tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'comments__btn-all')]"))
            )
            driver.execute_script("arguments[0].click();", reviews_tab)
        except Exception:
            return []

        time.sleep(3)

        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(6):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")
        reviews_container = soup.find("ul", class_="comments__list")
        if not reviews_container:
            return []

        reviews = []
        for review in reviews_container.select("li.comments__item"):
            reviewer = review.find("p", class_="feedback__header")
            reviewer = reviewer.get_text(strip=True) if reviewer else "Аноним"

            rating_element = review.find("span", class_="feedback__rating")
            rating = 0
            if rating_element and "stars-line" in rating_element.get("class", []):
                for cls in rating_element.get("class", []):
                    if cls.startswith("star") and cls[4:].isdigit():
                        rating = int(cls[4:])
                        break

            advantages, disadvantages, comment = "", "", ""
            text_block = review.find("p", class_="feedback__text")
            if text_block:
                for span in text_block.find_all("span", class_="feedback__text--item"):
                    bold_text = span.find("span", class_="feedback__text--item-bold")
                    if bold_text:
                        label = bold_text.get_text(strip=True)
                        content = span.get_text(strip=True).replace(label, "").strip()
                        if "Достоинства" in label:
                            advantages = content
                        elif "Недостатки" in label:
                            disadvantages = content
                        elif "Комментарий" in label:
                            comment = content
                    else:
                        comment = span.get_text(strip=True)

            reviews.append(
                {
                    "reviewer": reviewer,
                    "rating": rating,
                    "advantages": advantages,
                    "disadvantages": disadvantages,
                    "comment": comment,
                }
            )

        return reviews

    finally:
        driver.quit()


if __name__ == "__main__":
    product_id = "155404700"
    reviews = get_reviews_selenium(product_id)

    if reviews:
        for i, review in enumerate(reviews, 1):
            print(f"Отзыв #{i}:")
            print(f"Автор: {review['reviewer']}")
            print(f"Оценка: {review['rating']}/5")
            print(f"Достоинства: {review['advantages']}")
            print(f"Недостатки: {review['disadvantages']}")
            print(f"Комментарий: {review['comment']}")
            print("-" * 50)
    else:
        print("Отзывы не найдены.")
