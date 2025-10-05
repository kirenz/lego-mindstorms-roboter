# 🤖 Roboter-Steuerung

## Übersicht

Dieses Projekt steuert einen LEGO Mindstorms MVP-Buggy mit Python und Pybricks über Bluetooth vom Mac aus.

### Hardware-Konfiguration

- **Motor A**: Lenkung (vorne mitte)
- **Motor B**: Antrieb (hinten mitte)  
- **Motor C**: Greifarm Drehung (über Motor A)
- **Motor D**: Greifarm Hoch/Runter (über Motor C)
- **Port F**: Ultraschall-Abstandssensor (vorne mitte)

## Installation

```bash
# Dependencies installieren
cd lego-mindstorms-roboter
uv sync
```

## 🎮 Verwendung (Empfohlen: Tastatur-Steuerung)

### Methode 1: Tastatur-Steuerung vom Mac (Empfohlen!)

Die komfortabelste Methode - steuere mit WASD + IJKL von deinem Mac aus:

**Schritt 1: Roboter-Programm starten**
```bash
# Terminal 1
uv run pybricksdev run ble src/main.py
```

Warte bis der Roboter bereit ist (grünes Licht).

**Schritt 2: Controller starten**
```bash
# Terminal 2 (neues Terminal öffnen!)
uv run python src/keyboard_controller.py
```

Der Controller verbindet sich automatisch mit dem Roboter.

**Tastatur-Steuerung:**

| Taste | Funktion |
|-------|----------|
| `W` | ⬆️ Vorwärts fahren |
| `S` | ⬇️ Rückwärts fahren |
| `A` | ⬅️ Links lenken |
| `D` | ➡️ Rechts lenken |
| `I` | ⬆️ Greifarm hoch |
| `K` | ⬇️ Greifarm runter |
| `J` | ↪️ Greifarm links drehen |
| `L` | ↩️ Greifarm rechts drehen |
| `0` | 🎯 Lenkung zentrieren |
| `X` | 🛑 Alles stoppen |
| `M` | 📏 Abstand messen |
| `H` | ❓ Hilfe anzeigen |
| `Q` | 👋 Beenden |

### Methode 2: Roboter mit Hub-Tasten steuern (Fallback)

Einfache Steuerung direkt am Hub (funktioniert auch wenn Mac-Controller nicht verbunden ist):

**Steuerung am Hub:**
- **Linke Taste**: Links lenken
- **Rechte Taste**: Rechts lenken
- **Bluetooth-Taste**: Programm beenden



## Funktionen

### `execute_command(cmd)`

Führt einen Steuerbefehl aus. Verfügbare Befehle:

- `'w'`: Vorwärts (1 Sekunde)
- `'s'`: Rückwärts (1 Sekunde)
- `'a'`: Links lenken (45°)
- `'d'`: Rechts lenken (45°)
- `'i'`: Arm hoch (1 Sekunde)
- `'k'`: Arm runter (1 Sekunde)
- `'j'`: Arm links drehen (1 Sekunde)
- `'l'`: Arm rechts drehen (1 Sekunde)
- `'0'`: Lenkung zentrieren
- `'x'` oder `' '`: Alles stoppen
- `'m'`: Abstand messen und anzeigen

## Konfiguration

Geschwindigkeiten und Winkel können in `src/main.py` angepasst werden:

```python
DRIVE_SPEED = 500        # Fahrgeschwindigkeit (Grad/Sekunde)
STEERING_ANGLE = 45      # Maximaler Lenkwinkel (Grad)
ARM_ROTATE_SPEED = 300   # Greifarm Drehgeschwindigkeit
ARM_LIFT_SPEED = 300     # Greifarm Hebe-Geschwindigkeit
```

## Problembehandlung

### Verbindung schlägt fehl

1. Stelle sicher, dass der Hub eingeschaltet ist
2. Bluetooth muss am Mac aktiviert sein
3. Hub sollte in Reichweite sein (< 10m)
4. Versuche den Hub neu zu starten

### Motoren reagieren nicht

1. Überprüfe die Port-Verbindungen (A, B, C, D)
2. Stelle sicher, dass die Motoren richtig eingesteckt sind
3. Teste jeden Motor einzeln im REPL

### Sensor-Fehler

1. Überprüfe, ob der Sensor an Port F angeschlossen ist
2. Stelle sicher, dass der Sensor nicht blockiert ist
3. Teste mit `execute_command('m')` im REPL

## Lizenz

MIT License
