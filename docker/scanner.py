import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random

# --- Configuration de Blue ---
AMAZON_BASE_URL = "https://www.amazon.ca"  # Nous ciblons Amazon Canada
PRODUCT_SEARCH_PATH = "/s?k=laptop"      # Recherche initiale pour les ordinateurs portables
MIN_DISCOUNT_PERCENTAGE = 20              # Pourcentage de rabais minimum pour considérer une offre
OUTPUT_FILE_NAME = "amazon_deals.csv"     # Nom du fichier pour sauvegarder les résultats

# --- Headers pour simuler un navigateur réel (très important pour le scraping) ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Connection": "keep-alive"
}


# --- Fonction principale du Scanner ---
def run_blue_scanner():
    print("Blue Scanner : Démarrage de l'analyse des deals Amazon...")
    all_deals = []
    page_num = 1 # On commence par la première page

    while True: # Boucle pour parcourir plusieurs pages de résultats
        search_url = f"{AMAZON_BASE_URL}{PRODUCT_SEARCH_PATH}&page={page_num}"
        print(f"Blue Scanner : Récupération de la page {page_num} : {search_url}")

        try:
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Blue Scanner Erreur de requête sur la page {page_num} : {e}")
            break # Arrête si une erreur de requête survient

        soup = BeautifulSoup(response.content, 'lxml') # Utilisation du parser lxml !

        # Trouver tous les produits sur la page
        # Les sélecteurs CSS d'Amazon changent souvent, c'est une estimation.
        # Nous devrons peut-être les ajuster si le script ne trouve rien.
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        if not products:
            print(f"Blue Scanner : Aucuns produits trouvés sur la page {page_num}. Fin de la recherche.")
            break # Plus de produits, on arrête

        for product in products:
            title_tag = product.find("span", class_="a-size-medium a-color-base a-text-normal")
            price_whole_tag = product.find("span", class_="a-price-whole")
            price_fraction_tag = product.find("span", class_="a-price-fraction")
            old_price_tag = product.find("span", class_="a-price a-text-price")
            product_link_tag = product.find("a", class_="a-link-normal s-underline-text s-link-style a-text-normal")

            title = title_tag.text.strip() if title_tag else "N/A"
            current_price_str = ""
            if price_whole_tag and price_fraction_tag:
                current_price_str = f"{price_whole_tag.text.strip()}{price_fraction_tag.text.strip()}"
            current_price = float(current_price_str.replace('$', '').replace(',', '')) if current_price_str else 0.0

            old_price_str = old_price_tag.find("span", class_="a-offscreen").text.strip() if old_price_tag and old_price_tag.find("span", class_="a-offscreen") else ""
            old_price = float(old_price_str.replace('$', '').replace(',', '')) if old_price_str else 0.0

            product_link = AMAZON_BASE_URL + product_link_tag['href'] if product_link_tag and 'href' in product_link_tag else "N/A"

            discount_percentage = 0
            if old_price > 0 and current_price > 0:
                discount_percentage = ((old_price - current_price) / old_price) * 100

            if discount_percentage >= MIN_DISCOUNT_PERCENTAGE:
                all_deals.append({
                    "Titre": title,
                    "Prix Actuel ($CA)": current_price,
                    "Ancien Prix ($CA)": old_price,
                    "Rabais (%)": round(discount_percentage, 2),
                    "Lien Produit": product_link,
                    "Date du Scan": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        # Pause aléatoire pour ne pas surcharger Amazon et éviter les blocages
        time.sleep(random.uniform(5, 10))
        page_num += 1
        # Pour le test, on peut limiter le nombre de pages. Décommenter la ligne ci-dessous pour ne scanner que 2 pages par exemple.
        # if page_num > 2: break

    if all_deals:
        df = pd.DataFrame(all_deals)
        output_path = os.path.join("data", OUTPUT_FILE_NAME)
        # Assurez-vous que le répertoire 'data' existe
        os.makedirs("data", exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nBlue Scanner : {len(all_deals)} deals trouvés et sauvegardés dans {output_path}")
        print("Blue Scanner : Voici les 5 premiers deals :")
        print(df.head().to_string()) # Affiche les 5 premiers deals dans le terminal
    else:
        print("Blue Scanner : Aucuns deals significatifs trouvés pour le moment.")

    print("Blue Scanner : Fin de l'opération.")


if __name__ == "__main__":
    run_blue_scanner()
