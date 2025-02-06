# RTX 5090 FE Stock Tracker

This project is a Python-based web scraper that monitors the availability of the NVIDIA GeForce RTX 5090 FE graphics card on the NVIDIA marketplace. It uses Selenium to periodically check the product page and sends email notifications when the product is in stock or if potential blocking is detected.

## Features

-   **Automated Stock Checking:** Monitors the NVIDIA marketplace for RTX 5090 FE availability.
-   **Email Notifications:** Sends email alerts when the product is in stock or if potential blocking is detected.
-   **Configurable:** Allows customization of email settings, product URL, CSS selector, check interval, and "out of stock" text via a `config.ini` file.
-   **Robust URL Handling:**  Handles URLs with special characters in `config.ini` without manual escaping.
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
        url = https://marketplace.nvidia.com/sv-se/consumer/graphics-cards/?locale=sv-se&page=1&limit=12&gpu=RTX%205090&gpu_filter=RTX%205090~1,RTX%205080~1  # The URL of the product page - URLs with special characters are supported directly
        selector = #resultsDiv > div > div:nth-child(2) > div:nth-child(2) > div.product_detail_78.nv-priceAndCTAContainer > div > div.clearfix.pdc-87.fe-pids > a > button  # The CSS selector for the availability button
        blocking_text = NVIDIA GeForce RTX 5090  # Text to check for potential blocking
        out_of_stock_text = finns ej i lager # The text indicating the product is out of stock - will be converted to lowercase in the script

        [SETTINGS]
        check_interval = 60  # The interval in seconds between checks
        ```

## Usage

1. **Run the script:**

    ```bash
    python rtx5090fe_tracker.py
    ```

    The script will start monitoring the product page and send email notifications based on the configured settings.

## Finding the CSS Selector

To configure the `selector` in `config.ini`, you need to identify the CSS selector of the button or element on the webpage that indicates product availability. You can easily find this using Chrome DevTools:

1.  **Open the Product Page in Chrome:** Navigate to the product page you want to monitor in your Google Chrome browser.
2.  **Open DevTools:** Right-click on the button or the text indicating availability (e.g., "Add to Cart," "Out of Stock") and select "Inspect" or "Inspect Element." This will open the Chrome DevTools panel.
3.  **Identify the Element:** The "Elements" panel in DevTools will highlight the HTML code of the element you right-clicked on.
4.  **Copy the Selector:** Right-click on the highlighted HTML code in the "Elements" panel.
5.  **Select "Copy" -> "Copy Selector":**  This will copy the CSS selector of the element to your clipboard.
6.  **Paste into `config.ini`:** Paste the copied CSS selector into the `selector` field in your `config.ini` file.

**Example:**

If you want to find the selector for a button that says "Buy Now":

1.  Right-click on the "Buy Now" button on the webpage.
2.  Select "Inspect."
3.  In the DevTools "Elements" panel, right-click on the highlighted `<button>` tag.
4.  Select "Copy" -> "Copy Selector."
5.  Paste the copied selector into your `config.ini` file as the value for the `selector` variable.

The CSS selector will look something like `#product-actions > button` or `div.add-to-cart-button > button.primary`.  The exact selector will vary depending on the website's structure.

![Chrome DevTools - Copy Selector](https://i.imgur.com/ODMtq9f.png)
_*Example of using Chrome DevTools to copy a CSS selector.*_

## Troubleshooting

-   **Chrome Crashes:** The script is designed to automatically restart after a Chrome crash. However, if you encounter frequent crashes, consider updating Chrome to the latest version or adjusting the `check_interval` in `config.ini` to a higher value.
-   **Blocking:** If the script detects potential blocking, it will send an email notification. You may need to manually check the product page and update the `blocking_text` in `config.ini` if necessary.
-   **Email Issues:** Ensure that your Gmail address and app password are correct in `config.ini`. Also, check your spam folder if you are not receiving notifications.

## Testing the Email Functionality

To ensure that the email notification system is working correctly, you can perform a simple test:

1. **Modify `config.ini`:**
    -   Open the `config.ini` file in a text editor.
    -   Change the `blocking_text` under the `[PRODUCT]` section to a random string that you are certain does not exist on the webpage. For example:

        ```ini
        blocking_text = asdfghjklqwertyuiop
        ```

2. **Run the script:**

    ```bash
    python rtx5090fe_tracker.py
    ```

3. **Check for email:**
    -   The script should now send an email to the address specified in `config.ini` with the subject "Possible Blocking Detected."
    -   Check your inbox (and spam folder) for the email.

4. **Revert `config.ini`:**
    -   **Important:** After testing, change the `blocking_text` back to its original value:

        ```ini
        blocking_text = NVIDIA GeForce RTX 5090
        ```

This test helps verify that the script can successfully send emails and that your email settings are configured correctly.

## Notes

-   The script has been running for five days without detecting blocking in the provided test case. However, websites may change their structure or implement anti-bot measures, which could affect the script's functionality.
-   Regularly check the `product_checker.log` file for any errors or warnings.

## Disclaimer

This project is for educational and informational purposes only. The author is not responsible for any misuse or consequences resulting from the use of this script. Use at your own risk.
