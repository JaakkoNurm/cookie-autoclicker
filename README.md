# Cookie Clicker Bot

An automated bot for playing Cookie Clicker using Selenium WebDriver.

## Description

This project is a Python-based automation bot for the popular idle game [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/). The bot automatically clicks the cookie, purchases buildings, and acquires upgrades using an optimized strategy based on Return on Investment (ROI).

## Features

- Automatic cookie clicking
- Smart purchasing strategy based on ROI (Return on Investment)
- Prioritizes new building types and upgrades
- Tracks CPS (Cookies Per Second) contribution for each building type
- Handles game UI interactions using Selenium WebDriver

## Requirements

- Python 3.6+
- Selenium WebDriver
- Chrome WebDriver

## Installation

1. Clone this repository or download the script
2. Install required packages:

```bash
pip install selenium
```

3. Ensure you have Chrome WebDriver installed and in your PATH, or use a WebDriver manager like `webdriver-manager`

## Usage

Run the script with Python:

```bash
python cookie_clicker_bot.py
```

The bot will:
1. Open a Chrome browser window
2. Navigate to the Cookie Clicker website
3. Set up the game (click through initial prompts, select language)
4. Begin automatically playing the game

To stop the bot, press `Ctrl+C` in the terminal.

## How It Works

The bot uses the following strategy:

1. **Click the Cookie**: Rapidly clicks the big cookie to generate cookies
2. **Check for Upgrades**: Always prioritizes purchasing available upgrades
3. **Calculate ROI for Buildings**: 
   - For new building types, purchase immediately to unlock them
   - For existing buildings, calculate the Return on Investment (cookies generated per cookie spent)
   - Purchase the building with the highest ROI

## Customization

You can modify various aspects of the bot's behavior:

- Change the number of clicks per cycle by modifying the `clicks` parameter in the `click_cookie()` function call
- Adjust the purchasing strategy in the `best_purchase()` function
- Add additional game features like Golden Cookie clicking or achievements

## Known Issues

- The bot may occasionally encounter StaleElementReferenceExceptions due to the dynamic nature of the game
- Performance may vary depending on your system capabilities
- Some game features (like Golden Cookies, seasonal events) are not currently handled

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests with improvements.

## License

This project is available under the MIT License.

## Disclaimer

This bot is created for educational purposes and personal use. Using automated bots may be against the terms of service of some websites. Use responsibly.
