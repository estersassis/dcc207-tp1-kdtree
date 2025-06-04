import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from pathlib import Path

BASE_URL = "https://comidadibuteco.com.br"
LISTA_BH = f"{BASE_URL}/butecos/belo-horizonte/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_links():
    print("Buscando bares em todas as páginas...")
    bares = []
    page = 1

    while True:
        url = f"{BASE_URL}/butecos/belo-horizonte/" if page == 1 else f"{BASE_URL}/butecos/belo-horizonte/page/{page}/"
        print(f"Página {page}: {url}")
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("div.item")

        if not items:
            print("Fim da paginação.")
            break

        for item in items:
            link_tag = item.select_one("a[href^='https://comidadibuteco.com.br/buteco/']")
            url = link_tag["href"] if link_tag else ""

            bares.append(url)

        page += 1
        time.sleep(0.5)

    return bares


def clean_name(title):
    return re.sub(r" - Comida di Buteco", "", title).strip()

def extract_data(url):
    try:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        title = soup.find("title").text.strip()
        name = clean_name(title)
        
        section = soup.select_one("div.section-text")
        ps = section.find_all("p")

        food_tag = ps[0].find("b")
        food = food_tag.text.strip() if food_tag else ""
        description = ps[0].text.replace(food, "").strip()

        address = ""
        phone = ""

        for p in ps:
            label = p.find("b")
            if not label: continue
            label_text = label.text.strip().lower()
            if "endereço" in label_text:
                address = p.text.replace(label.text, "").strip()
            elif "telefone" in label_text:
                phone = p.text.replace(label.text, "").strip()
        
        img_tag = soup.select_one("img.img-single.wp-post-image")
        img_url = img_tag["src"] if img_tag else ""

        return {"NOME": name, "PRATO": food, "DESCRICAO": description, "ENDERECO": address, "TELEFONE": phone, "IMG_URL": img_url}
    
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")

def main():
    print("Coletando links dos bares de BH...")
    links = extract_links()

    print(f"{len(links)} bares encontrados. Extraindo dados individuais...")
    data = []
    for url in links:
        info = extract_data(url)
        if info:
            data.append(info)

    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)
    output_file = DATA_DIR / "comida_di_buteco_2025.csv"
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    
    print("CSV gerado com sucesso.")

if __name__ == "__main__":
    main()