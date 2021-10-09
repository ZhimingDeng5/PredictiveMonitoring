// spec.js
describe('Testing monitor-creation', function() {
  var predictor_file = "/test-label-predictor.pkl";
  var absolutePath_predictor = __dirname+predictor_file;
  var schema_file = "/test-schema.json";
  var absolutePath_schema = __dirname+schema_file;


  it('should have a title', function() {
    browser.get('http://localhost:4200/monitor-creation');
    // put expected value here.
    expect(browser.getTitle()).toEqual('Predictive Monitoring');
  });
  // test if it can add some contents
  it('should type in monitor name', function() {
    var monitor_name = element(by.css('[formControlName="name"]') );
    monitor_name.sendKeys("monitor1")
    browser.sleep(2000)
  });
  it('should upload predictors', function() {
    element(by.css('[formControlName="predictors"]') ).sendKeys(absolutePath_predictor);
    browser.sleep(2000)
  });
  it('should upload Schema', function() {
    element(by.css('[formControlName="schema"]') ).sendKeys(absolutePath_schema);
    browser.sleep(2000)
  });
  it('should clear all information', function() {
    element(by.css('[class="reset_mon"]')).click();
    expect(element(by.css('[formControlName="name"]')).getText()).toEqual("");
    expect(element(by.css('[formControlName="predictors"]')).getText()).toEqual("");
    expect(element(by.css('[formControlName="schema"]')).getText()).toEqual("");
    browser.sleep(2000)
  });
  it('should create a monitor', function() {
    var monitor_name = element(by.css('[formControlName="name"]') );
    monitor_name.sendKeys("monitor1")
    browser.sleep(1000)
    element(by.css('[formControlName="predictors"]') ).sendKeys(absolutePath_predictor);
    browser.sleep(1000)
    element(by.css('[formControlName="schema"]') ).sendKeys(absolutePath_schema);
    browser.sleep(1000)
    element(by.css('[class="create_mon"]')).click();
    browser.sleep(2000)
  });
  it('should view monitors', function() {
    element(by.css('[class="view_mon"]')).click();
    browser.sleep(2000)
    expect(element(by.css('[class="monitor_text"]')).getText()).toEqual("monitor1");
  });


});
