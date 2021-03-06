
//create somewhere to put the force directed graph
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height")
    ;



var Tickindex = 0;


var nodes_data =  [
    ];

var links_data = [
];

var simulation = d3.forceSimulation()
    //.force("link", d3.forceLink().distance(null).id(function(d) { return d.id; }))
    //.force("link", d3.forceLink().distance(function(d) {return 5 + d._dist;}).strength(0).id(function(d) { return d.id; }))
    .force("link", d3.forceLink().strength(function(d) {return 0; if(d._dist > 1) return 0.1; return 0.001;}).id(function(d) { return d.id; }))
    //.force("charge", d3.forceManyBody().strength(1))
    .force("collide_force", d3.forceCollide().radius(10).strength(1))
    //.force("center_force", d3.forceCenter(width / 2, height / 2))
    .force("r", d3.forceRadial(function(d) {
                                 return d.type === "redditor" ? 100 : 500;
                                 })
                .strength(1)
                .x(width / 2).y(height / 2))
    .force("box_force", box_force);

var data = "hello";
console.log(data);
d3.json("./data/user_stat.json", function(error, json) {
    if (error) return console.warn(error);

    //create clean node data
    nodes_data = nodeData(json);
    console.log(nodes_data);
    //create clean link data
    link_data = linkData(json);
    console.log(link_data);
    //set up the simulation


    //add forces
    //we're going to add a charge to each node
    //also going to add a centering force
    //and a link force
    //var link_force = d3.forceLink(links_data).id(function(d) {return d.id;});
;


    simulation
      .nodes(nodes_data)
      .on("tick", tickActions);

    simulation.force("link")
      .links(link_data);




    //on hover=> link strength for this node ++, force for this node ++
    //1° by setting a selected attribute in the data ++easy implentation, faster -- mixing data and visual elements
    //2° by searching if the data node, has a dom element with attributes corresponding to a selection ++data visual separation -- more complexe, probably slower


    //draw lines for the links
    var link = svg.append("g")
          .attr("class", "links")
        .selectAll("line")
        .data(link_data)
        .enter().append("line")
          .attr("stroke-width", 0.5)
          .style("stroke", function(d) {return "steelblue"});



    //draw circles for the link. Draw after links to cover lines
    var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes_data)
            .enter()
            .append("circle")
            .attr("r", function(d) {return 2} )
            .attr("fill", function(d) {if(d.id == "tabb10") return "purple"; if (d.type == "redditor") return "brown"; return "green";})
            .on("mouseover", function(d) {
                console.log(d.id);
            })
          /*
            .on("mouseout", function(d) {
             d3.select(this).transition().attr("r" , 10);
             d.r = 5
             simulation.force("links").distance(50);
             //simulation.force("charge_force").strength(0);
             simulation.alphaTarget(0);
             d.fx = null;
             d.fy = null;
             })
             */



    var drag_handler = d3.drag()
       .on("start", drag_start)
       .on("drag", drag_drag)
       .on("end", drag_end);

    //same as using .call on the node variable as in https://bl.ocks.org/mbostock/4062045
    drag_handler(node)



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
    var radius = 5;
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

function tickActions() {
    //update circle positions each tick of the simulation
    var node = d3.selectAll("circle");

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
