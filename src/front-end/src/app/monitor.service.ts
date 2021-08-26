import { Injectable } from '@angular/core';
import{Monitor,monitorList} from "./monitor";
import { Observable, of } from 'rxjs';
import { LocalStorageService } from './local-storage.service';
@Injectable({
  providedIn: 'root'
})
export class MonitorService {
  selectedMonitor ?: Monitor;
  Monitors:Monitor[]=[];
  private generateid(list:Set<String>):string
  {
    //let monitorList:Set<string> = this.storage.get(ID_STORAGE_KEY) || (new Set<string>());

    let id=Math.floor(Math.random() * (999999999 + 1)).toString();
    while (true)
    {
      if(!list.has(id)) {
        list.add(id);
        break;
      }
      else
        id=Math.floor(Math.random() * (999999999 + 1)).toString();
    }
    return id;
  }
  constructor(public LocalStorage: LocalStorageService) {}
  createMonitor(monitorName:string,createTime:string,
                filesPredictors:File[],fileSchema:File) {
    let monitor:string[] = [
      monitorName,
      createTime,
      filesPredictors.length.toString(),
   ]
    let predictorFiles:File[]=[]
    for(let i=0;i<filesPredictors.length;i++)
    {
      predictorFiles[i] = filesPredictors[i];
    }
    let id: string;
    let finish: number = 0;
    this.LocalStorage.get(monitorList).then(res => {
      if (res) {
        let mlist: Set<string> = <Set<string>>res;
        id = this.generateid(mlist)
        monitor.push(id);
        this.LocalStorage.add(id, monitor);
        this.LocalStorage.add(monitorList, mlist);
      } else {
        let mlist: Set<string>=new Set<string>();
        id = this.generateid(mlist)
        monitor.push(id);
        this.LocalStorage.add(id, monitor);
        this.LocalStorage.add(monitorList, mlist);
      }
      this.LocalStorage.add(id + "schema", fileSchema);
      for (let i: number = 1; i <= predictorFiles.length; i++) {
        this.LocalStorage.add(id + "predictor" + (i.toString()), predictorFiles[i-1]);
      }
    })









  }
  getMonitors(): Observable<Monitor[]> {
    this.Monitors=[];
    this.LocalStorage.get(monitorList).then(res =>{
      if (res&&(<Set<string>>res).size>0) {
        let monitoridList:Set<string>=<Set<string>>res;
        console.log(monitoridList)
        for(let monitorid of monitoridList)
        {
          console.log(monitoridList)
          this.LocalStorage.get(monitorid).then(res1=>
          {
            if(res1)
            {
              let monitorList=<string[]>res1;
              console.log(parseInt(monitorList[2]))
              let monitor:Monitor= {
                predictors : parseInt(monitorList[2]),
                name : monitorList[0],
                timecreated:monitorList[1],
                id:monitorList[3],
              }
              console.log(monitor);
              this.Monitors.push(monitor);
            }
          })
        }
      } else {
          console.log("no monitor has been created")
      }
    })
    return of(this.Monitors)
  }
  Delete(monitor)
  {
    // var index = this.Monitors.indexOf(monitor)
    // if (index>-1) {
    //   this.Monitors.splice(index,1)
    // }
  

    // this.LocalStorage.delete(monitor.id).then(res=>{
    //   this.LocalStorage.delete(monitor.id+"schema").then(res=>{
    //     for (let i: number = 1; i <= monitor.predictors; i++) {
    //       this.LocalStorage.delete(monitor.id + "predictor" + i);
    //     }

    //   })
    // })

    this.LocalStorage.delete(monitor.id)
    this.LocalStorage.delete(monitor.id+"schema")
    for (let i: number = 1; i <= monitor.predictors; i++) {
      this.LocalStorage.delete(monitor.id + "predictor" + i);         
    }
    this.LocalStorage.get("monitorList").then(res=>{
      let mlist: Set<string> = <Set<string>>res;  
        mlist.delete(monitor.id)
        this.LocalStorage.add(monitorList, mlist);
    })

    
  }


  select(monitor:Monitor)
  {
    this.selectedMonitor=monitor
    localStorage.setItem("currentMonitor",JSON.stringify(monitor));
  }
  getselectedMonitor():Monitor
  {
      return this.selectedMonitor;
  }
}
