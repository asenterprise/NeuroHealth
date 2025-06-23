# NeuroHealth — PostgreSQL Schema for Lecture Data Storage

This repository contains the initial database schema for the NeuroHealth project — an AI-powered personal knowledge platform designed to structure and retrieve health and fitness lecture content.

## Database Structure (PostgreSQL)

The schema includes two main tables:

### 1. lectures_en

Stores metadata and the full, unsegmented content of each lecture.

| Column      | Type      | Description                               |
|------------|-----------|-------------------------------------------|
| id         | serial    | Primary key (unique lecture ID)            |
| title      | text      | Lecture title                              |
| content    | text      | Full text content of the lecture           |
| created_at | timestamp | Record creation date (default: now)        |

---

### 2. sections_en

Stores individual sections extracted from lectures, including their hierarchy and position.

| Column            | Type   | Description                                      |
|------------------|--------|--------------------------------------------------|
| id               | serial | Primary key (unique section ID)                  |
| lecture_id       | int    | Foreign key linking to lectures_en.id            |
| header           | text   | Section heading or title                         |
| content          | text   | Main text content of the section                 |
| section_type_id  | int    | Reserved for future classification              |
| level_1 to level_4 | text | Hierarchical heading levels (e.g., "1.1", "2.3") |
| section_number   | text   | Full section number (e.g., "2.3.1")               |
| level           | int    | Depth level (1–4) in the hierarchy               |

---

## Why this structure?

- Maintains original lecture data and parsed sections separately.
- Supports semantic search and vector indexing of individual sections.
- Allows future extension with additional metadata (tags, authors, sources).
- Ensures data integrity via foreign key constraints.

---

## License

MIT License — see LICENSE file for details.
