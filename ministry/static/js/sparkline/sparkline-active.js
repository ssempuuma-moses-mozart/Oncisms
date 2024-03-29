(function ($) {
 "use strict";
 
	$("#sparkline1").sparkline([34, 43, 43, 35, 44, 32, 44, 52, 25], {
        type: 'line',
        lineColor: '#17997f',
		lineWidth: 1,
		barSpacing: '100px',
        fillColor: '#42B54A',
    });
    $("#sparkline2").sparkline([-4, -2, 2, 0, 4, 5, 6, 7], {
        type: 'bar',
        barColor: '#42B54A',
        negBarColor: '#303030'});

    $("#sparkline3").sparkline([1, 1, 2], {
        type: 'pie',
        sliceColors: ['#42B54A', '#303030', '#ff9999']});

    $("#sparkline4").sparkline([34, 43, 43, 35, 44, 32, 15, 22, 46, 33, 86, 54, 73, 53, 12, 53, 23, 65, 23, 63, 53, 42, 34, 56, 76, 15, 54, 23, 44], {
        type: 'line',
        lineColor: '#42B54A',
        fillColor: '#ffffff',
    });

    $("#sparkline5").sparkline([1, 1, 0, 1, 1, 1, 1, 1, -1, -2, -3, -4], {
        type: 'tristate',
        posBarColor: '#42B54A',
        negBarColor: '#303030'});


    $("#sparkline6").sparkline([4, 6, 7, 7, 4, 3, 2, 1, 4, 4, 5, 6, 3, 4, 5, 8, 7, 6, 9, 3, 2, 4, 1, 5, 6, 4, 3, 7, ], {
        type: 'discrete',
        lineColor: '#42B54A'});

    $("#sparkline7").sparkline([52, 12, 44], {
        type: 'pie',
        height: '150px',
        sliceColors: ['#42B54A', '#303030', '#e4f0fb']});

    $("#sparkline8").sparkline([5, 6, 7, 2, 0, 4, 2, 4, 5, 7, 2, 4, 12, 14, 4, 2, 14, 12, 7], {
        type: 'bar',
        barWidth: 8,
        height: '150px',
        barColor: '#42B54A',
        negBarColor: '#303030'});

    $("#sparkline9").sparkline([34, 43, 43, 35, 44, 32, 15, 22, 46, 33, 86, 54, 73, 53, 12, 53, 23, 65, 23, 63, 53, 42, 34, 56, 76, 15, 54, 23, 44], {
        type: 'line',
        lineWidth: 1,
        width: '150px',
        height: '150px',
        lineColor: '#999',
        fillColor: '#42B54A',
    });
	
	 $('.sparklineadminpro').sparkline([ [1], [2], [3], [4, 2], [3], [5, 3] ], { type: 'bar', barColor: '#42B54A',
        negBarColor: '#303030',});
	
	
	

	var sparklineCharts = function(){
		 $("#sparkline22").sparkline([34, 43, 43, 35, 44, 32, 44, 52], {
			 type: 'line',
			 width: '100%',
			 height: '60',
			 lineColor: '#1ab394',
			 fillColor: "#ffffff"
		 });

		 $("#sparkline23").sparkline([24, 43, 43, 55, 44, 62, 44, 72], {
			 type: 'line',
			 width: '100%',
			 height: '60',
			 lineColor: '#1ab394',
			 fillColor: "#ffffff"
		 });

		 $("#sparkline24").sparkline([74, 43, 23, 55, 54, 32, 24, 12], {
			 type: 'line',
			 width: '100%',
			 height: '60',
			 lineColor: '#ed5565',
			 fillColor: "#ffffff"
		 });

		 $("#sparkline25").sparkline([24, 43, 33, 55, 64, 72, 44, 22], {
			 type: 'line',
			 width: '100%',
			 height: '60',
			 lineColor: '#ed5565',
			 fillColor: "#ffffff"
		 });

		 $("#sparkline51").sparkline([1, 4], {
			 type: 'pie',
			 height: '140',
			 sliceColors: ['#1ab394', '#F5F5F5']
		 });

		 $("#sparkline52").sparkline([5, 3], {
			 type: 'pie',
			 height: '140',
			 sliceColors: ['#1ab394', '#F5F5F5']
		 });

		 $("#sparkline53").sparkline([2, 2], {
			 type: 'pie',
			 height: '140',
			 sliceColors: ['#ed5565', '#F5F5F5']
		 });

		 $("#sparkline54").sparkline([2, 3], {
			 type: 'pie',
			 height: '140',
			 sliceColors: ['#ed5565', '#F5F5F5']
		 });
	};

	var sparkResize;

	$(window).resize(function(e) {
		clearTimeout(sparkResize);
		sparkResize = setTimeout(sparklineCharts, 500);
	});

	sparklineCharts();



	
	
})(jQuery); 