$(function () {
	$('.detail').click(function(){
		var uid = $(this).attr('data-gid');
		location.href = '/product/' + uid + '/';
	});
});