
var margin = {top: 20, right: 40, bottom: 30, left: 40},
    width = 980 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x0 = d3.scale.ordinal().rangeRoundBands([0, width], .4);
var x1 = d3.scale.ordinal();

var y0 = d3.scale.linear().range([height, 0]);
var y1 = d3.scale.linear().range([height, 0]);

var color = d3.scale.ordinal().range(["#98abc5", "#d0743c"]);

var xAxis = d3.svg.axis()
    .scale(x0)
    .orient("bottom")
    .ticks(5);

var yAxisLeft = d3.svg.axis()
    .scale(y0)
    .orient("left")
    .tickFormat(function(d) { return parseInt(d) });

var yAxisRight = d3.svg.axis()
    .scale(y1)
    .orient("right")
    .tickFormat(function(d) { return parseInt(d) });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var data = {"aggregate":{"bookings": 29,"bookings_rev":2495.0,"net_stays":9,"net_stays_rev":2495.0},"daily":{"2015-01-28":{"bookings":22,"bookings_rev": 10,"net_stays":4,"net_stays_rev":0},"2015-01-30":{"bookings":42,"bookings_rev":169.0,"net_stays":3,"net_stays_rev":0},"2015-02-02":{"bookings":32,"bookings_rev":726.0,"net_stays":5,"net_stays_rev":0},"2015-02-04":{"bookings":24,"bookings_rev":1152.0,"net_stays":8,"net_stays_rev":0},"2015-02-05":{"bookings":2,"bookings_rev":0,"net_stays":1,"net_stays_rev":538.0},"2015-02-09":{"bookings":3,"bookings_rev":0,"net_stays":1,"net_stays_rev":189.0},"2015-02-13":{"bookings":0,"bookings_rev":0,"net_stays":1,"net_stays_rev":199.0},"2015-02-24":{"bookings":0,"bookings_rev":0,"net_stays":1,"net_stays_rev":188.0},"2015-03-01":{"bookings":0,"bookings_rev":0,"net_stays":2,"net_stays_rev":448.0},"2015-03-10":{"bookings":0,"bookings_rev":0,"net_stays":1,"net_stays_rev":169.0},"2015-03-16":{"bookings":0,"bookings_rev":0,"net_stays":2,"net_stays_rev":764.0}}};
var dataset = [];

var keyNames = ['bookings','bookings_rev'];

for(i = 0; i < Object.keys(data.daily).length; i++ ) {
  var date = Object.keys(data.daily)[i];
  dataset[i] = {
    date: date,
    values: [
     {name: 'Bookings', value: data.daily[date][keyNames[0]]},
     {name: 'Bookings Revenue', value: data.daily[date][keyNames[1]]}
    ]
  };
}

x0.domain(function(d) { return d.date; });
x1.domain(['Bookings','Bookings Revenue']).rangeRoundBands([0, x0.rangeBand()]);

y0.domain([0, d3.max(dataset, function(d) { return d.values[0].value; })]);
y1.domain([0, d3.max(dataset, function(d) { return d.values[1].value; })]);

// Ticks on x-axis and y-axis
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y0 axis")
    .call(yAxisLeft)
  .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .style("fill", "#98abc5")
    .text("Bookings");

svg.select('.y0.axis')
  .selectAll('.tick')
    .style("fill","#98abc5");

svg.append("g")
    .attr("class", "y1 axis")
    .attr("transform", "translate(" + width + ",0)")
    .call(yAxisRight)
  .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -16)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .style("fill", "#d0743c")
    .text("Bookings Revenue");

svg.select('.y1.axis')
  .selectAll('.tick')
    .style("fill","#d0743c");
// End ticks

var graph = svg.selectAll(".date")
    .data(dataset)
    .enter()
    .append("g")
      .attr("class", "g")
      .attr("transform", function(d) { return "translate(" + x0(d.date) + ",0)"; });

graph.selectAll("rect")
    .data(function(d) { return d.values; })
    .enter()
    .append("rect")
      .attr("width", x1.rangeBand())
      .attr("x", function(d) { return x1(d.name); })
      .attr("y", function(d) { return y0(d.value); })
      .attr("height", function(d) { return height - y0(d.value); })
      .style("fill", function(d) { return color(d.name); });

// Legend
var legend = svg.selectAll(".legend")
    .data(['Bookings','Bookings Revenue'].slice())
    .enter()
    .append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

legend.append("rect")
    .attr("x", width - 48)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", color);

legend.append("text")
    .attr("x", width - 54)
    .attr("y", 9)
    .attr("dy", ".35em")
    .style("text-anchor", "end")
    .text(function(d) { return d; });
