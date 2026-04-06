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



from typing import List
import torch
from ultralytics import YOLO
from PIL import Image
import torchvision.transforms as transforms

# -----------------------------
# LOAD MODELS
# -----------------------------

# YOLO model (damage part detection)
yolo_model = YOLO("ml/Damage_Model/best.pt")

# ResNet model (damage classification)
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

# Image transform
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

    for image_path in image_paths:

        # Run YOLO
        results = yolo_model(image_path)

        image = Image.open(image_path).convert("RGB")

        for r in results:
            boxes = r.boxes

            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy()
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, xyxy)

                # Crop detected region
                crop = image.crop((x1, y1, x2, y2))

                # Prepare for ResNet
                img_tensor = transform(crop).unsqueeze(0).to(device)

                with torch.no_grad():
                    outputs = resnet(img_tensor)
                    _, predicted = torch.max(outputs, 1)
                    damage_type = class_names[predicted.item()]
                    damage_conf = torch.softmax(outputs, dim=1)[0][predicted].item()

                # Get part name from YOLO
                part_name = yolo_model.names[cls_id]

                # Simple severity logic
                if damage_conf > 0.85:
                    severity = "high"
                elif damage_conf > 0.6:
                    severity = "medium"
                else:
                    severity = "low"

                damages.append({
                    "part": part_name,
                    "damage_type": damage_type,
                    "casue": "accident",
                    "severity": severity,
                    "confidence": round(damage_conf * 100, 2)
                })

    return {
        "total_damages_found": len(damages),
        "damages": damages,
        "status": "success"
    }