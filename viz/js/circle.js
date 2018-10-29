
function Point(x, y) {

  if(x < 0 || y < 0) {
    throw new RangeError("Coordinates must not be nagative");
  }

  this.x = x;
  this.y = y;

  this.distanceTo = function(point) {
    return Math.sqrt( Math.pow(this.x - point.x, 2) +  Math.pow(this.y - point.y, 2) );
  }

  this.centerOf = function(otherPoint) {
    return new Point((this.x + otherPoint.x) / 2, (this.y + otherPoint.y) / 2);
  }
}

Point.prototype.equals = function (otherPoint) {
  if(! (otherPoint instanceof Point)) {
    throw new TypeError((typeof otherPoint) + " is not a Point object");
  }

  return this.x == otherPoint.x && this.y == otherPoint.y;
};


function Circle(center, rad) {
  this.center = center;
  this.r = rad;
  this.startPoint = new Point(center.x + this.r, center.y);

  this.pointToArcDist = function(point, startArcPoint, enArcPoint, step=1) {
  }

  /**
   * get a point on the circle from a given angle
   * @param  {[float]} a [angle]
   * @return {[Point]}   [a Point on the circle]
   */
  this.getPointFromAngle = function(a) {
    var x = this.center.x + this.r * Math.cos(a * (Math.PI / 180));
    var y = this.center.y + this.r * Math.sin(a * (Math.PI / 180));
    return new Point(x, y);
  }

  /**
   * get angle between a point and circle center
   * @param  {[Point]} point [the point to get the angle from]
   * @return {[float]}       [the angle between the point and the circle center in degrees]
   */
  this.getAngleFromPoint = function(point) {

    var midPoint = point.centerOf(this.startPoint);
    var adj = point.distanceTo(midPoint);
    var hyp = this.r;

    var alphaAngle = Math.acos(adj/hyp) * (180 / Math.PI);
    var pointAngle = 180 - 2*alphaAngle;

    if(point.y < this.center.y) {
      return 360 - pointAngle;
    }
    return pointAngle;
  }


}
