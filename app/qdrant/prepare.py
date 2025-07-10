def build_header_text(section):
    return " ".join([
        section.get("level_1") or "",
        section.get("level_2") or "",
        section.get("level_3") or "",
        section.get("level_4") or ""
    ]).strip()

def prepare_payload(section: dict, include_content=False) -> dict:
    payload = {
        "lecture_id": section.get("lecture_id"),
        "level_1": section.get("level_1") or "",
        "level_2": section.get("level_2") or "",
        "level_3": section.get("level_3") or "",
        "level_4": section.get("level_4") or "",
    }
    if include_content:
        payload["content"] = section.get("content") or ""
    return payload
