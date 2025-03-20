/* tangbin - http://www.planeArt.cn - MIT Licensed */
(function($){
	// tipWrap
	// maxNumber
	$.fn.artTxtCount = function(tipWrap, maxNumber){
		var countClass = 'js_txtCount',		
			fullClass = 'js_txtFull',		
			disabledClass = 'disabled';		
		
		// 统计字数 count
		var count = function(){
			var btn = $(this).closest('form').find(':submit'),
				val = $(this).val().length,
				
				
				disabled = {
					on: function(){
						btn.removeAttr('disabled').removeClass(disabledClass);
					},
					off: function(){
						btn.attr('disabled', 'disabled').addClass(disabledClass);
					}
				};
				
			if (val == 0) disabled.off();
			if(val <= maxNumber){
				if (val > 0) disabled.on();
				tipWrap.html('<span class="' + countClass + '">\u8FD8\u80FD\u8F93\u5165 <strong>' + (maxNumber - val) + '</strong> \u4E2A\u5B57</span>');
			}else{
				disabled.off();
				tipWrap.html('<span class="' + countClass + ' ' + fullClass + '">\u5DF2\u7ECF\u8D85\u51FA <strong>' + (val - maxNumber) + '</strong> \u4E2A\u5B57</span>');
			};
		};
		$(this).bind('keyup change', count);
		
		return this;
	};
})(jQuery);
