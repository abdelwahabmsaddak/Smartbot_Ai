// ================== MARKET AUTO-UPDATE ==================
async function loadPrices() {
    try {
        document.getElementById("btc").innerText = "↑ 67,200$";
        document.getElementById("eth").innerText = "↑ 3,250$";
        document.getElementById("gold").innerText = "↓ 2314$";
        document.getElementById("sp").innerText = "↑ 5100$";
    } catch (e) {}
}
setInterval(loadPrices, 2000);
loadPrices();

// ================== SEARCH ==================
function searchNow() {
    let q = document.getElementById("searchInput").value;
    if (q.trim() === "") return alert("اكتب اسم العملة أو السهم");

    window.location.href = "analyze.html?item=" + q;
}

// ================== CHAT ==================
function toggleChat() {
    let box = document.getElementById("chatbot");
    box.style.display = box.style.display === "block" ? "none" : "block";
}
