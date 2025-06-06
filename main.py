"""
main.py: třetí projekt do Engeto Online Python Akademie (Elections Scraper)

Autor: Marek Sedlák
Email: sedlak.marek14@icloud.com

Popis:
Tento skript slouží ke scrapování výsledků voleb z roku 2017 pro zvolený územní celek
z webu volby.cz. Po zadání správné URL a názvu výstupního souboru vygeneruje CSV
s výsledky pro všechny obce v zadaném celku.

Spuštění:
python main.py "URL" název_výstupního_souboru.csv
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv


def check_arguments():
    """Zkontroluje, zda uživatel zadal správné argumenty (URL a výstupní soubor).
    Ukončí program, pokud jsou argumenty neplatné.

    Returns:
        tuple: (url, output_file)
    """
    if len(sys.argv) != 3:
        print("❌ Chyba: Program potřebuje 2 argumenty: URL a název výstupního CSV souboru.")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    if "volby.cz/pls/ps2017nss/" not in url:
        print("❌ Chyba: URL není platná adresa z volby.cz.")
        sys.exit(1)
    return url, output_file


def get_soup(url):
    """Vrátí objekt BeautifulSoup z dané URL.

    Args:
        url (str): Adresa stránky.

    Returns:
        BeautifulSoup: Parsovaný HTML obsah stránky.
    """
    response = requests.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')


def get_village_links(soup, base_url):
    """Získá seznam obcí (kód, název, detailní URL) z výchozí stránky.

    Args:
        soup (BeautifulSoup): Parsovaný HTML obsah hlavní stránky.
        base_url (str): Základní část URL.

    Returns:
        list: Seznam trojic (kód obce, název, detailní odkaz).
    """
    links = []
    rows = soup.select("table tr")

    for row in rows:
        link = row.find("a")
        if link and "href" in link.attrs:
            full_url = base_url + link["href"]
            code = row.find("td").text.strip()
            location = row.find_all("td")[1].text.strip()
            links.append((code, location, full_url))
    return links


def get_party_names(soup):
    """Získá názvy všech kandidujících stran z detailní stránky obce.

    Args:
        soup (BeautifulSoup): Parsovaný HTML obsah stránky obce.

    Returns:
        list: Seznam názvů politických stran.
    """
    party_names = []
    tables = soup.find_all("table", {"class": "table"})[-2:]

    for table in tables:
        for row in table.find_all("tr")[2:]:
            cells = row.find_all("td")
            if len(cells) >= 2:
                party_name = cells[1].text.strip()
                if party_name and party_name != "-":
                    party_names.append(party_name)
    return party_names


def parse_village_data(code, location, url):
    """Získá volební výsledky pro jednu obec včetně hlasů pro jednotlivé strany.

    Args:
        code (str): Kód obce.
        location (str): Název obce.
        url (str): Detailní URL obce.

    Returns:
        list: Seznam dat pro řádek ve výsledné tabulce.
    """
    soup = get_soup(url)
    tds = soup.find_all("td", class_="cislo")
    registered = int(tds[3].text.replace("\xa0", "").replace(" ", ""))
    envelopes = int(tds[4].text.replace("\xa0", "").replace(" ", ""))
    valid = int(tds[7].text.replace("\xa0", "").replace(" ", ""))

    # Hlasy pro všechny strany
    party_votes = []

    tables = soup.find_all("table", {"class": "table"})[-2:]

    for table in tables:
        for row in table.find_all("tr")[2:]:
            cells = row.find_all("td")
            if len(cells) >= 3:
                vote_str = cells[2].text.strip().replace("\xa0", "").replace(" ", "")
                try:
                    votes = int(vote_str) if vote_str and vote_str != "-" else 0
                except ValueError:
                    votes = 0
                party_votes.append(votes)

    # Ořízni případné nadbytečné sloupce
    party_votes = party_votes[:len(get_party_names(soup))]
    return [code, location, registered, envelopes, valid] + party_votes


def save_to_csv(header, results, filename):
    """Uloží výsledky do výstupního CSV souboru.

    Args:
        header (list): Hlavička CSV souboru (názvy sloupců).
        results (list): Seznam řádků s výsledky.
        filename (str): Název výstupního souboru.
    """
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(results)

    print(f"✅ Výsledky byly úspěšně uloženy do souboru {filename}")


def main():
    """Hlavní běh programu – načítá vstupní URL, scrapuje výsledky a ukládá do CSV."""
    url, output_file = check_arguments()
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    print(f"⏳ Stahuji data z vybrané URL: {url}")
    main_soup = get_soup(url)
    village_links = get_village_links(main_soup, base_url)

    # Získání názvů stran z první obce
    first_village_soup = get_soup(village_links[0][2])
    party_names = get_party_names(first_village_soup)

    header = ["code", "location", "registered", "envelopes", "valid"] + party_names
    results = []

    for code, location, link in village_links:
        row = parse_village_data(code, location, link)
        results.append(row)

    save_to_csv(header, results, output_file)


if __name__ == "__main__":
    main()
