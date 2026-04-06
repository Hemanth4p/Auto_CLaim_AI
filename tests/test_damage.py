from app.services.damage_detection import detect_damage

# Give 1 or 2 sample images
image_paths = [
    "data/uploads/demo1.jpg",
    "data/uploads/demo2.jpg",
    "data/uploads/demo3.jpg"
]

result = detect_damage(image_paths)

print("==== DAMAGE RESULT ====")
print(result)