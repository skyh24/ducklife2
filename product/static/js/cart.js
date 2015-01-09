$(function () {
	//删除已选购的物品
	$('.icon-trash').click(function(){
		var change = 0;
		$.post('/cancel/',
		      {
		      	productID:$(this).attr('data-pid'),
		      	number:$(this).attr('data-num')
		      },
		      function(data, textStatus){
		      	if(textStatus == 'success') {
		      		change = data.total;
		      	}
		      	else {
		      		alert("操作失败，请刷新后重新操作。");
		      	}
		      },'json');
		$(this).parent().parent().slideUp("slow",function(){alert("成功移除商品。");$('#total').attr('value',change);});
	    var linum =  $('.table-view').children('.sgoods').length;
	    if (linum == 1) {
	    	$('#check').attr('disabled',true);
	    }
	});

	//检测是否填好了表单
	$('#check').click(function(event){
		var name = $("[name='name']").val();
		var phone = $("[name='phone']").val();
		var address = $("[name='address']").val();
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
		else {
			return;
		}
	});
});