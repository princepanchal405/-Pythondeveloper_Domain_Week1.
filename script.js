function loadInternships() {
    fetch("/api/internships")
        .then(res => res.json())
        .then(data => display(data));
}

function filterInternships() {
    let company = document.getElementById("filterCompany").value;
    let duration = document.getElementById("filterDuration").value;

    let url = "/api/internships?";

    if (company) url += `company=${company}&`;
    if (duration) url += `duration=${duration}`;

    fetch(url)
        .then(res => res.json())
        .then(data => display(data));
}

function display(data) {
    let list = "";
    data.forEach(i => {
        list += `
        <div class="card p-3 mb-2 shadow-sm">
            <h5>${i.title}</h5>
            <p><b>Company:</b> ${i.company}</p>
            <p><b>Duration:</b> ${i.duration}</p>
            <p><b>Stipend:</b> ${i.stipend || 'N/A'}</p>
            <button class="btn btn-danger" onclick="deleteInternship(${i.id})">Delete</button>
        </div>
        `;
    });
    document.getElementById("list").innerHTML = list;
}

function addInternship() {
    let data = {
        title: document.getElementById("title").value,
        company: document.getElementById("company").value,
        duration: document.getElementById("duration").value,
        stipend: document.getElementById("stipend").value
    };

    fetch("/api/internships", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(() => loadInternships());
}

function deleteInternship(id) {
    fetch(`/api/internships/${id}`, {
        method: "DELETE"
    }).then(() => loadInternships());
}

loadInternships();
