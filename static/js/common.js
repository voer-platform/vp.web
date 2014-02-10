$(document).ready(function(){

	/*$('.tooltipsg').tooltip();*/
	changebg();

	$(".hfslidebg > div:gt(0)").hide();
	slideInterval = setInterval(function(){
		var active = $('.hfslidebg > div.active');
		var next = active.next();
		next.addClass('active');
		next.css('display','block');
		active.removeClass('active');
		active.css('display','none');
		active.appendTo('.hfslidebg');
	},10000);

	$(".hfslide > div:gt(0)").hide();
	slideInterval = setInterval(function(){
		var active = $('.hfslide > div.active');
		var next = active.next();
		next.addClass('active');
		next.css('display','block');
		active.removeClass('active');
		active.css('display','none');
		active.appendTo('.hfslide');
	},10000);

	if($('#checkbox-showpassword').hasClass('checked')){
		$('.passwordsg').removeAttr('type');
		$('.passwordsg').attr('type', 'text');
	}
	else{
		$('.passwordsg').removeAttr('type');
		$('.passwordsg').attr('type', 'password');
	}


	function changebg(){
	var images = ['bg-slide1.jpg', 'bg-slide2.jpg', 'bg-slide3.jpg'];
	$('#slider').css({'background-image': 'url(/static/images/' + images[Math.floor(Math.random() * images.length)] + ')'});
	$('#slider').css({'background-size': 'cover'});


}

//	$('.carousel').carousel({
//		interval: 8000,
//		pause: false
//	})

});

