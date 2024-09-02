import os
import requests
from bs4 import BeautifulSoup

def download_images(query, num_images=5):
    # Crea un directorio para guardar las imágenes
    if not os.path.exists(query):
        os.makedirs(query)

    # Realiza una búsqueda en Google Imágenes
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Error al acceder a la página de búsqueda.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra las URLs de las imágenes
    image_urls = []
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url and img_url.startswith("http"):
            image_urls.append(img_url)
        if len(image_urls) >= num_images:
            break

    # Descarga las imágenes
    for i, img_url in enumerate(image_urls):
        try:
            img_data = requests.get(img_url).content
            with open(f"{query}/image_{i+1}.jpg", 'wb') as img_file:
                img_file.write(img_data)
            print(f"Descargada imagen {i+1}: {img_url}")
        except Exception as e:
            print(f"Error al descargar la imagen {i+1}: {e}")

if __name__ == "__main__":
    query = "vasos"
    download_images(query, num_images=100)
