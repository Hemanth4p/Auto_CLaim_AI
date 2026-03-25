def identify_vehicle(image_path: str) -> dict:
    """
    Identifies the vehicle make, model and year from an image.
    Currently returns a placeholder response.
    Will be replaced with real ResNet-50 model on Colab day.
    """

    return {
        "make": "Tata",
        "model": "Nexon",
        "year": "2021",
        "variant": "XZ+",
        "confidence": 91.5,
        "status": "placeholder - real model coming soon"
    }