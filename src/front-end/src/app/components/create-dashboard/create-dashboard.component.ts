import { Component, OnInit } from '@angular/core';
import {Monitor} from "../../monitor";
import {MonitorService} from "../../monitor.service";
import {FormBuilder, Validators} from "@angular/forms";
import axios from "axios";
import { LocalStorageService } from 'src/app/local-storage.service';
import { environment } from 'src/environments/environment';
import {Router} from "@angular/router";

@Component({
  selector: 'app-create-dashboard',
  templateUrl: './create-dashboard.component.html',
  styleUrls: ['./create-dashboard.component.css']
})
export class CreateDashboardComponent implements OnInit {
  eventLog:File=null;
  userForm=null;
  selectedMonitor:Monitor;
  testPickle:File;
  currentMonitor:String;
  showSpinner = false;
  constructor(private fb:FormBuilder,private monitorService:MonitorService, public LocalStorage: LocalStorageService, private router:Router) {
    this.userForm = this.fb.group({
      eventlog :['',Validators.required],
      dashName :['',Validators.required]
    })
  }
  ngOnInit(): void {
    //this.selectedMonitor=this.monitorService.selectedMonitor;

    this.selectedMonitor = JSON.parse(localStorage.getItem("currentMonitor"));
    console.log(this.selectedMonitor)
  }

  EventLogUpload(event) {
    this.eventLog= <File>event.target.files[0];
    console.log(this.eventLog);
  }

  //for test
  getPickle(){
    this.LocalStorage.get(this.selectedMonitor.name).then(res=>{
      if(res){
        //console.log("here")
        console.log(res)
      }
    })
  }


  async CreateDashboard(){

    this.showSpinner=true;
    // setTimeout(() => {
    //   this.showSpinner=false
    // }, 5000);
    let formData = new FormData();
    formData.append("event_log", this.eventLog);
    //let predictors:File[]=this.selectedMonitor.predictors;
     //let pickle:File
    for(let i=1;i<=this.selectedMonitor.predictors;i++)
    {
      this.LocalStorage.get(this.selectedMonitor.id+"predictor"+(i.toString())).then(res => {
        if (res) {
          let pickle:File = <File>res;
          formData.append("predictors", pickle);
          if(i==this.selectedMonitor.predictors) {
          }
        }
      })
    };
    this.LocalStorage.get(this.selectedMonitor.id+"schema").then(res=>{
      if(res)
      {
        let schema:File=<File>res;
        formData.append("schema",schema);
        axios.post(environment.backend + "/create-dashboard", formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then((res) => {
          if (res.status == 201) {
            localStorage.setItem(res.data.task_id,this.selectedMonitor.name);
            if(localStorage.getItem('dashboardList') != null && localStorage.getItem('cancelList')!= null){
              var mylist = JSON.parse(localStorage['dashboardList']);
              mylist.push(res.data.task_id);
              localStorage['dashboardList'] = JSON.stringify(mylist);
            }else{
              localStorage['dashboardList'] = JSON.stringify([res.data.task_id]);
              localStorage['cancelList'] = JSON.stringify([]);
              localStorage['completedList'] = JSON.stringify([]);
            }
            localStorage[res.data.task_id+"Name"]= this.userForm.value.dashName;

            console.log(res.data.task_id);
            console.log(this.selectedMonitor.name)
            console.log("Monitor files uploaded!")
           // window.location.href= './dashboard';
            this.router.navigateByUrl('/dashboard');

            //this.selectedMonitor.taskid=res.data;
            //window.location.href='/monitor-viewing';
            //console.log(this.selectedMonitor.taskid);
          }
        })
      }
    })


  }
}
