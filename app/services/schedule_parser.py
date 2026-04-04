import fitz
import re
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_schedule(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        if not page_text.strip():
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.convert("L")
            page_text = pytesseract.image_to_string(img)
        text += page_text + "\n"
    doc.close()
    return text.lower()


def extract_policy_type(text: str) -> str:
    if "comprehensive" in text or "package policy" in text or "private car package" in text:
        return "Comprehensive"
    elif "third party" in text and "own damage" not in text:
        return "Third Party Only"
    elif "own damage" in text and "third party" not in text:
        return "Own Damage Only"
    return "Comprehensive"


def extract_idv(text: str) -> float:
    patterns = [
        r"idv[\s:₹rs\.]*([0-9,]+)",
        r"insured declared value[\s:₹rs\.]*([0-9,]+)",
        r"sum insured[\s:₹rs\.]*([0-9,]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = match.group(1).replace(",", "")
            try:
                return float(value)
            except:
                continue
    return 500000.0


def extract_vehicle_number(text: str) -> str:
    pattern = r"\b[a-z]{2}[\s-]?\d{2}[\s-]?[a-z]{1,2}[\s-]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        return match.group(0).upper().replace(" ", "").replace("-", "")
    return "NOT FOUND"


def extract_insurer(text: str) -> str:
    insurers = {
        "bajaj allianz": "Bajaj Allianz",
        "hdfc ergo": "HDFC ERGO",
        "new india": "New India Assurance",
        "icici lombard": "ICICI Lombard",
        "united india": "United India Insurance",
        "national insurance": "National Insurance",
        "oriental insurance": "Oriental Insurance",
        "reliance general": "Reliance General",
        "tata aig": "Tata AIG",
    }
    for key, value in insurers.items():
        if key in text:
            return value
    return "Unknown Insurer"


def extract_addons(text: str) -> list:
    addons = []
    if "zero dep" in text or "zero depreciation" in text or "nil dep" in text:
        addons.append("Zero Depreciation")
    if "engine protect" in text or "engine cover" in text:
        addons.append("Engine Protection")
    if "roadside" in text or "rsa" in text:
        addons.append("Roadside Assistance")
    if "ncb" in text or "no claim bonus" in text:
        addons.append("NCB Protection")
    return addons


def parse_schedule(pdf_path: str) -> dict:
    text = extract_text_from_schedule(pdf_path)

    policy_type = extract_policy_type(text)
    idv = extract_idv(text)
    vehicle_number = extract_vehicle_number(text)
    insurer = extract_insurer(text)
    addons = extract_addons(text)
    has_zero_dep = "Zero Depreciation" in addons

    return {
        "policy_type": policy_type,
        "idv": idv,
        "vehicle_number": vehicle_number,
        "insurer": insurer,
        "addons": addons,
        "has_zero_dep": has_zero_dep
    }