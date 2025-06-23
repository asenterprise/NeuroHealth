-- Создание таблицы lectures_en
CREATE TABLE lectures_en (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Создание таблицы sections_en
CREATE TABLE sections_en (
    id SERIAL PRIMARY KEY,
    lecture_id INTEGER REFERENCES lectures_en(id),
    header TEXT,
    content TEXT,
    section_type_id INTEGER,
    level_1 TEXT,
    level_2 TEXT,
    level_3 TEXT,
    level_4 TEXT,
    section_number TEXT,
    level INTEGER CHECK (level BETWEEN 1 AND 4)
);