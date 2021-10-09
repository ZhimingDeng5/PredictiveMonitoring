// spec.js
describe('Testing monitor-viewing', function() {
  var predictor_file = "/test-label-predictor.pkl";
  var absolutePath_predictor = __dirname+predictor_file;
  var schema_file = "/test-schema.json";
  var absolutePath_schema = __dirname+schema_file;
  browser.get('http://localhost:4200/monitor-creation');
  // go to monitor_viewing page
  it('should create a monitor and view monitors', function() {
    var monitor_name = element(by.css('[formControlName="name"]') );
    monitor_name.sendKeys("monitor1")
    browser.sleep(1000)
    element(by.css('[formControlName="predictors"]') ).sendKeys(absolutePath_predictor);
    browser.sleep(1000)
    element(by.css('[formControlName="schema"]') ).sendKeys(absolutePath_schema;
    browser.sleep(1000)
    element(by.css('[class="create_mon"]')).click();
    browser.sleep(2000)
    element(by.css('[class="view_mon"]')).click();
    browser.sleep(2000)
    expect(element(by.css('[class="monitor_text"]')).getText()).toEqual("monitor1");

  });
  it('should go to create-dashboard page and go back', function() {
    element(by.buttonText('create')).click();
    browser.sleep(2000)
    element(by.buttonText('Back to Monitor Viewing')).click();
    browser.sleep(2000)

  });
  it('should delete the monitor', function() {
    element(by.buttonText('delete')).click();
    browser.sleep(2000)
    browser.navigate().refresh();
    browser.sleep(2000)
  });
  



  


});
