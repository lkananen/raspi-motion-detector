# Camera image motion detector
Raspberry Pi and camera module based motion detector that send notifications of movement to Telegram.

## Table of Contents
- [Camera image motion detector](#camera-image-motion-detector)
  - [Table of Contents](#table-of-contents)
  - [Directory structure](#directory-structure)
    - [Overall picture](#overall-picture)
    - [Detailed list](#detailed-list)
  - [Architecture](#architecture)
  - [How to run](#how-to-run)
    - [Requirements](#requirements)
      - [Hardware requirements](#hardware-requirements)
      - [Software requirements](#software-requirements)
    - [Step by step instructions](#step-by-step-instructions)
    - [Testing](#testing)


## Directory structure
### Overall picture
```
 root
 ├── assets
 |    ├── Diagram.drawio
 |    └── Diagram.jpg
 ├── scripts
 |    ├── test_bot_manual.py
 |    ├── test_camera_manual.py
 |    └── test_img_diff.py
 ├── .gitignore
 ├── REAME.md
 ├── config.py
 ├── main.py
 └── requirements.txt
```

### Detailed list
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
Set up the hardware, gather required software, create telegram bot, obtain the bot token and your Telegram chat id.

### Requirements
#### Hardware requirements
- Raspberry Pi
- Raspberry Pi Camera module v2

The program has been tested to work with Raspberry Pi Camera module v2. Other support not guaranteed.

#### Software requirements
- Python
  - Packages in: `requirements.txt`
- Telegram account

### Step by step instructions
1. Clone the repository.
2. Install the requirements.
   1. `pip install -r requirements.txt`.
3. Use Telegram chat to create a bot.
   1. Find user: `@BotFather`.
   2. Run following commands and fill out your details on "<>" marked sections:
   ```
   /start
   /newbot
   <BotName>
   <BotUsername_bot>
   ```
   1. Get the HTTP API access token. Example token: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
   2. Save the token to `secrets.py` as `telegram_bot_token`.
      1. `telegram_bot_token="XXXXXX:XX-XXXX-XXXXX-XXXXX"`
   3. Find the bot by name and send some message to it.
   4. Go to see your bot's message history from the API. Example addess: `https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates`. Fill in your token to the address.
   5. Obtain the chat id of your user. Save it to `secrets.py` as `telegram_chat_id`.
      1. `telegram_chat_id="XXXXXXXXXX"`
   6. Documentation (in case something fails):  
   [Telegram bots](https://core.telegram.org/bots)
4. Setup the camera module for the Raspberry Pi.
   1. Documentation:  
   [Camera module setup](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
5. Run the program.
   1. `python main.py`

### Testing
- `test_bot_manual.py`
  - Telegram bot connection testing. Sends message to the given chat id.
- `test_camera_manual.py`
  - Camera module testing. Can be used to manually check that image capture and video recording works.
- `test_img_diff.py`
  - Image difference calculation logic test file.
