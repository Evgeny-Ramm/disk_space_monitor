import subprocess
import os
import argparse
import shutil

def convert_to_bytes(value, unit):
    if unit == "KB":
        return value * 1024
    elif unit == "MB":
        return value * 1024 * 1024
    elif unit == "GB":
        return value * 1024 * 1024 * 1024
    else:
        raise ValueError(f"Неизвестная единица: {unit}")

def check_disk_space(path, threshold_bytes):
    total, used, free = shutil.disk_usage(path)
    return free < threshold_bytes

def send_notification(message):
    try:
        result = subprocess.run(['notify-send', 'Мониторинг диска', message], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Ошибка notify-send: {result.stderr}")
    except Exception as e:
        print(f"Исключение: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Мониторинг свободного места на диске")
    parser.add_argument("--path", default="/", help="Путь для проверки (по умолчанию /)")
    parser.add_argument("--threshold", type=float, default=10.0, help="Порог свободного места (число)")
    parser.add_argument("--unit", default="GB", choices=["KB", "MB", "GB"], help="Единица измерения")
    parser.add_argument("--notify", action="store_true", help="Отправить уведомление через notify-send")
    return parser.parse_args()

def main():
    os.environ['DISPLAY'] = ':0'
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'  # 1000 замени на свой uid
    args = parse_arguments()
    threshold_bytes = convert_to_bytes(args.threshold, args.unit)
    if check_disk_space(args.path, threshold_bytes):
        message = f"Внимание! Свободного места на {args.path} осталось менее {args.threshold} {args.unit}"
        print(message)
        if args.notify:
            send_notification(message)
    else:
        print(f"Свободного места достаточно (порог {args.threshold} {args.unit})")

if __name__ == "__main__":
    main()
