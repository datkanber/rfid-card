from flask import Flask, redirect
import threading
import time
import hid
import pygame
from collections import deque

app = Flask(__name__)

VENDOR_ID = 0xffff
PRODUCT_ID = 0x0035
CONFIRM_SOUND_FILE = 'confirm.wav'
REJECT_SOUND_FILE = 'reject.wav'
AUTHORIZED_CARD = '00001e00'  # Only this card is authorized
DEBOUNCE_PERIOD = 3  # Minimum seconds between card reads

pygame.mixer.init()
confirm_sound = pygame.mixer.Sound(CONFIRM_SOUND_FILE)
reject_sound = pygame.mixer.Sound(REJECT_SOUND_FILE)

last_card_time = time.time() - DEBOUNCE_PERIOD
last_card_number = None  # Define this globally to fix the NameError

def play_sound(sound):
    sound.play()

def read_card():
    global last_card_time, last_card_number
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print("RFID Reader initialized")

    try:
        while True:
            data = device.read(64)
            if data:
                # Process only non-zero bytes and format as hexadecimal
                card_number = ''.join(format(x, '02x') for x in data if x != 0).lower()
                print("Card read:", card_number)
                
                if card_number and (time.time() - last_card_time) > DEBOUNCE_PERIOD:
                    last_card_time = time.time()
                    last_card_number = card_number  # Update the global variable here
                    
                    if card_number == AUTHORIZED_CARD:
                        print(f"Authorized Access: Card Number {card_number}")
                        play_sound(confirm_sound)
                    else:
                        print(f"Unauthorized Access: Card Number {card_number}")
                        play_sound(reject_sound)
            time.sleep(0.1)
    finally:
        device.close()

@app.route('/')
def home():
    if last_card_number == AUTHORIZED_CARD:
        return redirect("https://www.xxxx12354.com.tr/tr/", code=302)
    else:
        return "Unauthorized Access"

if __name__ == '__main__':
    thread = threading.Thread(target=read_card)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    thread.join()
