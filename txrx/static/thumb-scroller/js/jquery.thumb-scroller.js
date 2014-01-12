/**
 * jQuery Thumb Scroller
 * Copyright (c) 2013 Allan Ma (http://codecanyon.net/user/webtako)
 * Version: 2.1 (11/27/2013)
 */
(function($) {
	var IS_TOUCH = 'ontouchstart' in window;
	
	var PLUGIN_NAME = 'thumbScroller';
	var ANIMATE_SPEED = 400;
	var SWIPE_MIN = 50;
	
	var REFRESH_INFO = 'tsRefreshInfo';
	var REFRESH_BUTTONS = 'tsRefreshButtons';
	var REFRESH_SCRUBBER = 'tsRefreshScrubber';
	var REFRESH_NAV = 'tsRefreshNav';
	var COLLAPSE_NAV = 'tsCollapseNav';
	var RESIZE_SCROLLBAR = 'tsResizeScrollbar';
	var COLLAPSE_SCROLLBAR = 'tsCollapseScrollbar';
	var START_TIMER = 'tsStartTimer';
	var RESUME_TIMER = 'tsResumeTimer';
	var LOAD_CONTENT = 'tsLoadContent';
	var PAUSE_INTERACTION = 'tsPauseOnAction';
	
	var SCROLLER_INIT = 'scrollerInit';
	var SCROLLER_PLAY = 'scrollerPlay';
	var SCROLLER_PAUSE = 'scrollerPause';
	var SCROLLER_PREV = 'scrollerPrevious';
	var SCROLLER_NEXT = 'scrollerNext';
	var SCROLLER_BEGIN = 'scrollerBegin';
	var SCROLLER_END = 'scrollerEnd';
	
	var MSIE6 = msieCheck(6);
	var MSIE7 = msieCheck(7);
	var MSIE6_RESIZE = 'tsMsie6Resize';
	
	styleSupport('transition');
	styleSupport('transform');
	styleSupport('box-sizing');
	
	//Class Thumb Scroller
	function ThumbScroller(obj, opts) {
		this._options = opts;
		
		this._isVertical = ('vertical' === opts.orientation);
		this._collapsible = opts.collapsible && !this._isVertical;
		this._responsive = !this._collapsible && opts.responsive;
		var borderBox = !(MSIE7 && this._responsive);
		
		this._numDisplay = getPosInteger(opts.numDisplay, 4);
		this._slideWidth = getPosInteger(opts.slideWidth, 300);
		this._slideHeight = getPosInteger(opts.slideHeight, 200);
		this._slideMargin = (borderBox ? getNonNegInteger(opts.slideMargin, 0) : 0);
		this._borderWidth =	(borderBox ? getNonNegInteger(opts.slideBorder, 0) : 0);
		this._captionHeight = getNonNegInteger(opts.captionHeight, 'auto');
		this._rotate = opts.autoPlay;
		this._delay = getPosInteger(opts.delay, 5000);
		this._duration = getPosInteger(opts.speed, 800);
		this._easing = opts.easing;
		
		this._$scroller;
		this._$slidePanel;
		this._$slideList;
		this._$slides;
		this._$navList;
		this._$scrollbar;
		this._$scrubber;
		this._$scroller = $(obj);
		
		this._namespace = '.' + ((typeof this._$scroller.attr('id') !== 'undefined') ? this._$scroller.attr('id') : 'scroller');
		this._numItems;
		this._limit;
		this._currIndex = 0;
		this._timerId = null;
		this._resumeId = null;
		
		this._startX = null;
		this._startY = null;
		this._swipeDist = null;
		this._scrolling;
		
		this.init();
	}

	ThumbScroller.prototype = {
		init: function() {
			this._$scroller.addClass(this._isVertical ? 'ts-vertical' : 'ts-horizontal');
			
			this._$slideList = this._$scroller.find('>ul').addClass('ts-list');
			this._$slides =	this._$slideList.find('>li').addClass('ts-slide');
			
			this._$slideList.wrap($('<div></div>').addClass('ts-container'));
			this._$slidePanel = this._$slideList.parent();
			
			this._numItems = this._$slides.length;
			this._numDisplay = Math.min(this._numDisplay, this._numItems);
			var numSlides = ('index' === this._options.control ? this._numDisplay * Math.ceil(this._numItems/this._numDisplay) : this._numItems);
			this._limit = numSlides - this._numDisplay;
			this._currIndex = Math.min(getNonNegInteger(this._options.startIndex, 0), this._limit);
			
			if (this._options.shuffle) {
				this.shuffleItems();
			}
			
			//init components
			this.initSlides();
			this.initSlidePanel();
			this.initHeader();
			this.initControl();
			this.initContainer();
			
			//bind events
			if (this._collapsible) {
				this._minDisplay = parseInt(this._options.minDisplay, 0);
				if (isNaN(this._minDisplay) || this._minDisplay < 1) {
					this._minDisplay = 1;
				}
				this._maxDisplay = parseInt(this._options.maxDisplay, 0);
				if (isNaN(this._maxDisplay)) {
					this._maxDisplay = this._numDisplay;
				}
				else if (this._maxDisplay > this._numItems) {
					this._maxDisplay = this._numItems;
				}
			
				this.collapse();
				$(window).bind('resize' + this._namespace, $.proxy(this.collapse, this));
			}
			else if (this._responsive) {
				this.resize();
				$(window).bind('resize' + this._namespace, $.proxy(this.resize, this));
			}			
			
			if (IS_TOUCH) {
				if (this._options.swipe) {
					this._$slidePanel.bind('touchstart', $.proxy(this.touchStart, this));
				}
			}
			else {
				if (this._options.mousewheel) {
					this._$scroller.bind('mousewheel DOMMouseScroll', $.proxy(this.mouseScroll, this));
				}
			
				if (this._options.pauseOnHover) {
					this._$scroller.hover($.proxy(this.pause, this), $.proxy(this.play, this));
				}			
			}
			
			if (this._options.keyboard) {
				$(document).bind('keyup' + this._namespace, $.proxy(this.keyControl, this));
			}
			
			if (this._options.pauseOnInteraction) {
				this._$scroller.bind(PAUSE_INTERACTION, $.proxy(this.pause, this));
			}
			
			this._$scroller.bind(START_TIMER, $.proxy(this.startTimer, this));
			
			this.updateSlideList(false);
		},
		
		collapse: function() {
			this.pauseTimer();
			
			var width = this._$scroller.parent().width() - (this._$scroller.outerWidth(true) - this._$scroller.width());
			var numFit = Math.floor(width/this._$slides.outerWidth());
			
			if (numFit != this._numDisplay && this._minDisplay <= numFit && numFit <= this._maxDisplay) {
				this._numDisplay = numFit;
				this._$slidePanel.width(this._numDisplay * this._$slides.outerWidth());
				this._$scroller.width(this._$slidePanel.width());
				
				if ('index' === this._options.control) {
					var numSlides = this._numDisplay * Math.ceil(this._numItems/this._numDisplay);
					this._limit = numSlides - this._numDisplay;
					this._currIndex = Math.floor(this._currIndex/this._numDisplay) * this._numDisplay;
				}
				else {
					this._limit = this._numItems - this._numDisplay;
					if (this._currIndex > this._limit) {
						this._currIndex = this._limit;
					}
				}
				
				this._$scroller.trigger(COLLAPSE_NAV).trigger(COLLAPSE_SCROLLBAR);
				this.updateSlideList(false);
			}
		},
		
		resize: function() {
			this.pauseTimer();
			
			var $wrappers = this._$slides.find('>.ts-wrapper'),
				ratio = $wrappers.width()/this._slideWidth;
			
			$wrappers.height(Math.round(ratio * this._slideHeight));
			this._$slides.find('>.ts-caption').outerHeight(Math.round(ratio * this._captionHeight));
			
			if (this._isVertical) {
				this._$slidePanel.height(this._numDisplay * this._$slides.outerHeight());
				this._$slideList.css({top:-this._currIndex * this._$slides.outerHeight()});
			}
			else {
				this._$slidePanel.height(this._$slides.outerHeight());
				this._$slideList.css({left:-this._currIndex * this._$slides.outerWidth()});
			}
			
			this._$scroller.height(this._$slidePanel.height() + this._$scroller.find('>.ts-header').outerHeight(true) + this._$scroller.find('>.ts-control').outerHeight(true));
			
			this._$slides.each($.proxy(function(n, el) {
				var $caption = $(el).find('.ts-caption');
				$caption.css({fontSize:Math.floor($caption.data('fontSize') * ratio) + 'px', lineHeight:Math.floor($caption.data('lineHeight') * ratio) + 'px'});
			}, this));
						
			this._$scroller.trigger(RESIZE_SCROLLBAR).trigger(MSIE6_RESIZE);
		},
		
		//init scroller container
		initContainer: function() {
			var padding = getNonNegInteger(this._options.padding, 0),
				$prevButton = this._$scroller.find('>.ts-prev'),
				$nextButton = this._$scroller.find('>.ts-next'),
				$header = this._$scroller.find('>.ts-header'),
				$cpanel = this._$scroller.find('>.ts-control'),
				css;
			
			if (!this._responsive) {
				this._$scroller.width(this._$slidePanel.width()).height(this._$slidePanel.height() + $header.outerHeight(true) + $cpanel.outerHeight(true));
			}
				
			if (this._isVertical) {
				css = {paddingLeft:padding, paddingRight:padding};
				
				if (0 === $prevButton.length && 0 === $header.length) {
					css['paddingTop'] = padding;
				}
				
				if (0 === $nextButton.length && 0 === $cpanel.length) {
					css['paddingBottom'] = padding;
				}
				
				this._$scroller.css(css);
				
				if (MSIE6) {
					this._$scroller.bind(MSIE6_RESIZE, $.proxy(function() {
						$prevButton.width(this._$scroller.outerWidth(true));
						$nextButton.width(this._$scroller.outerWidth(true));
					}, this)).trigger(MSIE6_RESIZE);
				}
			}
			else {
				css = {};
				
				if (0 === $header.length) {
					css['paddingTop'] = padding;
				}
				
				if (0 === $prevButton.length) {
					css['paddingLeft'] = padding;
				}
				
				if (0 === $nextButton.length) {
					css['paddingRight'] = padding;
				}
				
				if (0 === $cpanel.length) {
					css['paddingBottom'] = padding;
				}
				
				this._$scroller.css(css);
				
				if (MSIE6) {
					this._$scroller.bind(MSIE6_RESIZE, $.proxy(function() {
						$prevButton.height(this._$scroller.outerHeight(true));
						$nextButton.height(this._$scroller.outerHeight(true));
					}, this)).trigger(MSIE6_RESIZE);
				}
			}
			
			this.setOptColor(this._$scroller.add($prevButton).add($nextButton), this._options.backgroundColor, 'backgroundColor');
			this.setOptColor(this._$scroller, this._options.color, 'color');
		},
		
		//init slides
		initSlides: function() {
			if ('outside' === this._options.captionPosition) {
				this._$slides.addClass('ts-outside').one('tsInitCaption', $.proxy(this.initExtCaption, this));
			}
			else {
				this._$slides.addClass('ts-inside').one('tsInitCaption', $.proxy(this.initCaption, this));
			}
			
			this._$slides.each($.proxy(function(n, el) {
				var $slide = $(el).wrapInner($('<div></div>').addClass('ts-wrapper')),
					$wrapper = $slide.find('>.ts-wrapper').css({borderWidth:this._borderWidth});
				
				$slide.data({
					'image-position':getValue($slide.data('image-position'), this._options.imagePosition),
					'caption-align': getValue($slide.data('caption-align'),  this._options.captionAlign), 
					'caption-effect':getValue($slide.data('caption-effect'), this._options.captionEffect),
					'caption-button':getValue($slide.data('caption-button'), this._options.captionButton)
				});
				
				if (this._options.pauseOnInteraction) {
					$wrapper.click($.proxy(this.pause, this));
				}
				
				if (isEmpty($slide.data('src'))) {
					var $link = $wrapper.find('>a:not(.ts-link-button, .ts-zoom-button)').first(),
						$content;
					
					if ($link.length) {
						$link.data({title:$link.attr('title')}).removeAttr('title');
						$content = $link.find('>:first-child');
					}
					else {
						$content = $wrapper.find('>:first-child');
					}
					
					if ($content.length) {
						$content.addClass('ts-content');
						if ($content.is('img')) { 
							$content.one('load', $.proxy(this.processImg, this));
							if ($content[0].complete || 'complete' === $content[0].readyState) {
								$content.trigger('load');
							}
						}
					}
				}
				else {
					$slide.one(LOAD_CONTENT, $.proxy(this.processContent, this));
				}
				
				var $linkButton = $wrapper.find('>a.ts-link-button'),
					$zoomButton = $wrapper.find('>a.ts-zoom-button');
				
				if ($zoomButton.length) {
					$zoomButton.data({title:$zoomButton.attr('title')}).removeAttr('title');
					if ($linkButton.length) {
						$linkButton.addClass('ts-button-align-right');
						$zoomButton.addClass('ts-button-align-left');
					}
				}
				
				$slide.trigger('tsInitCaption');
			}, this));
			
			if ('outside' === this._options.captionPosition) {
				var $captions = this._$slides.find('>.ts-caption');
				
				if (isNaN(this._captionHeight)) {
					var $wrappers = this._$slides.find('>.ts-wrapper');
					$captions.outerWidth(this._slideWidth + ($wrappers.outerWidth() - $wrappers.width()))
							 .outerHeight(Math.max.apply(null, $captions.map(function() { return $(this).outerHeight(); }).get()));
							 
					this._captionHeight = $captions.outerHeight();
					$captions.outerWidth('100%'); 
				}
				else {
					$captions.outerHeight(this._captionHeight);
				}
			}
		},
		
		initExtCaption: function(e) {
			var $slide = $(e.currentTarget),
				$caption = $slide.find('>.ts-wrapper').find('>:not(a,img,.ts-content,.ts-overlay)').first();
				
			if (1 > $caption.length) {
				$caption = $('<div></div>');
			}
			
			$caption.addClass('ts-caption');
			if ('top' === $slide.data('caption-align')) {						
				$slide.prepend($caption);
			}
			else {
				$slide.append($caption);
			}
			
			$caption.data({fontSize:parseInt($caption.css('fontSize'), 0), lineHeight:parseInt($caption.css('lineHeight'), 0)});
		},
		
		initCaption: function(e) {
			var $slide = $(e.currentTarget),
				$wrapper = $slide.find('>.ts-wrapper'),
				$caption = $wrapper.find('>:not(a,img,.ts-content,.ts-overlay)').first();
				
			if ($caption.length) {
				var isTop = ('top' === $slide.data('caption-align'));
				$caption.addClass('ts-caption').css(isTop ? 'top' : 'bottom', 0)
						.data({fontSize:parseInt($caption.css('fontSize'), 0), lineHeight:parseInt($caption.css('lineHeight'), 0)});
				
				if (!isNaN(this._captionHeight)) {
					if (this._responsive) {
						$caption.outerHeight((this._captionHeight/this._slideHeight * 100) + '%');
					}
					else {
						$caption.outerHeight(this._captionHeight);
					}
				}
				
				if ($slide.data('caption-button')) {
					var $button = $('<div><div></div></div>').addClass('ts-caption-button').css(isTop ? 'bottom' : 'top', 0).click($.proxy(this.toggleCaption, this)).mousedown(preventDefault);
					$wrapper.append($button);
					this.bindCaptionEvents($slide, 'tsShowCaption', 'tsHideCaption');
				}
				else if (!IS_TOUCH) {
					this.bindCaptionEvents($slide, 'mouseenter', 'mouseleave');
				}	
			}
		},
		
		bindCaptionEvents: function($slide, showEvent, hideEvent) {
			var $wrapper = $slide.find('>.ts-wrapper');
			var $caption = $wrapper.find('>.ts-caption');
			
			switch($slide.data('caption-effect')) {
				case 'slide':
					if ($.support.transition && $.support.transform) {
						var className;
						if ('top' === $slide.data('caption-align')) {
							className = 'ts-slide-down';
							$caption.css({top:'auto', bottom:'100%'});
						}
						else {
							className = 'ts-slide-up';
							$caption.css({top:'100%', bottom:'auto'});
						}
						$wrapper.bind(showEvent, function() { $caption.addClass(className); }).bind(hideEvent, function() { $caption.removeClass(className); });
					}
					else {
						var pos = ('top' === $slide.data('caption-align') ? 'top' : 'bottom');
						$caption.css(pos, '-100%');
						$wrapper.bind(showEvent, {position:pos}, this.slideInCaption).bind(hideEvent, {position:pos}, this.slideOutCaption);
					}
					break;
				case 'fade':
					$caption.css({opacity:0});
					$wrapper.bind(showEvent, this.fadeInCaption).bind(hideEvent, this.fadeOutCaption);
					break;
				case 'normal':
					$caption.hide();
					$wrapper.bind(showEvent, function() { $caption.show(); }).bind(hideEvent, function() { $caption.hide(); });
					break;
				default:
					var $button = $wrapper.find('>.ts-caption-button');
					if ($button.length) {
						$wrapper.find('>.ts-caption-button').addClass('ts-collapse');
						$wrapper.bind(showEvent, function() { $caption.show(); }).bind(hideEvent, function() { $caption.hide(); });
					}
					break;
			}
		},
		
		//init slide panel
		initSlidePanel: function() {
			var numSlides = ('index' === this._options.control ? this._numDisplay * Math.ceil(this._numItems/this._numDisplay) : this._numItems);
			var $wrappers = this._$slides.find('>.ts-wrapper');
			
			if (this._responsive) {
				this._$slides.addClass('ts-border-box');
				if (this._isVertical) {
					this._$slides.width('100%').css({paddingTop:this._slideMargin, paddingBottom:this._slideMargin});
					this._$slideList.width('100%');
				}
				else {
					this._$slides.width((1/this._numItems * 100) + '%').css({paddingLeft:this._slideMargin, paddingRight:this._slideMargin});
					this._$slideList.width((this._numItems/this._numDisplay * 100) + '%');
				}
			}
			else {
				$wrappers.width(this._slideWidth).height(this._slideHeight);
				this._$slides.width($wrappers.outerWidth()).height($wrappers.outerHeight() + this._$slides.find('>.ts-caption').outerHeight());
					
				if (this._isVertical) {
					this._$slides.css({paddingTop:this._slideMargin, paddingBottom:this._slideMargin});
					this._$slideList.height(numSlides * this._$slides.outerHeight()).width(this._$slides.outerWidth());
					this._$slidePanel.height(this._numDisplay * this._$slides.outerHeight()).width(this._$slides.outerWidth());
				}
				else {
					this._$slides.css({paddingLeft:this._slideMargin, paddingRight:this._slideMargin});
					this._$slideList.width(numSlides * this._$slides.outerWidth()).height(this._$slides.outerHeight());
					this._$slidePanel.width(this._numDisplay * this._$slides.outerWidth()).height(this._$slides.outerHeight());
				}
			}
			
			this.setOptColor($wrappers, this._options.slideBackgroundColor, 'backgroundColor');
			this.setOptColor($wrappers, this._options.slideBorderColor, 'borderColor');
		},
		
		//init header
		initHeader: function() {
			var displayTitle = !isEmpty(this._options.title) && false !== this._options.title,
				displayInfo = this._options.pageInfo,
				displayPlay = this._options.playButton;
			
			if (displayTitle || displayInfo || displayPlay || 'small' === this._options.navButtons) {
				var $panel = $('<div></div>').addClass('ts-header');
				this._$scroller.prepend($panel);
				
				if (displayTitle) {
					$panel.append($('<div></div>').addClass('ts-title').html(this._options.title));
				}
				
				if (displayPlay) {
					$panel.append($('<div><div></div></div>').addClass('ts-play-button').toggleClass('ts-pause', !this._rotate).click($.proxy(this.togglePlay, this)));
				}
				
				if (displayInfo) {
					var $pageInfo = $('<div></div>').addClass('ts-page-info');
					$panel.append($pageInfo);
					
					this._$scroller.bind(REFRESH_INFO, $.proxy(function() {
						var start = this._currIndex + 1,
							end = Math.min(this._currIndex + this._numDisplay, this._numItems);
						$pageInfo.text((start != end ? (start + '-' + end) : start) + ' of ' + this._numItems);
					}, this));
				}
			}
		},
		
		//init control
		initControl: function() {
			this.initButtons();
			
			if ('scrollbar' === this._options.control || 'index' === this._options.control) {
				this._$scroller.append($('<div></div>').addClass('ts-control'));
				if ('scrollbar' === this._options.control) {
					this.initScrollbar();
				}
				else {
					this.initNav();
				}
			}
		},
		
		//init buttons
		initButtons: function() {							
			if (false !== this._options.navButtons && 'none' !== this._options.navButtons) {
				var $prevButton = $('<div><div></div></div>'),
					$nextButton = $('<div><div></div></div>'),
					$buttons = $prevButton.add($nextButton);
				
				if ('hover' === this._options.navButtons || 'mouseover' === this._options.navButtons) {
					$prevButton.addClass('ts-hover-prev');
					$nextButton.addClass('ts-hover-next');
					this._$slidePanel.append($buttons);
					
					var margin = ('+=' + (this._slideMargin + this._borderWidth));
					if (this._isVertical) {
						$prevButton.css({marginTop:margin});
						$nextButton.css({marginBottom:margin});
					}
					else {
						$prevButton.css({marginLeft:margin});
						$nextButton.css({marginRight:margin});
					}
					
					if (IS_TOUCH) {
						$buttons.css({opacity:1});
					}
					else {
						if ($.support.transition) {
							$buttons.addClass('ts-css-hover');
						}
						else {
							this._$slidePanel.hover(
								function() {
									$buttons.animate({opacity:1}, {duration:ANIMATE_SPEED, queue:false});
								}, 
								function() {
									$buttons.animate({opacity:0}, {duration:ANIMATE_SPEED, queue:false});
								});
						}
					}
				}
				else if ('small' === this._options.navButtons) {
					var $header = this._$scroller.find('>.ts-header'),
						$playButton = $header.find('>.ts-play-button');
					
					$prevButton.addClass('ts-small-prev');
					$nextButton.addClass('ts-small-next');
										
					if ($playButton.length) {
						$playButton.before($nextButton).after($prevButton);
					}
					else {
						$header.prepend($prevButton).prepend($nextButton);
					}
				}
				else {
					$prevButton.addClass('ts-prev');
					$nextButton.addClass('ts-next');
					this._$scroller.append($buttons).css({overflow:'visible'});
					
					if (this._isVertical) {
						this._$scroller.css({marginTop:$prevButton.outerHeight(), marginBottom:$nextButton.outerHeight()});
						$prevButton.css({top:-$prevButton.outerHeight()});
						$nextButton.css({bottom:-$nextButton.outerHeight()});
					}
					else {
						this._$scroller.css({marginLeft:$prevButton.outerWidth(), marginRight:$nextButton.outerWidth()});
						$prevButton.css({left:-$prevButton.outerWidth()});
						$nextButton.css({right:-$nextButton.outerWidth()});
					}
				}
				
				$prevButton.click($.proxy(this.prevSlides, this));
				$nextButton.click($.proxy(this.nextSlides, this));
				
				if (!this._options.continuous) {
					this._$scroller.bind(REFRESH_BUTTONS, $.proxy(function() {
						$prevButton.toggleClass('ts-disabled', 0 === this._currIndex);
						$nextButton.toggleClass('ts-disabled', this._limit == this._currIndex);  
					}, this));
				}
			}
		},
		
		//init scrollbar
		initScrollbar: function() {
			var	$cpanel = this._$scroller.find('>.ts-control');
			this._$scrubber = $('<div></div>').addClass('ts-scrubber');
			this._$scrollbar = $('<div></div>').addClass('ts-scrollbar').append(this._$scrubber);
			$cpanel.append(this._$scrollbar);
			
			if (!this._isVertical) {
				$cpanel.css({paddingLeft:this._slideMargin, paddingRight:this._slideMargin});
			}
			
			this._$scrollbar.click($.proxy(function(e) {
								this._$scroller.trigger(PAUSE_INTERACTION);
								this.autoStop((e.pageX - this._$scrollbar.offset().left)/this._$scrollbar.width());
							}, this)).mousedown(preventDefault);
			
			this._$scrubber.width((this._numDisplay/this._numItems * 100) + '%').click(function(e) { e.stopPropagation(); });
			
			try {
				this._$scrubber.draggable({
					containment:'parent',
					start: $.proxy(function() {
						this._$scroller.trigger(PAUSE_INTERACTION);   
						this.stopTimer();
						this._$scroller.unbind(START_TIMER); 
					}, this),
					stop: $.proxy(function() { 
						this._$scroller.unbind(START_TIMER).bind(START_TIMER, $.proxy(this.startTimer, this));
						this.autoStop(this._$scrubber.position().left/(this._$scrollbar.width() - this._$scrubber.width())); 
					}, this),
					drag: this._isVertical ? $.proxy(this.scrubVertical, this) : $.proxy(this.scrubHorizontal, this)
				});
			}
			catch (ex) {
				//not draggable.
			}
			
			this._$scroller.bind(REFRESH_SCRUBBER, $.proxy(function(e, animate) { 
				var pos = Math.round(this._currIndex/this._limit * (this._$scrollbar.width() - this._$scrubber.width()));
					
				if (animate) {
					this._$scrubber.animate({left:pos}, {duration:this._duration, easing:this._easing, queue:false});
				}
				else {
					this._$scrubber.css({left:pos});
				}
			}, this));
			
			
			if (this._collapsible) {
				this._$scroller.bind(COLLAPSE_SCROLLBAR, $.proxy(this.collapseScrollbar, this));
			}
			else if (this._responsive) {
				this._$scroller.bind(RESIZE_SCROLLBAR, $.proxy(this.resizeScrollbar, this));
			}		
		},
		
		scrubHorizontal: function(e) {
			var ratio = (this._$slideList.width() - this._$slidePanel.width())/(this._$scrollbar.width() - this._$scrubber.width());
			this._$slideList.css({left:-Math.round(this._$scrubber.position().left * ratio)});
		},
		
		scrubVertical: function(e) {
			var ratio = (this._$slideList.height() - this._$slidePanel.height())/(this._$scrollbar.width() - this._$scrubber.width());
			this._$slideList.css({top:-Math.round(this._$scrubber.position().left * ratio)});
		},
		
		resizeScrollbar: function() {
			var range = (this._$scrollbar.width() - this._$scrubber.width()),
				pct = this._currIndex/this._limit;
			this._$scrubber.stop(true).css({left:Math.round(pct * range)});
		},
		
		collapseScrollbar: function() {
			this._$scrubber.width((this._numDisplay/this._numItems * 100) + '%');
			this.resizeScrollbar();
		},
		
		//init control nav
		initNav: function() {
			this._$navList = $('<ul class="ts-nav"></ul>');
			this._$scroller.find('>.ts-control').append(this._$navList);
			this.initNavItems();
				
			this._$navList.on('click', '>li', $.proxy(this.selectNav, this))
						  .on('mousedown', '>li', preventDefault);
			
			this._$scroller.bind(REFRESH_NAV, $.proxy(function() {
				var index = Math.floor(this._currIndex/this._numDisplay);
				this._$navList.find('>li').removeClass('ts-active').eq(index).addClass('ts-active');
			}, this));
			
			if (this._collapsible) {
				this._$scroller.bind(COLLAPSE_NAV, $.proxy(this.initNavItems, this));
			}
		},
		
		//select control nav
		selectNav: function(e) {
			this._$scroller.trigger(PAUSE_INTERACTION);
			
			var $item = $(e.currentTarget);
			if (!$item.hasClass('ts-active')) {			
				this._currIndex = $item.index() * this._numDisplay;
				this.updateSlideList(true);
			}
		},
		
		initNavItems: function() {
			var size = Math.ceil(this._numItems/this._numDisplay);
			this._$navList.empty();
			if (1 < size) {
				for (var i = 0; i < size; i++) {
					this._$navList.append($('<li></li>'));
				}
				
				var $navItems = this._$navList.find('>li');
				this._$navList.width($navItems.length * $navItems.outerWidth(true));
			}
		},
		
		//update slide list
		updateSlideList: function(animate) {
			this.stopTimer();
			
			var props = {};
			if (this._isVertical) {
				props['top'] = -this._currIndex * this._$slides.outerHeight();
			}
			else {
				props['left'] = -this._currIndex * this._$slides.outerWidth();
			}
			
			if (animate) {
				this._$slideList.stop(true).animate(props, this._duration, this._easing, $.proxy(function() { this._$scroller.trigger(START_TIMER); }, this));
			}
			else {
				this._$slideList.stop(true).css(props);
				this._$scroller.trigger(START_TIMER);
			}
			
			this._$scroller.trigger(REFRESH_INFO).trigger(REFRESH_BUTTONS).trigger(REFRESH_SCRUBBER, [animate]).trigger(REFRESH_NAV);
			
			if (0 === this._currIndex) {
				this._$scroller.trigger(SCROLLER_BEGIN);
				this._options.onBegin.call(this);
			}
			
			if (this._currIndex == this._limit) {
				this._$scroller.trigger(SCROLLER_END);
				this._options.onEnd.call(this);
				if (this._options.playOnce) {
					this.pause();
				}				
			}
			
			//trigger content load
			var size = Math.min(this._currIndex + this._numDisplay, this._numItems);
			for (var i = this._currIndex; i < size; i++) {
				this._$slides.eq(i).trigger(LOAD_CONTENT);
			}
		},
		
		//auto stop
		autoStop: function(pct) {			
			var move, unitSize, range;
			
			if (this._isVertical) {
				unitSize = this._$slides.outerHeight();
				range = this._$slideList.height() - this._$slidePanel.height();
			}
			else {
				unitSize = this._$slides.outerWidth();
				range = this._$slideList.width() - this._$slidePanel.width();
			}
			
			var newPos = pct * range,
				pos = this._currIndex * unitSize;
			
			if (newPos > pos) {
				move = Math.ceil(newPos/unitSize);
			}
			else if (newPos < pos) {
				move = Math.floor(newPos/unitSize);
			}
			else {
				return;
			}
			
			this._currIndex = Math.min(move, this._limit);
			this.updateSlideList(true);
		},
		
		//go to previous slides
		prevSlides: function() {
			this._$scroller.trigger(PAUSE_INTERACTION);
			
			if (this._currIndex > 0) {
				this._currIndex -= (this._options.moveByOne ? 1 : Math.min(this._numDisplay, this._currIndex));
			}
			else if (this._options.continuous) {
				this._currIndex = this._limit;
			}
			else {
				return;
			}
			
			this._$scroller.trigger(SCROLLER_PREV);
			this._options.onPrevious.call(this);
			
			this.updateSlideList(true);
		},
		
		//go to next slides
		nextSlides: function() {
			this._$scroller.trigger(PAUSE_INTERACTION);

			if (this._currIndex < this._limit) {
				this._currIndex += this._options.moveByOne ? 1 : Math.min(this._numDisplay, this._limit - this._currIndex);
			}
			else if (this._options.continuous) {
				this._currIndex = 0;
			}
			else {
				return;
			}
			
			this._$scroller.trigger(SCROLLER_NEXT);
			this._options.onNext.call(this);
			
			this.updateSlideList(true);
		},
		
		//rotate slides
		rotateSlides: function() {
			if (this._currIndex < this._limit) {
				this._currIndex += this._options.moveByOne ? 1 : Math.min(this._numDisplay, this._limit - this._currIndex);
			}
			else {
				this._currIndex = 0;
			}
			this.updateSlideList(true);
		},
		
		//toggle play/pause
		togglePlay: function() {
			if (this._rotate) { 
				this.pause();
			}
			else {
				this.play();
			}
		},
		
		play: function() {
			if (!this._rotate) {
				this._$scroller.find('>.ts-header>.ts-play-button').removeClass('ts-pause');
				this._rotate = true;
				this._$scroller.trigger(START_TIMER).trigger(SCROLLER_PLAY);
				this._options.onPlay.call(this);
			}
		},
		
		pause: function() {
			if (this._rotate) {
				this._$scroller.find('>.ts-header>.ts-play-button').addClass('ts-pause');
				this._rotate = false;
				this.stopTimer();
				
				this._$scroller.trigger(SCROLLER_PAUSE);
				this._options.onPause.call(this);
			}
		},
		
		//process & load content
		processContent: function(e) {
			var $slide = $(e.currentTarget),
				$wrapper = $slide.find('>.ts-wrapper'),
				url = $slide.data('src'),
				contentType = $slide.data('content-type');
			
			if (isEmpty(contentType)) {
				contentType = getExtType(url);
			}
			
			$wrapper.find('>img:first-child, >.ts-content').remove();
			
			var $container = $wrapper;
			var $link = $wrapper.find('>a:first-child:not(.ts-link-button, .ts-zoom-button)');
			if ($link.length) {
				$container = $link;
			}
			
			if ('image' === contentType) {
				var $img = $('<img/>').addClass('ts-content');
				$container.prepend($img);
				
				$img.one('load', $.proxy(this.processImg, this)).attr('src', url);
				if ($img[0].complete || 'complete' === $img[0].readyState) {
					$img.trigger('load');
				}
			}
			else if ('inline' === contentType) {
				var $el = $(url);
				if ($el.length) {
					$container.prepend($('<div></div>').addClass('ts-content').html($el.html()));
					this.showContent($slide);
				}
			} 
			else if ('flash' === contentType) {
				var html =  "<object type='application/x-shockwave-flash' data='" + url + "' width='100%' height='100%'>" +
							"<param name='movie' value='" + url + "'/>" +
							"<param name='allowFullScreen' value='true'/>" +
							"<param name='quality' value='high'/>" +
							"<param name='wmode' value='transparent'/>" +
							"<param name='scale' value='default'>" +
							"</object>";
								
				$container.prepend($('<div></div>').addClass('ts-content').html(html));
				this.showContent($slide);
			}
			else if ('ajax' === contentType) {
				var $div = $('<div></div>').addClass('ts-content');
				$container.prepend($div);
				
				var index = url.indexOf('?'), 
					varData = '';
			
				if (-1 < index) {
					varData = url.substring(index + 1);
					url = url.substring(0, index);
				}	
			
				var methodType = $slide.data('method');
				if (isEmpty(methodType)) {
					methodType = 'GET';
				}
				
				$.ajax({url:url, type:methodType, data:varData,
  					success:$.proxy(function(data) {
						$div.html(data);
						this.showContent($slide);
					}, this)
				});
			}
			else {
				var $iframe = $('<iframe frameborder="0" hspace="0" scrolling="auto" width="100%" height="100%"></iframe>').addClass('ts-content');
				$container.prepend($iframe);
				
				$iframe.load($.proxy(function() {
					this.showContent($slide);
				}, this)).attr('src', url);
			}
		},
		
		//process image size & position
		processImg: function(e) {
			var $img = $(e.currentTarget),
				$slide = $img.closest('.ts-slide');
			
			switch($slide.data('image-position')) {
				case 'fill':
					this.fillContent($img, this._slideWidth, this._slideHeight);
					break;
				case 'fit':
					this.fitContent($img, this._slideWidth, this._slideHeight);
					break;
				case 'center':
					this.centerContent($img, this._slideWidth, this._slideHeight);
					break;
				case 'stretch':
					this.stretchContent($img, this._slideWidth, this._slideHeight);
					break;
			}
			
			if (this._responsive) {
				var top = parseInt($img.css('top'), 0);
				top = isNaN(top) ? 0 : ((top/this._slideHeight * 100) + '%');
				
				var left = parseInt($img.css('left'), 0);
				left = isNaN(left) ? 0 : ((left/this._slideWidth * 100) + '%');
				
				var width = ($img.width()/this._slideWidth * 100) + '%',
					height = ($img.height()/this._slideHeight * 100) + '%';
				
				$img.css({top:top, left:left, bottom:'auto', right:'auto'}).width(width).height(height);
			}
			
			if ($.support.opacity) {
				$img.after($('<div></div>').addClass('ts-overlay'));
			}
					
			this.showContent($slide);
		},
		
		//center content
		centerContent: function($img, boxWidth, boxHeight) {
			$img.css({top:(boxHeight - $img.height())/2, left:(boxWidth - $img.width())/2});
		},
		
		//fill content
		fillContent: function($img, boxWidth, boxHeight) {
			var width = $img.width(), height = $img.height(),
				scale = Math.max(boxHeight/height, boxWidth/width);
			
			$img.width(width * scale).height(height * scale);
			this.centerContent($img, boxWidth, boxHeight);
		},
		
		//fit content
		fitContent: function($img, boxWidth, boxHeight) {
			var width = $img.width(), 
				height = $img.height(),
				boxRatio = boxWidth/boxHeight, 
				ratio = width/height;
			
			if (boxRatio > ratio) {
				width *= boxHeight/height;
				height = boxHeight;
			}
			else {
				height *= boxWidth/width;
				width = boxWidth;
			}
			
			$img.width(width).height(height);
			this.centerContent($img, boxWidth, boxHeight);
		},
		
		//stretch content
		stretchContent: function($img, boxWidth, boxHeight) {
			$img.css({top:0, left:0, width:boxWidth, height:boxHeight});
		},
		
		showContent: function($slide) {
			$slide.find('>.ts-wrapper').css({backgroundImage:'none'}).find('.ts-content').css({opacity:1});
		},
		
		//toggle caption
		toggleCaption: function(e) {
			this._$scroller.trigger(PAUSE_INTERACTION);
			
			var $button = $(e.currentTarget),
				$wrapper = $button.parent(),
				$caption = $wrapper.find('>.ts-caption'),
				visible = $button.hasClass('ts-collapse');
				
			if (visible) {
				$wrapper.trigger('tsHideCaption');
				$button.removeClass('ts-collapse');
			}
			else {
				$wrapper.trigger('tsShowCaption');
				$button.addClass('ts-collapse');
			}
		},
		
		//slide in caption
		slideInCaption: function(e) {
			var $caption = $(e.currentTarget).find('>.ts-caption'), 
				props = {};
			props[e.data.position] = 0;
			$caption.animate(props, {duration:ANIMATE_SPEED, queue:false});
		},
		
		//slide out caption
		slideOutCaption: function(e) {
			var $caption = $(e.currentTarget).find('>.ts-caption'), 
				props = {};
			props[e.data.position] = '-100%';
			$caption.animate(props, {duration:ANIMATE_SPEED, queue:false});
		},
		
		//fade in caption
		fadeInCaption: function(e) {
			$(e.currentTarget).find('>.ts-caption').animate({opacity:1}, {duration:ANIMATE_SPEED, queue:false});
		},
		
		//fade out caption
		fadeOutCaption: function(e) {
			$(e.currentTarget).find('>.ts-caption').animate({opacity:0}, {duration:ANIMATE_SPEED, queue:false});
		},
		
		//shuffle slides
		shuffleItems: function() {
			var slides = this._$slides.toArray();
			shuffleArray(slides);
			this._$slideList.append(slides);
		},
		
		//start timer
		startTimer: function() {
			if (null === this._timerId && this._rotate) {
				this._timerId = setTimeout($.proxy(this.rotateSlides, this), this._delay);
			}
		},
		
		//stop timer
		stopTimer: function() {
			clearTimeout(this._timerId);
			this._timerId = null;
		},
		
		pauseTimer: function() {
			this.stopTimer();
			this._$scroller.unbind(START_TIMER);
			
			clearTimeout(this._resumeId);
			this._resumeId = setTimeout($.proxy(function() {
				this._$scroller.unbind(START_TIMER).bind(START_TIMER, $.proxy(this.startTimer, this)).trigger(START_TIMER);
			}, this), 1000);
		},
		
		setOptColor: function($el, color, prop) {
			if (typeof color !== 'undefined') {
				if ('backgroundColor' === prop || 'background-color' === prop) {
					if ('' === $.trim(color)) {
						color = 'transparent';
					}
				}
				$el.css(prop, color);
			}
		},
		
		//mousewheel scroll content
		mouseScroll: function(e) {
			e.preventDefault();
			if (!this._$slideList.is(':animated')) {
				var delta = (typeof e.originalEvent.wheelDelta === 'undefined') ?  -e.originalEvent.detail : e.originalEvent.wheelDelta;
				if (0 < delta) {
					this.prevSlides();
				}
				else {
					this.nextSlides();
				}
			}
		},
		
		//keyup event handler
		keyControl: function(e) {
			switch(e.keyCode) {
				case 37:
					this.prevSlides();
					break;
				case 39:
					this.nextSlides();
					break;
				case 80:
					this.togglePlay();
					break;
			}
		},
		
		touchStart: function(e) {
			if (1 === e.originalEvent.touches.length) {
				this._startX = e.originalEvent.touches[0].pageX;
				this._startY = e.originalEvent.touches[0].pageY;
				this._$slidePanel.bind('touchmove', $.proxy(this.touchMove, this)).one('touchend', $.proxy(this.touchEnd, this));
			}
		},
		
		touchMove: function(e) {
			var xDist = this._startX - e.originalEvent.touches[0].pageX;
			var	yDist = this._startY - e.originalEvent.touches[0].pageY;
				
			if (this._isVertical) {
				this._swipeDist = yDist;
				this._scrolling = Math.abs(this._swipeDist) < Math.abs(xDist);
			}
			else {
				this._swipeDist = xDist;
				this._scrolling = Math.abs(this._swipeDist) < Math.abs(yDist);
			}
			
			if (!this._scrolling) {
				e.preventDefault();
			}
		},
		
		touchEnd: function(e) {
			this._$slidePanel.unbind('touchmove');
			
			if (!this._scrolling) {
				if (null !== this._swipeDist && Math.abs(this._swipeDist) > SWIPE_MIN) {
					if (this._swipeDist > 0) {
						if (this._currIndex < this._limit) {
							this.nextSlides();
						}
					}
					else {
						if (this._currIndex > 0) {
							this.prevSlides();
						}
					}
				}
			}
		
			this._startX = this._startY = this._swipeDist = null;
		},
		
		processFlickr: function() {
			var url = this._options.flickr;
			
			$.getJSON(url, $.proxy(function(data) {				
				this._options.title = data.title;
				
				var content = '<ul>';
				$.each(data.items, $.proxy(function(n, img) {
					content += 	'<li><img src="' + img.media.m + '"/><div>' + img.title + '</div></li>';
				}, this));
				content += '</ul>';
				
				this._$scroller.empty().append(content);
				this.init();
			}, this));
		}
	};
	
	//shuffle array
	function shuffleArray(arr) {
		var i = arr.length;
		while(--i > 0) {
			var ri = Math.floor(Math.random() * (i+1)),
				temp = arr[i];
			arr[i] = arr[ri];
			arr[ri] = temp;
		}
	}
	
	//prevent default behavior
	function preventDefault(e) {
		e.preventDefault();
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
	
	//check is empty
	function isEmpty(val) {
		return (typeof val === 'undefined' || '' === $.trim(val));
	}
	
	//get positive int
	function getPosInteger(val, defaultVal) {
		val = parseInt(val, 0);
		return (isNaN(val) || val <= 0) ? defaultVal : val;
	}
	
	//get nonnegative int
	function getNonNegInteger(val, defaultVal) {
		val = parseInt(val, 0);
		return (isNaN(val) || val < 0) ? defaultVal : val;
	}
	
	//get string value
	function getValue(val, defaultVal) {
		return (typeof val !== 'undefined') ? val : defaultVal;
	}
	
	//get extension type
	function getExtType(url) {
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
	
	var methods = {
  		previous: function() {
			$(this).data(PLUGIN_NAME).prevSlide();
		},
		next: function() {
			$(this).data(PLUGIN_NAME).nextSlide();
		},
		play: function() {
			$(this).data(PLUGIN_NAME).play();
		},
		pause: function() {
			$(this).data(PLUGIN_NAME).pause();
		},
		destroy: function() {
			var obj = $(this).data(PLUGIN_NAME);
			obj.pause();
			if (!isEmpty(obj._namespace)) {
				$(window).add($(document)).unbind(obj._namespace);
			}
			obj._$scroller.add($('*', obj._$scroller)).unbind().removeData();
			$(this).removeData(PLUGIN_NAME);
		}
 	};
	
	var defaults = {
		responsive:false,
		collapsible:false,
		orientation:'horizontal',
		title:'',
		numDisplay:4,
		slideWidth:300,
		slideHeight:200,
		slideMargin:0,
		slideBorder:0,
		padding:10,
		captionHeight:'auto',
		startIndex:0,
		autoPlay:false,
		delay:5000,
		speed:800,
		easing:'',		
		playOnce:false,		
		pauseOnHover:false,
		pauseOnInteraction:false,
		moveByOne:false,
		control:'index',
		navButtons:'normal',
		playButton:true,
		captionButton:false,
		captionAlign:'bottom',
		captionPosition:'inside',
		captionEffect:'fade',
		imagePosition:'fill',
		continuous:true,
		shuffle:false,
		mousewheel:false,
		keyboard:false,
		swipe:true,
		pageInfo:true,
		onInit:function() {},			
		onPlay:function() {},
		onPause:function() {},
		onPrevious:function() {},
		onNext:function() {},
		onBegin:function() {},
		onEnd:function() {}
	};
		
	$.fn.thumbScroller = function() {
		var args = arguments;
		var params = args[0];
		
		return this.each(
			function(n, el) {
				if (methods[params]) {
					if (typeof $(el).data(PLUGIN_NAME) !== 'undefined') {
						methods[params].apply(el, Array.prototype.slice.call(args, 1));
					}
				}
				else if (typeof params === 'object' || !params) {
					var plugin = new ThumbScroller(el, $.extend({}, defaults, params));
					$(el).data(PLUGIN_NAME, plugin);
					
					plugin._$scroller.trigger(SCROLLER_INIT);
					plugin._options.onInit.call(plugin);
				}
			}
		);
	};
})(jQuery);