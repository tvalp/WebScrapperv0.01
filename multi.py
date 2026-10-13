import requests
import bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_trendyol_links():
    url = "https://www.trendyol.com/bilgisayar-x-c108656"
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    listeler = []
    
    for a in soup.find_all('a', {"class": "product-card"}) or soup.find_all('a', {"class": "p-card-wrppr"}) or soup.find_all("span", {"class":"price-value"}):
        if a.name == "span":
            price_elem = a
            parent = a.find_parent("div", {"class":"p-card-wrppr"}) or a.parent.parent.parent.parent
            link_elem = parent.find("a")
        else:
            link_elem = a
            price_elem = a.find("span", {"class":"price-value"})
            parent = a
            
        if not price_elem:
            continue
            
        try:
            price = price_elem.text
            temiz_fiyat = float(price.replace(" TL", "").replace(".", "").replace(",", "."))
            urun_adi = parent.text.strip().replace("\n", " - ")
            
            href = link_elem.get("href", "") if link_elem else ""
            if href:
                link = href if href.startswith("http") else "https://www.trendyol.com" + href
            else:
                link = "Link yok"
                
            listeler.append((temiz_fiyat, urun_adi, link))
        except:
            continue
        
    if not listeler:
        return (0.0, "Bulunamadı", "Link yok"), (0.0, "Bulunamadı", "Link yok")
        
    en_ucuz = min(listeler, key=lambda x: x[0])
    en_pahali = max(listeler, key=lambda x: x[0])
    return en_ucuz, en_pahali

def get_n11_links():
    url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar"
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    links = []
    
    for a in soup.find_all('a', {"class": "product-item"}):
        href = a.get("href", "")
        if href:
            link = href if href.startswith("http") else "https://www.n11.com" + href
        else:
            link = "Link yok"
        
        price_elem = a.find('h3', {"class":"price-currency"}) or a.find('div', {"class":"priceContainer"})
        if not price_elem:
            continue
            
        price_text = price_elem.text.replace(" TL", "").replace(".", "").replace(",", ".")
        temiz_fiyat = float(''.join(c for c in price_text if c.isdigit() or c == '.'))
        
        text = a.find("h2", {"class":"product-item-title two-lines"}) or a.find("h3", {"class":"product-item-title"})
        urun_adi = text.text.strip() if text else "Ürün adı bulunamadı"
        
        links.append((temiz_fiyat, urun_adi, link))
        
    if not links:
        return (0.0, "Bulunamadı", "Link yok"), (0.0, "Bulunamadı", "Link yok")
        
    en_ucuz = min(links, key=lambda x: x[0])
    en_pahali = max(links, key=lambda x: x[0])
    return en_ucuz, en_pahali

def get_Enbuyuk_fiyat():
    t_ucuz, t_pahali = get_trendyol_links()
    n_ucuz, n_pahali = get_n11_links()
    
    print("=" * 60)
    print(" TRENDYOL EN UYGUN ÜRÜN:")
    print(f"İsim : {t_ucuz[1]}")
    print(f"Fiyat: {t_ucuz[0]} TL")
    print(f"Link : {t_ucuz[2]}\n")
    
    print(" TRENDYOL EN PAHALI ÜRÜN:")
    print(f"İsim : {t_pahali[1]}")
    print(f"Fiyat: {t_pahali[0]} TL")
    print(f"Link : {t_pahali[2]}")
    print("=" * 60)
    
    print(" N11 EN UYGUN ÜRÜN:")
    print(f"İsim : {n_ucuz[1]}")
    print(f"Fiyat: {n_ucuz[0]} TL")
    print(f"Link : {n_ucuz[2]}\n")
    
    print(" N11 EN PAHALI ÜRÜN:")
    print(f"İsim : {n_pahali[1]}")
    print(f"Fiyat: {n_pahali[0]} TL")
    print(f"Link : {n_pahali[2]}")
    print("=" * 60)

get_Enbuyuk_fiyat()