
# from datetime import datetime


# def check_fraud(exif, incident_date):
#     """
#     Fraud detection based on EXIF metadata.

#     Returns:
#         fraud (bool)
#         reason (str)
#     """

#     # ⚠️ Case 1: No EXIF data
#     if not exif:
#         return False, "No EXIF data (cannot verify image authenticity)"

#     # ⚠️ Case 2: Missing timestamp
#     if "DateTimeOriginal" not in exif:
#         return False, "Timestamp missing in metadata"

#     try:
#         # 📸 Extract photo timestamp
#         photo_date = datetime.strptime(
#             exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S"
#         )

#         # 📅 Parse incident date
#         incident_date = datetime.strptime(incident_date, "%Y-%m-%d")

#         # ✅ IMPORTANT FIX: Compare ONLY DATE (ignore time)
#         photo_date_only = photo_date.date()
#         incident_date_only = incident_date.date()

#         diff = (incident_date_only - photo_date_only).days

#         # 🚨 Fraud: Photo taken BEFORE incident (too old)
#         if diff > 2:
#             return True, "Image captured well before incident (possible fraud)"

#         # 🚨 Fraud: Photo taken AFTER incident
#         if diff < 0:
#             return True, "Image captured after incident (invalid evidence)"

#     except Exception:
#         return False, "Metadata parsing error"

#     # ✅ Valid case
#     return False, "Image metadata verified (appears valid)"



from datetime import datetime


def check_fraud(exif, incident_date):
    """
    Fraud detection based on EXIF metadata.

    Rules:
    - No EXIF → Suspicious (Fraud)
    - Missing timestamp → Suspicious (Fraud)
    - Image too old → Fraud
    - Image taken after incident → Fraud
    - Otherwise → Valid

    Returns:
        fraud (bool)
        reason (str)
    """

    # ⚠️ Case 1: No EXIF data
    if not exif:
        return True, "No EXIF data (suspicious image)"

    # ⚠️ Case 2: Missing timestamp
    if "DateTimeOriginal" not in exif:
        return True, "Timestamp missing in metadata (suspicious)"

    try:
        # 📸 Extract photo timestamp
        photo_date = datetime.strptime(
            exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S"
        )

        # 📅 Parse incident date
        incident_date_obj = datetime.strptime(incident_date, "%Y-%m-%d")

        # Compare ONLY date (ignore time)
        photo_date_only = photo_date.date()
        incident_date_only = incident_date_obj.date()

        diff = (incident_date_only - photo_date_only).days

        # 🚨 Fraud: Image too old
        if diff > 2:
            return True, "Image captured well before incident (possible fraud)"

        # 🚨 Fraud: Image after incident
        if diff < 0:
            return True, "Image captured after incident (invalid evidence)"

    except Exception as e:
        return True, f"Metadata parsing error (suspicious): {str(e)}"

    # ✅ Valid case
    return False, "Image metadata verified (appears valid)"