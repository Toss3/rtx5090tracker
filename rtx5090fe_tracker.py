import configparser
import logging
import smtplib
import time
from email.mime.text import MIMEText
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("product_checker.log"),
        logging.StreamHandler(),
    ],
)
logger: logging.Logger = logging.getLogger(__name__)

class Config:
    """Manages configuration settings from an INI file."""

    def __init__(self, config_file: str = "config.ini") -> None:
        """Initializes the Config class.

        Args:
            config_file (str): The path to the configuration file.
        """
        self.config_file: str = config_file
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.config.read(self.config_file)

    @property
    def email_user(self) -> str:
        """Gets the email username from the configuration.

        Returns:
            str: The email username.
        """
        return self.config["EMAIL"]["user"]

    @property
    def email_pass(self) -> str:
        """Gets the email password from the configuration.

        Returns:
            str: The email password.
        """
        return self.config["EMAIL"]["password"]

    @property
    def email_to(self) -> str:
        """Gets the recipient email address from the configuration.

        Returns:
            str: The recipient email address.
        """
        return self.config["EMAIL"]["to"]

    @property
    def url(self) -> str:
        """Gets the URL to track from the configuration.

        Returns:
            str: The URL to track.
        """
        return self.config["PRODUCT"]["url"]

    @property
    def selector(self) -> str:
        """Gets the CSS selector for the button from the configuration.

        Returns:
            str: The CSS selector for the button.
        """
        return self.config["PRODUCT"]["selector"]

    @property
    def check_interval(self) -> int:
        """Gets the check interval in seconds from the configuration.

        Returns:
            int: The check interval in seconds.
        """
        return int(self.config["SETTINGS"]["check_interval"])

    @property
    def blocking_text(self) -> str:
        """Gets the text to check for blocking from the configuration.

        Returns:
            str: The text to check for blocking.
        """
        return self.config["PRODUCT"]["blocking_text"]

class WebPage:
    """Handles webpage rendering and element interaction using Selenium."""

    def __init__(self) -> None:
        """Initializes the WebPage class."""
        options: Options = Options()
        # Remove since we are not in headless mode
        options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        )
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")  # For Docker environments
        # options.add_argument("--disable-dev-shm-usage")  # For Docker environments
        self.driver: webdriver.Chrome = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.wait: WebDriverWait = WebDriverWait(self.driver, 10)

    def load_page(self, url: str) -> None:
        """Loads the specified URL in the browser.

        Args:
            url (str): The URL to load.
        """
        # Debugging
        logger.info(f"Loading page: {url}")
        try:
            self.driver.get(url)
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
        except Exception as e:
            # Debugging
            logger.error(f"Error loading page: {e}")
            raise

    def get_element_text(self, selector: str) -> Optional[str]:
        """Gets the text content of the element specified by the CSS selector.

        Args:
            selector (str): The CSS selector of the element.

        Returns:
            Optional[str]: The text content of the element, or None if the element is not found.
        """
        try:
            element: Optional[
                webdriver.remote.webelement.WebElement
            ] = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element.text.lower()
        except NoSuchElementException:
            # Debugging
            logger.error(f"Element not found: {selector}")
            return None
        except Exception as e:
            # Debugging
            logger.error(f"Error getting element text: {e}")
            return None

    def is_text_present(self, text: str) -> bool:
        """Checks if the specified text is present on the page.

        Args:
            text (str): The text to search for.

        Returns:
            bool: True if the text is present, False otherwise.
        """
        try:
            return text.lower() in self.driver.page_source.lower()
        except Exception as e:
            # Debugging
            logger.error(f"Error checking for text: {e}")
            return False

    def close(self) -> None:
        """Closes the browser."""
        # Debugging
        logger.info("Closing browser.")
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logger.exception(f"Error while closing browser: {e}")

class EmailNotifier:
    """Handles sending email notifications."""

    def __init__(self, user: str, password: str) -> None:
        """Initializes the EmailNotifier class.

        Args:
            user (str): The email username.
            password (str): The email password.
        """
        self.user: str = user
        self.password: str = password
        self.server: Optional[smtplib.SMTP_SSL] = None

    def connect(self) -> None:
        """Connects to the SMTP server."""
        # Debugging
        logger.info("Connecting to SMTP server.")
        try:
            self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            self.server.login(self.user, self.password)
        except Exception as e:
            # Debugging
            logger.error(f"Error connecting to SMTP server: {e}")
            raise

    def send_email(self, to: str, subject: str, body: str) -> None:
        """Sends an email.

        Args:
            to (str): The recipient email address.
            subject (str): The email subject.
            body (str): The email body.
        """
        if self.server is None:
            raise Exception("SMTP server not connected.")

        msg: MIMEText = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to
        # Debugging
        logger.info(f"Sending email to {to} with subject: {subject}")
        try:
            self.server.sendmail(self.user, to, msg.as_string())
        except Exception as e:
            # Debugging
            logger.error(f"Error sending email: {e}")
            raise

    def disconnect(self) -> None:
        """Disconnects from the SMTP server."""
        # Debugging
        logger.info("Disconnecting from SMTP server.")
        if self.server:
            self.server.quit()

class ProductChecker:
    """Orchestrates the product checking process."""

    def __init__(self, config: Config) -> None:
        """Initializes the ProductChecker class.

        Args:
            config (Config): The configuration object.
        """
        self.config: Config = config
        self.email_notifier: EmailNotifier = EmailNotifier(
            self.config.email_user, self.config.email_pass
        )

    def check_product(self) -> None:
        """Checks if the product is in stock and sends an email if necessary."""
        self.web_page: WebPage = WebPage()
        try:
            self.web_page.load_page(self.config.url)

            if not self.web_page.is_text_present(self.config.blocking_text):
                # Debugging
                logger.warning("Possible blocking detected.")
                self.email_notifier.connect()
                self.email_notifier.send_email(
                    self.config.email_to,
                    "Possible Blocking Detected",
                    f"The script might be blocked. Check the page: {self.config.url}",
                )
                self.email_notifier.disconnect()
                return

            button_text: Optional[str] = self.web_page.get_element_text(
                self.config.selector
            )

            # Log the button text
            if button_text:
                logger.info(f"Button text: {button_text}")
            else:
                logger.info("Button not found.")

            if button_text and button_text != "finns ej i lager":
                # Debugging
                logger.info("Product is in stock!")
                self.email_notifier.connect()
                self.email_notifier.send_email(
                    self.config.email_to,
                    "Product In Stock",
                    f"The product is in stock! Check it out: {self.config.url}",
                )
                self.email_notifier.disconnect()
        except Exception as e:
            # Debugging
            logger.exception(f"An error occurred: {e}")
            try:
                self.email_notifier.connect()
                self.email_notifier.send_email(
                    self.config.email_to,
                    "Error in Product Checker",
                    f"An error occurred while checking the product: {e}",
                )
                self.email_notifier.disconnect()
            except Exception as email_error:
                logger.error(f"Failed to send error email: {email_error}")
        finally:
            self.web_page.close()

    def run(self) -> None:
        """Runs the product checker in a loop."""
        # Debugging
        logger.info("Starting product checker.")
        while True:
            self.check_product()
            # Debugging
            logger.info(
                f"Waiting for {self.config.check_interval} seconds before next check."
            )
            time.sleep(self.config.check_interval)

if __name__ == "__main__":
    config: Config = Config()
    checker: ProductChecker = ProductChecker(config)
    checker.run()