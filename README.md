# Camera image motion detector
Raspberry Pi and camera module based motion detector.

## Table of Contents
- [Camera image motion detector](#camera-image-motion-detector)
  - [Table of Contents](#table-of-contents)
  - [Directory structure](#directory-structure)
  - [Architecture](#architecture)
  - [How to run](#how-to-run)
    - [Requirements](#requirements)
    - [Step by step instructions](#step-by-step-instructions)


## Directory structure
- `assets` Readme related web site assets.
- `scripts` Smaller parts of the application used to test out things.
- `config.py` Configurations for the application.
- `main.py` The overall application can be started by running this file.
- `secrets.py` Secret configurations left out of the version control like tokens etc.
- `requirements.txt` The required Python packages neede to run this program.


## Architecture
The program constantly captures images on certain intervals. Upon detecting motion between the images, a notification gets sent through Telegram API to a certain user to notify about the detection.

<p align="center">
    <img src="./assets/Diagram.jpg">
    <!-- ![Diagram](./assets/Diagram.jpg) -->
</p>

## How to run

### Requirements
TODO: detailed list coming soon

### Step by step instructions
1. Clone the repository.
2. Install the requirements with pip.
   1. Can be done by running: `pip install -r requirements.txt`.
3. Use Telegram chat to create a bot.
   1. Find user: `@BotFather`.
   2. Run following commands and fill out your details on "<>" marked sections:
   ```
   /start
   /newbot
   <BotName>
   <BotUsername_bot>
   ```
   3. Get the HTTP API access token. Example token: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
   4. Save the token to `secrets.py` as `telegram_bot_token`.
   5. Find the bot by name and send some message to it.
   6. Go to see your bot's message history from the API. Example addess: `https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates`. Fill in your token.
   7. Obtain the chat id of your user. Save it to `secrets.py` as `telegram_chat_id`.
   8. Further documentation: [Telegram bots](https://core.telegram.org/bots)
4. Setup the camera module for the Raspberry Pi.
   1. TODO: more instructions related to this coming soon.
5. Run `python main.py`.
