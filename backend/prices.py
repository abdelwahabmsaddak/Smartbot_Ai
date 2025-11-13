// أسعار تجريبية محلية (يمكن لاحقًا ربط API عام)
const t = (id,val)=>{ const el=document.getElementById(id); if(el) el.textContent = val; };

function mockPrices(){
  // مجرد أرقام متغيرة لإظهار الحركة
  const base = Date.now()/1000;
  const btc = 104000 + Math.sin(base/10)*400;
  const eth = 3500 + Math.cos(base/9)*30;
  const floki = 0.00004 + Math.sin(base/6)*0.000002;
  const pepe = 0.0000002 + Math.cos(base/7)*0.00000003;

  t('t-btc', btc.toFixed(0));
  t('t-eth', eth.toFixed(0));
  t('t-floki', floki.toFixed(8));
  t('t-pepe', pepe.toFixed(8));
}
mockPrices();
setInterval(mockPrices, 2000);
