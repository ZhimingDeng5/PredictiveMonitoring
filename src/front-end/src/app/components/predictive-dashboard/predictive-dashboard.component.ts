import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router'
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
  constructor(private monitorService:MonitorService, public LocalStorage: LocalStorageService, private router: Router) { }

  ngOnInit(): void {
    this.selectedMonitor=this.monitorService.selectedMonitor;


    axios.get("https://apromore-predict.cloud.ut.ee/backend/tasks", {
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

        if (res.data.tasks[i].status==="COMPLETED"){


        }else{

        }


      }


    });





    //polling
    setInterval(()=>{
      axios.get("https://apromore-predict.cloud.ut.ee/backend/tasks", {
      }).then((res)=>{

        console.log(res)
        if(res.data.tasks.length != this.length){
          this.router.navigateByUrl("/dashboard")
          // window.location.reload();
        }

        for(var i = 0; i<this.length; i++){
          if(res.data.tasks[i].id != this.initTasks[i]["id"] || res.data.tasks[i].status != this.initTasks[i]["status"]){
            this.router.navigateByUrl("/dashboard")
            // window.location.reload();
          }
        }
        console.log("nothing updated");
      });
    }, 10000);
  }


  view(item){
    if(item.status==="COMPLETED"){

      axios.get('https://apromore-predict.cloud.ut.ee/backend/dashboard/' + item.id, {}).then((res) => {
          const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
          this.LocalStorage.add(item.id +'csv', blob).then((res)=> {
            this.router.navigateByUrl("/dashboard_detail/"+item.id)
            // window.location.href="/dashboard_detail/"+item.id
          })
        })
      }
    else{
      alert("cannot view a cancelled dashboard or uncompleted dashboard!")

    }

  }

  operation(task_id) {
        if(this.initTasks[this.length - 1]['status'] === "COMPLETED" || this.initTasks[this.length - 1]['status'] === "CANCELLED" )
        {
         this.deleteDashboard(task_id);
        }
        if (this.initTasks[this.length - 1]['status'] === "PROCESSING" || this.initTasks[this.length - 1]['status'] === "QUEUED")
        {
         this.cancelDashboard(task_id);
        }


  }



  cancelDashboard(task_id)
  {
    axios.delete("https://apromore-predict.cloud.ut.ee/backend/cancel/" + task_id, {}).then((res) => {
      this.router.navigateByUrl("/dashboard")
      // window.location.reload();
      console.log("Cancel going on!");
    });
  }

  // we need to introduce formal "delete" endpoint after the demo
  // here I use /dashboard endpoint to replace
  deleteDashboard(task_id)
  {

    if(localStorage.getItem(task_id) != null) {
      localStorage.removeItem(task_id);

      axios.get("https://apromore-predict.cloud.ut.ee/backend/dashboard/" + task_id, {}).then(() => {
        this.router.navigateByUrl("/dashboard")
        // window.location.reload();

      })
    }
    else {
      window.alert("not found in localStorage, error!");
    }

  }


}
