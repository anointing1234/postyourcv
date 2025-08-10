/*------------------------------------------------------------------------------------
    
JS INDEX
=============

01 - Dropdown Menu JS
02 - Main Slider JS
03 - Course Slider JS
04 - Scroll JS
05 - Youtube Popup JS
06 - Team Slider JS
07 - Gallery JS
08 - Top Product JS
09 - Countdown JS
09 - Progressbar JS
10 - MAP JS
11 - Responsive Menu JS
12 - Btn To Top JS


-------------------------------------------------------------------------------------*/


(function ($) {
	"use strict";

    jQuery(document).ready(function($){
        
        /* 
        =================================================================
        01 - Dropdown Menu JS
        =================================================================	
        */
        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.btn-dropdown').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.btn-dropdown').val($(this).data('value'));
            });  
          };


        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.call-dropdown').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.call-dropdown').val($(this).data('value'));
            });  
          };

        
        /* 
        =================================================================
        02 - Main Slider JS
        =================================================================	
        */
        $(".kick-slide").owlCarousel({
            animateOut: 'fadeOut',
            animateIn: 'fadeIn',
            items: 1,
            nav: true,
            dots: false,
            autoplay: true,
            loop: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            mouseDrag: false,
            touchDrag: false
        });
        
        $(".kick-slide").on("translate.owl.carousel", function(){
            $(".kick-main-slide h2, .kick-main-slide p").removeClass("animated fadeInUp").css("opacity", "0");
            $(".kick-main-slide .kick-btn").removeClass("animated fadeInDown").css("opacity", "0");
        });
        $(".kick-slide").on("translated.owl.carousel", function(){
            $(".kick-main-slide h2, .kick-main-slide p").addClass("animated fadeInUp").css("opacity", "1");
            $(".kick-main-slide .kick-btn").addClass("animated fadeInDown").css("opacity", "1");
        });
        
        
        /* 
        =================================================================
        03 - Course Slider JS
        =================================================================	
        */
        $(".upcoming-slider").owlCarousel({
            autoplay:true,
            loop:true,
            margin:20,
            touchDrag:false,
            mouseDrag:false,
            nav: true,
            dots: false,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsive:{
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1000: {
                    items: 2
                },
                1200: {
                    items: 3
                }
            }
        });
        
        
        /* 
        =================================================================
        04 - Scroll JS
        =================================================================	
        */
        
        $(".kick-score-scroll").perfectScrollbar();
        
        /* 
        =================================================================
        05 - Youtube Popup JS
        =================================================================	
        */
        
         $('.popup-youtube').magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,

            fixedContentPos: false
        });

        /* 
        =================================================================
        06 - Team Slider JS
        =================================================================	
        */
        $(".top-player-slider").owlCarousel({
            autoplay:true,
            loop:true,
            margin:20,
            touchDrag:false,
            mouseDrag:false,
            nav: true,
            dots: false,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsive:{
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
        
        
        /* 
        =================================================================
        07 - Gallery JS
        =================================================================	
        */
        
        $(".gallery-lightbox").magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            },
             zoom: {
                    enabled: true, 
                    duration: 300, 
                    easing: 'ease-in-out',
                    opener: function (openerElement) {
                        
                        return openerElement.is('img') ? openerElement : openerElement.find('img');
                    }
                }
        });
        
        
        /* 
        =================================================================
        08 - Top Product JS
        =================================================================	
        */
        $(".top-product-slider").owlCarousel({
            autoplay:true,
            loop:true,
            margin:20,
            touchDrag:false,
            mouseDrag:false,
            nav: true,
            dots: false,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsive:{
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
        
        /* 
        =================================================================
        09 - Countdown JS
        =================================================================	
        */
       
        $('#coming-soon').countdown('2018/7/5', function (event) {
            var $this = $(this).html(event.strftime('' + '<p><span>%D</span>days</p>  ' + '<p><span>%H</span>Hours</p>  ' + '<p><span>%M</span>Minutes</p>  ' + '<p><span>%S</span>Seconds</p> '));
        });
        
        
        /* 
        =================================================================
        08 - Best Moment Slider JS
        =================================================================	
        */
        $(".moment-slider").owlCarousel({
            autoplay:true,
            loop:true,
            margin:20,
            touchDrag:false,
            mouseDrag:false,
            nav: true,
            dots: false,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsive:{
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1000: {
                    items: 1
                },
                1200: {
                    items: 1
                }
            }
        });
        
        /* 
        =================================================================
        09 - Progressbar JS
        =================================================================	
        */
            var $pcircle = $('.circle');
            var $pbar = $('.bar');
            $pcircle.each(function(i) {
            var circle = new ProgressBar.Circle(this, {
                color: 'rgba(224, 26, 34, 0.82)',
                trailColor: 'rgba(224, 26, 34, 0.82)',
                strokeWidth: 2,
                trailWidth: 2,
                duration: 2000,
                easing: 'easeInOut'
            });
            var cvalue = ($(this).attr('data-value') / 100);
            $pcircle.waypoint(function() {
                circle.animate(cvalue);
                }, {
                offset: "100%"
                })
            });
            $pbar.each(function(i) {
            var bar = new ProgressBar.Line(this, {
                color: '#0d0d0d',
                trailColor: 'rgba(168, 167, 167, 0.87)',
                strokeWidth: 2,
                trailWidth: 2,
                duration: 3000,
                easing: 'easeInOut',
                text: {
                    style: {
                        color: '#222222',
                        position: 'absolute',
                        right: '0',
                        top: '-30px',
                        padding: 0,
                        margin: 0,
                        transform: null
                    },
                    autoStyleContainer: false
                },
                step: function(state, bar, attachment) {
                    bar.setText(Math.round(bar.value() * 100) + ' %');
                }
            });
            var bvalue = ($(this).attr('data-value') / 100);
            $pbar.waypoint(function() {
                bar.animate(bvalue);
            },   {
                    offset: "100%"
                })
            });
        
        
        
        /* 
        =================================================================
        10 - MAP JS
        =================================================================	
        */
            if($('#map-canvas').length){
                google.maps.event.addDomListener(window, 'load', initialize);
            }
	
            function initialize() {
                var MY_MAPTYPE_ID = 'custom_style';
                var map;
                var brooklyn = new google.maps.LatLng(40.6743890, -73.9455);
                var featureOpts = [
                    {
                    "featureType": "road",
                    "elementType": "geometry",
                    "stylers": [
                        {
                            "lightness": 100
                        },
                        {
                            "visibility": "simplified"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "color": "#d6e9b9"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#d6e9b9"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#fbe7a4"
                        }
                    ]
                }
                ];	

                var mapOptions = {
                    zoom: 13,
                    scrollwheel: false,
                    center: brooklyn,
                    mapTypeControlOptions: {
                      mapTypeIds: [google.maps.MapTypeId.ROADMAP, MY_MAPTYPE_ID]
                    },
                    mapTypeId: MY_MAPTYPE_ID
                };


                map = new google.maps.Map(document.getElementById('map-canvas'),
                      mapOptions);

                var styledMapOptions = {
                    name: 'Custom Style'
                };

                var customMapType = new google.maps.StyledMapType(featureOpts, styledMapOptions);

                map.mapTypes.set(MY_MAPTYPE_ID, customMapType);
                var marker=new google.maps.Marker({
                  position:brooklyn,
                  });

                marker.setMap(map);
            }
        
        /* 
        =================================================================
        11 - Responsive Menu JS
        =================================================================	
        */
        
            $("ul#navigation_menu").slicknav({
                prependTo: ".responsive-menu-2"
            });
        
            $("ul#navigation_menu_2").slicknav({
                prependTo: ".responsive-menu-1"
            });

        /* 
        =================================================================
        12 - Btn To Top JS
        =================================================================	
        */
        if ($("body").length) {
            var btnUp = $('<div/>', {
                'class': 'btntoTop'
            });
            btnUp.appendTo('body');
            $(document).on('click', '.btntoTop', function() {
                $('html, body').animate({
                    scrollTop: 0
                }, 700);
            });
            $(window).on('scroll', function() {
                if ($(this).scrollTop() > 200) $('.btntoTop').addClass('active');
                else $('.btntoTop').removeClass('active');
            });
        }
        
        
    });
}(jQuery));	
