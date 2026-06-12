from decimal import Decimal
from .models import ImportCostRule


def predict_import_cost(car, delivery_city=None):
    rule = ImportCostRule.objects.filter(
        origin_country=car.origin_country,
        is_active=True
    ).first()

    if not rule:
        return None

    car_price = Decimal(car.price)

    customs_fees = car_price * (rule.customs_rate / Decimal("100"))
    insurance_fees = car_price * (rule.insurance_rate / Decimal("100"))

    performance_factor = Decimal("0")

    if car.power_hp >= 600:
        performance_factor = Decimal("0.10")
    elif car.power_hp >= 400:
        performance_factor = Decimal("0.07")
    elif car.power_hp >= 250:
        performance_factor = Decimal("0.04")

    performance_extra = car_price * performance_factor

    age_extra = Decimal("0")

    if car.year < 2000:
        age_extra = Decimal("3000")
    elif car.year < 2010:
        age_extra = Decimal("1500")

    delivery_fee = Decimal("0")

    if delivery_city:
        delivery_fee = Decimal(delivery_city.delivery_price)

    predicted_import_cost = (
        rule.base_shipping_cost
        + customs_fees
        + insurance_fees
        + rule.processing_fee
        + performance_extra
        + age_extra
    )

    total_estimated_cost = (
        car_price
        + predicted_import_cost
        + delivery_fee
    )

    return {
        "car_price": car_price,
        "base_shipping_cost": rule.base_shipping_cost,
        "customs_fees": customs_fees,
        "insurance_fees": insurance_fees,
        "processing_fee": rule.processing_fee,
        "performance_extra": performance_extra,
        "age_extra": age_extra,
        "delivery_fee": delivery_fee,
        "predicted_import_cost": predicted_import_cost,
        "total_estimated_cost": total_estimated_cost,
        "estimated_days": rule.estimated_days,
    }