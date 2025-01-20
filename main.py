import os
import distro
import platform
import subprocess
import random
import time
import logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


previous_connection_status = None

def mark_value(value):
    # If the value is a dictionary, recursively mark its values
    if isinstance(value, dict):
        return {key: mark_value(val) for key, val in value.items()}
        
    # If the value is a list, recursively mark each item in the list
    elif isinstance(value, list):
        return [mark_value(item) for item in value]

    # If the value is a string, mask it by keeping the first 3 and last 3 digits, up to 3 stars in the middle
    elif isinstance(value, str):
        digits = value
        if len(digits) > 40:
            return (
                digits[:5]
                + "*" * 5
                + digits[int(0.5 * len(digits)) - 5 : int(0.5 * len(digits)) + 5]
                + "*" * 5
                + digits[-5:]
            )
        elif len(digits) > 20:
            return digits[:5] + "*" * 5 + digits[-5:]
        elif len(digits) > 6:
            return digits[:3] + "*" * 3 + digits[-3:]
        else:
            return value

    # If it's a number, return the number as-is (we can customize for number handling if needed)
    else:
        return value

def handle_banner(driver):
    close_buttons = driver.find_elements(By.XPATH, "//button[text()='Close']")
    # Check if any buttons were found
    if len(close_buttons) > 0:
        # Loop through each button and click it
        for button in close_buttons:
            button.click()
    show_loading_animation(random.randint(2, 4))
    i_got_it_buttons = driver.find_elements(By.XPATH, "//button[text()= 'I got it']")
    # Check if any buttons were found
    if len(i_got_it_buttons) > 0:
        # Loop through each button and click it
        for button in i_got_it_buttons:
            button.click()
    
# Setup logging configuration
def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


# Display CLI loading animation
def show_loading_animation(duration):
    for _ in range(duration):
        for frame in "|/-\\|/-\\|/-\\":
            print(f"\rLoading... {frame}", end="", flush=True)
            time.sleep(0.1)
    print("\r", end="")


# Check connection status
def check_connection_status(driver):
    global previous_connection_status
    if wait_for_element_exists(driver, By.XPATH, "//*[text()='Good']"):
        logging.info("Status: Connected!")
        previous_connection_status = "Connected"
    elif wait_for_element_exists(driver, By.XPATH, "//*[text()='Disconnected']"):
        logging.warning("Status: Disconnected!")
        previous_connection_status = "Disconnected"
    else:
        previous_connection_status = "Unknown"
        logging.warning("Status: Unknown!")


# Wait for an element to exist
def wait_for_element_exists(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False


# Wait for an element to be present
def wait_for_element(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException as e:
        logging.error(f"Error waiting for element {value}: {e}")
        raise


# Get ChromeDriver version
def get_chromedriver_version():
    try:
        result = subprocess.run(
            ["chromedriver", "--version"], capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Could not get ChromeDriver version: {e}")
        return "Unknown version"


# Get OS information
def get_os_info():
    try:
        os_info = {"System": platform.system(), "Version": platform.version()}
        if os_info["System"] == "Linux":
            os_info.update(
                {
                    "System": distro.name(pretty=True),
                    "Version": distro.version(pretty=True, best=True),
                }
            )
        return os_info
    except Exception as e:
        logging.error(f"Could not get OS information: {e}")
        return "Unknown OS"


# Main execution function
def main():
    setup_logging()

    version = os.getenv("VERSION")
    restart_delay = 60
    logging.info(f"Script version: {version}")
    try:
        os_info = get_os_info()
        logging.info(f"OS Info: {os_info}")

        # Read environment variables
        extension_id = os.getenv("EXTENSION_ID")
        web_url = os.getenv("WEB_URL")

        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        if not all([email, password]):
            logging.error(
                "Missing required environment variables. Please set EMAIL, PASSWORD."
            )
            return

        chrome_options = Options()
        chrome_options.add_extension(f"./{extension_id}.crx")
        chrome_options.add_argument("--no-sandbox")
        if not os.getenv("DISABLE_HEADLESS") == "True":
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        )

        # Initialize WebDriver
        chromedriver_version = get_chromedriver_version()
        logging.info(f"Using ChromeDriver: {chromedriver_version}")
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        logging.error(f"Restarting in {restart_delay} seconds...")
        show_loading_animation(restart_delay)
        main()
        return

    try:
        # logins
        driver.set_window_size(1024, driver.get_window_size()["height"])
        logging.info("Accessing gradient dashboard page...")
        driver.get(web_url)

        show_loading_animation(random.randint(1, 3))

        while not wait_for_element_exists(driver, By.XPATH, "//*[text()='Forgot Password']"):
            show_loading_animation(random.randint(1, 3))

        logging.info("Login...")

        logging.info("Entering credentials...")

        logging.info(f"Entering email: {mark_value(email)}")
        email_em = driver.find_element(
            By.XPATH, "//input[contains(@placeholder,'Enter Email')]"
        )

        email_em.send_keys(email)
        
        logging.info(f"Entering email: {mark_value(password)}")
        passworld_em = driver.find_element(
            By.XPATH, "//input[contains(@placeholder,'Enter Password')]"
        )
        passworld_em.send_keys(password)

        logging.info("Clicking the login button...")
        login_em = driver.find_element(By.XPATH, "//button[text()='Log In']")
        login_em.click()

        while not wait_for_element_exists(driver, By.XPATH, "//*[text()='Node Status']"):
            show_loading_animation(random.randint(1, 3))

        show_loading_animation(random.randint(1, 3))
        logging.info("Accessing extension page...")
        driver.get(f"chrome-extension://{extension_id}/popup.html")

        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

        while not wait_for_element_exists(
            driver, By.XPATH, "//*[text()='Status']"
        ):
            logging.info("Refreshing extension page...")
            show_loading_animation(random.randint(1, 3))
            driver.refresh()
        logging.info("Login Extension Success...")
        
        show_loading_animation(random.randint(3, 5))
        handle_banner(driver)
        # Get handles for all windows
        all_windows = driver.window_handles

        # Get the handle of the active window
        active_window = driver.current_window_handle

        # Close all windows except the active one
        for window in all_windows:
            if window != active_window:
                driver.switch_to.window(window)
                driver.close()

        # Switch back to the active window
        driver.switch_to.window(active_window)

        check_connection_status(driver)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(f"Restarting in {restart_delay} seconds...")
        driver.quit()
        show_loading_animation(restart_delay)
        main()

    while True:
        try:
            logging.info(f"Refresh in {60 if previous_connection_status in ["Disconnected", None] else 3600} seconds")
            time.sleep(60 if previous_connection_status in ["Disconnected", None] else 3600)
            driver.refresh()
            check_connection_status(driver)
        except KeyboardInterrupt:
            logging.info("Stopping the script...")
            driver.quit()
            break


main()
