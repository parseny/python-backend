from celery import Celery
from config import REDIS_URL, RMQ_URL
from schemas import DeliveryOreder
from shared import order_items

celery_app = Celery('tasks', broker=RMQ_URL, backend=REDIS_URL)

@celery_app.task(name="tasks.accept_order")
def accept_order(order_description: str) -> DeliveryOreder:
    """
    Принять заказ и добавить в список заказов.
    
    :param order_description: Описание заказа.
    :return: DeliveryOreder
    """
    new_order = {
        "id": len(order_items),
        "description": order_description,
        "is_prepared": False,
        "is_delivered": False
    }
    order_items.append(new_order)
    return DeliveryOreder(**new_order)
    

@celery_app.task(name="tasks.prepare_order")
def prepare_order(order_id: int) -> DeliveryOreder:
    """
    Начать готовить заказ.

    :param order_id: ID заказа для подготовки.
    :return: DeliveryOreder
    """
    for item in order_items:
        if item["id"] == order_id:
            order_to_prepare = item
        else:
            order_to_prepare = None
    if order_to_prepare:
        order_to_prepare["is_prepared"] = True
        deliver_order.delay(order_to_prepare["id"])
    return DeliveryOreder(**order_to_prepare)


@celery_app.task(name="tasks.deliver_order")
def deliver_order(order_id: int) -> DeliveryOreder:
    """
    Доставить заказ.
    
    :param order_id: ID заказа для доставки.
    :return: DeliveryOreder
    """
    order_to_deliver = next((item for item in order_items if item["id"] == order_id), None)
    if order_to_deliver:
        order_to_deliver["is_delivered"] = True
    return DeliveryOreder(**order_to_deliver)
