(function($) {
  $.fn.huadong = function( obj, obja, time ) {
    var left = $(obj).width(), up = this, num = 0, heigh = $('.navbar-header').height();
    $(obj).height($(window).height()).width(0).hide();
    $(obja).click(function(){
      $('.navbar').height($(window).height()).css({'position':'absolute', 'top':'0px', 'left' : '0px'});
      $(obj).show().animate({'width':left + 'px'}, time);
    });
    /*$('logout').mouseout(function(){
      $(this).animate({'width':'0px'}, time, function(){ $(this).hide(); });
      $('.navbar').height(heigh);
    });*/
  }
})(jQuery);

 $(document).ready(function(e) {
  $('.navbar').huadong('.hidediv', '#useraccount', 200);
  //调用方法
  // 最外部容器元素对象.huadong(要隐藏的对象, 触发事件的对象, 隐藏/显示过渡时间（1秒=1000毫秒）);
 });
