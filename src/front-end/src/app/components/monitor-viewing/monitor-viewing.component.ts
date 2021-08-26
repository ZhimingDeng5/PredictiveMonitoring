import { Component, OnInit } from '@angular/core';
import {Monitor} from "../../monitor";
import {MonitorService} from "../../monitor.service";

@Component({
  selector: 'app-monitor-viewing',
  templateUrl: './monitor-viewing.component.html',
  styleUrls: ['./monitor-viewing.component.css']
})
export class MonitorViewingComponent implements OnInit {
  MonitorList !: Monitor[];
  selectedMonitor:Monitor
  constructor(private monitorService : MonitorService)
  {}

  ngOnInit(): void {
      this.getMonitors()
  }

  delete(monitor:Monitor)
  {
    this.monitorService.Delete(monitor);
    location.reload();


  }
  getMonitors()
  {
    this.monitorService.getMonitors().
    subscribe(Monitors => this.MonitorList = Monitors);
  }
  select(monitor:Monitor)
  {
    this.monitorService.select(monitor);
    
    

  }
}