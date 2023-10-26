from typing import Optional

from pydantic import BaseModel, RootModel


class DeliveryOreder(BaseModel):
    """
    Модель заказа для доставки.

    Attributes:
    ----------
    id: int
        Уникальный идентификатор заказа.

    description: Optional[str]
        Необязательное описание содержимого заказа.

    address: str
        Адрес, по которому необходимо доставить заказ.

    is_prepared: bool
        Статус подготовки заказа. Если True - заказ готов к доставке.

    is_delivered: bool
        Статус доставки заказа. Если True - заказ доставлен.
    """

    id: int
    description: Optional[str]
    address: str
    is_prepared: bool
    is_delivered: bool

