import os
import gzip
import re
import requests

def extraire_premiere_url(contenu_bytes):
    try:
        texte = contenu_bytes.decode("utf-8")
    except UnicodeDecodeError:
        texte = contenu_bytes.decode("latin-1", errors="ignore")

    urls = re.findall(r'https?://[^\s\'"]+', texte)
    for url in urls:
        match = re.match(r'(https?://.*?\.(?:png|jpg))', url)
        if match:
            return match.group(1)
    return None

def telecharger_image(url, chemin_dest):
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(chemin_dest, 'wb') as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False

def ajouter_url_non_telechargee(url):
    with open("mismatched_urls.txt", "a") as f:
        f.write(url + "\n")

def traiter_fichiers():
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    fichiers = [f for f in os.listdir("input") if f.endswith(".dat")]

    if not fichiers:
        print("Aucun fichier .dat trouvé dans le dossier 'input'.")
        return

    for fichier in fichiers:
        chemin = os.path.join("input", fichier)
        try:
            with gzip.open(chemin, 'rb') as f:
                contenu = f.read()
        except OSError:
            print(f"Erreur : fichier {fichier} n'est pas un fichier gzip valide.")
            continue

        url = extraire_premiere_url(contenu)
        if url:
            nom_fichier = os.path.basename(url).split('?')[0]
            chemin_image = os.path.join("output", nom_fichier)
            if telecharger_image(url, chemin_image):
                print(f"Téléchargé : {nom_fichier}")
            else:
                print(r"Échec du téléchargement pour : {url}")
                ajouter_url_non_telechargee(url)
        else:
            print(f"Aucune URL détectée dans : {fichier}")

if __name__ == "__main__":
    traiter_fichiers()
