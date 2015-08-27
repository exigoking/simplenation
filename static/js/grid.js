$(document).ready(function(){
	$('.term-filtered').hide();
	$('.main-loader').show();

	$(window).load(function(){
		$('.main-loader').hide();
		$('.term-filtered').show();
    isotopize();
	});
});