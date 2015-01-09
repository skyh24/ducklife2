$(function(){
	$('.index').click(function(){
		location.href = '/';
	});
	$('.scar').click(function(){
		location.href = '/cart/';
	});
	$('.product').click(function(){
		var product_id = $(this).attr('data-pid');
		location.href = '/' + product_id + '/product/';
	});

	$('.notpay').click(function(){
		location.href = '/order/';
	});

	$('.havepay').click(function(){
		location.href = '/order/havepay/';
	});

	$('.havecancel').click(function(){
		location.href = '/order/havecancel/';
	});
});