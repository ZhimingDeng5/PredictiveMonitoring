import { Component, OnInit } from '@angular/core';
import {Monitor, Monitors} from "../../monitor";
import {MonitorService} from "../../monitor.service";
import {FormBuilder, Validators} from "@angular/forms";
import axios from "axios";
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
  async CreateDashboard(){
    let formData = new FormData();
    formData.append("event_log", this.eventLog);
    let predictors:File[]=this.selectedMonitor.predictors;
    console.log(this.selectedMonitor.predictors);
    for(let i=0;i<predictors.length;i++)
    {
      formData.append("monitor",predictors[i]);
    }
    axios.post("http://localhost:8000/create-dashboard", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then((res)=>{
      if(res.status == 201){
        //this.selectedMonitor.taskid=res.data;
        //window.location.href='/monitor-viewing';
        //console.log(this.selectedMonitor.taskid);
      }
    });
    console.log("Monitor files uploaded!")
  }
}
