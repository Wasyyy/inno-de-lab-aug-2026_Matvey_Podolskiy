# Список транзакций, полученных от платежного шлюза
raw_transactions = ["SUCCESS:100", "FAILED:50", "SUCCESS:-10", "SUCCESS:0", "SUCCESS:250", "ERROR:200"]

# Реализация фильтрации в одну строку с помощью List Comprehension
valid_amounts = [int(amount) for status, amount in (t.split(":") for t in raw_transactions) if status == "SUCCESS" and int(amount) > 0]

print(f"ОЧищенные транзакции:{valid_amounts}")