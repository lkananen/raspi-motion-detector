# Camera image motion detector
Raspberry Pi and camera module based motion detector that send notifications of movement to Telegram.

## Table of Contents
- [Camera image motion detector](#camera-image-motion-detector)
  - [Table of Contents](#table-of-contents)
  - [Directory structure](#directory-structure)
    - [Overall picture](#overall-picture)
    - [Detailed list](#detailed-list)
  - [Architecture](#architecture)
  - [Requirements](#requirements)
    - [Hardware requirements](#hardware-requirements)
    - [Software requirements](#software-requirements)
  - [How to run (development)](#how-to-run-development)
    - [Step by step instructions](#step-by-step-instructions)
    - [Testing](#testing)
  - [How to run (production)](#how-to-run-production)
    - [Step by step instructions](#step-by-step-instructions-1)


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

## Requirements
### Hardware requirements
- Raspberry Pi
- Raspberry Pi Camera module v2

The program has been tested to work with Raspberry Pi Camera module v2. Other support not guaranteed.

### Software requirements
- Python
  - Packages in: `requirements.txt`
- Telegram
  - An account
  - A bot user

## How to run (development)
Set up the hardware, gather required software, create telegram bot, obtain the bot token and your Telegram chat id.

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
   3. Get the HTTP API access token.
      1. Example: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
   4. Save the token to `secrets.py` as `telegram_bot_token`.
      1. `telegram_bot_token="XXXXXX:XX-XXXX-XXXXX-XXXXX"`
   5. Message your bot.
      1. Find the bot by name.
      2. Send some message to it.
   6. Check bot's message history for your chat id.
      1. Go to see your bot's message history from the API.
      2. Fill in your token to the address.
      3. Example: `https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates`.
   7. Obtain the chat id of your user as a secret.
      1. Save the ID to `secrets.py` as `telegram_chat_id`.
      2. Example: `telegram_chat_id="XXXXXXXXXX"`
   8. Documentation (in case something fails):  
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

## How to run (production)
Once the development is working the program can be changed to run on startup.

### Step by step instructions
1. Create `MotionDetector.desktop` file to `/home/pi/.config/autostart/`.
   1. `cd /home/pi/.config/autostart/`
   2. `touch MotionDetector.desktop`
2. Write the following content to that file:
```
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=MotionDetector
Comment=This runs the motion detector on startup.
Exec=  python /home/pi/raspi-motion-detector/main.py
StartupNotify=false
Terminal=true
Hidden=false
```
3. Reboot.