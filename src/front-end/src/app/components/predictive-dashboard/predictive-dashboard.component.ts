import { Component, OnInit } from '@angular/core';
import { discardPeriodicTasks } from '@angular/core/testing';
import axios from 'axios';
import { timer } from 'rxjs';
import {Monitor} from "../../monitor";
import {MonitorService} from "../../monitor.service";
import { LocalStorageService } from '../../local-storage.service';




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
  constructor(private monitorService:MonitorService, public LocalStorage: LocalStorageService) { }


  operation(task_id) {

    if(this.initTasks[length]['buttonString'] === "Cancel")
    {
      this.cancelDashboard(task_id);

    }
    else if (this.initTasks[length]['buttonString'] === "Delete") {
      this.deleteDashboard(task_id);
    }

  }


  cancelDashboard(task_id)
  {
    axios.delete("http://localhost:8000/cancel/" + task_id, {}).then((res) => {
      window.location.reload();
      console.log("Cancel going on!");
    });
  }

  // we need to introduce formal "delete" endpoint after the demo
  // here I use /dashboard endpoint to replace
  deleteDashboard(task_id)
  {
    axios.get("http://localhost:8000/dashboard/" + task_id, {}).then(() => {
      window.location.reload();

    })
    localStorage.removeItem(task_id);
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
        this.initTasks[i]['name']=localStorage.getItem(res.data.tasks[i].taskID);
        console.log(localStorage.getItem(res.data.tasks[i].taskID))
        console.log(this.initTasks[i]['name'])
        this.initTasks[i]['status']=res.data.tasks[i].status;
        if (res.data.tasks[i].status==="PROCESSING"){

          this.initTasks[i]['buttonString']="Cancel"
        }else{
          this.initTasks[i]['buttonString']="Delete"
        }

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
