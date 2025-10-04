# LEGO® MINDSTORMS® Robot Inventor (51515) mit Python programmieren

Diese Anleitung zeigt, wie man den 51515-Hub mit **Python** programmieren kann (auf macOS).

Wir nutzen **Pybricks** (läuft direkt auf dem Hub) und **uv** (verwaltet Python).

Am Ende kannst du aus **VS Code** heraus dein Python-Programm per **Bluetooth** auf den Hub übertragen und starten.

## 1) `uv` installieren (einmalig)

`uv` ist ein Tool, das die Erstellung von Python-Projekte vereinfacht. 

Terminal öffnen und ausführen:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Danach das Terminal neu starten.

## 2) Dieses GitHub-Repository klonen

In dem Terminal ausführen, wo du das Projekt speichern möchtest:

```bash
git clone https://github.com/kirenz/lego-mindstorms-roboter.git
```

In den Projektordner wechseln:

```bash
cd lego-mindstorms-roboter
```


---

## 3) Abhängigkeiten installieren

Im Projektordner:

```bash
uv sync
```

uv erstellt die Python-Umgebung und installiert die Pakete 

---

## 4) Pybricks-Firmware einmalig flashen (per USB)

Damit der Hub Python-Programme **direkt auf dem Gerät** ausführt, muss einmalig die **Pybricks-Firmware** installiert werden:

1. Hub **per USB** mit dem Mac verbinden.
2. Browser öffnen → [code.pybricks.com](https://code.pybricks.com)
3. Oben: **Tools → Install Pybricks firmware** und dem Assistenten folgen.
4. Nach dem Flashen den Hub **neu starten** (aus/ein).


> **Wichtig:** Das erste Flashen muss über USB erfolgen. Danach kannst du via Bluetooth arbeiten.



---

## 5) Projekt in VS Code öffnen 

**VS Code** starten → **File → Open Folder…** → den geklonten Ordner `lego-mindstorms-roboter` wählen.


---

## 6) Hub verbinden & Programm starten (Bluetooth)

**Bluetooth am Mac aktivieren** und **Hub einschalten** (Taste drücken, bis die LED **blau blinkt**).

### 6.1 Hub scannen (optional, zur Kontrolle)

Im VS Code Terminal:

```bash
uv run pybricksdev devices
```

Du solltest deinen Hub in der Liste sehen.

### 6.2 Programm übertragen & starten

```bash
uv run pybricksdev run src/main.py
```

* Das Skript wird **per Bluetooth** auf den Hub übertragen und sofort ausgeführt.
* Beim ersten Mal fragt macOS evtl. nach **Bluetooth-Rechten** – bitte **erlauben**.

*(USB-Start ist ebenfalls möglich, falls unterstützt: `uv run pybricksdev usb --run src/main.py`)*

---

## Häufige Fragen (FAQ)

**Muss ich jedes Mal `uv sync` ausführen?**
Nein. Nur wenn du das Projekt neu aufsetzt.

**Kann ich `src/main.py` lokal am Mac starten?**
Technisch ja (`uv run python src/main.py`), aber viele Pybricks-Funktionen brauchen die Hub-Hardware. Sinnvoll ist der Start **auf dem Hub**.


**Kann ich zur LEGO-Firmware zurück?**
Ja. In `code.pybricks.com` → **Tools → Restore Firmware**.

---

## Troubleshooting (bitte der Reihe nach prüfen)

**Hub wird nicht gefunden (`devices` zeigt nichts):**

1. Hub an? LED **blinkt blau**?
2. Hub **nah** an den Mac legen (30–50 cm).
3. In macOS-Bluetooth alte Kopplungen **entfernen** und erneut versuchen.
4. Hub aus- und wieder einschalten.
5. Mac neu starten.

**Firmware-Flash schlägt fehl:**

1. **USB-Kabel** prüfen (Datenkabel, kein reines Ladekabel).
2. Anderen USB-Port/Adapter testen.
3. Browser-Tab neu laden und den **Install-Assistenten** erneut durchlaufen.

**Programm startet, aber nichts passiert:**

1. Hängt der **Motor/Sensor** am **richtigen Port** (z. B. `Port.A`)?
2. Sehr kleines Testskript versuchen (z. B. nur LED umschalten), um Verbindungsprobleme auszuschließen.
3. **Akkustand** des Hubs prüfen.

**Keine Autovervollständigung (Pybricks):**

1. In VS Code den Interpreter auf `.venv/bin/python` setzen (siehe oben).
2. Terminal/VS Code neu öffnen.
3. Ggf. `uv sync` erneut ausführen.

