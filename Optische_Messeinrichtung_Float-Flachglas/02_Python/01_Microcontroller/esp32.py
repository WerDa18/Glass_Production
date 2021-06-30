import json
import wifi
import ntptime
from umqtt.robust import MQTTClient
from machine import Pin, ADC, TouchPad
from time import sleep, time, localtime
from hcsr04 import HCSR04
from machine import SoftI2C
from ds3231 import DS3231


# ESP32

# START BUTTON SETTINGS _______________________________________________________________________________________________
button = TouchPad(Pin(12, Pin.IN))
button.config(200)


# RTC SETTINGS ________________________________________________________________________________________________________
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
ds = DS3231(i2c)


# LED SETTINGS ________________________________________________________________________________________________________
led_green = Pin(27, Pin.OUT)
led_blue = Pin(26, Pin.OUT)
led_red = Pin(25, Pin.OUT)


# ROT SENSOR SETTINGS _________________________________________________________________________________________________
rot_pin = Pin(19, Pin.IN)


# DISTANCE SENSOR SETTINGS ____________________________________________________________________________________________
sensor = HCSR04(trigger_pin=15, echo_pin=2)  # 5 = D1, 4=D2


# LDR SENSOR SETTINGS _________________________________________________________________________________________________
attenuation = ADC.ATTN_6DB
data_rate = ADC.WIDTH_9BIT

weiss_adc = ADC(Pin(39))
weiss_adc.atten(attenuation)  # 6dB attenuation, gives a maximum input voltage of approximately 2.00v
weiss_adc.width(data_rate)  # 9 bit data

grau_adc = ADC(Pin(36))
grau_adc.atten(attenuation)  # 6dB attenuation, gives a maximum input voltage of approximately 2.00v
grau_adc.width(data_rate)  # 9 bit data

lila_adc = ADC(Pin(35))
lila_adc.atten(attenuation)  # 6dB attenuation, gives a maximum input voltage of approximately 2.00v
lila_adc.width(data_rate)  # 9 bit data

blau_adc = ADC(Pin(34))
blau_adc.atten(attenuation)  # 6dB attenuation, gives a maximum input voltage of approximately 2.00v
blau_adc.width(data_rate)  # 9 bit data

gruen_adc = ADC(Pin(33))
gruen_adc.atten(attenuation)  # 6dB attenuation, gives a maximum input voltage of approximately 2.00v
gruen_adc.width(data_rate)  # 9 bit data

gelb_adc = ADC(Pin(32))
gelb_adc.atten(attenuation)  # 6dB attenuation, gives a maximum input voltage of approximately 2.00v
gelb_adc.width(data_rate)  # 9 bit data


# MAIN PRODUCTION PROGRAM _____________________________________________________________________________________________
msg = {'rotation_time': 0}


def set_rtc():
    ntptime.host = '1.europe.pool.ntp.org'

    ntptime.settime()
    ds.set_time(localtime()[0], localtime()[1], localtime()[2], localtime()[3], localtime()[4], localtime()[5],
                localtime()[6], localtime()[7])


def get_time():
    time_tuple = ds.get_time()

    hh = time_tuple[3] + 2
    mm = time_tuple[4]
    ss = time_tuple[5]

    time_stamp = '%0.2d' % hh + ':' + '%0.2d' % mm + ':' + '%0.2d' % ss

    return time_stamp


def get_date():
    time_tuple = ds.get_time()

    year = time_tuple[0]
    month = time_tuple[1]
    day = time_tuple[2]

    date_stamp = '%0.2d' % year + '-' + '%0.2d' % month + '-' + '%0.2d' % day

    return date_stamp


def measurement_program():
    led_blue.on()

    wifi.connect_wifi()

    MQTT_PORT = 8883

    # MQTT settings to David:
    CERT_FILE = "cert.der"
    KEY_FILE = "cert_private.der"
    MQTT_CLIENT_ID = "Name AWS Thing"
    MQTT_TOPIC = "personal-Topic"
    MQTT_HOST = "personal-arn"

    # MQTT settings to Jens:
    # CERT_FILE = "cert_jens\cert.der"
    # KEY_FILE = "cert_jens\private.der"
    # MQTT_CLIENT_ID = "my_d1_mini"
    # MQTT_TOPIC = "esp32"
    # MQTT_HOST = "a1zprslflzesje-ats.iot.eu-central-1.amazonaws.com"

    with open(KEY_FILE, "r") as f:
        key = f.read()

    with open(CERT_FILE, "r") as f:
        cert = f.read()

    mqtt_client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT, keepalive=5000, ssl=True,
                             ssl_params={"cert": cert, "key": key, "server_side": False})
    mqtt_client.connect()

    sleep(0.5)
    led_blue.off()

    set_rtc()

    while True:
        button_pressed = button.read()
        sleep(1)

        if button_pressed < 150:
            t0 = time()

            led_green.on()

            sleep(1)

            while (time()-t0) < 3600:
                button_pressed = button.read()
                t1 = time()

                msg['ldr_weiss'] = weiss_adc.read()
                msg['ldr_grau'] = grau_adc.read()
                msg['ldr_lila'] = lila_adc.read()
                msg['ldr_blau'] = blau_adc.read()
                msg['ldr_gruen'] = gruen_adc.read()
                msg['ldr_gelb'] = gelb_adc.read()
                msg['time'] = get_time()
                msg['date'] = get_date()

                msg['distance'] = -1
                while msg['distance'] < 20:
                    msg['distance'] = sensor.distance_mm() + 10

                    if msg['distance'] > 60:
                        sleep(0.1)
                        msg['distance'] = sensor.distance_mm() + 10

                while (time()-t1) < 1:
                    if rot_pin.value() == 0:
                        msg['rotation_time'] = time()

                msg_send = json.dumps(msg)
                mqtt_client.publish(MQTT_TOPIC, msg_send)

                led_red.on()
                sleep(0.5)
                led_red.off()

                if button_pressed < 150:
                    led_green.off()
                    led_red.on()
                    break

            sleep(1)
            led_green.off()
            led_red.off()


try:
    measurement_program()

except Exception as ex:
    for i in range(0, 10):
        led_green.off()
        led_red.on()
        sleep(0.2)
        led_red.off()
        sleep(0.2)

