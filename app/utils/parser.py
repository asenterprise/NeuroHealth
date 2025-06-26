import re
from typing import List, Dict

def parse_lecture(content: str) -> List[Dict[str, str]]:
    sections = []
    # Matches headings like "1.", "1.1.", "2.3.4." followed by a space and text
    pattern = re.compile(r"^(\d+(?:\.\d+)*\.)\s(.+)$", re.MULTILINE)

    matches = list(pattern.finditer(content))
    hierarchy = {1: "", 2: "", 3: "", 4: ""}  # Store current titles at each heading level

    for i, match in enumerate(matches):
        number = match.group(1).strip()  # e.g., "1.", "1.1.", "1.1.1."
        title = match.group(2).strip()   # Heading title text

        level = number.count(".")        # Determine heading depth (1 = top level)
        level = min(level, 4)            # Limit to a maximum of 4 levels

        # Update heading hierarchy
        hierarchy[level] = title
        for lvl in range(level + 1, 5):  # Clear sublevels after current level
            hierarchy[lvl] = ""

        start_pos = match.end()                            # Start of section content
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_text = content[start_pos:end_pos].strip()  # Extract section text

        sections.append({
            "number": number,
            "title": title,
            "level": level,
            "level_1": hierarchy[1] if level >= 1 else "",
            "level_2": hierarchy[2] if level >= 2 else "",
            "level_3": hierarchy[3] if level >= 3 else "",
            "level_4": hierarchy[4] if level >= 4 else "",
            "content": section_text
        })

    return sections
