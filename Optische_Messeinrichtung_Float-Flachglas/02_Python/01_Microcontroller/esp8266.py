from machine import Pin, ADC, PWM
from time import sleep, time


# START BUTTON SETTINGS _______________________________________________________________________________________________

def handle_interrupt(pin):
    global button_pressed
    button_pressed = True


# Create button object for running the machine:
button = Pin(10, Pin.IN)
button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
button_pressed = False


# LED SETTINGS ________________________________________________________________________________________________________

# Create LED objects:
led_green = Pin(13, Pin.OUT)
led_red = Pin(15, Pin.OUT)

# ROT SENSOR SETTINGS _________________________________________________________________________________________________
rot_pin = Pin(16, Pin.IN)


# MOTOR CONTROL SETTINGS ______________________________________________________________________________________________

# Create the drives object for the direction of rotation of the DC motors
m11 = Pin(4, Pin.OUT)
m12 = Pin(0, Pin.OUT)
en1 = PWM(Pin(5, Pin.OUT))

m21 = Pin(2, Pin.OUT)
m22 = Pin(14, Pin.OUT)
en2 = PWM(Pin(12, Pin.OUT))

freq_value1 = 60
duty_value1 = 300

freq_value2 = 60
duty_value2 = 300

# MAIN PRODUCTION PROGRAM _____________________________________________________________________________________________
prod_time = 7200
ldr_measuring = True
ldr_measure_delay = 0.2
ldr_accuracy = 20

while True:

    # Start production:
    if button_pressed:

        sleep(0.5)
        button_pressed = False
        sleep(0.5)

        reset = False

        # Start engines:
        en1.init(freq=freq_value1, duty=duty_value1)
        m11.value(1)
        m12.value(0)

        en2.init(freq=freq_value2, duty=duty_value2)
        m21.value(1)
        m22.value(0)

        for _ in range(0, 5):
            led_green.on()
            sleep(0.1)
            led_green.off()
            sleep(0.1)

        # Set starting time:
        start = time()
        duration = 0

        # Green LED signal for running machine:
        led_green.on()

        # Set detected error count to zero:
        detected_errors = 0

        # Production in progress:
        while duration < prod_time:

            # Check current production time:
            if prod_time != 0:
                end = time()
                duration = end - start

            # Check emergency stop:
            if button_pressed:

                sleep(0.5)
                button_pressed = False
                sleep(0.5)

                emergency_stop = True

                # Stop engines and switch off green LED:
                m11.value(0)
                m12.value(0)

                m21.value(0)
                m22.value(0)

                led_green.off()

                # Blinking red LED signal for machine error:
                while emergency_stop is True:

                    led_red.on()
                    sleep(0.3)
                    led_red.off()
                    sleep(0.3)

                    # Check reset:
                    if button_pressed:

                        sleep(0.5)
                        button_pressed = False
                        sleep(0.5)

                        # Switch off red LED:
                        led_red.off()
                        sleep(0.5)

                        # Blinking green LED for reset:
                        led_green.on()
                        led_red.on()
                        sleep(3)

                        led_green.off()
                        led_red.off()

                        sleep(2)

                        reset = True
                        emergency_stop = False

                if reset is True:
                    reset = False
                    break


        # Stop engines after success, switch off green LED and switch on blue LED:
        m11.value(0)
        m12.value(0)

        m21.value(0)
        m22.value(0)

        led_green.off()


