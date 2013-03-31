var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
$('#userNotice').hide();
$("body").bind("ajaxSend", function(elm, xhr, s){
   if (s.type == "POST") {
      xhr.setRequestHeader('X-CSRF-Token', csrf_token);
   }
});

function requestDelete(id)
{
  $('input[name=batchid]').val(id);
}

function batchDestroy() {
var batchId = $('input[name=batchid]').val();
var data = { batchToDelete: batchId, csrfmiddlewaretoken: csrf_token };
$.post('/batchResults', data, function(response) {

  if (response == 1)
  {
    $('#userNotice').html("Batch Successfully Removed, <strong>Refreshing Page...<strong>");
    $("#userNotice").attr('alert alert-info');
    $('#userNotice').show(1000);
    setTimeout("location.reload(true);", 2500);
    
  }
  else if (response == -1)
  {
    $('#userNotice').html("Batch Removal Unsuccessful");
    $("#userNotice").attr('alert alert-error');
    $('#userNotice').show(1000)
  }

  $('#ConfirmDeleteModal').modal('hide')
});

}
