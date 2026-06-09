function toggleComments(ideaId) {
    const box = document.getElementById(`comments-${ideaId}`);

    if (!box) {
        console.error(`Container comments-${ideaId} non trovato`);
        return;
    }

    if (box.style.display === "block") {
        box.style.display = "none";
    } else {
        box.style.display = "block";
        loadComments(ideaId);
    }
}

async function loadComments(ideaId) {
    try {
        const list = document.getElementById(`list-${ideaId}`);

        if (!list) {
            console.error(`list-${ideaId} non trovato`);
            return;
        }

        const response = await fetch(`/ideas/${ideaId}/comments/`);

        if (!response.ok) {
            throw new Error(`Errore HTTP: ${response.status}`);
        }

        const data = await response.json();

        list.innerHTML = "";

        data.forEach(comment => {
            const div = document.createElement("div");

            div.className = comment.is_admin
                ? "comment admin-comment"
                : "comment";

            div.innerHTML = comment.is_admin
                ? `</strong>${comment.text}`
                : `</strong> ${comment.text}`;

            list.appendChild(div);
        });

    } catch (error) {
        console.error("Errore caricamento commenti:", error);
    }
}

async function addComment(ideaId) {
    try {
        const input = document.getElementById(`input-${ideaId}`);

        if (!input) {
            console.error(`input-${ideaId} non trovato`);
            return;
        }

        const text = input.value.trim();

        if (!text) return;

        const response = await fetch(`/ideas/${ideaId}/comments/add/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        console.log("Risposta server:", data);

        if (!response.ok) {
            alert(data.error || "Errore durante l'invio");
            return;
        }

        input.value = "";

        await loadComments(ideaId);

    } catch (error) {
        console.error("Errore invio commento:", error);
    }
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

console.log("comments.js caricato");