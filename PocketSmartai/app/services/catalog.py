from urllib.parse import quote_plus

def search_url(platform,q):
    q=quote_plus(q)
    urls={"Amazon":f"https://www.amazon.in/s?k={q}","Flipkart":f"https://www.flipkart.com/search?q={q}","IKEA":f"https://www.ikea.com/in/en/search/?q={q}","Swiggy":f"https://www.swiggy.com/search?query={q}","Zomato":f"https://www.zomato.com/search?query={q}","OYO":f"https://www.oyorooms.com/search?location={q}"}
    return urls.get(platform,f"https://www.google.com/search?q={q}")
HOME=[("LED Ceiling Light","lighting",899,"Amazon"),("Modern Ceiling Fan","fan",2499,"Amazon"),("Compact Study Table","furniture",4999,"IKEA"),("2-Seater Dining Table","furniture",7499,"IKEA"),("Wall Art Set","decor",1299,"Flipkart"),("Storage Cabinet","storage",3999,"IKEA"),("Floor Lamp","lighting",2199,"IKEA"),("Decorative Mirror","decor",1799,"Flipkart")]
PARTY=[("Budget Catering Package","catering",250,"Swiggy"),("Party Food Package","catering",300,"Zomato"),("Birthday Decoration Package","decoration",2500,"Amazon"),("Event Lighting Set","decoration",1800,"Amazon"),("Guest Stay Search","accommodation",1500,"OYO"),("Party Return Gifts","gifts",120,"Flipkart")]
JEWELRY=[("Minimal Gold-Tone Earrings","earrings",699,"Amazon"),("Pearl Drop Earrings","earrings",899,"Flipkart"),("Traditional Jhumka Earrings","earrings",799,"Amazon"),("Elegant Necklace Set","necklace",1499,"Flipkart"),("Simple Bracelet","bracelet",599,"Amazon"),("Statement Necklace","necklace",1899,"Flipkart")]
def catalog(kind): return HOME if kind=="home" else PARTY if kind=="party" else JEWELRY
