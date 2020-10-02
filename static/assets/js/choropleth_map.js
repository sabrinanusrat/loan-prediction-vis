    //Width and height
      var w = 960;
      var h = 500;

      var margin = {
          top: 60,
          bottom: 40,
          left: 70,
          right: 40
        };

        var width = w - margin.left - margin.right;
        var height = h - margin.top - margin.bottom;

      
      var tooltip = d3.select("body")
	.append("div")
	.style("position", "absolute")
	.style("z-index", "10")
	.style("visibility", "hidden");
	
      // define map projection
      var projection = d3.geo.albers()
        .translate([w/2, h/2])
        .scale([500]);

      //Define default path generator
      var path = d3.geo.path()
        .projection(projection);
        
      var fl3 = "/static/assets/data/us-states.json" ;//document.getElementById('file1').textContent; //states-albers-10m-2 //USA-Pop2010-input.json
		var fl4 = "/static/assets/data/test_bivar.csv"; //document.getElementById('file2').textContent;  

      /*var svg = d3.select("body")
        .append("svg")
        .attr("id", "chart2")
        .attr("width", w)
        .attr("height", h)
        .append("g")
        .attr("tranform", "translate(0" + margin.left + "," + margin.top + ")");*/


var svg2 = d3.select("#chart").append("svg:svg")
  .attr("width", 900)
    .attr("height", 500)
    
    
        var color = d3.scale.linear().range(["#e5f5e0", "#31a354"]);
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

        svg2.selectAll("path")
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
		


      });

})


// https://bl.ocks.org/JulienAssouline/1ae3480c5277e2eecd34b71515783d6f