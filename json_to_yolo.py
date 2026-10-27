import json
from pathlib import Path

# Папки относительно корня проекта
JSON_DIR = Path("images")
LABELS_DIR = Path("labels")

# Порядок должен совпадать с class.txt:
# строка 1 — ID 0, строка 2 — ID 1
CLASS_IDS = {
    "game": 0,
    "pokypki": 1,
}


def convert_json_to_yolo(json_path: Path) -> None:
    try:
        data = json.loads(json_path.read_text(encoding="utf-8-sig"))
    except Exception as error:
        print(f"Ошибка чтения {json_path}: {error}")
        return

    width = data.get("imageWidth")
    height = data.get("imageHeight")
    shapes = data.get("shapes", [])

    print(
        f"\n{json_path.name}: "
        f"размер изображения={width}x{height}, "
        f"фигур={len(shapes)}, "
        f"классы={[shape.get('label') for shape in shapes]}"
    )

    if not width or not height:
        print("Пропуск: в JSON нет imageWidth или imageHeight.")
        return

    lines = []

    for shape in shapes:
        label = shape.get("label")
        if label not in CLASS_IDS:
            print(f"Пропуск неизвестного класса: {label!r}")
            continue

        points = shape.get("points", [])
        if len(points) < 2:
            print(f"Пропуск фигуры без достаточного числа точек: {label}")
            continue

        xs = [float(point[0]) for point in points]
        ys = [float(point[1]) for point in points]

        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        # YOLO: class_id x_center y_center box_width box_height
        x_center = ((x_min + x_max) / 2) / width
        y_center = ((y_min + y_max) / 2) / height
        box_width = (x_max - x_min) / width
        box_height = (y_max - y_min) / height

        lines.append(
            f"{CLASS_IDS[label]} "
            f"{x_center:.6f} {y_center:.6f} "
            f"{box_width:.6f} {box_height:.6f}"
        )

    LABELS_DIR.mkdir(parents=True, exist_ok=True)
    txt_path = LABELS_DIR / f"{json_path.stem}.txt"
    txt_path.write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8"
    )

    if lines:
        print(f"Создан {txt_path}: записано объектов — {len(lines)}")
    else:
        print(f"Создан пустой файл {txt_path}: подходящих фигур не найдено.")


def main() -> None:
    if not JSON_DIR.exists():
        print(f"Папка не найдена: {JSON_DIR.resolve()}")
        return

    json_files = list(JSON_DIR.glob("*.json"))
    if not json_files:
        print(f"В папке {JSON_DIR.resolve()} нет файлов .json")
        return

    print(f"Найдено JSON-файлов: {len(json_files)}")
    for json_path in json_files:
        convert_json_to_yolo(json_path)


if __name__ == "__main__":
    main()
