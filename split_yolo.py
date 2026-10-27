from pathlib import Path
import random
import shutil

# Исходные папки
IMAGES_DIR = Path("images")
LABELS_DIR = Path("labels")

# Итоговая структура
OUTPUT_DIR = Path("dataset")

# Доля данных для обучения
TRAIN_RATIO = 0.8

# Поддерживаемые форматы изображений
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Для повторяемого результата при каждом запуске
random.seed(42)


def main():
    if not IMAGES_DIR.exists():
        raise FileNotFoundError(f"Не найдена папка: {IMAGES_DIR.resolve()}")

    if not LABELS_DIR.exists():
        raise FileNotFoundError(f"Не найдена папка: {LABELS_DIR.resolve()}")

    image_paths = [
        path for path in IMAGES_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]

    pairs = []
    missing_labels = []

    for image_path in image_paths:
        label_path = LABELS_DIR / f"{image_path.stem}.txt"

        if label_path.exists():
            pairs.append((image_path, label_path))
        else:
            missing_labels.append(image_path.name)

    if not pairs:
        raise RuntimeError(
            "Не найдено ни одной пары «изображение + одноимённый .txt»."
        )

    random.shuffle(pairs)

    train_count = int(len(pairs) * TRAIN_RATIO)
    train_pairs = pairs[:train_count]
    val_pairs = pairs[train_count:]

    for split_name, split_pairs in (
        ("train", train_pairs),
        ("val", val_pairs),
    ):
        images_out = OUTPUT_DIR / "images" / split_name
        labels_out = OUTPUT_DIR / "labels" / split_name

        images_out.mkdir(parents=True, exist_ok=True)
        labels_out.mkdir(parents=True, exist_ok=True)

        for image_path, label_path in split_pairs:
            shutil.copy2(image_path, images_out / image_path.name)
            shutil.copy2(label_path, labels_out / label_path.name)

    print(f"Готово. Всего пар: {len(pairs)}")
    print(f"Train: {len(train_pairs)}")
    print(f"Val:   {len(val_pairs)}")

    if missing_labels:
        print(f"\nИзображений без соответствующего .txt: {len(missing_labels)}")
        for name in missing_labels:
            print(f"  {name}")


if __name__ == "__main__":
    main()
