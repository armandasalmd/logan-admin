document.getElementById('select_year').onchange = function () {
    console.log("hello1");
    var sel_month = document.getElementById('select_month');
    window.location = "?filter_year=" + this.value + "&filter_month=" + sel_month.value;
};

document.getElementById('select_month').onchange = function () {
    console.log("hello2");
    var sel_month = document.getElementById('select_year');
    window.location = "?filter_year=" + sel_month.value + "&filter_month=" + this.value;
};

$.noConflict();

jQuery(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	} );

	jQuery('.selectpicker').selectpicker;


	$('#menuToggle').on('click', function(event) {
		$('body').toggleClass('open');
	});

	// $('.user-area> a').on('click', function(event) {
	// 	event.preventDefault();
	// 	event.stopPropagation();
	// 	$('.user-menu').parent().removeClass('open');
	// 	$('.user-menu').parent().toggleClass('open');
	// });


});
