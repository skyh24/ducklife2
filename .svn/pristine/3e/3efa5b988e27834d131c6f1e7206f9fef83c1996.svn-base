$(function() {
    $("#indexPage").addClass("liActive");
    $("#orderBox").hide();
    $("#productBox").hide();
    $("#categoryBox").hide();

    $("#orderPage").click(function() {
        $(this).siblings().removeClass("liActive");
        $(this).addClass("liActive");
        $("#orderBox").fadeIn();
        $("#productBox").hide();
        $("#categoryBox").hide();
    });

    $("#indexPage").click(function() {
        $(this).siblings().removeClass("liActive");
        $(this).addClass("liActive");
        $("#orderBox").hide();
        $("#productBox").hide();
        $("#categoryBox").hide();
    });

    $("#productPage").click(function() {
        $(this).siblings().removeClass("liActive");
        $(this).addClass("liActive");
        $("#orderBox").hide();
        $("#productBox").fadeIn();
        $("#categoryBox").hide();
    });

    $("#categoryPage").click(function() {
        $(this).siblings().removeClass("liActive");
        $(this).addClass("liActive");
        $("#orderBox").hide();
        $("#productBox").hide();
        $("#categoryBox").fadeIn();
    });

    $("#categoryForm").submit(function() {
        var name = $('#categoryName').val();
        if (name == "") {
            $('.warningMessage').fadeIn(2000).fadeOut(2000);
            return false;
        }
        $.post('/backend/create/category/',
        {
            'name' : name,
        }, function(data) {
            $('#categoryList').prepend(data);
            var number = $('#categoryList').find('.deleteButton').first().attr('data-id');
            $('#productCategory').prepend('<option value="' + number + '" id="option' + number + '">' + name + '</option>');
            $('#categoryName').val('');
            alert('创建成功');
            return false;
        });
        return false;
    });

    $('.deleteButton').each(function() {
        $(this).click(function() {
            var dom = $(this);
            var id = $(this).attr('data-id');
            $.getJSON('/backend/delete/category/',
            {
                'categoryId' : id,
            }, function(data) {
                if (data['success']) {
                    alert('删除成功');
                    $('#category' + id).parent().slideUp(1000, function() {
                        $(this).remove();
                        $('#productCategory').find('#option' + id).remove();
                    });
                }
            });
        });
    });

    $('#productForm').submit(function() {
        var name = $('#productName').val();
        if (name == "") {
            $('#productName').siblings('.warningMessage').fadeIn(2000).fadeOut(2000);
            return false;
        }
        var price = $('#productPrice').val();
        if (price == "") {
            $('#productPrice').siblings('.warningMessage').fadeIn(2000).fadeOut(2000);
            return false;
        }
        var description = $('#productDescription').val();
        if (description == "") {
            $('#productDescription').siblings('.warningMessage').fadeIn(2000).fadeOut(2000);
            return false;
        }
        var category;
        var options = $('#productCategory').children();
        for (var i = 0; i < options.length; i++) {
            if (options[i].selected) {
                category = options[i].value;
            }
        }
        var files = $('#productPicture')[0].files;
        if (files.length == 0) {
            $('#productPicture').siblings('.warningMessage').fadeIn(2000).fadeOut(2000);
            return false;
        } 
        var picture = files[0];
        return true;
    });

    $('#previewImage').hide();
    document.getElementById('productPicture').onchange = function(evt) {
        if (!window.FileReader) return;
        var files = evt.target.files;
        for (var i = 0, f; f = files[i]; i++) {
            if (!f.type.match('image.*')) {
                continue;
            }
            var reader = new FileReader();
            reader.onload = (function(theFile) {
                return function(e) {
                    document.getElementById('previewImage').src = e.target.result;
                };
            })(f);
            reader.readAsDataURL(f);
        }
        $('#previewImage').show();
    }

    $('.deleteProduct').each(function() {
        $(this).click(function() {
            var uid = $(this).attr('data-id');
            $.getJSON('/backend/delete/product/',
            {
                'uid' : uid,
            }, function(data) {
                if (data['success']) {
                    $('#product' + uid).parent().slideUp(1000, function() {
                        $(this).remove();
                        $('#table' + uid).remove();
                    })
                }
            });
        });
    });

    $('.deliveryComfirm').each(function() {
        $(this).click(function() {
            $.getJSON('/backend/delivery/order/',
                {
                    'id' : $(this).attr('data-id'),
                }, function(data) {
                    if (data['success']) {
                        alert('确认成功');
                    }
                });
        });
    });

    $('.cancelComfirm').each(function() {
        $(this).click(function() {
            $.getJSON('/backend/cancel/order/',
                {
                    'id' : $(this).attr('data-id'),
                }, function(data) {
                    if (data['success']) {
                        alert('取消订单成功');
                    }
                });
        });
    });

    $('.paidComfirm').each(function() {
        $(this).click(function() {
            $.getJSON('/backend/paid/order/',
                {
                    'id' : $(this).attr('data-id'),
                }, function(data) {
                    if (data['success']) {
                        alert('确认成功');
                    }
                });
        });
    });

    var uploading = false;
    $('#uploadFrame').load(function() {
        if (uploading) {
            $('#uploadMessage').hide().text($(this).contents().find('body').html()).slideDown(500);
            uploading = false;
        };
    });

    $('#uploadPictures').submit(function() {
        $('#uploadMessage').text('上传图片中...');
        uploading = true;
    })

    tinymce.init({
        selector: "textarea",
        language: "zh_CN",
        skin: "lightgray",
        plugins: [
            "advlist autolink autosave link image lists charmap print preview hr anchor pagebreak spellchecker",
            "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
            "table contextmenu directionality emoticons template textcolor paste fullpage textcolor"
        ],
    })
});