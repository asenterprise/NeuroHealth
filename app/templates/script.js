async function submitLecture() {
    const form = document.getElementById('lectureForm');
    const formData = new FormData(form);

    try {
        // 1. Send lecture to /lectures-ui/add
        let response = await fetch('/lectures-ui/add', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error("Failed to save the lecture!");
        }

        let result = await response.json(); // Expect {"lecture_id": 123}
        let lectureId = result.lecture_id;

        if (!lectureId) {
            throw new Error("Failed to get lecture ID!");
        }

        // 2. Add lecture_id to formData and send to /lectures-ui/parse
        formData.append('lecture_id', lectureId);

        response = await fetch('/lectures-ui/parse', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error("Failed to split the lecture into sections!");
        }

        // 3. Load the page with section preview (sections_preview.html)
        let html = await response.text();

        // Clear the page and write new HTML
        document.open();
        document.write(html);
        document.close();

    } catch (error) {
        alert(error.message);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const previewButton = document.getElementById("previewJsonButton");
    const saveButton = document.getElementById("saveToDatabaseButton");

    previewButton.addEventListener("click", function () {
        const jsonData = getJsonFromForm();
        const newWindow = window.open();
        const blob = new Blob([jsonData], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = newWindow.document.createElement('a');
        a.href = url;
        a.download = 'lecture_sections.json';
        newWindow.document.body.appendChild(a);
        a.click();

        setTimeout(() => {
            URL.revokeObjectURL(url);
            newWindow.close();
        }, 100);
    });

    saveButton.addEventListener("click", async function () {
        const formData = prepareSectionData();

        try {
            const response = await fetch('/sections/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error("Failed to save to database!");
            }

            const result = await response.json();
            if (result.success) {
                alert("Sections saved successfully!");
            } else {
                throw new Error(result.message || "Database save failed");
            }
        } catch (error) {
            alert(error.message);
        }
    });

    function prepareSectionData() {
        const form = document.getElementById("saveSectionsForm");
        const formData = new FormData(form);
        const sections = [];
        const sectionCount = formData.getAll("section_numbers[]").length;

        for (let i = 0; i < sectionCount; i++) {
            sections.push({
                lecture_id: formData.get("lecture_id"),
                section_number: formData.getAll("section_numbers[]")[i],
                title: formData.getAll("titles[]")[i],
                level: formData.getAll("levels[]")[i],
                level_1: formData.getAll("level_1[]")[i],
                level_2: formData.getAll("level_2[]")[i],
                level_3: formData.getAll("level_3[]")[i],
                level_4: formData.getAll("level_4[]")[i],
                content: formData.getAll("texts[]")[i]
            });
        }

        return {
            lecture_id: formData.get("lecture_id"),
            sections: sections
        };
    }

    function getJsonFromForm() {
        return JSON.stringify(prepareSectionData(), null, 4);
    }
});