import math
import os
import time

# Bildschirmgröße
width = 80
height = 24

# Donut-Parameter
theta_spacing = 0.07
phi_spacing = 0.02

# Licht- und Schattenparameter
A = 0
B = 0

try:
    while True:
        # Erstelle leere Puffer für die Ausgabe und die Z-Buffer
        output = [' '] * (width * height)
        zbuffer = [0] * (width * height)

        for theta in [i * theta_spacing for i in range(int(2 * math.pi / theta_spacing))]:
            for phi in [i * phi_spacing for i in range(int(2 * math.pi / phi_spacing))]:
                # Koordinaten des Donuts im 3D-Raum
                sin_theta = math.sin(theta)
                cos_theta = math.cos(theta)
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)
                sin_A = math.sin(A)
                cos_A = math.cos(A)
                sin_B = math.sin(B)
                cos_B = math.cos(B)

                # Donut-Parameter
                R1 = 1  # Radius des Donuts
                R2 = 2  # Abstand vom Zentrum

                # 3D-Koordinaten vor Rotation
                circle_x = R2 + R1 * cos_theta
                circle_y = R1 * sin_theta

                # 3D-Koordinaten nach Rotation
                x = circle_x * (cos_B * cos_phi + sin_A * sin_B * sin_phi) - circle_y * cos_A * sin_B
                y = circle_x * (sin_B * cos_phi - sin_A * cos_B * sin_phi) + circle_y * cos_A * cos_B
                z = 5 + cos_A * circle_x * sin_phi + circle_y * sin_A
                ooz = 1 / z  # "One over z" für Tiefenberechnung

                # Projektionskoordinaten auf die Bildschirmfläche
                xp = int(width / 2 + 30 * ooz * x)
                yp = int(height / 2 - 15 * ooz * y)

                # Berechnung der Beleuchtung
                L = cos_phi * cos_theta * sin_B - cos_A * cos_theta * sin_phi - sin_A * sin_theta + cos_B * (cos_A * sin_theta - cos_theta * sin_A * sin_phi)
                # Helligkeit
                luminance_index = int(max(0, min(11, L * 8)))

                # Z-Buffer-Index
                idx = xp + yp * width
                if 0 <= xp < width and 0 <= yp < height:
                    if ooz > zbuffer[idx]:
                        zbuffer[idx] = ooz
                        # ASCII-Zeichen basierend auf Helligkeit
                        luminance_chars = ".,-~:;=!*#$@"
                        output[idx] = luminance_chars[luminance_index]

        # Bildschirm aktualisieren
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(height):
            print(''.join(output[i * width:(i + 1) * width]))
        # Rotation erhöhen
        A += 0.04
        B += 0.02
        time.sleep(0.03)
except KeyboardInterrupt:
    pass