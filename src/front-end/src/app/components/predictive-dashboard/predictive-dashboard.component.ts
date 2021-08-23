import { Component, OnInit } from '@angular/core';
import { discardPeriodicTasks } from '@angular/core/testing';
import axios from 'axios';
import { timer } from 'rxjs';
import {Monitor} from "../../monitor";
import {MonitorService} from "../../monitor.service";

@Component({
  selector: 'app-predictive-dashboard',
  templateUrl: './predictive-dashboard.component.html',
  styleUrls: ['./predictive-dashboard.component.css']
})
export class PredictiveDashboardComponent implements OnInit {

  length = 0;
  initTasks = [];
  newTasks = [];
  selectedMonitor: Monitor;


  viewDetail() {
    alert('Hello');
  }
  constructor(private monitorService:MonitorService) { }

  cancleDashboard(task_id){

    //alert(task_id);

    axios.delete("http://localhost:8000/cancel/"+task_id , {
    }).then((res)=>{
      window.location.reload();
    });



  }




  ngOnInit(): void {
    this.selectedMonitor=this.monitorService.selectedMonitor;


    axios.get("http://localhost:8000/tasks", {
    }).then((res)=>{
      this.length = res.data.tasks.length;
      console.log(this.length);


      for(var i = 0; i<this.length; i++){
        this.initTasks[i] =[];
        this.initTasks[i]['id']=res.data.tasks[i].taskID;
        this.initTasks[i]['name']=res.data.tasks[i].name;
	      this.initTasks[i]['status']=res.data.tasks[i].status;
      }


    });


    //polling
    setInterval(()=>{
      axios.get("http://localhost:8000/tasks", {
    }).then((res)=>{


      if(res.data.tasks.length != this.length){

        location.reload();

      }

      for(var i = 0; i<this.length; i++){
        if(res.data.tasks[i].id != this.initTasks[i]["id"] || res.data.tasks[i].status != this.initTasks[i]["status"]){

          location.reload();

        }
      }

      console.log("nothing updated");

    });
    }, 10000);
  }

}