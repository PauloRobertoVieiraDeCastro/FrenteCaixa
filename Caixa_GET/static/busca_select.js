$(document).ready(function(){


	$("#codigo").select2({
		theme: 'bootstrap4',
      	width: 'style',
      	placeholder: $(this).attr('placeholder'),
      	//closeOnSelect: truek,

	})

	$("#codigo").focus();
	
	/*$('select').each(function () {
    		$(this).select2({
      			theme: 'bootstrap4',
      			width: 'style',
      			placeholder: $(this).attr('placeholder'),
      			allowClear: Boolean($(this).data('allow-clear')),
    		});
 });*/
});

$(document).on('select2:open', function(e) {
  document.querySelector(`[aria-controls="select2-${e.target.id}-results"]`).focus();
});