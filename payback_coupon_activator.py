from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os


def element(by, value, parent, timeout=10):
    return WebDriverWait(parent, timeout).until(
        expected_conditions.presence_of_element_located((by, value))
    )


def main():
    if os.name == "nt":
        user_data_dir = (
            os.getenv("LOCALAPPDATA"),
            "Google",
            "Chrome",
            "User Data",
        )

    elif os.name == "posix":
        user_data_dir = (
            os.path.expanduser("~"),
            ".config",
            "google-chrome",
        )

    options = Options()
    options.add_argument("user-data-dir=" + os.path.join(user_data_dir))

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
