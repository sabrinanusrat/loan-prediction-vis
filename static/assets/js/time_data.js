    //Width and height
     /* var w = 960;
      var h = 500;

      var margin = {
          top: 60,
          bottom: 40,
          left: 70,
          right: 40
        };

        var width = w - margin.left - margin.right;
        var height = h - margin.top - margin.bottom;*/

      
      var tooltip = d3.select("body")
	.append("div")
	.style("position", "absolute")
	.style("z-index", "10")
	.style("visibility", "hidden");
	
      // define map projection
      //var projection = d3.geo.albers()
        //.translate([w/2, h/2])
        //.scale([500]);

      //Define default path generator
     // var path = d3.geo.path()
       // .projection(projection);
        
      var fl0 =  "/static/assets/data/foreclosures_by_year_month.csv" ;//document.getElementById('file1').textContent; //states-albers-10m-2 //USA-Pop2010-input.json
	
	//"/static/assets/data/time_data2.txt" 
//time_data.csv

//var svg = d3.select("#chart0").append("svg:svg")
  //.attr("width", 900)
    //.attr("height", 500)
    
    
   /**     var color = d3.scale.linear().range(["#e5f5e0", "#31a354"]);
        //var color = d3.scale.linear().range(["rgb(237, 248, 233)", "rgb(1,109,44)"]);
        //d3.scale.quantile().range(["rgb(237, 248, 233)", "rgb(186, 228, 179)", "rgb(116,196,118)", "rgb(49,163,84)", "rgb(0,109,44)"]);

      d3.csv(fl4, function(data){

		//console.log(data);
        color.domain([ d3.min(data, function(d){ return parseInt(d.fc); }),
          d3.max(data, function(d){ return parseInt(d.fc); })
          ]);

      d3.json(fl3, function(json){

	console.log(json);
        //Merge the agriculture and GeoJSON data
        //Loop through once for each agriculture data value
        for(var i = 0; i < data.length; i++){
          // grab state name
          var dataState = data[i].name;

          //grab data value, and convert from string to float
          var dataValue = parseInt(data[i].fc);

		//console.log(dataValue);
          //find the corresponding state inside the GeoJSON
          for(var n = 0; n < json.features.length; n++){

            // properties name gets the states name
            var jsonState = json.features[n].properties.name;
            
            //console.log(jsonState);
            // if statment to merge by name of state
            if(dataState == jsonState){
              //Copy the data value into the JSON
              // basically creating a new value column in JSON data
              json.features[n].properties.value = dataValue;
              

              //stop looking through the JSON
              break;
            }
          }
        }

        svg.selectAll("path")
          .data(json.features)
          .enter()
          .append("path")
          .attr("d", path)
          .style("fill", function(d){
            //get the data value
            var value = d.properties.value;

            if(value){
              //If value exists
              return color(value);
            } else {
              // If value is undefined
              //we do this because alaska and hawaii are not in dataset we are using but still in projections
              return "#ccc"
            }

          })
          .on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.properties.name+": "+d.properties.value);})
		.on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
		.on("mouseout", function(){return tooltip.style("visibility", "hidden");});  
		
		*/
		
		//// code
		
		
		
var total_width = 960,
  	total_height = 400,
	margin = {top: 10, right: 10, bottom: total_height*.2, left: 120},
    bottompanelmargin = {top: total_height - margin.bottom + 30, right: margin.right, bottom: 20, left: margin.left},
	leftpanelmargin = {top: margin.top, right: margin.left-40, bottom: margin.bottom, left: 40},
    width = total_width - margin.left - margin.right,
    height = total_height - margin.top - margin.bottom,
    bottompanelheight = total_height - bottompanelmargin.top - bottompanelmargin.bottom,
	leftpanelwidth = leftpanelmargin.right - leftpanelmargin.left;

var parseDate = d3.time.format("%b %Y").parse;

var x = d3.time.scale().range([0, width]),
    bottompanelx = d3.time.scale().range([0, width]),
    leftpanelx = d3.scale.linear().range([0, leftpanelwidth]),
    y = d3.scale.linear().range([height, 0]),
    bottompanely = d3.scale.linear().range([bottompanelheight, 0]),
    leftpanely = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis().scale(x).orient("bottom"),
    bottompanelxAxis = d3.svg.axis().scale(bottompanelx).orient("bottom"),
    yAxis = d3.svg.axis().scale(y).orient("left"),
    leftpanelyAxis = d3.svg.axis().scale(leftpanely).orient("left");

var brushx = d3.svg.brush()
    .x(bottompanelx)
    .on("brush", brushedx);

var brushy = d3.svg.brush()
    .y(leftpanely)
    .on("brush", brushedy);

var area = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y0(height)
    .y1(function(d) { return y(d.foreclosure); });

var bottompanelarea = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return bottompanelx(d.date); })
    .y0(bottompanelheight)
    .y1(function(d) { return bottompanely(d.foreclosure); });

var leftpanelarea = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return leftpanelx(d.date); })
    .y0(height)
    .y1(function(d) { return leftpanely(d.foreclosure); });

var svg = d3.select("#chart0").append("svg:svg")
//d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

svg.append("defs").append("clipPath")
    .attr("id", "clip")
  .append("rect")
    .attr("width", width)
    .attr("height", height);

var focus = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var leftpanelcontext = svg.append("g")
    .attr("transform", "translate(" + leftpanelmargin.left + "," + leftpanelmargin.top + ")");

var bottompanelcontext = svg.append("g")
    .attr("transform", "translate(" + bottompanelmargin.left + "," + bottompanelmargin.top + ")");

d3.csv(fl0, function(error, data) {

  data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.foreclosure = +d.foreclosure;
  });

  x.domain(d3.extent(data.map(function(d) { return d.date; })));
  y.domain([0, d3.max(data.map(function(d) { return d.foreclosure; }))]);
  bottompanelx.domain(x.domain());
  bottompanely.domain(y.domain());
  leftpanelx.domain(x.domain());
  leftpanely.domain(y.domain());

  focus.append("path")
      .datum(data)
      .attr("clip-path", "url(#clip)")
      .attr("d", area);

  focus.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + (height-90) + ")")
      .call(xAxis);

  focus.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  leftpanelcontext.append("path")
      .datum(data)
      .attr("d", leftpanelarea);

  bottompanelcontext.append("path")
      .datum(data)
      .attr("d", bottompanelarea);
 
  bottompanelcontext.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + bottompanelheight + ")")
      .call(bottompanelxAxis);

  leftpanelcontext.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" - leftpanelwidth + ", 0 )")
      .call(leftpanelyAxis);

  bottompanelcontext.append("g")
      .attr("class", "x brush")
      .call(brushx)
    .selectAll("rect")
      .attr("y", -6) // 6 goes along with 7 below for shifting.
      .attr("height", bottompanelheight + 7);

  leftpanelcontext.append("g")
      .attr("class", "y brush")
      .call(brushy)
    .selectAll("rect")
      .attr("width", leftpanelwidth);
});

function brushedx() {
  x.domain(brushx.empty() ? bottompanelx.domain() : brushx.extent());
  focus.select("path").attr("d", area);
  focus.select(".x.axis").call(xAxis);
}

function brushedy() {
  y.domain(brushy.empty() ? leftpanely.domain() : brushy.extent());
  focus.select("path").attr("d", area);
  focus.select(".y.axis").call(yAxis);
}

		


     // });

//})


// https://bl.ocks.org/JulienAssouline/1ae3480c5277e2eecd34b71515783d6f