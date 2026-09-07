# Список ролей, переданный в запросе на авторизацию (содержит повторы)
requested_roles = ["guest", "developer", "guest", "admin", "developer", "guest"]

# Набор обязательных ролей для выполнения административных функций
required_admin_roles = {"admin", "security_officer", "audit_manager"}

# Преобразование списка в множество для удаления дубликатов
unique_requested_roles = set(requested_roles)

# Пересечение множеств роли, присутствующие и там, и там
common_admin_roles = unique_requested_roles & required_admin_roles

# Разность множеств обязательные роли, которых нет среди запрошенных
missing_admin_roles = required_admin_roles - unique_requested_roles

# Проверка наличия роли через оператор in
has_security_officer = "security_officer" in unique_requested_roles

print(f"Уникальные запрошенные роли: {unique_requested_roles}")
print(f"Общие административные роли: {common_admin_roles}")
print(f"Недостающие административные роли: {missing_admin_roles}")
print(f"Наличие роли security_officer в запросе: {has_security_officer}")