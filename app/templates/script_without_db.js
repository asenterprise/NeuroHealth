document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.addEventListener('click', submitLecture);
});

async function submitLecture() {
    const form = document.getElementById('lectureForm');
    const formData = new FormData(form);

    try {
        //lecture_id = 1
        formData.set('lecture_id', '1');

        const response = await fetch('/lectures-ui/parse', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error("Failed to parse the lecture!");
        }

        const html = await response.text();
        document.open();
        document.write(html);
        document.close();

    } catch (error) {
        alert(error.message);
    }
}