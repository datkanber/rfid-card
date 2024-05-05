import hid
import time
import pygame

# Constants
VENDOR_ID = 0xffff
PRODUCT_ID = 0x0035
CONFIRM_SOUND_FILE = 'confirm.wav'
REJECT_SOUND_FILE = 'reject.wav'
AUTHORIZED_CARD = '00001e00'  # Bu kart numarası onaylanacak
DEBOUNCE_TIME = 3  # seconds

def init_sound_system():
    pygame.mixer.init()
    sounds = {
        'confirm': pygame.mixer.Sound(CONFIRM_SOUND_FILE),
        'reject': pygame.mixer.Sound(REJECT_SOUND_FILE)
    }
    return sounds

def play_sound(sounds, sound_key):
    sounds[sound_key].play()

def main():
    sounds = init_sound_system()
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
                card_number = ''.join(format(x, '02x') for x in data[:4]).lower()

                if card_number != '00000000' and card_number != last_card_number:  # Check for non-zero and change of card
                    current_time = time.time()

                    if (current_time - last_detection_time) > DEBOUNCE_TIME:
                        if card_number == AUTHORIZED_CARD:
                            print(f"Authorized User detected: Card Number {card_number}")
                            play_sound(sounds, 'confirm')
                        else:
                            print(f"Unauthorized Access: Card Number {card_number}")
                            play_sound(sounds, 'reject')

                        last_detection_time = current_time
                        last_card_number = card_number
                    else:
                        print(f"Card detected but still in debounce period: {card_number}")

            time.sleep(0.1)  # Delay to prevent too frequent polling

    except KeyboardInterrupt:
        print("Interrupted by user, closing device.")
    finally:
        device.close()
        pygame.mixer.quit()

if __name__ == '__main__':
    main()
