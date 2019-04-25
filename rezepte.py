import string
import random
import picamera
import time
from fractions import Fraction

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)
camera.vflip = True
camera.hflip = True


def ZeichenketteErstellen():
    """Diese Funktion erstellt einen String mit dem Dateipfad und einem
    zufällig erstellten Dateinamen, damit nicht ausversehen Dateien
    überschrieben werden
    """
    Dateiname = './Bilder/'
    for x in range(5):
        Dateiname = Dateiname + random.choice(string.ascii_letters)
    return Dateiname + '_'


def TagAufnahme(ZeitZwischenBildern=5, ZeitVorStart=30):
    """Diese Funktion erstellt fortlaufend Bilder, die später zu einem
    Time-Lapse Video zusammengestellt werden. Das Argument
    'ZeitZwischenBildern' bestimmt die Pause zwischen zwei Bildern in Sekunden.
    Das Argument 'ZeitVorStart' kann benutzt werden um die Aufnahme erst nach
    einer bestimmten Zeit in Sekunden gestartet wird. Das Arguemnt sollte
    jedoch mindestens einen Wert von 30 haben, damit die Kamera Zeit hat sich
    an die Lichtverhältnisse anzupassen
    """
    Dateiname = ZeichenketteErstellen() + '{counter:05d}.png'
    camera.sharpness = 100
    camera.exposure_mode = 'auto'
    # Mögliche Werte: 'off', 'auto', 'night', 'nightpreview', 'backlight'
    # 'spotlight', 'sports', 'snow', 'beach', 'verylong', 'fixedfps',
    # 'antishake', 'fireworks'
    camera.meter_mode = 'average'
    # Mögliche Werte: 'average', 'spot', 'backlit', 'matrix'
    camera.awb_mode = 'auto'
    # Mögliche Werte: 'auto', 'shade', 'tungsten', 'fluorescent', 'flash',
    # 'incandescent', 'cloudy', 'horizon', sunlight', 'off'
    for x in range(ZeitVorStart):
        print('Noch ' + str(ZeitVorStart - x) +
              ' Sekunden bis die Aufnahme beginnt')
        time.sleep(1)
    for filename in camera.capture_continuous(output=Dateiname, format='png'):
        print('Bild aufgenommen %s' % filename)
        time.sleep(ZeitZwischenBildern)


def NachtAufnahme(Belichtungszeit=6):
    """Diese Funktion startet eine Aufnahme bei schlechten Lichtverhältnissen.
    Das Argument Belichtungszeit steht für die Belichtungszeit in Sekunden
    Beim Kameramodul V1 sind Werte zwischen 1 und 6 zulässig, V2 erlaubt eine
    Belichtungszeit von bis zu 10 Sekunden. Mit der Funktion 'NachtTest' können
    die verschiedenen Belichtungszeiten ausprobiert werden.
    """
    Dateiname = ZeichenketteErstellen()
    camera.framerate = Fraction(1, Belichtungszeit)
    # Framerate und Shutterspeed (also Belichtungszeit) sind bei der Kamera
    # voneinander abhängig. Die zweite Zahl sollte bei Nachtaufnahmen
    # zwischen 1 und 6 liegen
    camera.shutter_speed = 1000000 * Belichtungszeit
    # hier steht jetzt die Belichtungszeit, diese sollte den Wert der
    # Framerate mal 1000000 sein. Bsp Framerate (1, 6) und Shutterspeed 6000000
    # entspricht einer Belichtungszeit von 6 Sekunden
    camera.exposure_mode = 'sports'
    # hier stellen wir die Kamera auf die Belichtungseinstellung "sports"
    # diese Einstellung ergibt die besten Bilder bei
    # schlechten Lichtverhältnissen
    time.sleep(30)
    counter = 0
    while True:
        counter = counter + 1
        if counter < 10:
            camera.capture(Dateiname + '000' + str(counter) + '.png')
        elif counter < 100:
            camera.capture(Dateiname + '00' + str(counter) + '.png')
        elif counter < 1000:
            camera.capture(Dateiname + '0' + str(counter) + '.png')
        else:
            camera.capture(Dateiname + str(counter) + '.png')
        print('Klick')


def NachtTest():
    """Diese Funktion erstellt zwölf Bilder mit verschiedenen
    Belichtungseinstellungen. Wird das Kameramodul V2 benutzt kann die Variable
    'Belichtungszeit' auf 10 gesetzt werden
    """
    print('NachtTest gestartet')
    Dateiname = ZeichenketteErstellen()
    Belichtungszeit = 6
    camera.iso = 800
    camera.exposure_mode = 'off'
    while Belichtungszeit > 0:
        camera.framerate = Fraction(1, Belichtungszeit)
        camera.shutter_speed = 1000000 * Belichtungszeit
        time.sleep(3)
        camera.capture(Dateiname + '_' + str(Belichtungszeit) +
                       '_Sekunden_Belichtung.png')
        print('Bild geschossen mit einer Belichtung von ' +
              str(Belichtungszeit) + ' Sekunden')
        Belichtungszeit -= 1

    # zweiter Test im Sport Modus
    Belichtungszeit = 6
    camera.iso = 0
    camera.exposure_mode = 'sports'

    while Belichtungszeit > 0:
        camera.framerate = Fraction(1, Belichtungszeit)
        camera.shutter_speed = 1000000 * Belichtungszeit
        time.sleep(3)
        camera.capture(Dateiname + '_' + str(Belichtungszeit) +
                       'Sekunden_Belichtung_im_Sportmodus.png')
        print('Bild geschossen mit einer Belichtung von ' +
              str(Belichtungszeit) + ' Sekunden')
        Belichtungszeit -= 1
