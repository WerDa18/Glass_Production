# Glas_Production
MVP zur Qualitätsüberwachung einer Float-Glass Produktion

Dies ist ein IoT-Projekt im Rahmen des Moduls Industrielle Produktion & Industrie 4.0, des Masterstudiengangs Industriell Engineering der FH-Aachen. 

Mithilfe des Projektes soll gezeigt werden, wie Microcontroller und somit Sensoren in der Produktion eingesetzt werden und eingesetzt werden können. Sie sind eine Schnittstelle zu einer modernen Produktion im Sinne von Industrie 4.0. Dabei werden Sensordaten mit Microcontrollern aufgenommen, an AWS (Amazon Web Services) übermittelt und anschließend mit einem Python Programm wieder ausgelesen. Für unser Projekt haben wir uns folgenden Use-Case überlegt: In der Glasproduktion kommt es immer wieder zu defekten oder zu Einschlüssen im produzierten Glass. Beides kann dazu führen, dass Glasscheiben reklamiert, oder Maschinen beschädigt werden. Um dies zu verhindern, haben wir eine Sensorstation entwickelt, die mithilfe von LDR-Sensoren, die die Fehler im Produkt erkennen kann. Durchgeführt haben wir das ganze an einem Modell.

![image](https://user-images.githubusercontent.com/86350904/123081064-d48bbd80-d41d-11eb-9158-e742a7139e92.png)

In dem Modell wurde das Glas mithilfe einer Papierrolle simuliert. Die Ungleichmäßigkeiten in der Papierrolle dienen dabei als Fehler. Ein Bruch des Glases lässt sich durch einen aufgemalten Strich darstellen. Damit nicht nur Sensordaten über die Fehler aufgenommen werden, wurde zusätzlich noch ein Ultraschallsensor verbaut, welcher den Materialstand überwacht und eine Gabellichtschranke eingesetzt, um die Materialgeschwindigkeit aufzunehmen. Um das Ganze in einen zeitlichen Kontext einzuordnen, wurde ein Real Time Clock Modul angeschlossen. Gleichzeitig ist eine Zustandskontrolle der Maschine über verbaute LEDs in der Controller-Konsole möglich. Ein kontinuierlicher Betrieb wird durch zwei verbaute Motoren gewährleistet, welche ebenfalls von einem Microcontroller gesteuert werden. In dem Modell werden zwei Kontroller verwendet. Zum einen ein ESP 8266. Dieser übernimmt die Antriebstechnik des Models. Zum anderen ein ESP32. Dieser zeichnet alle Werte der Sensoren auf und übermittelt sie an AWS.
Verwendete Sensoren:
- LDR Fotowiderstandsmodule
- LED Stripe (SMD RGB Modul)
- Ultraschallsensor (HC-SR04)
- Gabellichtschrankenmodul
- Real Time Clock (DS3231 RTC)
- Taster Modul
- Status LED (LED RGB Modul)

Im Folgenden ist das Pinout mit allen Komponenten dargestellt:

![image](https://user-images.githubusercontent.com/86350904/123093023-6948e800-d42b-11eb-96ed-19fc87ec4d1c.png)

Die Datenverarbeitung erfolgt über AWS. Dazu sendet der Microcontroller Daten an IoT Core. Vom IoT Core greift ein Lambda Programm die Daten ab und wertet sie aus. Ist ein Riss im Glas vorhanden, wird eine Benachrichtigung per Mail zu versenden. Vom IoT Core werden die Daten an IoT Analytics weitergeleitet, wo sie von einem Python Programm ausgelesen werden können. Die erhaltenen Daten werden dann in dem Python Programm ausgewertet und in einer GUI dargestellt. Das nachfolgende Bild veranschaulicht noch einmal diese Datenstruktur.

![image](https://user-images.githubusercontent.com/86350904/123080116-e456d200-d41c-11eb-905a-f34e19855eb6.png)

Als Ergenis lässt sich festhalten, dass das Ziel vollständig erfüllt wurde. Es ist aber davon auszugehen, dass in einem Industriellen Kontext die Fehler aufnahme deutlich komplexer zu gestalten ist. Da die LDR-Sensoren in ihrem Messbereich und ihrer Genauigkeit begrenzt sind.

Als letztes ist noch einmal das fertige Modell dargestellt. Die Abweichungen zwischen dem 3D Modell und dem realen Modell kommen daher, dass im 3D das ursprüngliche Konzept dargestellt wurde und im laufe des Projekt verschiedene Sachen angepasst werden mussten um einen Problemlosen lauf zu generieren. 

![IMAG6725](https://user-images.githubusercontent.com/86350904/123096349-4b7d8200-d42f-11eb-9cfc-a90703f6da2f.jpg)

Dieses Repository ist als weiterer Anhang der Projektarbeit zu werten. 
