import requests
from datetime import datetime, timedelta


def get_data_for_chart(id):
    # Получаем данные из API
    url = f"http://127.0.0.1:8000/api/view/data?id={id}&filter=month"
    response = requests.get(url)
    data = response.json()["data"]

    # Преобразуем данные в формат, необходимый для Chart.js
    labels = []
    values = []
    for item in data:
        date_str = item["date"]
        count_view = item["count_view"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        labels.append(date_obj.strftime("%d.%m.%Y"))
        values.append(count_view)

    # Добавляем последний день текущего месяца, чтобы график был полным
    end_of_month = datetime.now().replace(day=1, month=datetime.now().month + 1) - timedelta(days=1)
    if end_of_month > datetime.now():
        end_of_month = datetime.now()
    if labels[-1] != end_of_month.strftime("%d.%m.%Y"):
        labels.append(end_of_month.strftime("%d.%m.%Y"))
        values.append(0)

    return {"labels": labels, "values": values}
