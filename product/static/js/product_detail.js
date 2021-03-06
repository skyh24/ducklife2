$(function () {
	$('#plus').click(function () {
		var num = $('#num').val();
		num++;
		$('#num').val(num);
		$('#number').val(num);
		money = $('#num').attr('money');
		$('#price').val(money * num);     
	});

	$('#sub').click(function () {
		var num = $('#num').val();
		if (num >= 1) num--;
		$('#num').val(num);
		$('#number').val(num);
		money = $('#num').attr('money');
		$('#price').val(money * num);  
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

  	$('.addr').click(function(event) {
  		var address = $("[name='address']").val();
  		if(!address) {
  			$("[name='address']").val($(this).html());
  		} else {
  			$(this).html(address);
  			$(this).addClass("btn-negative");
  		}
  	})

  	//检测是否填好了表单
	$('#check').click(function(event){
		var name = $("[name='name']").val();
		var phone = $("[name='phone']").val();
		var address = $("[name='address']").val();
		//var partten = /^1[3,5,8]\d{9}$/;
		if(!name) {
			alert("请填好收货人姓名。");
			event.preventDefault();
		}
		else if (!phone) {
			alert("请填好收货人手机。");
			event.preventDefault();
		}
		else if (!address) {
			alert("请填好收货人地址。");
			event.preventDefault();
		}
		/*else if(!partten.test(phone)) ｛
			alert("请填好合法手机号码，11位数");
			event.preventDefault();
		｝*/
		else {
			if($('.addr').hasClass("btn-negative")) {
				$.post('/address/',
			      {
					addr1 : $('#ad1').html(),
					addr2 : $('#ad2').html()
			      },function(data, textStatus){
				      if( textStatus == "success") {
				      	  alert("添加默认地址" + addr1 + addr2);
				      } else {
				      	  alert('添加默认地址不成功');
				      }
			      }, 'json');
			}
			alert("您的订单已提交。")
			return;
		}
	});
});

