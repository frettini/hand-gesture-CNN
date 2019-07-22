from pynput import keyboard
from threading import Thread
import time

from modules import connectpi


def execute():
    print('Do something')

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}
]

# The currently active modifiers
current = set()

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


def keyboard_thread():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def main():
    count = 0
    print('accessing the main function')
    while True:
        count += 1 
        print(count)
        time.sleep(1)
        if count == 100:
            break



def socket_thread():
    connectpi.connectToPi()
    connectpi.sendMessage('customEvent', {'data':'Greetings server!'}, '/socket')
    connectpi.sio.wait()


if __name__ == '__main__': 
    thread = Thread(target=keyboard_thread)
    thread.daemon = True
    thread.start()
    main()
    
