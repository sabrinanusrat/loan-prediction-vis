function draw_chart(elementId, data, name, labels, width, height) {   
    var svg = d3.select("#"+elementId)
        .append("svg:svg")
        .attr("width", width)
        .attr("height", height)
        .append("svg:g");
    
    var left = 50;
    var right = width-50;
    var bottom = height-100;
    var top = 50;
    console.log("left="+left);
    console.log("right="+right);
    console.log("bottom="+bottom);
    console.log("top="+top);

    var x_min = d3.min(data, d=>d[0]);
    var x_max = d3.max(data, d=>d[0]);
    var x_interval = x_max - x_min;

    var y_min = d3.min(data, d=>d[1]);
    var y_max = d3.max(data, d=>d[1]);
    var scale_x = d3.scale.linear()
        .domain([x_min - x_interval/20, x_max+x_interval/20])
        .range([left, right]);
    var scale_y = d3.scale.linear()
        .domain([y_min-1, y_max+1])
        //.domain([0, y_min+y_max>100? 100: y_min+y_max])
        .range([bottom, top]);
    
    var valueline = d3.svg.line()
        .x(d => scale_x(d[0]))
        .y(d => scale_y(d[1]));
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));

    svg.selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", "point")
        .attr("r", 4)
        .attr("cx", d => scale_x(d[0]))
        .attr("cy", d => scale_y(d[1]))
        .on("mouseover", d => {
            tooltip
                .style("visibility", "visible")
                .text(labels[0]+": "+d[0]+'\n'+labels[1]+": "+d[1])
        })
	    .on("mousemove", () => tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px"))
        .on("mouseout", () => tooltip.style("visibility", "hidden"))
        .on("click", d => {console.log(d);});

    var xAxis = d3.svg.axis().scale(scale_x)
        .orient("bottom");//.ticks(tick_intervals[0]);
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0, " + bottom + ")")
        .call(xAxis);
    svg.append("text")
        .attr("class", "axis-label")
        .attr("text-anchor", "middle")
        .attr("x", (left+right)/2)
        .attr("y", bottom+40)
        .text(labels[0]);

    var yAxis = d3.svg.axis().scale(scale_y)
        .orient("left");//.ticks(tick_intervals[1]);
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + left + ", 0)")
        .call(yAxis);
    svg.append("text")
        .attr("class", "axis-label")
        .attr("text-anchor", "middle")
        .attr("x", -(top+bottom)/2)
        .attr("y", left-35)
        .attr("transform", "rotate(-90)")
        .text(labels[1]);

    svg.append("text")
        .attr("class", "title")
        .attr("text-anchor", "middle")
        .attr("x", (left+right)/2)
        .attr("y", height-20)
        .text(name);

}