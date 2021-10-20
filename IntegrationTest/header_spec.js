// spec.js
describe('Testing header', function() {
  browser.get('http://localhost:4200/monitor-creation');
  // go to monitor_viewing page
  it('should click Predictive Monitoring', function() {
    element(by.buttonText('Predictive Monitoring')).click();
    browser.sleep(2000)
  });

  it('should click View Monitors', function() {
    element(by.cssContainingText('a', 'View Monitors')).click();
    browser.sleep(2000)
  });

  it('should click Back', function() {
    element(by.buttonText('Back')).click();
    browser.sleep(2000)
    browser.navigate().refresh();

  });

  it('should click View Dashboards', function() {
    element(by.buttonText('Predictive Monitoring')).click();
    browser.sleep(2000)
    element(by.cssContainingText('a', 'View Dashboards')).click();
    browser.sleep(2000)
  });

  it('should click Create Monitor', function() {
    browser.navigate().refresh();
    element(by.buttonText('Predictive Monitoring')).click();
    browser.sleep(2000)
    element(by.cssContainingText('a', 'Create Monitor')).click();
    browser.sleep(2000)
  });






  



  


});
