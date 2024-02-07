import machine
import time

# Define button pins
button1 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button3 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button4 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

def watchButtons():
    while True:
        # Check if button1 is pressed (button connected to pin 5)
        if button1.value() == 0:
            print("Button 1 is pressed")

        # Check if button2 is pressed (button connected to pin 4)
        if button2.value() == 0:
            print("Button 2 is pressed")

        # Check if button3 is pressed (button connected to pin 0)
        if button3.value() == 0:
            print("Button 3 is pressed")

        # Check if button4 is pressed (button connected to pin 2)
        if button4.value() == 0:
            print("Button 4 is pressed....Exiting")
            break

        # Add a small delay to avoid rapid button presses
        time.sleep_ms(300)

# Call the function to watch for button presses
watchButtons()
