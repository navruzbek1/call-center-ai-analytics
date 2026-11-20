"""Gemini'dan tuzilmali (structured output) javob olish uchun JSON sxema NAMUNASI.

Haqiqiy tizimdagi modullar, kategoriyalar va baholash qoidalari bu yerda yo'q.
Quyidagi qiymatlar faqat sxema tuzilishini ko'rsatish uchun uydirma.
"""

EXAMPLE_CATEGORIES_BY_MODULE = {
    "Kassa": ["Kassa-Printer", "Kassa-Smena yopilmayapti", "Kassa-To'lov o'tmayapti"],
    "Ombor": ["Ombor-Kirim", "Ombor-Narx o'zgartirish"],
    "Boshqa": ["Noto'g'ri murojaat"],
}

_MEZON_SCHEMA = {
    "type": "object",
    "properties": {
        "ball": {"type": "integer", "nullable": True},
        "max": {"type": "integer"},
    },
    "required": ["ball", "max"],
}

EXAMPLE_SCHEMA = {
    "type": "object",
    "properties": {
        "audio_transkripsiyasi": {"type": "string"},
        "modul": {"type": "string", "enum": list(EXAMPLE_CATEGORIES_BY_MODULE)},
        "sabab_kategoriyasi": {"type": "string"},
        "muammo_holati": {"type": "string", "enum": ["Dastur xatosi", "Tushunmovchilik", "Muammo hal bo'lgan", "Boshqa"]},
        "suhbat_holati": {"type": "string", "enum": ["ODDIY", "TO'SATDAN_UZILGAN", "OLDINGI_SUHBAT_DAVOMI"]},
        "operator_ohangi": {"type": "string", "enum": ["Hushmuomala", "Neytral", "Beparvo/loqayd", "Jahl bilan/qo'pol"]},
        "confidence": {"type": "number"},
        "ai_bahosi": {"type": "string"},
        "operator_ai_hulosa": {
            "type": "object",
            "properties": {
                "salomlashish": _MEZON_SCHEMA,
                "diagnostika_yechim": _MEZON_SCHEMA,
                "savollarga_javob": _MEZON_SCHEMA,
                "xayrlashuv": _MEZON_SCHEMA,
            },
        },
    },
    "required": ["modul", "sabab_kategoriyasi", "muammo_holati", "suhbat_holati", "confidence"],
}
