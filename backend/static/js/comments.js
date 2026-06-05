function toggleComments(ideaId) {
    const box = document.getElementById(`comments-${ideaId}`);

    if (box.style.display === "block") {
        box.style.display = "none";
        return;
    }

    box.style.display = "block";
    loadComments(ideaId);
}

async function loadComments(ideaId) {
    const list = document.getElementById(`list-${ideaId}`);

    const res = await fetch(`/ideas/${ideaId}/comments/`);
    const data = await res.json();

    list.innerHTML = "";

    data.forEach(c => {
        const div = document.createElement("div");
        div.classList.add("comment");
        div.innerText = c.text;
        list.appendChild(div);
    });
}

async function addComment(ideaId) {
    const input = document.getElementById(`input-${ideaId}`);

    if (!input.value.trim()) return;

    await fetch(`/ideas/${ideaId}/comments/add/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            text: input.value
        })
    });

    input.value = "";
    loadComments(ideaId);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const c = cookies[i].trim();
            if (c.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}