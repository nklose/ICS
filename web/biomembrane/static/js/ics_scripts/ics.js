   $(function() {
    $( "#sortable-img" ).sortable();
    $( "#sortable-img" ).disableSelection();
   });

  var selected = null;
  $('a[data-toggle="tab"]').on('shown', function (e) {
   selected = e.target // activated tab
   e.relatedTarget // previous tab
   $("#id_userSelected").val(selected.id);
   $("#userNotice").val(selected.id).html(showSelected(selected.id) +" is Selected");
  });

  $('#start').button();
   $('#start').click(function() {
    $(this).button('loading');
    // Then whatever you actually want to do i.e. submit form
    // After that has finished, reset the button state using
    // $(this).button('reset');
  });

  function showSelected(value)
  {
    if (value == "id_auto")
    {
      return "<strong>Note</strong>: Auto Correlation";
    }
    else if (value == 'id_cross')
    {
      return "<strong>Note</strong>: Cross Correlation";
    }
    else if (value == 'id_triplecross')
    {
      return "<strong>Note</strong>: Triple Correlation";
    }
    else if (value == 'id_all')
    {
      return "<strong>Note</strong>: All Correlations";
    }
    else
    {
      return "<strong>Note</strong>: Please Select a Correlation Type";
    }
  }
