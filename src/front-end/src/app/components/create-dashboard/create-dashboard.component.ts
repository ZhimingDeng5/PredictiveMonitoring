import { Component, OnInit } from '@angular/core';
import {Monitor, Monitors} from "../../monitor";
import {MonitorService} from "../../monitor.service";
import {FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'app-create-dashboard',
  templateUrl: './create-dashboard.component.html',
  styleUrls: ['./create-dashboard.component.css']
})
export class CreateDashboardComponent implements OnInit {
  eventLog:File=null;
  userForm=null;
  selectedMonitor:Monitor;
  constructor(private fb:FormBuilder,private monitorService:MonitorService) {
    this.userForm = this.fb.group({
      eventlog :['',Validators.required]
    })
  }
  ngOnInit(): void {
    this.selectedMonitor=this.monitorService.selectedMonitor;
  }
  EventLogUpload(event) {
    this.eventLog= <File>event.target.files[0];
    console.log(this.eventLog);
  }
  CreateDashboard(){
    console.log("Dashboard Created!")
  }
}
