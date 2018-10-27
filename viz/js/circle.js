
/**
 * Get distances from a static point to a list of points on a circle arc.
 * @param  {[object]} fromPoint   the static point with x and y coordinates
 * @param  {[type]} circle        the arc's cirlce with x, y center coordinates and r radius
 * @param  {[type]} startArcPoint the start point on the circle arc with x and y coordinates
 * @param  {[type]} stopArcPoint  the stop point on the circle with x and y coordinates
 * @return {[type]}               a dictionary with the following structure {"" : dist}
 */
function pointToArcDist(fromPoint, circle, startArcPoint, stopArcPoint) {


}


function Point(x, y) {
  this.x = x;
  this.y = y;

  this.distance = function(point) {
    return Math.sqrt( Math.pow(this.x - point.x, 2) +  Math.sqrt(this.y - point.y, 2) );
  }
}


function Circle(center, rad) {
  this.center = center;
  this.r = rad;

  this.pointToArcDist = function(point, startArcPoint, enArcPoint, step=1) {


  }

  this.getCirclePointFromAngle = function(a) {
    var x = this.x + this.r * Math.cos(a * (Math.PI / 180));
    var y = this.y + this.r * Math.sin(a * (Math.PI / 180));
    return new Point(x, y);
  }
}
