# Поток данных телеметрии от серверов кластера
system_telemetry = [
    ("srv_01", 12.5, 64, "online"),
    ("srv_02", 85.0, 92, "online"),
    ("srv_03", 0.0, 0, "offline"),
    ("srv_04", 45.2, 78, "online"),
    ("srv_05", 95.1, 99, "online")
]

# Реализация конвейера агрегации метрик

# Распаковка кортежей и фильтрация offline-серверов
active_servers = [
    (node_name, cpu_load, ram_usage)
    for node_name, cpu_load, ram_usage, status in system_telemetry
    if status != "offline"
]

# Формирование списка имен активных серверов
active_node_names = [node_name for node_name, cpu_load, ram_usage in active_servers]

# Формирование отдельных списков показателей для агрегации
cpu_loads = [cpu_load for node_name, cpu_load, ram_usage in active_servers]
ram_usages = [ram_usage for node_name, cpu_load, ram_usage in active_servers]

# Рассчёт суммарных показателей через len(), sum(), max()
active_count = len(active_node_names)
average_cpu = round(sum(cpu_loads) / active_count, 2)
max_ram = max(ram_usages)

# Формирование итогового вложенного словаря
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