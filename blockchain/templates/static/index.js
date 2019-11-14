async function get_transactions() {
  const data = await fetch("/transactions/get");
  const djson = await data.json();
  const transactions = [];
  console.log(djson);

}
