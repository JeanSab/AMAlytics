


describe("json load via d3", function() {
  it("checks if json file is loaded properly", function() {
    expect(loadJson()).toEqual(jasmine.any(Object));
  });
});
