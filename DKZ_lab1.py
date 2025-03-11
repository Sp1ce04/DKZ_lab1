import os
import platform
import psutil
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live


def get_system_info():
    return {
        "ОС": platform.system() + " " + platform.release(),
        "Процесор": platform.processor(),
        "Кількість ядер": psutil.cpu_count(logical=False),
        "Завантаження CPU": f"{psutil.cpu_percent()}%",
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Завантаження RAM": f"{psutil.virtual_memory().percent}%",
        "Диски": get_disks_info(),
        "Останнє оновлення": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
    }


def get_disks_info():
    disks = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disks.append(f"{partition.device} {round(usage.total / (1024 ** 3), 2)} GB ({usage.percent}%)")
    return "\n".join(disks)


def create_table():
    system_info = get_system_info()
    table = Table(title="Системна інформація", show_header=True, header_style="bold magenta")
    table.add_column("Метрика", style="bold cyan")
    table.add_column("Значення", style="bold yellow")

    for key, value in system_info.items():
        table.add_row(key, str(value))

    return table


def main():
    console = Console()
    with Live(auto_refresh=True, console=console) as live:
        while True:
            live.update(create_table())
            time.sleep(1)


if __name__ == "__main__":
    main()

hi