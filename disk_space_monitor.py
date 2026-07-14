#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# disk_space_monitor.py
# Мониторинг свободного места на диске с цветным выводом и уведомлениями.

import os
import shutil
import argparse
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

def convert_to_bytes(value, unit):
    if unit == "KB":
        return value * 1024
    elif unit == "MB":
        return value * 1024 * 1024
    elif unit == "GB":
        return value * 1024 * 1024 * 1024
    else:
        raise ValueError(f"Неизвестная единица: {unit}")

def send_notification(message):
    try:
        subprocess.run(['notify-send', 'Мониторинг диска', message])
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="мониторинг свободного места на диске")
    parser.add_argument("--path", default="/", help="путь для проверки")
    parser.add_argument("--threshold", type=float, default=10.0, help="порог свободного места")
    parser.add_argument("--unit", default="GB", choices=["KB", "MB", "GB"], help="единица измерения")
    parser.add_argument("--notify", action="store_true", help="отправить уведомление")
    args = parser.parse_args()

    threshold_bytes = convert_to_bytes(args.threshold, args.unit)
    total, used, free = shutil.disk_usage(args.path)

    free_gb = free / (1024**3)
    threshold_gb = args.threshold

    # цветной вывод
    if free_gb > threshold_gb * 1.5:
        color = Fore.GREEN
        status = "хорошо"
    elif free_gb > threshold_gb:
        color = Fore.YELLOW
        status = "внимание"
    else:
        color = Fore.RED
        status = "критично"

    print(f"{Fore.CYAN}Диск {args.path}:{Style.RESET_ALL}")
    print(f"Свободно: {color}{free_gb:.2f} ГБ{Style.RESET_ALL} из {total/(1024**3):.2f} ГБ")
    print(f"Статус: {color}{status}{Style.RESET_ALL} (порог {threshold_gb} ГБ)")

    if free_gb < threshold_gb and args.notify:
        message = f"Свободно {free_gb:.2f} ГБ (порог {threshold_gb} ГБ)"
        send_notification(message)

if __name__ == "__main__":
    main()
