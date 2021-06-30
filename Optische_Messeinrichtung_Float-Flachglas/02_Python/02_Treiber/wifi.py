import network
import ntptime


def disconnect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)


def connect_wifi():
    wifi_passwds = {}

    # wifi_passwds.txt insert "WIFI-Name":"Password"
    with open("cert\wifi_passwds.txt") as f:
        for line in f.readlines():
            wifi_id, passwd = line.strip().split(":")
            wifi_passwds[wifi_id] = passwd

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        visible_wifis = [w[0].decode("utf-8") for w in wlan.scan()]
        known_wifis = list(filter(lambda w: w in wifi_passwds.keys(), visible_wifis))

        if len(known_wifis) > 0:
            wifi = known_wifis[0]
            print('connecting to network', wifi)
            wlan.connect(wifi, wifi_passwds[wifi])
            while not wlan.isconnected():
                pass

            print("connected:", wlan.ifconfig())
        else:
            print('No known network available.')


def synchronize_rtc():
    # set the rtc datetime from the remote server
    ntptime.settime()
