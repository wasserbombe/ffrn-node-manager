# -*- coding: utf-8 -*-
from flask_mail import Message

def getMail(node):
    msg = Message("Hello", sender=("FFRN Node Registration", "noreply@freifunk-rhein-neckar.de"), recipients = [node['email']])
    msg.body = '''
Hey {nickname},
cool, du hast gerade einen neuen Knoten für das Netz von Freifunk Rhein Neckar registriert.
Die Daten deines Knotens lauten:
Hostname: {hostname}
MAC: {mac}
VPN Key: {key}
Koordinaten: {coords}
Nick: {nickname}
Mail: {email}
Token: {token}

Wir hoffen das du gut zurecht gekommen bist und würden uns freuen dich auch mal persönlich kennen zu lernen.
Solltest du Probleme oder Anregungen haben findest du die Kontaktmöglichkeiten im Wiki unter https://wiki.freifunk-rhein-neckar.de/doku.php/kontakt

Viele Grüße,

Freifunk Rhein Neckar
'''.format(**node)
    return msg
