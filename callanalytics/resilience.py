"""Gemini chaqiruvlarini barqaror qilish: qayta urinish, kvota tugashi va doimiy bloklar."""

import json
import time

from google.genai import errors as genai_errors


class ContentBlockedError(Exception):
    """
    Gemini audio mazmunini xavfsizlik siyosati bo'yicha bloklaganda (masalan
    PROHIBITED_CONTENT) ko'tariladi - bu doimiy holat, qayta urinish
    natijani o'zgartirmaydi. Vaqtinchalik xatolardan (tarmoq, kvota) farqli
    ravishda, chaqiruvchi kod buni "qayta urinishga arzimaydi" deb belgilashi kerak.
    """

    def __init__(self, block_reason):
        self.block_reason = block_reason
        super().__init__(f"Gemini audioni bloklagan: {block_reason}")


def call_with_retry(fn, max_retries: int = 5, base_delay: float = 2.0):
    """Server xatolari (5xx) va 429 da eksponensial kutish bilan qayta uriniladi.
    Model buzuq JSON qaytarsa ham qayta so'raladi. Boshqa 4xx xatolar darhol ko'tariladi."""
    for attempt in range(1, max_retries + 1):
        try:
            return fn()
        except genai_errors.ServerError:
            if attempt == max_retries:
                raise
            time.sleep(base_delay * (2 ** (attempt - 1)))
        except genai_errors.ClientError as e:
            if getattr(e, "code", None) != 429 or attempt == max_retries:
                raise
            time.sleep(base_delay * (2 ** (attempt - 1)))
        except json.JSONDecodeError:
            if attempt == max_retries:
                raise
            time.sleep(base_delay)


def is_quota_exceeded_error(exc: Exception) -> bool:
    """Gemini loyihaning xarajat chegarasi tugaganini aniqlaydi. Bunday holatda yozuv haqiqiy
    xato emas, faqat hozircha ishlanmagan hisoblanadi va keyinroq qayta olinadi."""
    text = str(exc)
    return "RESOURCE_EXHAUSTED" in text or "spending cap" in text.lower()


def usage_to_dict(usage) -> dict:
    """Gemini javobidagi token sarfini (modallik bo'yicha ham) lug'atga aylantiradi,
    har bir qo'ng'iroq narxini kuzatish uchun."""
    if usage is None:
        return {}
    modality_breakdown = {}
    for details_field in ("prompt_tokens_details", "candidates_tokens_details"):
        details = getattr(usage, details_field, None) or []
        for item in details:
            key = f"{details_field}:{item.modality}"
            modality_breakdown[key] = item.token_count
    return {
        "prompt_token_count": usage.prompt_token_count,
        "candidates_token_count": usage.candidates_token_count,
        "thoughts_token_count": getattr(usage, "thoughts_token_count", None),
        "cached_content_token_count": getattr(usage, "cached_content_token_count", None),
        "total_token_count": usage.total_token_count,
        "modality_breakdown": modality_breakdown,
    }
