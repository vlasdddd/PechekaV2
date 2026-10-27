from pathlib import Path
from ultralytics import YOLO

model = YOLO("bestV1.pt")
exported_file = Path(model.export(format="onnx", opset=12, simplify=True))

exported_file.replace("best.onnx")
print("Готово: best.onnx")
