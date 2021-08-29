import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router'
import { discardPeriodicTasks } from '@angular/core/testing';
import axios from 'axios';
import { timer } from 'rxjs';
import {Monitor} from "../../monitor";
import {MonitorService} from "../../monitor.service";
import { LocalStorageService } from '../../local-storage.service';
import { environment } from 'src/environments/environment';




@Component({
  selector: 'app-predictive-dashboard',
  templateUrl: './predictive-dashboard.component.html',
  styleUrls: ['./predictive-dashboard.component.css']
})
export class PredictiveDashboardComponent implements OnInit {
  tasks = [];
  selectedMonitor: Monitor;


  viewDetail() {
    alert('Hello');
  }
  constructor(private monitorService:MonitorService, public LocalStorage: LocalStorageService, private router: Router) { }

  ngOnInit(): void {
    this.selectedMonitor=this.monitorService.selectedMonitor;


    axios.get(environment.backend + "/tasks", {
    }).then((res)=>{

      console.log(res);
      for(var i = 0; i<res.data.tasks.length; i++){
        this.tasks[i] =[];
        this.tasks[i]['id']=res.data.tasks[i].taskID;
        this.tasks[i]['name']=localStorage.getItem(res.data.tasks[i].taskID);
        console.log(localStorage.getItem(res.data.tasks[i].taskID))
        console.log(this.tasks[i]['name'])
        this.tasks[i]['status']=res.data.tasks[i].status;
        if (res.data.tasks[i].status==="PROCESSING"){

          this.tasks[i]['buttonString']="Cancel"
        }else{
          this.tasks[i]['buttonString']="Delete"
        }
        if (res.data.tasks[i].status==="COMPLETED"){

        }else{

        }
      }
    });


    //polling
    setInterval(()=>{
      axios.get(environment.backend + "/tasks", {
      }).then((res)=>{
        let refresh = false;
        console.log(res)
        if(res.data.tasks.length != this.tasks.length){
          refresh = true;
          // window.location.reload();
        }
        else {
          for(var i = 0; i<this.tasks.length; i++){
            if(res.data.tasks[i].id != this.tasks[i]["id"] || res.data.tasks[i].status != this.tasks[i]["status"]){
              refresh = true;
              break;
              // window.location.reload();
            }
          }
        }
        if(refresh) {
          this.tasks = [];
          for(var i = 0; i<res.data.tasks.length; i++){
            this.tasks[i] =[];
            this.tasks[i]['id']=res.data.tasks[i].taskID;
            this.tasks[i]['name']=localStorage.getItem(res.data.tasks[i].taskID);
            console.log(localStorage.getItem(res.data.tasks[i].taskID))
            console.log(this.tasks[i]['name'])
            this.tasks[i]['status']=res.data.tasks[i].status;
            if (res.data.tasks[i].status==="PROCESSING"){
    
              this.tasks[i]['buttonString']="Cancel"
            }else{
              this.tasks[i]['buttonString']="Delete"
            }
            if (res.data.tasks[i].status==="COMPLETED"){
    
            }else{
    
            }
          }
        }
        else {
          console.log("nothing updated");
        }
       
      });
    }, 10000);
  }


  view(item){
    if(item.status==="COMPLETED"){

      axios.get(environment.backend + '/dashboard/' + item.id, {}).then((res) => {
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

    for(let i = 0; i<this.tasks.length; i++) {
      if (this.tasks[i]['status'] === "COMPLETED" || this.tasks[i]['status'] === "CANCELLED") {
      //  window.alert(" DELETE now: "+ task_id + "with status: " + this.tasks[i]['status']);
        this.deleteDashboard(task_id);
      }
      if (this.tasks[i]['status'] === "PROCESSING" || this.tasks[i]['status'] === "QUEUED") {
      //  window.alert(" CANCEL now: "+ task_id + "with status: " + this.tasks[i]['status']);
        this.cancelDashboard(task_id);
      }
    }

  }


  cancelDashboard(task_id)
  {
// <<<<<<< dev
    axios.delete(environment.backend + "/cancel/" + task_id, {}).then((res) => {
    console.log("Cancel tasks success!");
//       this.router.navigateByUrl("/dashboard")
//       // window.location.reload();
//       console.log("Cancel going on!");
//=======
//    axios.delete("http://localhost:8000/cancel/" + task_id, {}).then((res) => {
//      window.location.reload();
//      console.log("Cancel tasks success!");
//>>>>>>> BP-front-end
    });
  }


//<<<<<<< dev
//       axios.get(environment.backend + "/dashboard/" + task_id, {}).then(() => {
//         this.router.navigateByUrl("/dashboard")
//         // window.location.reload();

//       })
//     }
//     else {
//       window.alert("not found in localStorage, error!");
//=======
  deleteDashboard(task_id) {
    // this is a front-end-only function to clear the dashboard list
      if (localStorage.getItem(task_id) != null) {
        localStorage.removeItem(task_id);
        //window.location.reload();
      }
      //else {
        //window.location.reload();
     // }
//>>>>>>> BP-front-end
    }

  /*  axios.get("http://localhost:8000/dashboard/" + task_id, {}).then(() => {
      window.location.reload();
    });
  }*/
}
