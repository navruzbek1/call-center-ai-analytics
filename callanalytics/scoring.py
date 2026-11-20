"""Operatorga AI bahosini mezon ballaridan aniq (deterministik) hisoblash."""


def compute_ai_bahosi(data: dict) -> dict:
    """
    ai_bahosi'ni model yozgan qiymatdan emas, operator_ai_hulosa'dagi mezon
    ballaridan hisoblaydi.

    Sabab: model JSON'ni schema tartibida yozadi va ai_bahosi
    operator_ai_hulosa'dan OLDIN keladi - yakuniy ball mezonlar
    baholanishidan oldin "taxmin" qilinadi. Natijada ba'zan yig'indiga mos
    kelmaydi (masalan 3 o'rniga "4*") yoki ortiqcha so'z qo'shiladi
    ("7 setup"). Model yozgan qiymat farq qilsa "_ai_bahosi_model"da qoladi.

    Belgilar:
      "*"  -- diagnostika/yechim mezoni muammo holati sababli baholanmagan
      "N+" -- suhbat to'satdan uzilgan (baholab bo'lmagan mezonlar chiqarilgan)
      "+N" -- oldingi suhbatning davomi (salomlashish oldingi qo'ng'iroqda bo'lgan)
    """
    hulosa = data.get("operator_ai_hulosa")
    if not isinstance(hulosa, dict):
        return data
    total = sum(
        m["ball"] for m in hulosa.values()
        if isinstance(m, dict) and isinstance(m.get("ball"), int) and not isinstance(m.get("ball"), bool)
    )
    diag = hulosa.get("diagnostika_yechim")
    star = (
        isinstance(diag, dict) and diag.get("ball") is None
        and data.get("muammo_holati") in ("Muammo hal bo'lgan", "Boshqa")
    )
    baho = f"{total}{'*' if star else ''}"
    if data.get("suhbat_holati") == "TO'SATDAN_UZILGAN":
        baho += "+"
    elif data.get("suhbat_holati") == "OLDINGI_SUHBAT_DAVOMI":
        baho = "+" + baho
    if baho != data.get("ai_bahosi"):
        data["_ai_bahosi_model"] = data.get("ai_bahosi")
    data["ai_bahosi"] = baho
    return data
