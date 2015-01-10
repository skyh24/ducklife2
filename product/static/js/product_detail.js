$(function () {
	$('#plus').click(function () {
		var num = $('#num').val();
		num++;
		$('#num').val(num).change();
	});

	$('#sub').click(function () {
		var num = $('#num').val();
		if (num >= 1) num--;
		$('#num').val(num).change();
	});
  
  //url跳转
	$('.cart').click(function () {
		location.href = '/cart/';
	});
 
  //添加到购物车
  $('#add_to_cart').click(function(){
		$.post('/add/',
		      {
				productID:$(this).attr('data-pid'),
				number:$('#num').val()
		      },function(data, textStatus){
			      if( textStatus == "success") {
			      	  alert("已添加到购物车。");
			      } else {
			      	  alert('添加不成功，请重新操作！');
			      }
		      }, 'json');
	});

  	$('.send').click(function() {
  		$('.send').addClass("btn-outlined");
  		$(this).removeClass("btn-outlined");
  		send = $(this).html();
  		$('#send').val(send);
  	});

});

