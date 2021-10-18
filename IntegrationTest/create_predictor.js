// spec.js
describe('Testing creating predictor', function() {

  browser.get('http://localhost:4200/#/monitor-creation');
  var predictor_file = "/test-label-predictor.pkl";
  var absolutePath_predictor = __dirname+predictor_file;
  var schema_file = "/test-schema.json";
  var absolutePath_schema = __dirname+schema_file;
  var event_log = "/test-event-log.csv";
  var absolutePath_log = __dirname+event_log;
  // go to monitor_viewing page
  it('should click Training', function() {
    element(by.buttonText('Training')).click();
    browser.sleep(2000)
  });

  it('should click create predictor', function() {
    element(by.cssContainingText('a', 'create predictor')).click();
    browser.sleep(2000)
  });
  it('should type predictor name and upload files', function() {
    var predictor_name = element(by.css('[formControlName="predictorName"]') );
    predictor_name.sendKeys("predictor1")
    browser.sleep(2000)
    element(by.css('[formControlName="eventlog"]') ).sendKeys(absolutePath_log);
    browser.sleep(2000)
    element(by.css('[formControlName="schema"]') ).sendKeys(absolutePath_schema);
    browser.sleep(2000)
    element(by.buttonText('Create')).click();
    browser.sleep(2000)

  });
  it('should go to predictor list', function() {
    browser.refresh();
    element(by.buttonText('Training')).click();
    browser.sleep(2000)
    element(by.cssContainingText('a', 'predictor list')).click();
  });









  



  


});
