async function sendMessage() {
    let input = document.getElementById("chatInput");
    let box = document.getElementById("chatBody");

    let userMsg = input.value;
    box.innerHTML += `<div class='user-msg'>${userMsg}</div>`;
    input.value = "";

    let res = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: userMsg})
    });

    let data = await res.json();
    box.innerHTML += `<div class='bot-msg'>${data.reply}</div>`;
}
