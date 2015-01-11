(function($) {
  $.fn.huadong = function( obj, obja, time ) {
    var left = $(obj).width(), up = this, num = 0, heigh = $('.navbar-header').height();
    $(obj).height($('body').height()).width(0).hide();
    $(obja).click(function(){
      $('.navbar').height($('body').height()).css({'position':'fixed', 'top':'0px', 'left' : '0px'});
        $(obj).show().animate({ 'width':left + 'px'}, time);
      $('body').css({'top': '-10px', 'overflow': 'hidden'});
      $('.container-fluid').css('display', 'none');
    });
    /*$('.hidediv').mouseout(function(){
      $(this).animate({'width':'0px'}, time, function(){ $(this).hide(); });
      $('.navbar').height(heigh);
      $('body').css({'top': '0px', 'overflow': 'scroll'});
      $('.container-fluid').css('display', 'block');
    });*/
  }
})(jQuery);

 $(document).ready(function(e) {
  $('.navbar').huadong('.hidediv', '#useraccount', 200);
  //调用方法
  // 最外部容器元素对象.huadong(要隐藏的对象, 触发事件的对象, 隐藏/显示过渡时间（1秒=1000毫秒）);
 });
