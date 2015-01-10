$(function(){
	$('.cancelOrder').click(function(){
		var depen = 0;

		var cb = function(data) {
			      	if (data['success']) {
			      		depen = 1;
			      	    de();
			      	}
			      }

		var de = function() {
			if (depen == 1)
				$('#'+oid).slideUp('slow',function(){alert("订单已取消");});
			   //$('.orderform').slideUp('slow',function(){alert("订单已取消");});
	    }

		$.post('/order/cancel/',
		     {
		      	orderID:$(this).attr('data-oid')
		      },function(data){
			    cb(data);
		      }, 'json');
	});
});