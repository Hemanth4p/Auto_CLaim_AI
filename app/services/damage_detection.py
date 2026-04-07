# from typing import List


# def detect_damage(image_paths: List[str]) -> dict:
#     """
#     Detects damage from a list of car images.
#     Currently returns placeholder results.
#     Will be replaced with real YOLOv10 model on Colab day.
#     """

#     damages = [
#         {
#             "part": "front_bumper",
#             "damage_type": "dent",
#             "cause": "accident",
#             "severity": "high",
#             "confidence": 88.5
#         },
#         {
#             "part": "left_headlight",
#             "damage_type": "shatter",
#             "cause": "accident",
#             "severity": "high",
#             "confidence": 92.1
#         },
#         {
#             "part": "door_panel",
#             "damage_type": "scratch",
#             "cause": "accident",
#             "severity": "low",
#             "confidence": 76.3
#         }
#     ]

#     return {
#         "total_damages_found": len(damages),
#         "damages": damages,
#         "status": "placeholder - real YOLOv10 model coming soon"
#     }




# from typing import List
# import torch
# from ultralytics import YOLO
# from PIL import Image
# import torchvision.transforms as transforms
# import cv2
# import os

# # -----------------------------
# # LOAD MODELS
# # -----------------------------

# # YOLO model (damage part detection)
# yolo_model = YOLO("ml/Damage_Model/best.pt")

# # ResNet model (damage classification)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# checkpoint = torch.load("ml/Damage_Model/damage_classifier.pth", map_location=device)

# from torchvision import models
# import torch.nn as nn

# resnet = models.resnet50(pretrained=False)
# num_features = resnet.fc.in_features
# resnet.fc = nn.Sequential(
#     nn.Linear(num_features, 256),
#     nn.ReLU(),
#     nn.Dropout(0.4),
#     nn.Linear(256, 4)
# )

# resnet.load_state_dict(checkpoint['model_state_dict'])
# resnet.to(device)
# resnet.eval()

# class_names = checkpoint['classes']

# # Image transform
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406],
#                          [0.229, 0.224, 0.225])
# ])

# # -----------------------------
# # MAIN FUNCTION
# # -----------------------------

# def detect_damage(image_paths: List[str]) -> dict:

#     damages = []

#     # Create debug folders
#     os.makedirs("debug_outputs", exist_ok=True)
#     os.makedirs("debug_crops", exist_ok=True)

#     for image_path in image_paths:

#         print(f"\n🔍 Processing: {image_path}")

#         # Run YOLO with confidence threshold
#         results = yolo_model(image_path, conf=0.5)

#         image = Image.open(image_path).convert("RGB")
#         img_cv = cv2.imread(image_path)

#         for r in results:
#             boxes = r.boxes

#             print(f"Detected {len(boxes)} objects")

#             for box in boxes:
#                 xyxy = box.xyxy[0].cpu().numpy()
#                 cls_id = int(box.cls[0])
#                 conf = float(box.conf[0])

#                 # Skip low confidence detections
#                 if conf < 0.5:
#                     continue

#                 part_name = yolo_model.names[cls_id]

#                 x1, y1, x2, y2 = map(int, xyxy)

#                 # Safety bounds
#                 x1, y1 = max(0, x1), max(0, y1)
#                 x2, y2 = min(image.width, x2), min(image.height, y2)

#                 # Crop detected region
#                 crop = image.crop((x1, y1, x2, y2))

#                 # Save crop (debug)
#                 crop_filename = f"{part_name}_{x1}_{y1}.jpg"
#                 crop.save(os.path.join("debug_crops", crop_filename))

#                 # Prepare for ResNet
#                 img_tensor = transform(crop).unsqueeze(0).to(device)

#                 with torch.no_grad():
#                     outputs = resnet(img_tensor)
#                     _, predicted = torch.max(outputs, 1)
#                     damage_type = class_names[predicted.item()]
#                     damage_conf = torch.softmax(outputs, dim=1)[0][predicted].item()

#                 # Draw bounding box
#                 label = f"{part_name}-{damage_type}"

#                 cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(
#                     img_cv,
#                     label,
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     (0, 255, 0),
#                     2
#                 )

#                 # Severity logic
#                 if damage_conf > 0.85:
#                     severity = "high"
#                 elif damage_conf > 0.6:
#                     severity = "medium"
#                 else:
#                     severity = "low"

#                 print(f"{part_name} → {damage_type} ({damage_conf:.2f})")

#                 damages.append({
#                     "part": part_name,
#                     "damage_type": damage_type,
#                     "cause": "accident",
#                     "severity": severity,
#                     "confidence": round(damage_conf * 100, 2)
#                 })

#         # Save debug image with boxes
#         output_path = os.path.join("debug_outputs", os.path.basename(image_path))
#         cv2.imwrite(output_path, img_cv)

#         print(f"✅ Saved debug image: {output_path}")

#     return {
#         "total_damages_found": len(damages),
#         "damages": damages,
#         "status": "success"
#     }


# from typing import List
# import torch
# from ultralytics import YOLO
# from PIL import Image
# import torchvision.transforms as transforms
# import cv2
# import os

# # -----------------------------
# # LOAD MODELS
# # -----------------------------

# # YOLO model (damage part detection)
# yolo_model = YOLO("ml/Damage_Model/best.pt")

# # ResNet model (damage classification)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# checkpoint = torch.load("ml/Damage_Model/damage_classifier.pth", map_location=device)

# from torchvision import models
# import torch.nn as nn

# resnet = models.resnet50(pretrained=False)
# num_features = resnet.fc.in_features
# resnet.fc = nn.Sequential(
#     nn.Linear(num_features, 256),
#     nn.ReLU(),
#     nn.Dropout(0.4),
#     nn.Linear(256, 4)
# )

# resnet.load_state_dict(checkpoint['model_state_dict'])
# resnet.to(device)
# resnet.eval()

# class_names = checkpoint['classes']

# # Image transform
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406],
#                          [0.229, 0.224, 0.225])
# ])

# def detect_damage(image_paths: List[str]) -> dict:

#     damages = []

#     os.makedirs("debug_outputs", exist_ok=True)
#     os.makedirs("debug_crops", exist_ok=True)

#     for image_path in image_paths:

#         print(f"\n🔍 Processing: {image_path}")

#         results = yolo_model(image_path, conf=0.5)

#         image = Image.open(image_path).convert("RGB")
#         img_cv = cv2.imread(image_path)

#         image_area = image.width * image.height  # 🔥 important

#         for r in results:
#             boxes = r.boxes
#             print(f"Detected {len(boxes)} objects")

#             for box in boxes:
#                 xyxy = box.xyxy[0].cpu().numpy()
#                 cls_id = int(box.cls[0])
#                 conf = float(box.conf[0])

#                 if conf < 0.5:
#                     continue

#                 part_name = yolo_model.names[cls_id]

#                 x1, y1, x2, y2 = map(int, xyxy)

#                 # Safe bounds
#                 x1, y1 = max(0, x1), max(0, y1)
#                 x2, y2 = min(image.width, x2), min(image.height, y2)

#                 # -----------------------------
#                 # AREA CALCULATION (RELATIVE)
#                 # -----------------------------
#                 area = (x2 - x1) * (y2 - y1)
#                 damage_ratio = area / image_area   # 🔥 key improvement

#                 # Crop
#                 crop = image.crop((x1, y1, x2, y2))

#                 # Save crop
#                 crop_filename = f"{part_name}_{x1}_{y1}.jpg"
#                 crop.save(os.path.join("debug_crops", crop_filename))

#                 # Classification
#                 img_tensor = transform(crop).unsqueeze(0).to(device)

#                 with torch.no_grad():
#                     outputs = resnet(img_tensor)
#                     _, predicted = torch.max(outputs, 1)
#                     damage_type = class_names[predicted.item()]
#                     damage_conf = torch.softmax(outputs, dim=1)[0][predicted].item()

#                 # Draw box
#                 label = f"{part_name}-{damage_type}"
#                 cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(
#                     img_cv,
#                     label,
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     (0, 255, 0),
#                     2
#                 )

#                 # -----------------------------
#                 # 🔥 NEW SEVERITY LOGIC (AREA BASED)
#                 # -----------------------------
#                 if damage_ratio > 0.20:
#                     severity = "high"
#                 elif damage_ratio > 0.08:
#                     severity = "medium"
#                 else:
#                     severity = "low"

#                 print(
#                     f"{part_name} → {damage_type} | "
#                     f"Conf: {damage_conf:.2f} | "
#                     f"Ratio: {damage_ratio:.3f}"
#                 )

#                 damages.append({
#                     "part": part_name,
#                     "damage_type": damage_type,
#                     "cause": "accident",
#                     "severity": severity,
#                     "confidence": round(damage_conf * 100, 2),
#                     "area": area,
#                     "damage_ratio": round(damage_ratio, 3)  # 🔥 new field
#                 })

#         # Save debug image
#         output_path = os.path.join("debug_outputs", os.path.basename(image_path))
#         cv2.imwrite(output_path, img_cv)
#         print(f"✅ Saved debug image: {output_path}")

#     return {
#         "total_damages_found": len(damages),  # 🔥 keep duplicates
#         "damages": damages,
#         "status": "success"
#     }




from typing import List
import torch
from ultralytics import YOLO
from PIL import Image
import torchvision.transforms as transforms
import cv2
import os

# -----------------------------
# LOAD MODELS
# -----------------------------
yolo_model = YOLO("ml/Damage_Model/best.pt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = torch.load("ml/Damage_Model/damage_classifier.pth", map_location=device)

from torchvision import models
import torch.nn as nn

resnet = models.resnet50(pretrained=False)
num_features = resnet.fc.in_features
resnet.fc = nn.Sequential(
    nn.Linear(num_features, 256),
    nn.ReLU(),
    nn.Dropout(0.4),
    nn.Linear(256, 4)
)

resnet.load_state_dict(checkpoint['model_state_dict'])
resnet.to(device)
resnet.eval()

class_names = checkpoint['classes']

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def detect_damage(image_paths: List[str]) -> dict:

    damages = []

    os.makedirs("debug_outputs", exist_ok=True)

    for image_path in image_paths:

        print(f"\n🔍 Processing: {image_path}")

        results = yolo_model(image_path, conf=0.5)

        image = Image.open(image_path).convert("RGB")
        img_cv = cv2.imread(image_path)

        image_area = image.width * image.height

        for r in results:
            boxes = r.boxes

            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy()
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                if conf < 0.5:
                    continue

                part_name = yolo_model.names[cls_id]

                x1, y1, x2, y2 = map(int, xyxy)

                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(image.width, x2), min(image.height, y2)

                area = (x2 - x1) * (y2 - y1)
                damage_ratio = area / image_area

                # -----------------------------
                # CLASSIFICATION
                # -----------------------------
                crop = image.crop((x1, y1, x2, y2))
                img_tensor = transform(crop).unsqueeze(0).to(device)

                with torch.no_grad():
                    outputs = resnet(img_tensor)
                    _, predicted = torch.max(outputs, 1)
                    damage_type = class_names[predicted.item()]
                    damage_conf = torch.softmax(outputs, dim=1)[0][predicted].item()

                label = f"{part_name}-{damage_type}"

                # -----------------------------
                # 🔥 BETTER BOUNDING BOX
                # -----------------------------
                cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 4)

                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

                cv2.rectangle(img_cv, (x1, y1 - 30), (x1 + w, y1), (0, 255, 0), -1)

                cv2.putText(
                    img_cv,
                    label,
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2
                )

                # -----------------------------
                # SEVERITY
                # -----------------------------
                if damage_ratio > 0.20:
                    severity = "high"
                elif damage_ratio > 0.08:
                    severity = "medium"
                else:
                    severity = "low"

                damages.append({
                    "part": part_name,
                    "damage_type": damage_type,
                    "severity": severity,
                    "confidence": round(damage_conf * 100, 2),
                    "area": area,
                    "damage_ratio": round(damage_ratio, 3)
                })

        # -----------------------------
        # SAVE OUTPUT
        # -----------------------------
        base = os.path.basename(image_path)

        cv2.imwrite(f"debug_outputs/{base}", img_cv)

        # 🔥 HEATMAP
        heatmap = img_cv.copy()
        overlay = img_cv.copy()

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)

        heatmap = cv2.addWeighted(img_cv, 0.7, overlay, 0.3, 0)

        cv2.imwrite(f"debug_outputs/heatmap_{base}", heatmap)

    return {
        "total_damages_found": len(damages),
        "damages": damages,
        "status": "success"
    }