// spec.js
describe('Testing dashboard', function() {
  var predictor_file = "/test-label-predictor.pkl";
  var absolutePath_predictor = __dirname+predictor_file;
  var schema_file = "/test-schema.json";
  var absolutePath_schema = __dirname+schema_file;
  var event_log = "/test-event-log.csv";
  var absolutePath_log = __dirname+event_log;

  browser.get('http://localhost:4200/monitor-creation');
  // go to monitor_viewing page
  it('should create a monitor and view monitors', function() {
    var monitor_name = element(by.css('[formControlName="name"]') );
    monitor_name.sendKeys("monitor1")
    browser.sleep(1000)
    element(by.css('[formControlName="predictors"]') ).sendKeys(absolutePath_predictor);
    browser.sleep(1000)
    element(by.css('[formControlName="schema"]') ).sendKeys(absolutePath_schema);
    browser.sleep(1000)
    element(by.css('[class="create_mon"]')).click();
    browser.sleep(2000)
    element(by.css('[class="view_mon"]')).click();
    browser.sleep(2000)
    expect(element(by.css('[class="monitor_text"]')).getText()).toEqual("monitor1");

  });
  it('should go to create-dashboard page and check monitor name', function() {
    element(by.buttonText('create')).click();
    browser.sleep(2000)
    expect(element(by.cssContainingText('span', 'Monitor name:monitor1')).isPresent()).toBe(true);

  });

  it('should upload event log and type dashboard name and create dashboard', function() {
    element(by.css('[formControlName="eventlog"]') ).sendKeys(absolutePath_log);
    browser.sleep(2000)
    var dashboard_name = "dashboard1";
    element(by.css('[formControlName="dashName"]') ).sendKeys(dashboard_name); 
    browser.sleep(2000)
    element(by.buttonText('Create DashBoard')).click();

  });

  // it('should go back', function() {
  //   browser.sleep(500)
  //   element(by.buttonText('Back')).click();

  // });
  
  // it('should create second dashboard', function() {
  //   var event_log = "/Users/guolingge/PredictiveMonitoring/DataSamples/bpi/test-event-log.csv";
  //   element(by.css('[formControlName="eventlog"]') ).sendKeys(event_log); 
  //   var dashboard_name = "dashboard2";
  //   element(by.css('[formControlName="dashName"]') ).sendKeys(dashboard_name); 
  //   element(by.buttonText('Create DashBoard')).click();

  // });

  // it('should view dashboard and check status', function() {
  //   //element(by.buttonText('View Dashboard')).click();
  //   browser.sleep(1000)

  // });

  it('should click view', function() {
    //element(by.buttonText('View Dashboard')).click(); 
    browser.sleep(8000)
    browser.refresh();

    var tabledata = element(by.css('[class="dashtable"]'));
    // // get rows 
    var row = tabledata.all(by.tagName("tr")).first();
    
    var cells = row.all(by.tagName('td'));
    // var cellTexts = cells.map(function (elm) {
    //   return elm.getText();
    // });
    //expect(cellTexts).toEqual([""]);
    // // // // var row = element.all(by.ngFor('let item of initTasks')).first();
    //element(by.buttonText('view')).click();
    // // browser.sleep(2000)
  });

  // it('should download CSV', function() {
  //   //element(by.buttonText('View Dashboard')).click(); 
  //   browser.sleep(2000)
  //   element(by.buttonText('download CSV')).click();
  //   browser.sleep(2000)
  // });

  // it('should go back', function() {
  //   element(by.buttonText('Back')).click();
  // });

  // it('should click delete', function() {
  //   //element(by.buttonText('View Dashboard')).click(); 
  //   browser.sleep(2000)
  //   element(by.buttonText('Delete')).click();
  //   browser.sleep(2000)


  // });




      
















  



  


});
