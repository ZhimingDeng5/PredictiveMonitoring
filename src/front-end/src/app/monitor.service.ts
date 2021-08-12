import { Injectable } from '@angular/core';
import{Monitor,Monitors} from "./monitor";
import { Observable, of } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class MonitorService {
  selectedMonitor ?: Monitor;
  constructor() {}
  createMonitor(monitorname:String,createtime:String,
                filespredictors:File[],fileschema:File)
  {
    var monitor = {
      name:monitorname,
      timecreated:createtime,
      predictors:filespredictors,
      schema:fileschema
    }
    Monitors.push(monitor);
    console.log(monitor);
  }
  getMonitors(): Observable<Monitor[]> {
    return of(Monitors);
  }
  Delete(monitor)
  {
    var index = Monitors.indexOf(monitor)
    if (index>-1) {
      Monitors.splice(index,1)
    }
  }
  select(monitor:Monitor)
  {
    this.selectedMonitor=monitor
  }
  getselectedMonitor():Monitor
  {
      return this.selectedMonitor;
  }
}
