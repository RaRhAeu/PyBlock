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
