import json
from pydantic import BaseModel
from typing import Dict, Union, List
from fastapi import FastAPI, Request

app = FastAPI()

# Define data schema for input JSON
class SectionData(BaseModel):
    lecture_id: List[Union[int, str]]
    section_numbers: List[str]
    titles: List[str]
    levels: List[Union[int, str]]  # Allow both strings and numbers for manual conversion
    level_1: List[str]
    level_2: List[str]
    level_3: List[str]
    level_4: List[str]
    texts: List[str]

async def process_lecture_json(json_data: Dict) -> Dict:
    """Process lecture JSON data into structured sections."""
    sections = []
    lecture_id = 0  # Default value if processing fails

    try:
        # Get and validate lecture ID
        lecture_id = json_data.get("lecture_id", ["0"])[0]
        lecture_id = int(lecture_id) if str(lecture_id).isdigit() else 0

        # Unpack and validate all arrays
        section_numbers = json_data.get("section_numbers[]", [])
        titles = json_data.get("titles[]", [])
        contents = json_data.get("texts[]", [])
        levels = json_data.get("levels[]", [])
        level_1 = json_data.get("level_1[]", [])
        level_2 = json_data.get("level_2[]", [])
        level_3 = json_data.get("level_3[]", [])
        level_4 = json_data.get("level_4[]", [])

        # Validate array lengths match
        num_sections = len(section_numbers)
        required_arrays = [titles, contents, levels, level_1, level_2, level_3, level_4]
        if not all(len(lst) == num_sections for lst in required_arrays):
            raise ValueError("Invalid JSON structure: array lengths don't match")

        # Process each section
        for i in range(num_sections):
            try:
                level = levels[i]
                if isinstance(level, str) and level.isdigit():
                    level = int(level)
                elif not isinstance(level, int):
                    raise ValueError(f"Invalid level format: {level}")

                section = {
                    "number": str(section_numbers[i]).strip(),
                    "title": str(titles[i]).strip(),
                    "content": str(contents[i]).strip(),
                    "level": level,
                    "level_1": str(level_1[i]).strip(),
                    "level_2": str(level_2[i]).strip(),
                    "level_3": str(level_3[i]).strip(),
                    "level_4": str(level_4[i]).strip()
                }
                sections.append(section)
            except (IndexError, ValueError) as e:
                raise ValueError(f"Error processing section {i}: {str(e)}")

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error processing data: {str(e)}")

    return {"lecture_id": lecture_id, "sections": sections}