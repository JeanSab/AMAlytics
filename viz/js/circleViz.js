var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height")
    ;



var Tickindex = 0;
var nodes_data =  [];
var links_data = [];
var nodeRadius = 6;

var simulation = d3.forceSimulation()
  .force("link", d3.forceLink().strength(function(d) {
    return 0;
    if (d._dist > 1) return 0.1;
    return 0.001;
  }).id(function(d) {
    return d.id;
  }))
  .force("collide_force", d3.forceCollide().radius(6).strength(1))
  .force("box_force", box_force);


d3.json("./data/test_data.json", function(error, json) {
    if (error) return console.warn(error);

    //create clean node data
    var nodes_data = nodeData(json);
    //create clean link data
    var link_data = linkData(json);
    var tmp = nodes_data;

    nodes_data = subListsOf(nodes_data, ["redditor", "subreddit"]);
    //console.log(nodes_data[0].concat(nodes_data[1]));
    var concatNodes = (nodes_data[0]).concat(nodes_data[1]);

    simulation.force("r", d3.forceRadial(function(d) {
                            if(d.type === "redditor")
                                return circleRadius(nodes_data[0].length, nodeRadius, 1.2);
                            return circleRadius(nodes_data[1].length, nodeRadius, 1.2);
                                 })
                .strength(1)
                .x(width / 2).y(height / 2));

    simulation
      .nodes(concatNodes)
      .on("tick", tickActions);


    simulation.force("link")
      .links(link_data);

    //draw lines for the links
    var link = svg.append("g")
          .attr("class", "links")
        .selectAll("line")
        .data(link_data)
        .enter().append("line")
          .attr("stroke-width", 1)
          .style("stroke", function(d) {return "steelblue"})
          .on("mouseover", function(d) {
                d3.select(this).style("stroke", "red")
            })
          .on("mouseout", function(d) {
                d3.select(this).style("stroke", "steelblue");
            });

    //draw circles for the link. Draw after links to cover lines
    var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(concatNodes)
            .enter()
            .append("circle")
            .attr("r", function(d) {return nodeRadius} )
            .attr("fill", function(d) {if(d.id == "tabb10") return "purple"; if (d.type == "redditor") return "brown"; return "green";})
            .on("mouseover", function(d) {
                console.log(d.id);
                d3.select("g.links").selectAll("line")
                .style("stroke", function(d2) {
                    if(d2.source.id == d.id) {
                        console.log(d2);
                        return "red";
                    }
                    return "steelblue";
                })
            })
            .on("mouseout", function(d) {
                d3.select("g.links").selectAll("line")
                .style("stroke", "steelblue")
                });
            ;


    var drag_handler = d3.drag()
       .on("start", drag_start)
       .on("drag", drag_drag)
       .on("end", drag_end);

    drag_handler(node)
    ;

    node.call(initializeNodes);


});




//
function nodeData(rawData) {

    var nodes = [];
    var list = [];//id as list to check duplication
    var listw = {};
    Object.keys(rawData).forEach(function(e) {
        nodes.push({"id": e, "type":"redditor"});

        Object.keys(rawData[e]).forEach(function(e1) {
            if(! list.includes(e1)) {
                //console.log("adding node: " + e1);
                nodes.push({"id":e1, "type":"subreddit"})
                list.push(e1);
                listw[e1] = 1
            }
            else
                listw[e1] += 1;
        });
    });
    nodes.sort(function(a,b) {
        if(a.type === "subreddit" && b.type === "redditor")
            return -1;
        if(a.type === "redditor" && b.type === "subreddit")
            return +1;
        if(a.type === "subreddit" && b.type ==="subreddit")
            return listw[b.id] - listw[a.id];
        return 0;
        });

    nodes.forEach(function(e1) {
       e1["_size"] = listw[e1];
    });

    return nodes;
}

function linkData(rawData) {

    var links = [];
    var list = [];
    var listw = {};

    Object.keys(rawData).forEach(function(e) {

        Object.keys(rawData[e]).forEach(function(e1) {

            links.push({"source":e, "target":e1, "amount":rawData[e][e1]});

            if(! list.includes(e1)) {
                list.push(e1);
                listw[e1] = 1;
            }
            else
                listw[e1] += 1;
        });

    });

    links.forEach(function(e1) {
       e1["_dist"] = listw[e1["target"]];
    });

    links.sort(function(a, b) {
        return b._dist - a._dist;
    });

    return links;
}

//custom force to put stuff in a box
function box_force() {
    var radius = nodeRadius;
    for (var i = 0, n = nodes_data.length; i < n; ++i) {
        curr_node = nodes_data[i];
        curr_node.x = Math.max(radius, Math.min(width - radius, curr_node.x));
        curr_node.y = Math.max(radius, Math.min(height - radius, curr_node.y));
    }
}


function centering_force() {

    for (var i = 0, n = nodes_data.length; i < n; ++i) {
        curr_node = nodes_data[i];
        //if curr_node is subreddit
        curr_node.x = Math.max(radius, Math.min(width - radius, curr_node.x));
        curr_node.y = Math.max(radius, Math.min(height - radius, curr_node.y));
    }
}

function initializeNodes(selection) {

    var redditorNodes = [];
    var subredditNodes = [];
    var nodes = simulation.nodes();
    var nodeRad = nodeRadius;
    nodes.forEach(function(e) {

       if(e.type === "redditor") {
           redditorNodes.push(e);
       }
       else {
           subredditNodes.push(e);
       }
    });

    var cx = width /2, cy = height/2;

    var circleRad = circleRadius(redditorNodes.length, nodeRad, 1.2);
    d3.select("svg").append("circle").attr("r", circleRad).attr("cx", cx).attr("cy", cy).attr("fill", "none").attr("stroke", "black");

    var currAngle = 0;
    var theta = 360 / redditorNodes.length;
    redditorNodes.forEach(function(e) {
        e.x = cx + 2*circleRad * Math.cos(currAngle * (Math.PI / 180));
        e.y = cy + 2*circleRad * Math.sin(currAngle * (Math.PI / 180));
        currAngle += theta;
    });


    // outer circle
    circleRad = circleRadius(subredditNodes.length, nodeRad, 1.2)
    d3.select("svg").append("circle").attr("r", circleRad).attr("cx", cx).attr("cy", cy).attr("fill", "none").attr("stroke", "black");

    var currAngle = 0;
    var theta = 360 / subredditNodes.length;

    subredditNodes.forEach(function(e) {
        e.x = cx + 2*circleRad * Math.cos(currAngle * (Math.PI / 180));
        e.y = cy + 2*circleRad * Math.sin(currAngle * (Math.PI / 180));
        currAngle += theta;
    });

}

function subListsOf(list, types) {

    returnList = [];//list of lists

    types.forEach(function(e) {
        var subList = [];
        for(var i = 0; i < list.length; i++) {
            if(list[i].type === e)
                subList.push(list[i]);
        }
        returnList.push(subList);
    })
    return returnList;
}

/*
 *returns a radius size for a circle which would hold a certain number of nodes (on their center)
 *each node equidistante from themselves. Distance is defined according to the node radius (by default
 *the distance between two nodes is equal to 2 node radiuses
 */
function circleRadius(numberOfNodes, nodeRadius, distanceRate=2) {

    var circleRad = 0,
    theta = 360 / numberOfNodes,//node1-circle_center-node2 angle
    sigma = (180 - theta) / 2,//circle_center-node1-node2 angle
    gama = 180 - (90 + sigma);
    //rectangle triangle
   return (distanceRate*nodeRadius) / Math.tan(gama * (Math.PI / 180));
}

/*
* Drag event functions
**/
//drag handler
//d is the node
function drag_start(d) {
 if (!d3.event.active) simulation.alphaTarget(0.3).restart();//alpha will go up to 0.3, keeping the graph active!!
   d.fx = d.x;//a node with a defined node.fx has node.x reset to this value and node.vx set to zero
   d.fy = d.y;
}

function drag_drag(d) {
  d.fx = d3.event.x;//a node with a defined node.fx has node.x reset to this value and node.vx set to zero
  d.fy = d3.event.y;
}


function drag_end(d) {
  if (!d3.event.active) simulation.alphaTarget(0)/*.restart()*/;//alpha will go down to 0, eventually inactive
  //To unfix a node that was previously fixed, set node.fx and node.fy to null
  d.fx = null;
  d.fy = null;
}

/**
 * [actions to be performed at each tick of a simulation]
 */
function tickActions() {
    //update circle positions each tick of the simulation
    var node = d3.select("g.nodes").selectAll("circle");

        node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    //update link positions
    //simply tells one end of the line to follow one node around
    //and the other end of the line to follow the other node around

    var link = d3.selectAll("line");
        link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

}
