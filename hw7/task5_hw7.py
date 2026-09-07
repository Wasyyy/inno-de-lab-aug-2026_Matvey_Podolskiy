# Поток данных телеметрии от серверов кластера
system_telemetry = [
    ("srv_01", 12.5, 64, "online"),
    ("srv_02", 85.0, 92, "online"),
    ("srv_03", 0.0, 0, "offline"),
    ("srv_04", 45.2, 78, "online"),
    ("srv_05", 95.1, 99, "online")
]

# Единый проход: распаковка, фильтрация и сбор метрик одновременно
active_node_names = []
cpu_loads = []
ram_usages = []

for node_name, cpu_load, ram_usage, status in system_telemetry:
    if status != "offline":
        active_node_names.append(node_name)
        cpu_loads.append(cpu_load)
        ram_usages.append(ram_usage)

active_count = len(active_node_names)

# Защита от ZeroDivisionError, если все серверы offline
if active_count == 0:
    average_cpu = 0.0
    max_ram = 0
else:
    average_cpu = round(sum(cpu_loads) / active_count, 2)
    max_ram = max(ram_usages)

report = {
    "active_nodes_count": active_count,
    "metrics": {
        "average_cpu": average_cpu,
        "max_ram": max_ram
    }
}

print(f"Активные узлы в сети: {active_node_names}")
print("Итоговый отчет телеметрии:")
print(report)
