import { Component, OnInit } from '@angular/core';
import {Monitor, Monitors} from "../../monitor";
import {MonitorService} from "../../monitor.service";
import {FormBuilder, Validators} from "@angular/forms";
import axios from "axios";
import { LocalStorageService } from 'src/app/local-storage.service';
@Component({
  selector: 'app-create-dashboard',
  templateUrl: './create-dashboard.component.html',
  styleUrls: ['./create-dashboard.component.css']
})
export class CreateDashboardComponent implements OnInit {
  eventLog:File=null;
  userForm=null;
  selectedMonitor:Monitor;
  testPickle:File
  constructor(private fb:FormBuilder,private monitorService:MonitorService, public LocalStorage: LocalStorageService) {
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

  //for test 
  getPickle(){
    this.LocalStorage.get(this.selectedMonitor.name).then(res=>{
      if(res){
        console.log("here")
        console.log(res)
      }
    })
  }

  async CreateDashboard(){
    let formData = new FormData();
    formData.append("event_log", this.eventLog);
    //let predictors:File[]=this.selectedMonitor.predictors;
     //let pickle:File
     var pickle = this.LocalStorage.get(this.selectedMonitor.name);
     //let predictors:File[]=[pickle]
     let predictors = []
     predictors.push(pickle)
    
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
