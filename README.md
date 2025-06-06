# Elections Scraper

Tento Python skript slouží ke scrapování výsledků voleb do Poslanecké
sněmovny ČR z roku 2017 z webu [volby.cz](https://www.volby.cz/). Uživatel
zadá URL adresu okresu a výstupní název CSV souboru, a skript stáhne výsledky
hlasování ve všech obcích daného okresu.

## 👨‍💻 Autor
**Jméno:** Marek Sedlák  
**Email:** sedlak.marek14@icloud.com

---

## 🛠️ Instalace

1. **Vytvoř si virtuální prostředí (doporučeno):**

```bash
python -m venv venv
```

2. **Aktivuj virtuální prostředí:**

- Windows:
  ```bash
  .\venv\Scripts\activate
  ```
- macOS / Linux:
  ```bash
  source venv/bin/activate
  ```

3. **Nainstaluj requirements:**

```bash
pip install -r requirements.txt
```

---

## 🚀 Spuštění skriptu

Skript spustíš pomocí dvou argumentů:

```bash
python main.py "URL_OKRESU" "NAZEV_SOUBORU.csv"
```

- `URL_OKRESU`: odkaz na stránku konkrétního okresu (např. Tachov)
- `NAZEV_SOUBORU.csv`: jméno výstupního CSV souboru

### ✅ Příklad:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3207" vysledky_tachov.csv
```

---

## 📦 Výstup

Výstupem bude CSV soubor, kde každý řádek odpovídá jedné obci a obsahuje:

- kód obce
- název obce
- počet voličů v seznamu
- počet vydaných obálek
- počet platných hlasů
- počet hlasů pro každou kandidující stranu (každá strana má svůj sloupec)

### Ukázka výstupu (`vysledky_tachov.csv`):

| code   | location | registered | envelopes | valid | ANO 2011 | ODS | ... |
|--------|----------|------------|-----------|-------|----------|-----|-----|
| 560843 | Bor      | 4021       | 2487      | 2470  | 1023     | 223 | ... |

---

## ⚠️ Ošetření chyb

- Pokud nezadáš oba argumenty, skript se ukončí s hláškou.
- Pokud první argument není validní URL z volby.cz, skript se také ukončí.

---

## 📁 Obsah repozitáře

```
.
├── main.py             # hlavní skript
├── requirements.txt    # knihovny potřebné k běhu
├── README.md           # tento popis projektu
└── vysledky_tachov.csv # výstupní CSV (název volitelně)
```
