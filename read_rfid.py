import hid
import time
import pygame

# Constants
VENDOR_ID = 0xffff
PRODUCT_ID = 0x0035
CONFIRM_SOUND_FILE = 'confirm.wav'
USER_CARDS = {
    '00001e': 'Burak Kanber',  # Adjust these to actual expected hex values from reader
    '000021': 'Anonymous User'
}
DEBOUNCE_TIME = 3  # seconds

def init_sound_system():
    pygame.mixer.init()
    return pygame.mixer.Sound(CONFIRM_SOUND_FILE)

def play_confirmation_sound(sound):
    sound.play()

def get_user_from_card(card_number):
    return USER_CARDS.get(card_number, 'Unknown User')  # Ensure case-insensitive matching

def main():
    sound = init_sound_system()
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)

    print("Device initialized successfully")
    print("Manufacturer:", device.get_manufacturer_string())
    print("Product:", device.get_product_string())
    print("Serial No:", device.get_serial_number_string())

    last_detection_time = 0
    last_card_number = None

    try:
        while True:
            data = device.read(64)
            if data:
                # Parse bytes to hex string, assuming relevant data starts from byte 0
                card_number = ''.join(format(x, '02x') for x in data[:3]).lower()
                
                if card_number != '000000':  # Often RFID readers pad zeroes when no card is present
                    current_time = time.time()

                    if card_number != last_card_number:
                        if (current_time - last_detection_time) > DEBOUNCE_TIME:
                            user_name = get_user_from_card(card_number)
                            print(f"{user_name} detected: Card Number {card_number}")
                            play_confirmation_sound(sound)
                            last_detection_time = current_time
                            last_card_number = card_number
                        else:
                            print(f"Card detected but still in debounce period: {card_number}")
                    else:
                        print(f"Same card detected, ignoring: {card_number}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted by user, closing device.")
    finally:
        device.close()
        pygame.mixer.quit()

if __name__ == '__main__':
    main()
