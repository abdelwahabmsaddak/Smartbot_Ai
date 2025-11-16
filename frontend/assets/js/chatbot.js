function toggleChat() {
    document.getElementById("chatBody").classList.toggle("hidden");
}

function sendMessage() {
    const box = document.getElementById("chatBody");
    const text = document.getElementById("chatInput").value;

    if(text.trim() === "") return;

    box.innerHTML += `<div class="msg user">${text}</div>`;
    document.getElementById("chatInput").value = "";

    // رد سريع (placeholder)
    setTimeout(() => {
        box.innerHTML += `<div class="msg bot">🤖 سيتم ربط الذكاء الاصطناعي لاحقاً…</div>`;
        box.scrollTop = box.scrollHeight;
    }, 600);
}
