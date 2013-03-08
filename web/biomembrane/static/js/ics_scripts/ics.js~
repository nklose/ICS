   $(function() {
    $( "#sortable-img" ).sortable();
    $( "#sortable-img" ).disableSelection();
   });

  $('a[data-toggle="tab"]').on('shown', function (e) {
   e.target // activated tab
   e.relatedTarget // previous tab
  });

  $('#start').button();
   $('#start').click(function() {
    $(this).button('loading');
    // Then whatever you actually want to do i.e. submit form
    // After that has finished, reset the button state using
    // $(this).button('reset');
  });

$(function() {
    var select = $( "#resolutions" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( select ).slider({
      min: 1,
      max: 5,
      range: "min",
      value: select[ 0 ].selectedIndex + 1,
      slide: function( event, ui ) {
        select[ 0 ].selectedIndex = ui.value - 1;
      }
    });
    $( "#resolutions" ).change(function() {
      slider.slider( "value", this.selectedIndex + 1 );
    });
  });
