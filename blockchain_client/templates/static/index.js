$(function(){
  $('input').click(function(){
    $.ajax({
      url: '/wallet/new',
      type: 'GET',
      success: function(response){
        document.getElementById("private_key").innerHTML = response['private_key'];
        document.getElementById("public_key").innerHTML = response['public_key'];
        document.getElementById("warning").style.display = "block";
      },
      error: function(error){
        console.log(error);
      }
    });
  });
})
WTF????? JUST SUBMIT A FORM XDDD

function generate() {
  fetch('/wallet/new')
  .then((res) => {
    res.json()
  }).then((data) => {
    document.getElementById("private_key").innerHTML = data.private_key;
    document.getElementById("public_key").innerHTML = data.publickey;
    document.getElementById("warning").style.display = "block";
  })
}


<script>
      $(function () {
          $("#generate_transaction").click(function () {
            $.ajax({
              url: "/generate/transaction",
              type: "POST",
              dataType : 'json',
              data: $('#transaction_form').serialize(),
              success: function(response){
                document.getElementById("confirmation_sender_address").value = response["transaction"]["sender_address"];
                document.getElementById("confirmation_recipient_address").value = response["transaction"]["recipient_address"];
                document.getElementById("confirmation_amount").value = response["transaction"]["value"];
                document.getElementById("transaction_signature").value = response["signature"];
                $("#basicModal").modal('show');

              },
              error: function(error){
                console.log(error);
              }
            });
          });
      });
      $(function () {
          $("#button_confirm_transaction").click(function () {
            //console.log($('#confirmation_transaction_form').serialize());
            $.ajax({
              url: document.getElementById("node_url").value + "/transactions/new",
              type: "POST",
              headers: {'Access-Control-Allow-Origin':'*'},
              dataType : 'json',
              data: $('#confirmation_transaction_form').serialize(),
              success: function(response){
                //reset both forms
                $("#transaction_form")[0].reset();
                $("#confirmation_transaction_form")[0].reset();

                //clean text boxes
                $("#sender_address").val("");
                $("#sender_private_key").val("");
                $("#recipient_address").val("");
                $("#amount").val("");
                $("#basicModal").modal('hide');
                $("#success_transaction_modal").modal('show');

              },
              error: function(error){
                console.log(error);
              }
            });
          });
      });
    </script>

async function view_transactions() {
  // TODO: change to node IP
  const res = await fetch("127.0.0.1:5000/chain");
  const data = await res.json();
  const transactions = [];
  for(let i = 1; i < data.length; i++) {
    for(let j = 0; j< data["chain"][i]["transactions"].length; j++) {
      var opts = {  year: "numeric", month: "short",  day: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit"  };
      var formattedDateTime = date.toLocaleTimeString("en-us", options);
      let transaction = [count,
                    response["chain"][i]["transactions"][j]["recipient_address"],
                    response["chain"][i]["transactions"][j]["sender_address"],
                    response["chain"][i]["transactions"][j]["value"],
                    formattedDateTime,
                    response["chain"][i]["block_number"]];
      transactions.push(transaction);
    }
  }
  console.table(transactions);
}

    <script>
      $(function(){

        $('#view_transactions').click(function(){
          $.ajax({
            url: document.getElementById("node_url").value + "/chain",
            type: 'GET',
            success: function(response){
              console.log(response);
              //Generate Transactions Table
              var transactions = [];
              count = 1;
              for (i = 1; i < response.length; i++) {
                for (j = 0; j < response["chain"][i]["transactions"].length; j++) {
                  //format date
                  var options = {  year: "numeric", month: "short",  day: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit"  };
                  var date = new Date(response["chain"][i]["timestamp"] * 1000);
                  var formattedDateTime = date.toLocaleTimeString("en-us", options);
                  transaction = [count,
                                response["chain"][i]["transactions"][j]["recipient_address"],
                                response["chain"][i]["transactions"][j]["sender_address"],
                                response["chain"][i]["transactions"][j]["value"],
                                formattedDateTime,
                                response["chain"][i]["block_number"]];
                  transactions.push(transaction);
                  count += 1;
                };
              };
              // Restrict a column to 10 characters, do split words
                $('#transactions_table').dataTable( {
                  data: transactions,
                  columns: [{ title: "#" },
                            { title: "Recipient Address"},
                            { title: "Sender Address"},
                            { title: "Value"},
                            { title: "Timestamp"},
                            { title: "Block"}],
                  columnDefs: [ {targets: [1,2,3,4,5], render: $.fn.dataTable.render.ellipsis( 25 )}]
                } );
            },
            error: function(error){
              console.log(error);
            }
          });
        });
      })
    </script>
