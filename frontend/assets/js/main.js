async function updatePrices() {
    let res = await fetch("/api/prices");
    let data = await res.json();

    document.getElementById("btc_price").innerHTML = data.btc;
    document.getElementById("eth_price").innerHTML = data.eth;
}

setInterval(updatePrices, 5000);
updatePrices();
