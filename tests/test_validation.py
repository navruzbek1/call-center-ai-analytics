from callanalytics.schema_example import EXAMPLE_CATEGORIES_BY_MODULE as CATS
from callanalytics.validation import UNKNOWN_CATEGORY, flag_low_confidence, validate_module_category


def test_valid_pair_is_kept():
    data = {"modul": "Kassa", "sabab_kategoriyasi": "Kassa-Printer", "confidence": 0.9}
    out = validate_module_category(dict(data), CATS)
    assert out == data


def test_category_from_another_module_becomes_unknown():
    data = {"modul": "Kassa", "sabab_kategoriyasi": "Ombor-Kirim", "confidence": 0.9}
    out = validate_module_category(data, CATS)
    assert out["sabab_kategoriyasi"] == UNKNOWN_CATEGORY
    assert out["confidence"] == 0.3
    assert out["_validation_flag"] == "modul_va_kategoriya_mos_kelmadi"


def test_confidence_is_never_raised():
    data = {"modul": "Kassa", "sabab_kategoriyasi": "Yo'q", "confidence": 0.1}
    assert validate_module_category(data, CATS)["confidence"] == 0.1


def test_unknown_category_is_allowed():
    data = {"modul": "Kassa", "sabab_kategoriyasi": UNKNOWN_CATEGORY, "confidence": 0.8}
    out = validate_module_category(data, CATS)
    assert "_validation_flag" not in out and out["confidence"] == 0.8


def test_low_confidence_is_flagged_for_review():
    assert flag_low_confidence({"confidence": 0.4})["_needs_review"] is True
    assert "_needs_review" not in flag_low_confidence({"confidence": 0.5})
    assert "_needs_review" not in flag_low_confidence({})
