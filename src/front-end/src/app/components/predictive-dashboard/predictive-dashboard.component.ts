import {ChangeDetectorRef, Component, NgModule, OnInit} from '@angular/core';
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

  length = 0;
  initTasks = [];
  newTasks = [];
  selectedMonitor: Monitor;


  viewDetail() {
    alert('Hello');
  }

  constructor(private monitorService: MonitorService,
              public LocalStorage: LocalStorageService,
              private router: Router,
            ) {
  }

  ngOnInit(): void {


    this.selectedMonitor = this.monitorService.selectedMonitor;
    if (!localStorage['dashboardList']) {
      console.log("No tasks are generated now!!!");
    } else {
      var dashboardlist = JSON.parse(localStorage['dashboardList']);
      console.log(dashboardlist)
      var path = "";
      for (var i = 0; i < dashboardlist.length; i++) {
        path = path + dashboardlist[i] + "&";
        console.log(dashboardlist[i]);

      }
      path = path.substring(0, path.length - 1);
      console.log(path);
      console.log(environment.backend + "/task/" + path);
      if (!path) {
        console.log("No tasks to track!");
      } else {
        axios.get(environment.backend + "/task/" + path, {}).then((res) => {
          console.log(environment.backend + "/task/2" + path);
          var tasks = res.data.tasks
          console.log(tasks)
          for (var i = 0; i < dashboardlist.length; i++) {
            this.initTasks[i] = [];
            this.initTasks[i]['id'] = dashboardlist[i];
            this.initTasks[i]['name'] = localStorage.getItem(dashboardlist[i]);
            for (var j = 0; j < tasks.length; j++) {
              if (tasks[j]['taskID'] === this.initTasks[i]['id']) {
                this.initTasks[i]['status'] = tasks[j]['status']
              }
            }

            // Display different buttons according to 'status' of tasks
            if (this.initTasks[i]['status'] === "PROCESSING") {
              this.initTasks[i]['buttonString'] = "Cancel"
            } else {
              this.initTasks[i]['buttonString'] = "Delete"
            }
          }

          //console.log("check~~~ "+ this.initTasks.length);
        })


        // axios.get(environment.backend + "/tasks", {
        // }).then((res)=>{
        //   this.length = res.data.tasks.length;
        //   console.log(this.length);
        //   for(var i = 0; i<this.length; i++){
        //     this.initTasks[i] =[];
        //     this.initTasks[i]['id']=res.data.tasks[i].taskID;
        //     this.initTasks[i]['name']=localStorage.getItem(res.data.tasks[i].taskID);
        //     this.initTasks[i]['status']=res.data.tasks[i].status;
        //     if (res.data.tasks[i].status==="PROCESSING"){
        //       this.initTasks[i]['buttonString']="Cancel"
        //     }else{
        //       this.initTasks[i]['buttonString']="Delete"
        //     }
        //     if (res.data.tasks[i].status==="COMPLETED"){
        //     }else{
        //     }
        //   }
        // });


        //polling


       /* setInterval(() => {

          axios.get(environment.backend + "/task/" + path, {}).then((res) => {
            this.router.navigateByUrl("/dashboard")
            console.log("nothing updated");



            // console.log(res)
            // if(res.data.tasks.length != this.length){
            //   this.router.navigateByUrl("/dashboard")
            //   // window.location.reload();
            // }

            // for(var i = 0; i<this.length; i++){
            //   if(res.data.tasks[i].id != this.initTasks[i]["id"] || res.data.tasks[i].status != this.initTasks[i]["status"]){
            //     this.router.navigateByUrl("/dashboard")
            //     // window.location.reload();
            //   }
            // }
            //console.log("nothing updated");
          });

        }, 10000);*/
      }
    }
  }


  view(item) {
    if (item.status === "COMPLETED") {

      axios.get(environment.backend + '/dashboard/' + item.id, {}).then((res) => {


        const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
        this.LocalStorage.add(item.id + 'csv', blob).then((res) => {
          this.router.navigateByUrl("/dashboard_detail/" + item.id)

        })
      })
      this.deleteDashboard(item.id);

    } else {
      alert("cannot view a cancelled dashboard or uncompleted dashboard!")

    }


  }

  operation(task_id) {

    for (let i = 0; i < this.initTasks.length; i++) {


      if (this.initTasks[i]['status'] === "COMPLETED" || this.initTasks[i]['status'] === "CANCELLED") {
        //  window.alert(" DELETE now: "+ task_id + "with status: " + this.initTasks[i]['status']);
        this.deleteDashboard(task_id);
      }
      if (this.initTasks[i]['status'] === "PROCESSING" || this.initTasks[i]['status'] === "QUEUED") {
        //  window.alert(" CANCEL now: "+ task_id + "with status: " + this.initTasks[i]['status']);
        this.cancelDashboard(task_id);
      }
    }

  }


  cancelDashboard(task_id) {
// <<<<<<< dev
//     axios.delete(environment.backend + "/cancel/" + task_id, {}).then((res) => {
//       this.router.navigateByUrl("/dashboard")
//       // window.location.reload();
//       console.log("Cancel going on!");
//=======

    axios.delete(environment.backend + '/cancel/' + task_id, {}).then((res) => {
      //    window.location.reload();
      console.log("Use Cancel tasks success!");

//>>>>>>> BP-front-end
    });
  }


//<<<<<<< dev
//       axios.get(environment.backend + "/dashboard/" + task_id, {}).then(() => {
//         this.router.navigateByUrl("/dashboard")
//         // window.lo cation.reload();

//       })
//     }
//     else {
//       window.alert("not found in localStorage, error!");
//=======
  deleteDashboard(task_id) {
    // Remove the localstorage
      var dashboardlist = JSON.parse(localStorage['dashboardList']);
    for (var i = 0; i < dashboardlist.length; i++) {
      if (dashboardlist[i] === task_id) {
        dashboardlist.splice(i, 1)
        localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
        localStorage.removeItem(task_id);
        //    window.location.reload();
      }
    }
    // Apply '/cancel' endpoint to delete the task in the worker node

    axios.delete(environment.backend + '/cancel/' + task_id, {}).then((res) => {
      //    window.location.reload();
      console.log("Cancel tasks success!");
    });
    }



//>>>>>>> BP-front-end


    /*  axios.get("http://localhost:8000/dashboard/" + task_id, {}).then(() => {
        window.location.reload();
      });
    }*/

}
