document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function (event) {

            const name = document.querySelector('input[name="name"]').value.trim();
            const skills = document.querySelector('input[name="skills"]').value.trim();
            const experience = document.querySelector('textarea[name="experience"]').value.trim();

            if (name === "" || skills === "" || experience === "") {
                alert("Please fill in all the fields.");
                event.preventDefault();
                return;
            }

            alert("Resume Generated Successfully!");
        });
    }

});