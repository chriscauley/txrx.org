/**
 * jQuery Lightbox
 * Copyright (c) 2013 Allan Ma (http://codecanyon.net/user/webtako)
 * Version: 2.1 (11/27/2013)
 */
(function($) {		   
	var IS_TOUCH = 'ontouchstart' in window;   	
	var DEFAULT_DURATION = 600;
	var ANIMATE_SPEED = 400;
	var DEFAULT_DELAY = 5000;
	var DEFAULT_WIDTH = 720;
	var DEFAULT_HEIGHT = 460;
	var MIN_SIZE = 100;
	var INITIAL_SIZE = 250;
	var SWIPE_MIN = 50;
	
	var NAMESPACE = '.wtLightbox';
	var UPDATE_TEXT = 'lbUpdateText';
	var START_TIMER = 'lbStartTimer';
	var IE6_INIT = 	  'lbIE6Init';
	var IE6_CLEANUP = 'lbIE6Cleanup';
	var SHOW_CAPTION = 'lbShowCaption';
	var HIDE_CAPTION = 'lbHideCaption';
	
	var LIGHTBOX_OPEN = 'lightboxOpen';
	var LIGHTBOX_CLOSE = 'lightboxClose';
	var LIGHTBOX_PLAY = 'lightboxPlay';
	var LIGHTBOX_PAUSE = 'lightboxPause';
	var LIGHTBOX_PREV = 'lightboxPrevious';
	var LIGHTBOX_NEXT = 'lightboxNext';
	
	var MSIE6 = msieCheck(6);
	var ERROR_MSG = 'Error Loading Content';
	
	var CONTENT =  "<div id='lb-overlay'></div>\
					<div class='lb-wrapper'>\
						<div id='lb-box'>\
							<div class='lb-inner'>\
								<div class='lb-content'></div>\
								<div class='lb-prev-half'>\
									<div class='lb-hover-prev'><div></div></div>\
								</div>\
								<div class='lb-next-half'>\
									<div class='lb-hover-next'><div></div></div>\
								</div>\
								<div class='lb-timer'></div>\
								<div class='lb-desc'></div>\
							</div>\
							<div class='lb-ext-desc'></div>\
							<div class='lb-cpanel'>\
								<div class='lb-inner-cp'>\
									<div class='lb-prev-btn'><div></div></div>\
									<div class='lb-play-btn'><div></div></div>\
									<div class='lb-next-btn'><div></div></div>\
									<div class='lb-info'></div>\
									<div class='lb-text-btn'><div></div></div>\
								</div>\
							</div>\
							<div class='lb-preloader'></div>\
						</div>\
						<div class='lb-close-btn'></div>\
					</div>";
	
	var methods = {
		init: function() {
			init();
		},
  		destroy: function() {
			try {
				pauseTimer();
				$overlay.add($wrapper).remove();
				$(window).add($(document)).unbind(NAMESPACE);
				$overlay.unbind().removeData();
				$wrapper.add($('*', $wrapper)).unbind().removeData();
			}
			catch (ex) {
			}
		}
 	};
	
	var defaults = {
		responsive:true,
		autoPlay:false,
		playButton:true,
		delay:DEFAULT_DELAY,
		speed:DEFAULT_DURATION,
		easing:'',
		navButtons:'normal',
		numberInfo:true,
		timer:true,
		caption:true,
		captionPosition:'outside',
		captionButton:false,
		continuous:true,
		mousewheel:true,
		keyboard:true,
		swipe:true,
		errorMessage:ERROR_MSG
	};
		
	var $overlay;
	var $wrapper;
	var $lightbox;
	var $innerTextbox;
	var $outerTextbox;
	var $preloader;
	var $cpanel;
	var $closeButton;
	var $infoPanel;
	var $innerBox;
	var $contentBox;
	var $playButton;
	var $prevButton;
	var $nextButton;
	var $textButton;
	var $prevHalf;
	var $nextHalf;
		
	var $timer;
	var $item;
	var $currObj;
	var $currGroup;
	
	var currIndex;
	var numItems;
	var continuous;
	var margin;
	var timerId;
	var displayCPanel;
	var displayText;
	var insideText;
	var padding;
	
	var _startX = null;
	var _startY = null;
	var _swipeDist = null;
	var _scrolling;
	
	$(document).ready(init);
	
	function init() {
		styleSupport('transition');
		styleSupport('transform');
		styleSupport('box-sizing');
		
		timerId = null;
		$('body').append(CONTENT);
		
		$overlay = 	$('#lb-overlay');
		$wrapper =  $('.lb-wrapper');
		$lightbox =	$wrapper.find('>#lb-box').click(function(e) { e.stopPropagation(); });
		$preloader = $lightbox.find('>.lb-preloader');
		$innerBox =  $lightbox.find('>.lb-inner');
		$contentBox = $innerBox.find('>.lb-content');
		$timer =	  $innerBox.find('>.lb-timer').data('pct', 1);
		$innerTextbox = $innerBox.find('>.lb-desc');
		$outerTextbox = $lightbox.find('>.lb-ext-desc');
		$cpanel = $lightbox.find('>.lb-cpanel');
		$prevHalf = $innerBox.find('>.lb-prev-half');
		$nextHalf = $innerBox.find('>.lb-next-half');
		$prevButton = $cpanel.find('.lb-prev-btn').mousedown(preventDefault);
		$nextButton = $cpanel.find('.lb-next-btn').mousedown(preventDefault);
		$playButton = $cpanel.find('.lb-play-btn').mousedown(preventDefault);
		$textButton = $cpanel.find('.lb-text-btn').mousedown(preventDefault);
		$infoPanel =  $cpanel.find('.lb-info');
		$closeButton = $wrapper.find('.lb-close-btn').mousedown(preventDefault);
		
		$overlay.add($closeButton).add($wrapper).click(closeLightbox);
		$playButton.click(togglePlay);
		$prevButton.add($prevHalf.find('>.lb-hover-prev')).click(goPrev);
		$nextButton.add($nextHalf.find('>.lb-hover-next')).click(goNext);
		$textButton.click(toggleCaption);
					
		if (!$.support['box-sizing']) {
			$innerTextbox.add($outerTextbox).css({padding:0});
		}
		
		if ($.support.transition && $.support.transform) {
			$innerTextbox.css({top:'100%', bottom:'auto'});
			$wrapper.bind(SHOW_CAPTION, function() { $innerTextbox.reflow().addClass('lb-slide-up'); })
					.bind(HIDE_CAPTION, function() { $innerTextbox.reflow().removeClass('lb-slide-up'); });
		}
		else {
			$innerTextbox.css({bottom:0, top:'auto'});
			$wrapper.bind(SHOW_CAPTION, function() { $innerTextbox.css({visibility:'visible'}); })
				    .bind(HIDE_CAPTION, function() { $innerTextbox.css({visibility:'hidden'}); });
		}
			
		margin = $wrapper.outerWidth() - $wrapper.width();
		
		initMisc();
	}
	
	//init group
	$.fn.wtLightBox = function() {
		var args = arguments;
		var params = args[0];
		
		if (methods[params]) {
			methods[params].apply($(this), Array.prototype.slice.call(args, 1));
		}
		else if (typeof params === 'object' || !params) {
			var $obj = $(this);
			var opts = $.extend(true, {}, defaults, params);
			
			$obj.data({responsive:opts.responsive,
					   autoPlay:opts.autoPlay,
					   playButton:opts.playButton,
					   delay:getPosInteger(opts.delay, DEFAULT_DELAY), 
					   duration:getPosInteger(opts.speed, DEFAULT_DURATION),
					   navButtons:opts.navButtons, 
					   displayNum:opts.numberInfo, 
					   displayTimer:opts.timer, 
					   displayText:opts.caption,
					   captionPosition:opts.captionPosition,
					   captionButton:opts.captionButton,
					   continuous:opts.continuous,
					   easing:opts.easing,
					   color:opts.color,
					   backgroundColor:opts.backgroundColor,
					   overlayColor:opts.overlayColor,
					   overlayOpacity:opts.overlayOpacity,					   
					   mousewheel:opts.mousewheel,
					   keyboard:opts.keyboard,
					   swipe:opts.swipe,
					   errorMessage:opts.errorMessage})
				.each(function(n) {
						var $group,
							index,
							groupName = $(this).data('lightbox-group');
						
						if (isEmpty(groupName)) {
							$group = $(this);
							index = 0;
						}
						else {
							$group = $obj.filter('[data-lightbox-group="' + groupName + '"]');
							index = $group.index($(this));
						}
						
						if (typeof $(this).attr('href') === 'undefined') {
							$(this).attr('href', '');
						}
			
						var contentType = $(this).data('lightbox-type');
						
						if (isEmpty(contentType)) {
							contentType = getContentType($(this).attr('href'));
						}
						
						$(this).data({contentType:contentType}).click({index:index, group:$group}, openLightbox);
						
						//add zoom button
						var $parent = $(this).parent();
						if ($parent.length && $parent.hasClass('ts-wrapper')) {
							var $icon = $('<a><div></div></a>').addClass('ts-zoom-button');
							$parent.append($icon);
							$icon.click({index:index, group:$group}, openLightbox);
						}
				});
		}
		return this;
	};
	
	//force reflow
	$.fn.reflow = function() {
		return this.each(
			function() {
				var reflow = this.offsetWidth;
			}
		);
	};
	
	//open lightbox
	function openLightbox(e) {
		e.preventDefault();
		$currObj = $(this);
		$currGroup = e.data.group;
		currIndex = e.data.index;
		var rotate = $currGroup.data('autoPlay');
		
		numItems = $currGroup.length;
		continuous = $currGroup.data('continuous');
		displayText = $currGroup.data('displayText');
		insideText = 'inside' === $currGroup.data('captionPosition');
		
		var displayPlayButton,
			displayTimer,
			navButtons,
			displayNum;
		
		var displayTextButton = displayText && insideText && $currGroup.data('captionButton');
		if (numItems > 1) {
			displayPlayButton =  $currGroup.data('playButton');
			displayTimer = $currGroup.data('displayTimer');
			navButtons = $currGroup.data('navButtons');
			displayNum = $currGroup.data('displayNum');
		}
		else {
			rotate = false;
			$currGroup.data({autoPlay:rotate, mousewheel:false, keyboard:false, swipe:false});
			displayPlayButton = displayTimer = navButtons = displayNum = false;
		}
		displayCPanel = (displayPlayButton || (true === navButtons || 'normal' === navButtons) || displayNum || displayTextButton);
		
		$playButton.toggleClass('lb-pause', rotate).toggle(displayPlayButton);
		
		$lightbox.unbind(START_TIMER);
		if (rotate || displayPlayButton) {
			$lightbox.bind(START_TIMER, startTimer);
		}
		
		if (displayTimer) {
			$timer.css({visibility:'visible'});
		}
		else {
			$timer.css({visibility:'hidden'});
		}
		
		$prevButton.add($nextButton).toggle(true === navButtons || 'normal' === navButtons);
		$prevHalf.add($nextHalf).toggle('mouseover' === navButtons || 'hover' === navButtons);
		$textButton.toggle(displayTextButton);
		$infoPanel.toggle(displayNum);
		
		$lightbox.unbind(UPDATE_TEXT);
		if (displayText) {
			if (insideText) {
				$lightbox.bind(UPDATE_TEXT, updateInnerTextbox);
				$innerTextbox.show();
				$outerTextbox.hide();
			}
			else {
				$lightbox.bind(UPDATE_TEXT, updateOuterTextbox);
				$outerTextbox.show();
				$innerTextbox.hide();
			}
		}
		else {
			$innerTextbox.add($outerTextbox).hide();
		}
		
		$(document).unbind('keyup' + NAMESPACE);
		if ($currGroup.data('keyboard')) {
			$(document).bind('keyup' + NAMESPACE, keyClose);
		}
		
		$overlay.stop(true, true).fadeIn(300);
		$wrapper.width(INITIAL_SIZE).height(INITIAL_SIZE).css({marginLeft:-$wrapper.outerWidth()/2, marginTop:-$wrapper.outerHeight()/2}).show();   
		padding = $innerBox.outerWidth() - $innerBox.width();
			
		loadContent();
		$lightbox.trigger(IE6_INIT).trigger(LIGHTBOX_OPEN);
	}
	
	//close lightbox 
	function closeLightbox(e) {
		e.preventDefault();
		resetTimer();
		
		$(document).unbind('keyup' + NAMESPACE);
		disableCtrl();
		$wrapper.stop(true).hide();
		$overlay.stop(true,true).fadeOut(200);
		$preloader.hide();
		$contentBox.add($innerTextbox).add($outerTextbox).empty();
		$lightbox.trigger(IE6_CLEANUP).trigger(LIGHTBOX_CLOSE);
	}
	
	//load content
	function loadContent() {
		$item = $currGroup.eq(currIndex);
		
		disableCtrl();
		$prevHalf.add($nextHalf).css({visibility:'hidden'});
		
		if (insideText) {
			$innerTextbox.hide();
		}
		else {
			$lightbox.trigger(UPDATE_TEXT);
		}
		
		getContent();
	}
	
	function getContentSize($item, $el) {
		var width = $item.data('lightbox-width'),
			height = $item.data('lightbox-height'),
			elWidth, elHeight;
			
		if (typeof $el !== 'undefined' && $el.length) {
			if ($el.is('img')) {
				setImageSize($el, width, height);
			}
			
			elWidth = $el.outerWidth();
			elHeight = $el.outerHeight();
		}
		else {
			elWidth = DEFAULT_WIDTH;
			elHeight = DEFAULT_HEIGHT;
		}
		
		width = getSize(width, elWidth);
		height = getSize(height, elHeight);
		$item.data({'org-width':width, 'org-height':height});
		
		if ($currGroup.data('responsive')) {
			return getFittedSize(width, height);
		}
		
		return {width:width, height:height};
	}
	
	function setImageSize($img, width, height) {
		width = isNaN(width) ? 'auto' : parseInt(width, 0);
		height = isNaN(height) ? 'auto' : parseInt(height, 0);
		$img.width(width).height(height);
	}
	
	//get content
	function getContent() {
		var contentType = $item.data('contentType'),
			url = $item.attr('href'),
			hideCSS = {opacity:0, visibility:'hidden', overflow:'auto'};
		
		if ('image' === contentType) {
			$preloader.show();
			var $img = $('<img/>');
			$contentBox.css(hideCSS).empty().append($img);
			$img.one('load', function() {
					var $el = $(this), 
						size = getContentSize($item, $el);
					$el.width('100%').height('100%');
					displayContent(size.width, size.height);
				})
				.error(function() { displayError(); })
				.attr('src', url);
				
			if ($img[0].complete || 'complete' === $img[0].readyState) {
				$img.trigger('load');
			}
			return;
		}
		
		if ('inline' === contentType) {
			var $inline = $(url);
			if ($inline.length) {
				var size = getContentSize($item, $inline);
				$contentBox.css(hideCSS).html($inline.html());
				displayContent(size.width, size.height);
			}
			else {
				displayError();
			}
		}
		else if ('flash' === contentType) {
			var size = getContentSize($item);
			var content =  "<object type='application/x-shockwave-flash' data='" + url + "' width='100%' height='100%' style='display:block'>\
								<param name='movie' value='" + url + "'/>\
								<param name='allowFullScreen' value='true'/>\
								<param name='quality' value='high'/>\
								<param name='wmode' value='transparent'/>\
							</object>";
			$contentBox.css(hideCSS).html(content);
			displayContent(size.width, size.height);
		}
		else if ('ajax' === contentType) {
			$preloader.show();
			$contentBox.css(hideCSS).empty();
			
			var index = url.indexOf('?'),
				varData = '',
				method = (isEmpty($item.data('lightbox-method')) ? 'GET' : $item.data('lightbox-method'));
			
			if (-1 < index) {
				varData = url.substring(index + 1);
				url = url.substring(0, index);
			}
			
			$.ajax({url:url, type:method, data:varData,
					success:function(data) {
						$contentBox.html(data);
						var size = getContentSize($item);
						displayContent(size.width, size.height);
					},
					error:function() {
						displayError();
					}
			});
		}
		else {
			$preloader.show();
			var $iframe = $("<iframe frameborder='0' hspace='0' scrolling='auto' width='100%' height='100%'></iframe>");
			$contentBox.css(hideCSS).css({overflow:'hidden'}).empty().append($iframe);
			$iframe.load(function() {
				var size = getContentSize($item);
				displayContent(size.width, size.height); 
			}).attr('src', url);
		}
	}
	
	//display error message
	function displayError() {
		$(window).unbind('resize' + NAMESPACE, resize);
		var $errorBox = $('<div class="lb-error-box">' + $currGroup.data('errorMessage') + '</div>');
		$contentBox.css({opacity:0, visibility:'hidden', overflow:'auto', width:'auto', height:'auto'}).empty().append($errorBox);
		var width = $errorBox.outerWidth(), height = $errorBox.outerHeight();
		$contentBox.width('100%').height('100%');
		displayContent(width, height);
	}
	
	//display content
	function displayContent(contentWidth, contentHeight) {
		if ($lightbox.is(':visible')) {
			$preloader.hide();
			
			var width  = contentWidth + padding,
				height = contentHeight + padding;
			
			if (displayCPanel) {
				height += $cpanel.outerHeight();
			}
			
			if (displayText && !insideText && !isEmpty($outerTextbox.html())) {
				$outerTextbox.outerWidth(width);
				height += $outerTextbox.outerHeight();
			}
			
			$wrapper.stop(true).animate({marginLeft:-(width + margin)/2, marginTop:-(height + margin)/2, width:width, height:height}, $currGroup.data('duration'), $currGroup.data('easing'), 
				function() {
					$innerBox.width(contentWidth).height(contentHeight);
					$infoPanel.html((currIndex + 1) + ' / ' + numItems);
					if (displayText) {
						if (insideText) {
							$lightbox.trigger(UPDATE_TEXT);
						}
						else {
							if (!isEmpty($outerTextbox.html())) {
								$outerTextbox.show();
							}						
						}
					}
					
					enableCtrl();
					$contentBox.add($prevHalf).add($nextHalf).css({visibility:'visible'});
					$contentBox.animate({opacity:1}, ANIMATE_SPEED, 
							function() {
								$lightbox.trigger(START_TIMER); 
							});
				}
			);
		}
	}
	
	//display inner text box
	function updateInnerTextbox() {
		var text = $item.attr('title') || $item.data('title');
		if (!isEmpty(text)) {
			$textButton.css({visibility:'visible'});
			$innerTextbox.html(text).trigger(HIDE_CAPTION).show();
			if (!$textButton.hasClass('lb-expand')) {
				$innerTextbox.trigger(SHOW_CAPTION);
			}
		}
		else {
			$textButton.css({visibility:'hidden'});
		}
	}
	
	//display outer text box
	function updateOuterTextbox() {
		$outerTextbox.hide();
		var text = $item.attr('title') || $item.data('title');
		if (!isEmpty(text)) {
			$outerTextbox.html(text);
		}
		else {
			$outerTextbox.empty();
		}
	}
	
	//enable control panel
	function enableCtrl() {
		$(window).unbind('resize' + NAMESPACE, resize);
		if ($currGroup.data('responsive') && !$contentBox.children().hasClass('lb-error-box')) {
			$(window).bind('resize' + NAMESPACE, resize);
		}
		
		$(document).unbind('keyup' + NAMESPACE, keyCtrl);
		if ($currGroup.data('keyboard')) {
			$(document).bind('keyup' + NAMESPACE, keyCtrl);
		}
		
		$wrapper.unbind('mousewheel DOMMouseScroll');
		if ($currGroup.data('mousewheel')) {
			$wrapper.bind('mousewheel DOMMouseScroll', mouseScroll);
		}
		
		if (IS_TOUCH) {
			$wrapper.unbind('touchstart touchmove touchend');
			if ($currGroup.data('swipe')) {
				$wrapper.bind('touchstart', touchStart);
			}
		}
		
		if (displayCPanel) {
			if (!continuous) {
				$prevButton.add($prevHalf.find('>.lb-hover-prev')).toggleClass('lb-disable', 0 === currIndex);
				$nextButton.add($nextHalf.find('>.lb-hover-next')).toggleClass('lb-disable', numItems - 1 === currIndex);
			}
			$cpanel.find('>.lb-inner-cp').width($innerBox.width());
			$cpanel.show();
		}	
	}

	//disable control panel
	function disableCtrl() {
		$(window).unbind('resize' + NAMESPACE, resize);
		$(document).unbind('keyup' + NAMESPACE, keyCtrl);
		$wrapper.unbind('mousewheel DOMMouseScroll').unbind('touchstart touchmove touchend');
		$cpanel.hide();
	}
	
	function toggleCaption()  {
		if ($textButton.hasClass('lb-expand')) {
			$wrapper.trigger(SHOW_CAPTION);
			$textButton.removeClass('lb-expand');
		}
		else {
			$wrapper.trigger(HIDE_CAPTION);
			$textButton.addClass('lb-expand');
		}
	}
	
	//play/pause
	function togglePlay() {
		var play = !$currGroup.data('autoPlay');
		$currGroup.data('autoPlay', play);
		if (play) {
			$playButton.addClass('lb-pause');
			$lightbox.trigger(START_TIMER).trigger(LIGHTBOX_PLAY);
		}
		else {
			$playButton.removeClass('lb-pause');
			pauseTimer();
			
			$lightbox.trigger(LIGHTBOX_PAUSE);
		}
	}

	//previous
	function goPrev() {
		resetTimer();
		if (currIndex > 0) {
			currIndex--;
		}
		else if (continuous) {
			currIndex = numItems - 1;
		}
		else {
			return;
		}				
		loadContent();
		$lightbox.trigger(LIGHTBOX_PREV);
	}
	
	//next
	function goNext() {
		resetTimer();
		if (currIndex < numItems - 1) {
			currIndex++;
		}
		else if (continuous) {
			currIndex = 0;
		}
		else {
			return;
		}				
		loadContent();
		$lightbox.trigger(LIGHTBOX_NEXT);
	}

	//rotate next
	function rotateNext() {
		resetTimer();
		currIndex = (currIndex < numItems - 1) ? currIndex + 1 : 0;
		loadContent();
	}
	
	//key press
	function keyCtrl(e) {
		switch(e.keyCode) {
			case 37:
				goPrev();
				break;
			case 39:
				goNext();
				break;
			case 80:
				togglePlay();
				break;
		}
	}
	
	//key press close
	function keyClose(e) {
		if (27 === e.keyCode) {
			closeLightbox(e);
		}
	}
	
	//mousewheel scroll
	function mouseScroll(e) {
		e.preventDefault();
		if (!$wrapper.is(':animated')) {
			var delta = (typeof e.originalEvent.wheelDelta === 'undefined') ?  -e.originalEvent.detail : e.originalEvent.wheelDelta;
			if (0 < delta) {
				goPrev();
			}
			else {
				goNext();
			}
		}
	}
	
	function touchStart(e) {
		if (1 === e.originalEvent.touches.length) {
			_startX = e.originalEvent.touches[0].pageX;
			_startY = e.originalEvent.touches[0].pageY;
			$wrapper.bind('touchmove', touchMove).one('touchend', touchEnd);
		}
	}
		
	function touchMove(e) {
		var xDist = _startX - e.originalEvent.touches[0].pageX;
		var	yDist = _startY - e.originalEvent.touches[0].pageY;
				
		_swipeDist = xDist;
		_scrolling = Math.abs(_swipeDist) < Math.abs(yDist);
			
		if (!_scrolling) {
			e.preventDefault();
		}
	}
		
	function touchEnd(e) {
		$wrapper.unbind('touchmove');
			
		if (!_scrolling) {
			if (null !== _swipeDist && Math.abs(_swipeDist) > SWIPE_MIN) {
				if (_swipeDist > 0) {
					goNext();
				}
				else {
					goPrev();
				}
			}
		}
	
		_startX = _startY = _swipeDist = null;
	}
	
	//get type of content
	function getContentType(url) {
		//determine from url		
		if (url.match(/[^\s]+\.(jpg|gif|png|bmp)/i)) {
			return 'image';
		}
		
		if (url.match(/[^\s]+\.(swf)/i)) {
			return 'flash';
		}
		
		if (0 === url.indexOf('#')) {
			return 'inline';
		}
		
		return 'iframe';
	}
	
	//get box dimension
	function getFittedSize(width, height) {
		var ratio,
			maxWidth  = $(window).width() - margin - padding,
			maxHeight = $(window).height() - margin - padding;
		
		if (displayCPanel) {
			maxHeight -= $cpanel.outerHeight();
		}
		
		ratio = height/width;
		width = Math.max(maxWidth, MIN_SIZE);
		if (!isNaN($item.data('org-width'))) {
			width = Math.min(width, $item.data('org-width'));
		}
		height = ratio * width;
				
		if (height > maxHeight) {
			ratio = 1/ratio;
			height = Math.max(maxHeight, MIN_SIZE);
			if (!isNaN($item.data('org-height'))) {
				height = Math.min(height, $item.data('org-height'));
			}
			width = ratio * height;
		}
		
		return {width:width, height:height};
	}
	
	function initMisc() {
		if (MSIE6) {
			$overlay.css({position:'absolute'});
			$wrapper.css({position:'absolute'});
			setOverlayToDocSize();
			$(window).bind('resize' + NAMESPACE, setOverlayToDocSize);  
			$lightbox.bind(IE6_INIT, function() { $('body').find('select').addClass('lb-hide-selects'); })
					 .bind(IE6_CLEANUP, function() { $('body').find('select').removeClass('lb-hide-selects'); });
		}
		else if (IS_TOUCH) {
			setOverlayToDocSize();
			$(window).bind('resize' + NAMESPACE, setOverlayToDocSize);  
		}
	}
	
	function setOverlayToDocSize() {
		$overlay.css({width:$(document).width(), height:$(document).height()});
	}
	
	function resize() {
		resetTimer();
		
		var size = getFittedSize($contentBox.width(), $contentBox.height()),
			contentWidth = size.width,
			contentHeight = size.height,
			width  = contentWidth + padding,
			height = contentHeight + padding;
			
		if (displayCPanel) {
			$cpanel.find('>.lb-inner-cp').width(contentWidth);
			height += $cpanel.outerHeight();
		}
			
		if ($outerTextbox.is(':visible')) {
			$outerTextbox.outerWidth(width);
			height += $outerTextbox.outerHeight();
		}
		
		$wrapper.stop(true).css({marginLeft:-(width + margin)/2, marginTop:-(height + margin)/2}).width(width).height(height);
		$innerBox.width(contentWidth).height(contentHeight);
		
		startTimer();
	}
	
	//start timer
	function startTimer() {
		if ($currGroup.data('autoPlay') && null === timerId) {
			var newDelay = Math.round($timer.data('pct') * $currGroup.data('delay'));
			$timer.animate({width:'100%'}, newDelay, 'linear');
			timerId = setTimeout(rotateNext, newDelay);
		}
	}
	
	//reset timer
	function resetTimer() {
		clearTimeout(timerId);
		timerId = null;
		$timer.stop(true).width(0).data('pct', 1);
	}
	
	//pause timer
	function pauseTimer() {
		clearTimeout(timerId);
		timerId = null;
		var pct = 1 - ($timer.width()/($innerBox.width()+1));
		$timer.stop(true).data('pct', pct);
	}
	
	//get positive int
	function getPosInteger(val, defaultVal) {
		val = parseInt(val, 0);
		return (isNaN(val) || val <= 0) ? defaultVal : val;
	}
	
	//check is empty
	function isEmpty(val) {
		return (typeof val === 'undefined' || '' === $.trim(val));
	}
	
	function getSize(size, defaultSize) {
		return ((typeof size === 'undefined' || isNaN(size)) ? defaultSize  : Math.max(parseInt(size, 0), MIN_SIZE));
	}
	
	//msie ver. check
	function msieCheck(ver) {
		if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)) {
	 		if (typeof ver === 'undefined') {
				return true;
			}
			
			var ieVer = new Number(RegExp.$1);
			if (ieVer <= ver) {
				return true;
			}
		}
		return false;
	}
	
	function preventDefault(e) {
		e.preventDefault();
	}
	
	//get style property support
	function styleSupport(prop) {
		var prefixes = ['Webkit', 'Moz', 'O', 'ms'],
			elem = document.body || document.documentElement,
			style = elem.style,
			supportedProp = false;
	
		if (typeof style[prop] !== 'undefined') {
			supportedProp = prop;
		}
		else {
			var capProp = prop.charAt(0).toUpperCase() + prop.slice(1);
			for (var i = 0; i < prefixes.length; i++) {
				var prefixProp = prefixes[i] + capProp;
				if (typeof style[prefixProp] !== 'undefined') {
					supportedProp = prefixProp;
					break;
				}
			}
		}

		$.support[prop] = supportedProp;
		return supportedProp;
	}
})(jQuery);