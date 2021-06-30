import json
import boto3

print('Loading function')

reference1 = {"ldr_gelb": "0", "ldr_gruen": "0", "ldr_grau": "0", "ldr_blau": "0", "ldr_weiss": "0", "ldr_lila": "0"}
reference2 = {"ldr_gelb": "250", "ldr_gruen": "250", "ldr_grau": "250", "ldr_blau": "250", "ldr_weiss": "250",
              "ldr_lila": "250"}
r1 = ["ldr_weiss", "ldr_grau", "ldr_lila", "ldr_blau"]
r2 = ["ldr_grau", "ldr_lila", "ldr_blau", "ldr_gruen"]
r3 = ["ldr_lila", "ldr_blau", "ldr_gruen", "ldr_gelb"]
r4 = ["ldr_weiss", "ldr_grau", "ldr_lila", "ldr_blau", "ldr_gruen", ]
r5 = ["ldr_grau", "ldr_lila", "ldr_blau", "ldr_gruen", "ldr_gelb"]
r6 = ["ldr_weiss", "ldr_grau", "ldr_lila", "ldr_blau", "ldr_gruen", "ldr_gelb"]
combi = [r1, r2, r3, r4, r5, r6]


def lambda_handler(event, context):
    print("Event loading")
    print(event)     #Check ob Daten angekommen
    if test_for_SNS(event) == True:
        print("try SNS")
        SNS_massage()
        print("send message")
    print("Values checked")
    return


def test_for_SNS(event):
    check = []
    test = False
    delet_values = ["rotation_time", "distance", "date", "time"]  # zu Löschende Werte für den SNS
    [event.pop(value) for value in delet_values]

    for c, v in event.items():  # Iterrieren über eingegange Daten
        if int(v) > int(reference1[c]) and int(v) < int(reference2[c]):  # prüfen ob erhaltenen Daten relevant
            check.append(c)

    check.sort()  # List für späterne vergleich Alphabetisch sortieren
    print(check)  #

    if len(check) >= 4:  # Prüfen ob die Anzahl an Fehlern groß genug ist
        for r in combi:  # mögliche Kombinationen abgleichen
            r.sort()
            if r == check:
                test = True  # Wenn kombination ein Bruch sein kann, schlägt der Test an

    return test


def SNS_massage():
    # Erstellen eines SNS clinets für die Nachricht
    sns = boto3.client('sns')

    # Ausgegebene Nachricht der Daten
    message_text = 'ATTENTION - Glassbruch Erkennung nach Dickenmessung'

    # Publizierten der Nachricht
    response = sns.publish(
        TopicArn='personal arn:...',  # event['notify_topic_arn'],
        Message=message_text
    )

    return response

