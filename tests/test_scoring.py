from callanalytics.scoring import compute_ai_bahosi


def hulosa(**balls):
    maxes = {"salomlashish": 1, "diagnostika_yechim": 5, "savollarga_javob": 1, "xayrlashuv": 1}
    return {name: {"ball": ball, "max": maxes.get(name, 1)} for name, ball in balls.items()}


def test_sum_of_criteria_replaces_model_value():
    data = {"ai_bahosi": "9", "suhbat_holati": "ODDIY",
            "operator_ai_hulosa": hulosa(salomlashish=1, diagnostika_yechim=4, savollarga_javob=1, xayrlashuv=1)}
    out = compute_ai_bahosi(data)
    assert out["ai_bahosi"] == "7"
    assert out["_ai_bahosi_model"] == "9"


def test_matching_model_value_is_not_flagged():
    data = {"ai_bahosi": "3", "operator_ai_hulosa": hulosa(salomlashish=1, diagnostika_yechim=2)}
    out = compute_ai_bahosi(data)
    assert out["ai_bahosi"] == "3"
    assert "_ai_bahosi_model" not in out


def test_star_when_diagnosis_not_scored_because_problem_already_solved():
    data = {"muammo_holati": "Muammo hal bo'lgan",
            "operator_ai_hulosa": hulosa(salomlashish=1, diagnostika_yechim=None, xayrlashuv=1)}
    assert compute_ai_bahosi(data)["ai_bahosi"] == "2*"


def test_no_star_for_other_problem_states():
    data = {"muammo_holati": "Dastur xatosi", "operator_ai_hulosa": hulosa(salomlashish=1, diagnostika_yechim=None)}
    assert compute_ai_bahosi(data)["ai_bahosi"] == "1"


def test_cut_off_call_gets_plus_suffix():
    data = {"suhbat_holati": "TO'SATDAN_UZILGAN", "operator_ai_hulosa": hulosa(salomlashish=1, diagnostika_yechim=5)}
    assert compute_ai_bahosi(data)["ai_bahosi"] == "6+"


def test_continuation_call_gets_plus_prefix():
    data = {"suhbat_holati": "OLDINGI_SUHBAT_DAVOMI", "operator_ai_hulosa": hulosa(salomlashish=None, diagnostika_yechim=4)}
    assert compute_ai_bahosi(data)["ai_bahosi"] == "+4"


def test_booleans_are_not_counted_as_points():
    data = {"operator_ai_hulosa": {"salomlashish": {"ball": True, "max": 1}, "xayrlashuv": {"ball": 1, "max": 1}}}
    assert compute_ai_bahosi(data)["ai_bahosi"] == "1"


def test_missing_criteria_leaves_data_unchanged():
    data = {"ai_bahosi": "5"}
    assert compute_ai_bahosi(data) == {"ai_bahosi": "5"}
