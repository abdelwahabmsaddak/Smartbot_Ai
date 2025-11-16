function startSearch() {
    const q = document.getElementById("searchInput").value.trim();
    if(q === "") return alert("اكتب اسم العملة أو السهم");

    window.location.href = `analyze.html?query=${q}`;
}

// مثال أسعار (لاحقاً نربط API)
document.getElementById("btc_price").innerText = "↑ 72,100$";
document.getElementById("eth_price").innerText = "↓ 3,550$";
document.getElementById("gold_price").innerText = "↑ 2,420$";
document.getElementById("sp_price").innerText = "↑ 5,180";
