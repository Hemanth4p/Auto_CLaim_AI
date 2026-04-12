# import fitz
# import re
# import pytesseract
# from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# def extract_text_from_schedule(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         page_text = page.get_text()
#         if not page_text.strip():
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)
#         text += page_text + "\n"
#     doc.close()
#     return text.lower()


# def extract_policy_type(text: str) -> str:
#     if "comprehensive" in text or "package policy" in text or "private car package" in text:
#         return "Comprehensive"
#     elif "third party" in text and "own damage" not in text:
#         return "Third Party Only"
#     elif "own damage" in text and "third party" not in text:
#         return "Own Damage Only"
#     return "Comprehensive"


# def extract_idv(text: str) -> float:
#     patterns = [
#         r"idv[\s:₹rs\.]*([0-9,]+)",
#         r"insured declared value[\s:₹rs\.]*([0-9,]+)",
#         r"sum insured[\s:₹rs\.]*([0-9,]+)",
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, text)
#         if match:
#             value = match.group(1).replace(",", "")
#             try:
#                 return float(value)
#             except:
#                 continue
#     return 500000.0


# def extract_vehicle_number(text: str) -> str:
#     pattern = r"\b[a-z]{2}[\s-]?\d{2}[\s-]?[a-z]{1,2}[\s-]?\d{4}\b"
#     match = re.search(pattern, text)
#     if match:
#         return match.group(0).upper().replace(" ", "").replace("-", "")
#     return "NOT FOUND"


# def extract_insurer(text: str) -> str:
#     insurers = {
#         "bajaj allianz": "Bajaj Allianz",
#         "hdfc ergo": "HDFC ERGO",
#         "new india": "New India Assurance",
#         "icici lombard": "ICICI Lombard",
#         "united india": "United India Insurance",
#         "national insurance": "National Insurance",
#         "oriental insurance": "Oriental Insurance",
#         "reliance general": "Reliance General",
#         "tata aig": "Tata AIG",
#     }
#     for key, value in insurers.items():
#         if key in text:
#             return value
#     return "Unknown Insurer"


# def extract_addons(text: str) -> list:
#     addons = []
#     if "zero dep" in text or "zero depreciation" in text or "nil dep" in text:
#         addons.append("Zero Depreciation")
#     if "engine protect" in text or "engine cover" in text:
#         addons.append("Engine Protection")
#     if "roadside" in text or "rsa" in text:
#         addons.append("Roadside Assistance")
#     if "ncb" in text or "no claim bonus" in text:
#         addons.append("NCB Protection")
#     return addons


# def parse_schedule(pdf_path: str) -> dict:
#     text = extract_text_from_schedule(pdf_path)

#     policy_type = extract_policy_type(text)
#     idv = extract_idv(text)
#     vehicle_number = extract_vehicle_number(text)
#     insurer = extract_insurer(text)
#     addons = extract_addons(text)
#     has_zero_dep = "Zero Depreciation" in addons

#     return {
#         "policy_type": policy_type,
#         "idv": idv,
#         "vehicle_number": vehicle_number,
#         "insurer": insurer,
#         "addons": addons,
#         "has_zero_dep": has_zero_dep
#     }


# import fitz
# import re
# import pytesseract
# from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# def extract_text_from_schedule(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         if not page_text.strip():
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text + "\n"

#     doc.close()
#     return text.lower()


# # -------------------------------
# # 🔥 NEW FUNCTION (IMPORTANT)
# # -------------------------------
# def extract_vehicle_details(text: str) -> dict:
#     brands = [
#         "maruti", "suzuki", "hyundai", "tata",
#         "toyota", "honda", "mahindra", "kia",
#         "ford", "skoda", "volkswagen", "renault", "nissan"
#     ]

#     make = "Unknown"
#     model = "Unknown"

#     # Detect brand
#     for brand in brands:
#         if brand in text:
#             make = brand.capitalize()
#             break

#     # Detect model using patterns
#     patterns = [
#         r"model\s*[:\-]?\s*([a-z0-9\s]+)",
#         r"vehicle\s*[:\-]?\s*([a-z0-9\s]+)",
#         r"car\s*[:\-]?\s*([a-z0-9\s]+)"
#     ]

#     for pattern in patterns:
#         match = re.search(pattern, text)
#         if match:
#             model = match.group(1).strip().split("\n")[0]
#             break

#     # Clean model
#     if model != "Unknown":
#         model = model.title()
#         model = " ".join(model.split()[:2])

#     return {
#         "make": make,
#         "model": model
#     }


# def extract_policy_type(text: str) -> str:
#     if "comprehensive" in text or "package policy" in text:
#         return "Comprehensive"
#     elif "third party" in text and "own damage" not in text:
#         return "Third Party Only"
#     elif "own damage" in text:
#         return "Own Damage Only"
#     return "Comprehensive"


# def extract_idv(text: str) -> float:
#     patterns = [
#         r"idv[\s:₹rs\.]*([0-9,]+)",
#         r"insured declared value[\s:₹rs\.]*([0-9,]+)",
#         r"sum insured[\s:₹rs\.]*([0-9,]+)",
#     ]

#     for pattern in patterns:
#         match = re.search(pattern, text)
#         if match:
#             value = match.group(1).replace(",", "")
#             try:
#                 return float(value)
#             except:
#                 continue

#     return 500000.0


# def extract_vehicle_number(text: str) -> str:
#     pattern = r"\b[a-z]{2}[\s-]?\d{2}[\s-]?[a-z]{1,2}[\s-]?\d{4}\b"
#     match = re.search(pattern, text)

#     if match:
#         return match.group(0).upper().replace(" ", "").replace("-", "")

#     return "NOT FOUND"


# def extract_insurer(text: str) -> str:
#     insurers = {
#         "bajaj allianz": "Bajaj Allianz",
#         "hdfc ergo": "HDFC ERGO",
#         "icici lombard": "ICICI Lombard",
#         "tata aig": "Tata AIG",
#     }

#     for key, value in insurers.items():
#         if key in text:
#             return value

#     return "Unknown Insurer"


# def extract_addons(text: str) -> list:
#     addons = []

#     if "zero dep" in text:
#         addons.append("Zero Depreciation")

#     if "engine protect" in text:
#         addons.append("Engine Protection")

#     if "roadside" in text:
#         addons.append("Roadside Assistance")

#     return addons


# def parse_schedule(pdf_path: str) -> dict:
#     text = extract_text_from_schedule(pdf_path)

#     vehicle_info = extract_vehicle_details(text)

#     return {
#         "policy_type": extract_policy_type(text),
#         "idv": extract_idv(text),
#         "vehicle_number": extract_vehicle_number(text),
#         "insurer": extract_insurer(text),
#         "addons": extract_addons(text),
#         "has_zero_dep": "Zero Depreciation" in extract_addons(text),

#         # 🔥 NEW
#         "make": vehicle_info["make"],
#         "model": vehicle_info["model"]
#     }


import fitz
import re
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -------------------------------
# EXTRACT TEXT FROM PDF
# -------------------------------
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


# -------------------------------
# VEHICLE MAKE + MODEL
# -------------------------------
def extract_vehicle_details(text: str) -> dict:
    brands = [
        "maruti", "suzuki", "hyundai", "tata",
        "toyota", "honda", "mahindra", "kia",
        "ford", "skoda", "volkswagen", "renault", "nissan"
    ]

    make = "Unknown"
    model = "Unknown"

    # Detect make
    for brand in brands:
        if brand in text:
            make = brand.capitalize()
            break

    # Detect model
    patterns = [
        r"model\s*[:\-]?\s*([a-z0-9\s]+)",
        r"vehicle\s*[:\-]?\s*([a-z0-9\s]+)",
        r"car\s*[:\-]?\s*([a-z0-9\s]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            model = match.group(1).strip().split("\n")[0]
            break

    if model != "Unknown":
        model = model.title()
        model = " ".join(model.split()[:2])

    return {
        "make": make,
        "model": model
    }


# -------------------------------
# VEHICLE YEAR
# -------------------------------
def extract_vehicle_year(text: str) -> int:
    patterns = [
        r"year\s*of\s*manufacture\s*[:\-]?\s*(\d{4})",
        r"manufacturing\s*year\s*[:\-]?\s*(\d{4})",
        r"mfg\s*year\s*[:\-]?\s*(\d{4})",
        r"registration\s*date\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})",
        r"\b(20\d{2})\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = match.group(1)

            if "/" in value:
                return int(value.split("/")[-1])

            return int(value)

    return 2021


# -------------------------------
# POLICY TYPE
# -------------------------------
def extract_policy_type(text: str) -> str:
    if "comprehensive" in text or "package policy" in text:
        return "Comprehensive"
    elif "third party" in text and "own damage" not in text:
        return "Third Party Only"
    elif "own damage" in text:
        return "Own Damage Only"
    return "Comprehensive"


# -------------------------------
# IDV
# -------------------------------
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


# -------------------------------
# VEHICLE NUMBER
# -------------------------------
def extract_vehicle_number(text: str) -> str:
    pattern = r"\b[a-z]{2}[\s-]?\d{2}[\s-]?[a-z]{1,2}[\s-]?\d{4}\b"
    match = re.search(pattern, text)

    if match:
        return match.group(0).upper().replace(" ", "").replace("-", "")

    return "NOT FOUND"


# -------------------------------
# INSURER
# -------------------------------
def extract_insurer(text: str) -> str:
    insurers = {
        "bajaj allianz": "Bajaj Allianz",
        "hdfc ergo": "HDFC ERGO",
        "icici lombard": "ICICI Lombard",
        "tata aig": "Tata AIG",
    }

    for key, value in insurers.items():
        if key in text:
            return value

    return "Unknown Insurer"


# -------------------------------
# ADDONS
# -------------------------------
def extract_addons(text: str) -> list:
    addons = []

    if "zero dep" in text:
        addons.append("Zero Depreciation")

    if "engine protect" in text:
        addons.append("Engine Protection")

    if "roadside" in text:
        addons.append("Roadside Assistance")

    return addons


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def parse_schedule(pdf_path: str) -> dict:
    text = extract_text_from_schedule(pdf_path)

    vehicle_info = extract_vehicle_details(text)
    vehicle_year = extract_vehicle_year(text)

    return {
        "policy_type": extract_policy_type(text),
        "idv": extract_idv(text),
        "vehicle_number": extract_vehicle_number(text),
        "insurer": extract_insurer(text),
        "addons": extract_addons(text),
        "has_zero_dep": "Zero Depreciation" in extract_addons(text),

        # 🔥 VEHICLE INFO
        "make": vehicle_info["make"],
        "model": vehicle_info["model"],
        "year": vehicle_year
    }