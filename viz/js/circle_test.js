describe("checks Point class ", function() {
  it("creates a point with coordinates", function() {
    var max = 100;
    var x =  Math.floor(Math.random() * Math.floor(max));
    var y =  Math.floor(Math.random() * Math.floor(max));
    var point = new Point(x, y);
    expect(point.x).toEqual(x);
    expect(point.y).toEqual(y);
  });

  it("creates two points with coordinates and measures the distance between them", function() {

    var pointA = new Point(10, 5);
    var pointB = new Point(15, 7);
    expect(pointA.distanceTo(pointB)).toBeCloseTo(5.3852, 4);
  });

  it("checks if points are equal or not or if improper comparaison", function() {

    var pointA = new Point(10, 5);
    var pointB = new Point(15, 7);
    expect(pointA.equals(pointB)).toEqual(false);
    expect(pointA.equals(pointA)).toEqual(true);
    expect(pointA.equals(new Point(10, 5))).toEqual(true);
    expect(function() {pointA.equals("not a point");} ).toThrowError(TypeError);
  });

  it("checks if the center point of two points is correctly created", function() {

    var pointA = new Point(10, 10);
    var pointB = new Point(20, 10);
    var pointM = new Point(15, 10);

    expect(pointA.centerOf(pointB).equals(pointM)).toBe(true);
  });
});



describe("Checks Cirlce class ", function() {

    var x = 10;
    var y = 10;
    var rad = 10;
    var precision = 5;
    var test_data = [ {"x":x + rad, "y":y, "angle":0 },
                      {"x":x, "y":y + rad, "angle":90 },
                      {"x":x - rad, "y":y, "angle":180 },
                      {"x":x, "y":y - rad, "angle":270 },
                      {"x":x + rad, "y":y, "angle":360 },
                      {"x":x, "y":y + rad, "angle":450 }];

  describe("angle tests", function() {

    it("creates a circle", function() {

      var circle = new Circle(new Point(10,10), 5);
      expect().nothing();
    });

    it("gets angle from points on cirlce", function() {
      var center = new Point(x, y);
      var circle = new Circle(center, rad);

      test_data.forEach(function(e) {
        var angle = circle.getAngleFromPoint(new Point(e.x, e.y));
        expect(angle).toBeCloseTo(e.angle % 360);
      });

     expect().nothing();
    });

    it("creates two points with coordinates and measures the distance between them", function() {


      var center = new Point(x, y);
      var circle = new Circle(center, rad);

      test_data.forEach(function(e) {
        var anglePoint = circle.getPointFromAngle(e.angle);
        expect(anglePoint.x).toBeCloseTo(e.x);
        expect(anglePoint.y).toBeCloseTo(e.y);
      });

    });


  });


});
