Kostenoptimierung einer Flachglas Produktion
MVP zur Qualitätsoptimierung einer Flachglas Produktion im Float-Verfahren.
Bei der vorliegenden Arbeit handelt es sich um ein IoT-Projekt im Rahmen des Moduls „Industrielle Produktion & Industrie 4.0“ der FH-Aachen.
Die Resultate dieser Arbeit verdeutlichen den Einfluss einer Kombination von Microcontrollern und Sensoren im industriellen Produktionskontext. Sensoren stellen hierbei die Schnittstellen zur modernen Produktion im Sinne von Industrie 4.0 dar. Vom Microcontroller gesteuert, nehmen die Sensoren entsprechende Daten auf. Diese werden anschließend an AWS (Amazon Web Services) übermittelt und mit Hilfe eines (auf der Programmiersprache Python basierenden) Programms ausgelesen. 

Als Use-Case dient in diesem Projekt der fiktive Fall einer einjährigen Flachglas Produktion. Eine abschließende Analyse und Bewertung des Produktionsjahres hat eine Reklamationsquote von 40% ergeben. Die hohe Anzahl an Reklamationen lässt sich auf mangelhafte Qualität im Endprodukt zurückführen. 
Aufgrund des Fehlens einer optischen Online-Überwachung der Produktion hat eine Vielzahl von Kunden Flachglas mit groben Qualitätsmängeln wie Zinneinschlüssen, Steinchen, Blasen oder Walzenabdrücken erhalten.
Eine entsprechende Überwachungs- und Analyseeinheit ist nun gewünscht, um eine Reduktion der Fehler sicher zu stellen und ein Maß an Qualität im Endprodukt zu garantieren. 
Zur Verdeutlichung der Effektivität und des Einsparpotenzials einer optischen Fehlerdetektion-Einheit dient ein Modell. 

Im Modell sind folgende Komponenten verbaut:
Messtechnik
•	ESP8266 Microcontroller
•	LDR Fotowiderstandsmodule
•	LED Stripe (SMD RGB Modul)
•	5V Power Supply
•	Ultraschallsensor (HC-SR04)
•	Gabellichtschrankenmodul
•	Real Time Clock (DS3231 RTC)
•	Status LED (LED RGB Modul)
Antriebstechnik
•	ESP32 Microcontroller
•	12V DC Getriebemotoren
Sonstiges
•	Kassenbon Rolle
•	Verschiedene Modellelemente

Als fließendes Produkt dient im Modell die Kassenbon Rolle, welche materialbedingt unregelmäßig verteilte Faseranhäufungen aufweist. Die sich aufgrund der Anhäufungen ändernde Helligkeit des durchscheinenden LED-Lichts wird von den LDR-Sensoren erfasst. Je nach Helligkeitsabweichung, aufgrund der „Faser-Spot-Dichte“, können entsprechende Rückschlüsse auf die Fehlerklassen getroffen werden. 
Im Modell werden zur Produktionsüberwachung zwei weitere Sensoren verbaut, eine Gabellichtschranke zur Drehzahlmessung und ein Distanzsensor zur Material-Bestandsmessung. Mithilfe dieser Sensordaten kann die Bahngeschwindigkeit bestimmt und somit die Position erkannter Fehler im Produkt beurteilt werden.
Eine Controller-Konsole ermöglicht die Betriebssteuerung und Zustandsüberwachung des Modells. Hierbei werden Mess- und Antriebstechnik jeweils separat mittels Taster eingeschaltet. Ein Notaus kann ebenfalls separat initiiert werden.
Die gewonnen Erkenntnisse werden abschließend auf den fiktiven Fall übertragen.

![image](https://user-images.githubusercontent.com/86350904/123914111-554b3c00-d97f-11eb-80a0-b84c2b85a414.png)

Im Pinout sind alle Komponenten der Technik des Modells dargestellt:

![image](https://user-images.githubusercontent.com/86350904/123914145-5f6d3a80-d97f-11eb-9426-cb3f3fb3680d.png)

Im Zuge der Datenverarbeitung werden die Dienste IoT Core, IoT Analytics sowie Lambda der Amazon Web Services genutzt. 
Der Microcontroller sendet die Daten an IoT Core. Von dort verarbeitet ein Lambda Programm die Daten weiter und wertet diese aus. Sollte ein Glasbruch festgestellt werden, wird eine Benachrichtigung per Mail an den Anwender versendet. IoT Core sendet die aufgenommenen Datenpakete an IoT Analytics. Diese Datenpakete werden abschließend von einem lokalen Python Programm heruntergeladen, ausgewertet und in einem Graphical User Interface visualisiert. Folgende Darstellung veranschaulicht noch einmal diese Datenstruktur.

![image](https://user-images.githubusercontent.com/86350904/123914187-6b58fc80-d97f-11eb-90fd-60b09fd091f6.png)

Als Resultat der modellhaften Produktion lässt sich festhalten, dass die optische Detektion von (im Glas enthaltenen) Fehlern einen Mehrwert im Sinne der Beurteilung der Produktqualität liefert. In Abhängigkeit von verschiedenen Faktoren, u.a. Produktionsgeschwindigkeit, verwendete Sensoren und Leuchtmittel, können Fehler im Produkt erkannt und als Ausschuss bewertet werden, bevor es zum Kunden gelangt.
Übertragen auf den fiktiven Fall der einjährigen Produktion werden die gewonnen Daten an nachfolgende Arbeitssysteme weitergegeben und verarbeitet. Zu diesen Arbeitssystemen zählen u.a. die Längs-/Querschneider, der Schnittoptimierung und die Fehler-Markieranlage, sodass der anfallende Ausschuss entzogen und im Nachgang als Rohmaterial dem Produktionsprozess wieder zugeführt werden kann.

Grundsätzlich ist bei diesem Use-Case allerdings davon auszugehen, dass im realen industriellen Kontext hochauflösende Moiré-Kamera-Systeme im Bereich der Online-Fehlerdetektion zur Anwendung kommen. Aufgrund der enorm hohen Anschaffungskosten solcher Systeme steht in diesem Fall die verwendete LDR-Technik stellvertretend für die Erkennung von Fehlern mittels optischer Detektionssysteme.
Abschließend ist das fertige Modell dargestellt. Abweichungen zum oben aufgeführten 3D CAD Modell bestehen dadurch, dass Letzteres aus der Konzept Phase stammt. Es verdeutlicht lediglich das grundlegende Prinzip. Auf eine Anpassung geringfügiger Änderungen des realen Modells wurde daher verzichtet.

![image](https://user-images.githubusercontent.com/86350904/123914216-7449ce00-d97f-11eb-9269-8faba64fae41.png)

Dieses Repository ist als weiterer Anhang der Projektarbeit zu werten.
