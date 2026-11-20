"""Model natijasini tekshirish: noto'g'ri juftliklarni ushlash va shubhali natijalarni belgilash."""

UNKNOWN_CATEGORY = "NOANIQ HOLAT"


def validate_module_category(data: dict, categories_by_module: dict[str, list[str]]) -> dict:
    """Sabab kategoriyasi tanlangan modulga tegishli bo'lmasa, uni "NOANIQ HOLAT" ga tushiradi
    va ishonchni pasaytiradi. Model ba'zan boshqa modulning kategoriyasini tanlab yuboradi."""
    modul = data.get("modul", "")
    kategoriya = data.get("sabab_kategoriyasi", "")
    valid_categories = categories_by_module.get(modul, [])
    if kategoriya not in valid_categories and kategoriya != UNKNOWN_CATEGORY:
        data["sabab_kategoriyasi"] = UNKNOWN_CATEGORY
        data["confidence"] = min(data.get("confidence", 1.0), 0.3)
        data["_validation_flag"] = "modul_va_kategoriya_mos_kelmadi"
    return data


def flag_low_confidence(data: dict, threshold: float = 0.5) -> dict:
    """Ishonch past bo'lsa, natijani inson ko'rib chiqishi uchun belgilaydi."""
    if data.get("confidence", 1.0) < threshold:
        data["_needs_review"] = True
    return data
