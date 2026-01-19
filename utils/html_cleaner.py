from bs4 import BeautifulSoup
import bs4

ALLOWED_TAGS = ["p", "ul", "ol", "li", "p", "strong", "em", "b", "i", "u", "br"]

def clean_translated_html(text: str) -> str:
    if not text:
        return ""

    # Normaliza errores comunes en etiquetas mal cerradas
    text = text.replace("< ", "<").replace(" >", ">").replace("> ", ">").replace(" <", "<")
    text = text.replace(">>", ">").replace("> >", ">")

    soup = BeautifulSoup(text, "html.parser")

    # Elimina o desenrolla etiquetas que no estén permitidas
    for tag in soup.find_all():
        if isinstance(tag, bs4.element.Tag):
            if tag.name not in ALLOWED_TAGS:
                tag.unwrap()

    # Elimina etiquetas vacías
    for tag in soup.find_all():
        if isinstance(tag, bs4.element.Tag) and not tag.text.strip():
            tag.decompose()

    return str(soup).strip()