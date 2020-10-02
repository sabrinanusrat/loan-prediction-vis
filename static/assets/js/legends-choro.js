var w = 500;
var h = 350;
var topMargin = 100;
var padding = 35;
var centX = w/2;
var centY = (h-topMargin)/0.75;

var dataset = [];
var data = [ 0.1, 1, 5, 10];
						  
			data.forEach(function(d, i){dataset.push({r:Math.sqrt(d), x:centX, y:centY});});

//console.log(dataset);

			//Create scale functions
			var xScale = d3.scale.linear()
								 .domain([d3.min(dataset, function(d) { return d["x"]; }), d3.max(dataset, function(d) { return d["x"]; })])
								 .range([padding, w - padding * 2]);
//								 .range([padding, padding+ ]);

			var xScale1 = d3.scale.linear()
								 .domain([0.2*d3.min(dataset, function(d) { return d["x"]; }), 0.2*d3.max(dataset, function(d) { return d["x"]; })])
								 .range([padding, (w - padding * 2)]);
//								 .range([padding, padding+ ]);

			var yScale = d3.scale.linear()
								 .domain([0, d3.max(dataset, function(d) { return d["y"]; })])
								 .range([h - 2*padding, padding+topMargin]);

			var yScale1 = d3.scale.linear()
								 .domain([0, 0.2*d3.max(dataset, function(d) { return d["y"]; })])
								 .range([h - 2*padding, padding+topMargin]);

			var yScale2 = d3.scale.linear()
//								 .domain([0, d3.max(data)])
								 .domain(data)
								 .range([centY, centY+Math.sqrt(d3.max(data))]);

			//Define X axis
			var xAxis = d3.svg.axis()
							  .scale(xScale1)
							  .orient("bottom")
							  .ticks(10);

			//Define Y axis
			var yAxis = d3.svg.axis()
							  .scale(yScale2)
							  .orient("left")
							  .ticks(5);





var svg1 = d3.select("#chart3").append("svg:svg")
	.attr("width", w)
	.attr("height", h)
	.append("svg:g")
	.attr("transform", "translate(0,"+topMargin+") scale(0.75)");



svg1.selectAll("circle")
		.data(data)
		.enter()
		.append("circle")
		.style("stroke", "#111111")
		.style("stroke-width", function(d) { return 2; })
		.style("fill", "none")
		.attr("cx", centX)
		.attr("cy", centY)
		.attr("r", function(d)
					{
						return Math.sqrt(d)*25;
					});

///*
var varN1 = document.getElementById('var1').textContent;
var varN2 = document.getElementById('var2').textContent;

var off = 120;

svg1.append("text")
        .attr("x", off)
		.attr("y", 30)
		.attr("font-family", "sans-serif")
		.attr("font-size", "20px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v1 =");

svg1.append("text")
        .attr("x", off+150)
		.attr("y", 20)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text(varN1);

svg1.append("text")
        .attr("x", off+150)
		.attr("y", 40)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("Mean("+varN1+")");

svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(off+20)+", 25 L"+(off+300)+", 25")



svg1.append("text")
        .attr("x", off)
		.attr("y", 70)
		.attr("font-family", "sans-serif")
		.attr("font-size", "20px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v2 =");


svg1.append("text")
        .attr("x", off+110)
		.attr("y", 70)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text(varN2);

/*

svg1.append("text")
        .attr("x", off+150)
		.attr("y", 80)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("Mean("+varN2+")");

svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(off+20)+", 65 L"+(off+300)+", 65")







			//Create circles
			svg1.selectAll("circle")
			   .data(dataset)
			   .enter()
			   .append("circle")
			   .style("stroke", function(d) { if (1.03 * d["r1"] < d["r2"]) return "#FF6600"; else if (1.03*d["r2"]<d["r1"]) return "#0000FF"; else return "#acacac"; })
	           .style("stroke-width", function(d) { return 4; })
	           .style("stroke-opacity", function(d) { return 1; })
	           .style("fill", function(d) { if (1.03 * d["r1"] < d["r2"]) return "#FF6600"; else if (1.03*d["r2"]<d["r1"]) return "#0000FF"; else return "#acacac";  })
	           .attr("cx", function(d) { return xScale(d["x"]); })
	           .attr("cy", function(d) { return yScale(d["y"]); })
	           .attr("r", function(d, i) { 
					if (d["r1"] < d["r2"]) return d["r2"]; 
					else 
					return d["r1"]; 
					});
			   
			   
			   svg1
		      .selectAll("g")
		      .data(dataset)
		      .enter()
	          .append("circle")
			   .style("stroke", function(d) { return "#FFFFFF"; })
	           .style("stroke-width", function(d) { return 2; })
	           .style("stroke-opacity", function(d) { return 0.7; })
	          .style("fill", function(d) { return "#FFFFFF"; })
	           .attr("cx", function(d) { return xScale(d["x"]); })
	           .attr("cy", function(d) { return yScale(d["y"]); })
	           .attr("r", function(d, i) { 
					if (d["r1"] > d["r2"]) return d["r2"]; 
					else 
					return d["r1"]; 
					
					});
					
			   
			   
			//text for orange circle


var text1 = svg1
		.append("text")
        .attr("x", xScale(-2.8))
		.attr("y", yScale(0.6))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
//		.text("var 1");			
		.text("v1");			
			
			
var text2 = svg1
		.append("text")
		.attr("x", xScale(-3.2))
		.attr("y", yScale(0.6))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v2 >");	
		
		
		
			//text for blue circle


var text3 = svg1
		.append("text")
        .attr("x", xScale(3.2))
		.attr("y", yScale(0.6))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v2");			
			
			
var text4 = svg1
		.append("text")
		.attr("x", xScale(2.8))
		.attr("y", yScale(0.6))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v1 >");	
		
	//caption x	
var text5 = svg1
		.append("text")
		.attr("x", xScale(0))
		.attr("y", yScale(-1))
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("x = (v1 - v2)");	
		
			
	//caption y		
var text6 = svg1
		.append("text")
		.attr("x", xScale(0.55))
		.attr("y", yScale(1.5))
//		.attr("x", 200)
//		.attr("y", 150)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.attr("transform", "translate("+xScale(0.55)+", "+yScale(1.5)+") rotate(270) translate("+(-xScale(0.55))+", "+(-yScale(1.5))+")")
//		.attr("transform", function(d) {
//			return "rotate(0)" ;
//		})
		.text("y = max(v1, v2)");	
//		.text("xy");	
		
	//	svg.select(text2)
	//	.attr("transform", function(d) {
	//		return "rotate(30)" ;
	//	})



svg1.append("text")
		.attr("x", xScale(-3.9))
		.attr("y", yScale(1.7))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v2");
var stx = xScale(-3.55);		
var sty = yScale(1.7);		
svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(stx-10)+","+(sty-5)+" L"+stx+","+(sty-5)+" L"+stx+","+(sty-10)+" L"+stx+","+(sty)
		+" L"+(stx+10)+","+(sty-5)+" L"+stx+","+(sty-10))+" L"+stx+","+(sty-5)+" L"+(stx-10)+","+(sty-5);

svg1.append("text")
		.attr("x", xScale(-2.85))
		.attr("y", yScale(1.4))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v1");
var stx = xScale(-3.2);
var sty = yScale(1.4);		
svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(stx+10)+","+(sty-5)+" L"+stx+","+(sty-5)+" L"+stx+","+(sty-10)+" L"+stx+","+(sty)
		+" L"+(stx-10)+","+(sty-5)+" L"+stx+","+(sty-10))+" L"+stx+","+(sty-5)+" L"+(stx+10)+","+(sty-5);




svg1.append("text")
		.attr("x", xScale(3.9))
		.attr("y", yScale(1.7))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v1");
var stx = xScale(3.55);		
var sty = yScale(1.7);		
svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(stx+10)+","+(sty-5)+" L"+stx+","+(sty-5)+" L"+stx+","+(sty-10)+" L"+stx+","+(sty)
		+" L"+(stx-10)+","+(sty-5)+" L"+stx+","+(sty-10))+" L"+stx+","+(sty-5)+" L"+(stx+10)+","+(sty-5);
					

svg1.append("text")
		.attr("x", xScale(2.85))
		.attr("y", yScale(1.4))
		.attr("font-family", "sans-serif")
		.attr("font-size", "13px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v2");
var stx = xScale(3.2);
var sty = yScale(1.4);
svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(stx-10)+","+(sty-5)+" L"+stx+","+(sty-5)+" L"+stx+","+(sty-10)+" L"+stx+","+(sty)
		+" L"+(stx+10)+","+(sty-5)+" L"+stx+","+(sty-10))+" L"+stx+","+(sty-5)+" L"+(stx-10)+","+(sty-5);

			   
			
			//Create X axis
			svg1.append("g")
				.attr("class", "axis")
				.attr("transform", "translate(0," + (h - 2*padding) + ")")
				.call(xAxis);
			
			//Create Y axis
			svg1.append("g")
				.attr("class", "axis")
//				.attr("transform", "translate(" + (padding+258) + ",0)")
				.attr("transform", "translate(" + (w/2-padding/2) + ",0)")
				.call(yAxis);
//*/


var width = 200,
    height = 20;
var rectX = (w-width)/2,
	rectY = 130;



var gradient = svg.append("defs")
  .append("linearGradient")
    .attr("id", "gradient")
    .attr("x1", "0%")
    .attr("y1", "0%")
    .attr("x2", "100%")
    .attr("y2", "0%")
    .attr("spreadMethod", "pad");

gradient.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", "#e5f5e0")
    .attr("stop-opacity", 1);

gradient.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", "#31a354")
    .attr("stop-opacity", 1);

svg1.append("rect")
    .attr("x", rectX)
    .attr("y", rectY)
    .attr("width", width)
    .attr("height", height)
    .style("fill", "url(#gradient)");


svg1.append("text")
		.attr("x", rectX-30)
		.attr("y", rectY+height/2)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("min(v2)");

svg1.append("text")
		.attr("x", rectX+width+30)
		.attr("y", rectY+height/2)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("max(v2)");

svg1.append("text")
		.attr("x", rectX+width/2)
		.attr("y", rectY+height+15)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v2");

svg1.append("text")
		.attr("x", w/2+20)
		.attr("y", h-140+5)
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text("v1");


data.forEach(function(d, i)
	{
		svg1.append("text")
		.attr("x", centX+10)
		.attr("y", centY-25*Math.sqrt(d))
		.attr("font-family", "sans-serif")
		.attr("font-size", "15px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text(""+d);
	});



var arrowX = 10;
var arrowY = 15;

svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+w/2+","+h+" L"+w/2+","+(h-140)+" L"+(w/2-arrowX)+","+((h-140)+arrowY)+" L"+w/2+","+(h-140)+" L"+(w/2+arrowX)+","+((h-140)+arrowY));


svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(w/2-10)+","+(rectY+height+10)+" L"+rectX+","+(rectY+height+10)+" L"+(rectX+arrowY)+","+(rectY+height+10+arrowX)+" L"+rectX+","+(rectY+height+10)+" L"+(rectX+arrowY)+","+(rectY+height+10-arrowX));

svg1.append("path")
		.attr("fill", "none")
		.attr("stroke", "black")
		.attr("stroke-width", "1px")
		.attr("d", "M"+(w/2+10)+","+(rectY+height+10)+" L"+(rectX+width)+","+(rectY+height+10)+" L"+(rectX+width-arrowY)+","+(rectY+height+10+arrowX)+" L"+(rectX+width)+","+(rectY+height+10)+" L"+(rectX+width-arrowY)+","+(rectY+height+10-arrowX));
