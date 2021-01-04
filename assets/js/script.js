/*function load() {
		
}*/

$(document).mouseup(function (e){
	var div = $(".selectValueBox");
	if (!div.is(e.target) && div.has(e.target).length === 0) {
		$('.selectValueBox ul').slideUp(200)
	}
});

jQuery(document).ready(function($){	
	$('.menuBtn').on('click', function() {
    $('body').toggleClass('menuOpen');
    $('.menuBox').stop().slideToggle();
		return false
	})
	
	$('#datepicker').Zebra_DatePicker({
		view: 'years',
		container:$('.demoDateZebra'),
	    format: 'm/d/Y',
		show_icon:true,
		show_other_months:false
	});
	
	$('.selectValue').click(function() {
	  $(this).parent().children('ul').slideToggle(200)
	})
	$('.selectValueBox li').click(function() {
		let selectValue = $(this).html();
		$('.selectValue').html(selectValue);
		$('#selectInp').val(selectValue);
		$('.selectValueBox ul').slideUp(200)
	})
	$('.fileUploadBtn').click(function() {
	  $('.fileUpload').click()
	})
	
});

/*window.onscroll = function() {
	load();  
}

jQuery(window).resize(function () {
	load();
});

jQuery(window).bind("orientationchange",function(e){
	/load();
})*/
