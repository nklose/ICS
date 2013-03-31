   /* Jquery functions to control aspects of the web page */

   // Makes images sortable
   $(function() {
    $( "#sortable-img" ).sortable();
    $( "#sortable-img" ).disableSelection();
   });

  // Enables tab functionality
  var selected = null;
  $('a[data-toggle="tab"]').on('shown', function (e) {
   selected = e.target // activated tab
   e.relatedTarget // previous tab
  localStorage.setItem('lastTab', $(e.target).attr('id'));

  // Get which correlation selected by user
  if ($("#id_userSelected") != null)
        $("#id_userSelected").val(selected.id);

  // Get upload type selected by user
  if ($("#id_uploadType") != null)
        $("#id_uploadType").val(selected.id);
   $("#userNotice").val(selected.id).html(showSelected(selected.id) +" is Selected");
  });

  var lastTab = localStorage.getItem('lastTab');
  if (lastTab) {
      $('#'+lastTab).tab('show');
  }

 // Start Button 'Loading' Functionality
 $('#start').on('click', function () {
  $(this).button('loading')
  $('#settings-form').submit();
  })

  // Return which correlation is selected
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
    else if (value == 'id_triple')
    {
      return "<strong>Note</strong>: Triple Correlation";
    }
    else if (value == 'id_all')
    {
      return "<strong>Note</strong>: All Correlations";
    }
    else if (value == 'id_singleRGB')
    {
      return "<strong>Note</strong>: Single RGB Option";
    }
    else if (value == 'id_threeRGB')
    {
      return "<strong>Note</strong>: Three Image Channels Option";
    }
    else
    {
      return "<strong>Note</strong>: Please Choose an option";
    }
  }

  function getTabId(value) {

    if (value == "id_auto")
    {
      return "#auto";
    }
    else if (value == 'id_cross')
    {
      return '#cross';
    }
    else if (value == 'id_triplecross')
    {
      return "#triple";
    }
    else if (value == 'id_all')
    {
      return '#all';
    }
    else {
      return null;
    }
  }
