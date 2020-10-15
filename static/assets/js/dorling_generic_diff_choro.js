var force = d3.layout.force()
    .charge(0)
    .gravity(0)
   .size([960, 500]);
  //  .size([800, 400]);

var svg = d3.select("#chart2").append("svg:svg")
  .attr("width", 900)
    .attr("height", 500)
//.attr("width", 800 + 100)
  //  .attr("height", 400 + 100)

  .append("svg:g")
    .attr("transform", "translate(50,50) scale(0.75)");

var nodes, nodes2, links = [];

var Pop=[];

var PopMean;

var states;

// {{url_for('static', filename = 'assets/lib/d3.geo.js')}}

//var fl1 = "{{url_for('static', filename = 'assets/data/USA-Pop2010-input.json')}}" ;//document.getElementById('file1').textContent;
//var fl2 = "{{url_for('static', filename = 'assets/data/USA-Pop1960-input.json')}}"; //document.getElementById('file2').textContent;

//var fl1 = "/Users/sabrinanusrat/Documents/Codes/Python/Loan_Predict_Vis/static/assets/data/USA-Pop1960-input.json";
//var fl2 = "/Users/sabrinanusrat/Documents/Codes/Python/Loan_Predict_Vis/static/assets/data/USA-Pop1960-input.json"

var fl1 = "/static/assets/data/USA-Pop2010-input.json" ;//document.getElementById('file1').textContent;
var fl2 = "/static/assets/data/USA-Foreclosures.json"; //document.getElementById('file2').textContent;

var varName1 = "Population"; //document.getElementById('var1').textContent;
var varName2 = "Foreclosures"; //document.getElementById('var2').textContent;
var field1 = "Pop2010"; //document.getElementById('field1').textContent;
var field2 = "FC"; //document.getElementById('field2').textContent;


d3.json(fl1, function(states) {
//d3.json("USA-GDP2015-input.json", function(states) {


//	states=states1;
	states.features.map(function(d)
		{
//			console.log("command = "+"Pop.push(d.properties."+field1+")");
			eval("Pop.push(d.properties."+field1+")")
		}
		);
  

//	console.log( "Pop [0] = " + Pop[0]);


	var project = d3.geo.albersUsa(),
	idToNode = {};
//	PopMax = d3.max(Pop);
	PopMean = d3.mean(Pop);
	console.log("PopMean="+PopMean);
	nodes = states.features.map(function(d) {
	var xy = project(d.geometry.coordinates);
		return idToNode[d.id] = {
			x: xy[0],
			y: xy[1],
			gravity: {x: xy[0], y: xy[1]},
			r1: Math.sqrt(eval("d.properties."+field1)/PopMean)*25,
			var1: eval("d.properties."+field1),
			value1: eval("d.properties."+field1)/PopMean,
			name: d.properties.name
		};
	});



	//  console.log(nodes[0]);
	  
	var tooltip = d3.select("body")
	.append("div")
	.style("position", "absolute")
	.style("z-index", "10")
	.style("visibility", "hidden");


	  
	d3.json(fl2, function(states) {
//	d3.json("USA-GDP10-input.json", function(states) {
	
		var GDP=[];
	
		var GDPMean, GDPMin, GDPMax;
	
		states.features.map(function(d) {
			GDP.push(eval("d.properties."+field2))});

		var project = d3.geo.albersUsa(),
		idToNode = {},
		links = [];

		GDPMean= d3.mean(GDP);
		
		GDPMax=d3.max(GDP);
		
		console.log("GDPMax="+GDPMax);
		
		GDPMin=d3.min(GDP);
		
		console.log("GDPMin="+GDPMin);
		
		//console.log(nodes);
		
		states.features.map(function(d,i) {
			
			//console.log(nodes[i]);
			nodes[i].var2= eval("d.properties."+field2);
			//nodes[i].r2=Math.sqrt(eval("d.properties."+field2)/GDPMean)*25;
			nodes[i].value2=eval("d.properties."+field2); ///GDPMean;
		});

 
	
		var dx, dy, l, d1, d2, d;
		
		var rMax="#31a354", rMean="#a1d99b", rMin = "#e5f5e0";

var cScale = 
d3.scale.linear().domain([GDPMin, GDPMax]).range(["#eff3ff","#08519c"])//.range([rMin, rMax]);


console.log("Testing cScale="+cScale(0));
		
	svg.selectAll("circle")
	.data(nodes)
	.enter().append("svg:circle")
	//.style("stroke", function(d) { return "#0000FF"; })
	.style("stroke", function(d) { 
	//if (1.03*d.r1<d.r2) return "#FF6600"; else if (1.03*d.r2<d.r1) return "#0000FF"; else 
	return "#acacac"; 
	//return color(d.r1 - d.r2);	
	})
	.style("stroke-width", function(d) { return 1; })
	//.style("stroke-opacity", function(d) { return 0.7; })
	//.style("fill", "none")
	.style("fill", function(d, i) { 
	//if (1.03*d.r1<d.r2) return "#FF6600"; else if (1.03*d.r2<d.r1) return "#0000FF"; else return "#acacac"; 
		//return color(d.r1 - d.r2);
		//console.log("Testing nodes value2="+d.value2);
		
		//console.log("cScale="+cScale(d.value2));
		
		return ""+cScale(d.value2);
			
	})
	
	.attr("cx", function(d) { return d.x; })
	.attr("cy", function(d) { return d.y; })
	.attr("r", function(d, i) { //if (d.r1<d.r2) return d.r2; else 
	return d.r1; })
//		.on("mouseover", function(d){return tooltip.style("visibility", "visible").text("GDP "+"of "+ d.name +" in 2015 is " +d.var1+", in 2000 it was "+ d.var2);})
		.on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.name+": "+varName1+" is " +d.var1+", "+varName2+" is "+ d.var2);})
	.on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
	.on("mouseout", function(){return tooltip.style("visibility", "hidden");});  
		


		
		var factor=0.02;
		force
		.nodes(nodes)
		//.links(links)
		.start()
		.on("tick", function(e) {
			var k = e.alpha,
			kg = k * factor;
			var flag = 0;

			nodes.forEach(function(a, i) {

			//Apply gravity forces.
				a.x += (a.gravity.x - a.x) * kg;
				a.y += (a.gravity.y - a.y) * kg;
			  
				nodes.slice(i + 1).forEach(function(b, j) {
				// Check for collisions.
					b = nodes.slice(i+1)[j];

					dx = a.x - b.x,
					dy = a.y - b.y,
					l = Math.sqrt(dx * dx + dy * dy),
					d1 = a.r1 + b.r1+2,
					//d2 = a.r2 + b.r2+2;
					
					//d = d3.max([d1,d2]);
					d=d1;
					
					if (l < d) {
						l = (l - d) / l * k;
						dx *= l;
						dy *= l;
			  
						a.x -= dx;
						a.y -= dy;
						b.x += dx;
						b.y += dy;
						flag = 1;
					}
					nodes.slice(i+1)[j].x=b.x;
					nodes.slice(i+1)[j].y=b.y;
				});
				
				nodes[i].x=a.x;
				nodes[i].y=a.y;
			});
			
			if(flag>0)
			{
				factor = 0.98*factor;
//				console.log("factor decreased");
			}
			else
			{
//				console.log("factor increased");
				factor = 1.02*factor;
			}




			svg.selectAll("circle")
			.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });
			
			
			svg.selectAll("text")
			.attr("x", function(d) { return d.x; })
			.attr("y", function(d) { return d.y; });
			
		});


/*
	svg
		.selectAll("g")
		.data(nodes)
		.enter()
		.append("svg:circle")
		.style("stroke", function(d) { return "#FFFFFF"; })
		.style("stroke-width", function(d) { return 1; })
		.style("fill", "none")
		.attr("cx", function(d) { return d.x; })
    	.attr("cy", function(d) { return d.y; })
	    .attr("r", function(d, i) { if (d.r1>d.r2) return d.r2; else return d.r1; })	
		
//			.on("mouseover", function(d){return tooltip.style("visibility", "visible").text("GDP "+"of "+ d.name +" in 2015 is " +d.var1+", in 2000 it was "+ d.var2);})
		.on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.name+": "+varName1+" is " +d.var1+", "+varName2+" is "+ d.var2);})
	.on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");});
	//.on("mouseout", function(){return tooltip.style("visibility", "hidden");}); 
	
//*/
	
/*
var horizontalLegend = d3.svg.legend().units("Var 2").cellWidth(80).cellHeight(25).inputScale(cScale).cellStepping(1000);

console.log("HorizontalL = "+horizontalLegend);

  d3.select("svg").append("g").attr("transform", "translate(50,70)").attr("class", "legend").call(horizontalLegend);
//*/

	
	
	var text = svg
		.selectAll("text")
		.data(nodes)
		.enter()
		.append("svg:text")
         .attr("x", function(d){return d.x})
		.attr("y", function(d){return d.y})
		.attr("font-family", "sans-serif")
		.attr("font-size", "12px")
		.attr("text-anchor", "middle")
		.attr("fill", "black")
		.text(function(d){
		//console.log(d.name);
		 if(d.r1<12) return ""; 
		 else 
		 return d.name;})
		.on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.name+": "+varName1+" is " +d.var1+", "+varName2+" is "+ d.var2);})
	.on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");});


	});



  
  
});