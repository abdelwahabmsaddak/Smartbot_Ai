let profit = 0, trades = 0;
const profitEl = document.getElementById("profit");
const tradesEl = document.getElementById("trades");

function simulateTrade() {
  const result = Math.random() > 0.4 ? "win" : "loss";
  const amount = Math.floor(Math.random() * 50) + 10;
  trades++;
  if (result === "win") profit += amount;
  else profit -= amount / 2;
  profitEl.textContent = "$" + profit;
  tradesEl.textContent = trades;
}
