# RTX 5090 FE Stock Tracker

This project is a Python-based web scraper that monitors the availability of the NVIDIA GeForce RTX 5090 FE graphics card on the NVIDIA marketplace. It uses Selenium to periodically check the product page and sends email notifications when the product is in stock or if potential blocking is detected.

## Features

-   **Automated Stock Checking:** Monitors the NVIDIA marketplace for RTX 5090 FE availability.
-   **Email Notifications:** Sends email alerts when the product is in stock or if potential blocking is detected.
-   **Configurable:** Allows customization of email settings, product URL, CSS selector, and check interval via a `config.ini` file.
-   **Logging:** Logs events and errors to `product_checker.log` for debugging and monitoring.

## Prerequisites

-   Python 3.7 or higher
-   Google Chrome browser
-   A Gmail account for sending email notifications

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv .venv
    ```

3. **Activate the virtual environment:**

    -   On Windows:

        ```bash
        .venv\Scripts\activate
        ```

    -   On macOS/Linux:

        ```bash
        source .venv/bin/activate
        ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a Gmail App Password:**

    -   Go to your Google Account settings.
    -   Navigate to "Security" and then "2-Step Verification."
    -   At the bottom of the page, select "App passwords."
    -   Choose "Mail" as the app and "Other (Custom name)" as the device.
    -   Give it a name (e.g., "RTX 5090 Tracker") and click "Generate."
    -   Copy the generated 16-character app password.

2. **Configure `config.ini`:**

    -   Open the `config.ini` file in a text editor.
    -   Update the following fields:

        ```ini
        [EMAIL]
        user = YOUR_GMAIL_ADDRESS  # Your Gmail address
        password = YOUR_APP_PASSWORD  # The 16-character app password you generated
        to = RECIPIENT_EMAIL_ADDRESS  # The email address to receive notifications

        [PRODUCT]
        url = https://marketplace.nvidia.com/sv-se/consumer/graphics-cards/  # The URL of the product page
        selector = #resultsDiv > div > div:nth-child(2) > div:nth-child(2) > div.product_detail_78.nv-priceAndCTAContainer > div > div.clearfix.pdc-87.fe-pids > a > button  # The CSS selector for the availability button
        blocking_text = NVIDIA GeForce RTX 5090  # Text to check for potential blocking

        [SETTINGS]
        check_interval = 60  # The interval in seconds between checks
        ```

## Usage

1. **Run the script:**

    ```bash
    python rtx5090fe_tracker.py
    ```

    The script will start monitoring the product page and send email notifications based on the configured settings.

## Troubleshooting

-   **Chrome Crashes:** The script is designed to automatically restart after a Chrome crash. However, if you encounter frequent crashes, consider updating Chrome to the latest version or adjusting the `check_interval` in `config.ini` to a higher value.
-   **Blocking:** If the script detects potential blocking, it will send an email notification. You may need to manually check the product page and update the `blocking_text` in `config.ini` if necessary.
-   **Email Issues:** Ensure that your Gmail address and app password are correct in `config.ini`. Also, check your spam folder if you are not receiving notifications.

## Notes

-   The script has been running for five days without detecting blocking in the provided test case. However, websites may change their structure or implement anti-bot measures, which could affect the script's functionality.
-   Regularly check the `product_checker.log` file for any errors or warnings.

## Disclaimer

This project is for educational and informational purposes only. The author is not responsible for any misuse or consequences resulting from the use of this script. Use at your own risk.