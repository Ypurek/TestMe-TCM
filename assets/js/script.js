/*function load() {
		
}*/

jQuery(document).ready(function($){	
	$('.menuBtn').on('click', function() {
    $('body').toggleClass('menuOpen');
    $('.menuBox').stop().slideToggle();
		return false
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
