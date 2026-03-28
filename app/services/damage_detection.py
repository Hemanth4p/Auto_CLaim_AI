from typing import List


def detect_damage(image_paths: List[str]) -> dict:
    """
    Detects damage from a list of car images.
    Currently returns placeholder results.
    Will be replaced with real YOLOv10 model on Colab day.
    """

    damages = [
        {
            "part": "front_bumper",
            "damage_type": "dent",
            "cause": "accident",
            "severity": "high",
            "confidence": 88.5
        },
        {
            "part": "left_headlight",
            "damage_type": "shatter",
            "cause": "accident",
            "severity": "high",
            "confidence": 92.1
        },
        {
            "part": "door_panel",
            "damage_type": "scratch",
            "cause": "accident",
            "severity": "low",
            "confidence": 76.3
        }
    ]

    return {
        "total_damages_found": len(damages),
        "damages": damages,
        "status": "placeholder - real YOLOv10 model coming soon"
    }