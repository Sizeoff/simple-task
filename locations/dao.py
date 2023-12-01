import time
import random
from datetime import datetime, timedelta
from typing import List
from benchmark import timing


@timing
def get_current_dislocation() -> List:
    """
    Формирование текущей дислокации вагонов. 
    Получаем список вагонов и их дату прибытия.
    Каждый вагон может быть привязан к одной и той же накладной!
    Для того, чтобы получить предсказанную дату прибытия, необходимо вызывать сервис 'get_predicted_dates'
    """
    locations = []
    arrivale_dates = [None, None, None, datetime.now() - timedelta(days=3), datetime.now()]
    time.sleep(2)

    for i in range(0, 20000):
        arrivale_date = random.choice(arrivale_dates)
        location = {
            "wagon": random.randint(10000, 90000),
            "invoice": f"{random.randint(1, 30000)}__HASH__",
            "arrivale_date": arrivale_date.strftime("%d.%m.%Y") if arrivale_date else None,
        }
        locations.append(location)

    return locations


@timing
def get_predicted_date_by_invoices(invoices: List) -> List:
    """
    На вход необходимо передать список из уникальных накладных. 
    По каждой накладной будет сформировано время прибытия
    """
    time.sleep(1)
    predicted_results = []
    for invoice in invoices:
        predicted_date = datetime.now() + timedelta(days=random.randint(1, 5))
        data = {
            "invoice": invoice,
            "predicted_date": predicted_date.strftime("%d.%m.%Y")
        }
        predicted_results.append(data)

    return predicted_results


@timing
def api_call() -> List:
    """
    В качестве ответа должен выдаваться повагонный список из сервиса get_current_dislocation 
    с обновленной датой прибытия вагона из сервиса get_predicted_dates
    только по вагоном, у которых она отсутствует
    """
    locations = get_current_dislocation()

    # Получить список уникальных накладных из текущей дислокации только по тем вагонам,
    # где arrivale_date = None
    invoices = set([x['invoice'] for x in locations if x['arrivale_date'] == None])

    if len(invoices) == 0:
        '''Если ошибочно был подан список без пробелов в 'arrivale_date' '''

        return locations

    predicted_data = get_predicted_date_by_invoices(list(invoices))

    # Обновить оригинальный список вагонов данными, которые прислал сервис get_predicted_dates().\
    # Заменить вагоны, где arrivale_date = None на соответствующее поле predicted_date.
    for wag in locations:
        '''Хотел бы уточнить логику: если два вагона с одинаковым значением накладной один с датой и один без даты,
        как быть в данной ситуации не регламентировано. Если сервис get_predicted_date_by_invoices в боевых условиях 
        гарантированно дает одну дату для всех поездов с общей накладной, то дополнительной проверки не требуется
        Если нет, на всякий случай добавил проверку содержимого wag['arrivale_date'] и тогда с одной накладной 
        могут оказаться два вагона с разными датами: одна - если уже имелась изначально,
        вторая - после get_predicted_date_by_invoices.
        Можно было бы еще присвоить одну дату для вагонов с одинаковой накладной, если хотя бы для одного уже 
        указана дата, но такового не требовалось в явном виде в условии задачи'''

        if wag['invoice'] in invoices and wag['arrivale_date'] is None:
            wag.update({'arrivale_date': (
                [pred['predicted_date'] for pred in predicted_data if pred['invoice'] == wag['invoice']][0])})

    return locations
