import { Injectable } from '@angular/core';
import{Monitor,Monitors} from "./monitor";
import { Observable, of } from 'rxjs';
import { LocalStorageService } from './local-storage.service';
@Injectable({
  providedIn: 'root'
})
export class MonitorService {
  selectedMonitor ?: Monitor;
  constructor(public LocalStorage: LocalStorageService) {}
  createMonitor(monitorname:String,createtime:String,
                filespredictors:File[],fileschema:File)
  {
    var monitor = {
      name:monitorname,
      timecreated:createtime,
      predictors:[],
      schema:fileschema
    }
    for (let index in filespredictors)
    {
      monitor.predictors[index]=filespredictors[index];
    }


    Monitors.push(monitor);
    console.log(monitor.predictors[0]);
    this.LocalStorage.add(monitor.name,monitor.predictors[0]).then(res=>{
      if(res){
        alert("insert successfully")
      }
    }

     //for test 
 
    
  


    )

    this.LocalStorage.get(monitor.name).then(res=>{
      if(res){
        console.log("here")
        console.log(res)
      }
    })

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
