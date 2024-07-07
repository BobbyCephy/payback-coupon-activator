from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os
import platform


def element(by, value, parent, timeout=10):
    return WebDriverWait(parent, timeout).until(
        expected_conditions.presence_of_element_located((by, value))
    )


def main():
    if platform.system() == "Windows":
        user_data_dir = "~\\AppData\\Local\\Google\\Chrome\\User Data"

    elif platform.system() == "Linux":
        user_data_dir = "~/.config/google-chrome"

    elif platform.system() == "Darwin":
        user_data_dir = "~/Library/Application Support/Google/Chrome"

    options = Options()
    options.add_argument("user-data-dir=" + os.path.expanduser(user_data_dir))

    service = Service()
    driver = Chrome(options, service)
    driver.get("https://www.payback.de/coupons")
    center = element(By.ID, "coupon-center", driver).shadow_root
    headline = element(
        By.CLASS_NAME, "coupon-center__header-published-headline", center
    )
    container = element(
        By.CLASS_NAME, "coupon-center__container-published-coupons", center
    )
    coupons = container.find_elements(By.TAG_NAME, "pbc-coupon")

    for index, coupon in enumerate(coupons):
        button = element(
            By.CSS_SELECTOR, "pbc-coupon-call-to-action", coupon.shadow_root
        )
        button.click()
        print("Coupon", index + 1, "/", len(coupons), "activated")

    driver.quit()


if __name__ == "__main__":
    main()
