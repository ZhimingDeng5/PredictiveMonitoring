import { Injectable } from '@angular/core';
import{Monitor,Monitors} from "./monitor";
import { Observable, of } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class MonitorService {

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
}
