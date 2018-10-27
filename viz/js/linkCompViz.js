

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height")
    ;

var GRATTR = {"SUB_RAD" : 10, "RDT_RAD" : 10, "SUB_OFS" : 50 };

d3.json("./data/test_data.json", function(error, json) {
    if (error) return console.warn(error);

    data = getGraphData(json);
    nodes_data = data.nodes
    link_data = data.links

    setNodeCoord(nodes_data);

    var link = svg.append("g")
          .attr("class", "links")
        .selectAll("path")
        .data(link_data)
        .enter().append("path")
          .attr("stroke-width", 0.5)
          .attr("d", function(d) {return getCurvedPath(d.source.x, d.source.y, d.target.x, d.target.y);})
          .style("stroke", function(d) {return "steelblue"})
          .style("fill", "transparent");

    var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes_data)
            .enter()
            .append("circle")
            .attr("r", function(d) {return d.r} )
            .attr("cx", function(d) {return d.x;})
            .attr("cy", function(d) {return d.y;})
            .attr("fill", function(d) { if (d.type == "redditor") return "brown"; return "green";})
            .on("mouseover", function(d) {
                if(d.type == "subreddit") {
                  //console.log(d3.select(this.parentNode));

                  labelNodes.apply(this, [d]);
                }
                else {
                d3.select("g.links").selectAll("path")
                .style("stroke", function(d2) {
                    if(d2.source.id == d.id) {
                        return "red";
                    }
                    return "steelblue";
                })
              }
            })
            .on("mouseout", function(d) {
                d3.select("g.links").selectAll("path")
                .style("stroke", "steelblue");
                d3.selectAll(".subreddit_label").remove()
                });
            ;


});

function labelNodes(d, n=3) {

  var txtCoords = [getCirclePoint(d.x, d.y, 337.5, d.r + 20), getCirclePoint(d.x, d.y, 0, d.r + 20), getCirclePoint(d.x, d.y, 22.5, d.r + 20)];

  txtCoords[0].txt = "subreddit: " + d.id;
  txtCoords[1].txt = "number of posts: place holder";
  txtCoords[2].txt = "subscribers: place holder";

  tmp = this;
  txtCoords.forEach(function(e) {

    d3.select(tmp.parentNode).append("text")//append to our node selection (g previously appended) a text svg tag <g> <circle></circle> <text></text> </g>
      .attr("x", e.x)
      .attr("y", e.y)
      .attr("class", "subreddit_label")
      .attr("transform", "rotate(" + e.a + "," +  e.x + "," + e.y + ")")
      .text(e.txt);
  });

}


function getCirclePoint(cx, cy, a, r) {
  var x = cx + r * Math.cos(a * (Math.PI / 180));
  var y = cy + r * Math.sin(a * (Math.PI / 180));
  return {"x": x, "y": y, "a": a};
}


function setNodeCoord(nodes, xoffset=50, yoffset=10*GRATTR.SUB_RAD) {

  var rpad = {"x": xoffset, "y": xoffset, "count" : 0};
  var spad = {"x": xoffset*30 , "y": xoffset, "count" : 0}
  nodes.forEach(function(e) {
    if(e.type == "subreddit") {
        if(spad.count % 2 == 0) {
          spad.x += 20;
        }
        else {
          spad.x -= 20;
        }
      e.x = spad.x;
      e.y = spad.y;
      e.r = GRATTR.SUB_RAD;
      spad.y += yoffset;
      spad.count++;
    }
    else {
      rpad.count++;
    }
  });
  var spacing = (spad.y - yoffset)/ rpad.count;
  rpad.y = spacing/2;
  nodes.forEach(function(e) {
    if(e.type == "redditor") {
      e.x = rpad.x;
      e.y = rpad.y;
      e.r = GRATTR.RDT_RAD;
      rpad.y += spacing;
    }
  });
  svg.attr("height", spad.y + yoffset);
}


function getCurvedPath(x1, y1, x2=GRATTR.SUB_OFS*30, y2, coeff=0.5) {
  if(coeff < 0 && coeff > 1) throw "invalid curve";
  var path = "";

  x2=GRATTR.SUB_OFS*30;
  var curve = (x2-x1)*coeff;
  path +=  "M" + x1 + " " + y1
       + " C " + (x2 - curve) + " " + y1
       + ", "  + (x1 + curve) + " " + y2
       + ", "  + x2 + " " + y2;

  return path;
}


function getGraphData(rawData, verbose=false) {
  var nodes = [];
  var dnodes = {};
  var links = [];
  var list = [];//id as list to check duplication
  var listw = {};
  Object.keys(rawData).forEach(function(e) {
      var source = {"id": e, "type":"redditor"};
      nodes.push(source);

      Object.keys(rawData[e]).forEach(function(e1) {

          if(! list.includes(e1)) {
              var target = {"id":e1, "type":"subreddit"};
              //console.log("adding node: " + e1);
              nodes.push(target);
              list.push(e1);
              listw[e1] = 1
              dnodes[e1] = target;
          }
          else {
              listw[e1] += 1;
            }

          links.push({"source":source, "target":dnodes[e1], "amount":rawData[e][e1]});
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

  if(verbose)
    console.log(nodes);
  return {"nodes": nodes, "links": links};
}
