import time

import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO

model = YOLO(r"runs\detect\cookie_detector-3\weights\best.pt")

CONFIDENCE_THRESHOLD = 0.7
CLICK_OFFSET_Y = 30
pyautogui.FAILSAFE = True


def find_object(target_class):
    screenshot = np.array(pyautogui.screenshot())
    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    results = model.predict(
        source=screenshot_bgr,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False,
    )

    # Выбираем обнаружение с наибольшей уверенностью
    best_detection = None
    best_confidence = -1

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name != target_class:
                continue

            confidence = float(box.conf[0])
            if confidence > best_confidence:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2) - CLICK_OFFSET_Y
                best_detection = (center_x, center_y)
                best_confidence = confidence

    if best_detection:
        print(
            f"Найден {target_class}, "
            f"уверенность {best_confidence:.2f}: {best_detection}"
        )

    return best_detection


def click_object_three_times(target_class):
    point = find_object(target_class)

    if point is None:
        print(
            f"{target_class} не найден. "
            "Проверьте имя класса и попробуйте временно снизить "
            "CONFIDENCE_THRESHOLD, например до 0.5."
        )
        return

    for click_number in range(3):
        print(f"Клик {click_number + 1}/3 по {target_class}: {point}")
        pyautogui.click(*point)
        time.sleep(0.1)


print("Скрипт запущен. Для остановки нажмите Ctrl+C.")

try:
    while True:
        click_object_three_times("game")
        click_object_three_times("pokypki")

except KeyboardInterrupt:
    print("\nСкрипт остановлен.")
