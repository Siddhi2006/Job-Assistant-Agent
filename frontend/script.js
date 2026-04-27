const BASE_URL = "http://127.0.0.1:5000";

/* ---------------- NAVIGATION ---------------- */
function show(section) {

    document.querySelectorAll('.section').forEach(div => {
        div.classList.remove('active');
        div.classList.add('hidden');
    });

    document.getElementById(section).classList.add('active');
    document.getElementById(section).classList.remove('hidden');
}


/* ---------------- MAIN FUNCTION ---------------- */
async function runModule(module) {

    let formData = new FormData();
    formData.append("module", module);

    if (module === "resume" || module === "skills" ||
        module === "match" || module === "recommend" ||
        module === "gap" || module === "roadmap") {

        let file = document.getElementById("resumeFile")?.files[0];

        if (file) {
            formData.append("resume", file);
        }
    }

    if (module === "jobs") {
        formData.append("role", document.getElementById("role").value);
    }

    if (module === "chat") {
        formData.append("question", document.getElementById("question").value);
    }

    const res = await fetch(`${BASE_URL}/process`, {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    const outputMap = {
        resume: "resumeResult",
        skills: "skillsResult",
        jobs: "jobsResult",
        match: "matchResult",
        recommend: "recommendResult",
        gap: "gapResult",
        roadmap: "roadmapResult"
    };

    if (module === "chat") {
        document.getElementById("chatBox").innerHTML +=
            `<p><b>You:</b> ${document.getElementById("question").value}</p>
             <p><b>AI:</b> ${data.result}</p>`;
    } else {
        document.getElementById(outputMap[module]).innerText = data.result;
    }
}