import {ChangeDetectorRef, Component, NgModule, OnInit} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router'
import { discardPeriodicTasks } from '@angular/core/testing';
import axios from 'axios';
import {catchError, timer} from 'rxjs';
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
  mySubscription: any;

  viewDetail() {
    alert('Hello');
  }

  constructor(private monitorService: MonitorService,
              public LocalStorage: LocalStorageService,
              private router: Router,
  ) {
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };
    this.mySubscription = this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        // Trick the Router into believing it's last link wasn't previously loaded
        this.router.navigated = false;
      }
    });
  }

  ngOnInit(): void {
    this.selectedMonitor = this.monitorService.selectedMonitor;
    this.updateTask();

    //polling
    let interval = setInterval(() => {
      let url = location.href
      let site = url.lastIndexOf("\/");
      let loc = url.substring(site + 1, url.length);
      if (loc == "dashboard") {
        this.updateTask();
      } else {
        clearInterval(interval);
      }
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
    }, 5000);

  }

  updateTask() {
    if (!localStorage['dashboardList']) {
      console.log("No tasks are generated now!!!");
    } else {
      var dashboardlist = JSON.parse(localStorage['dashboardList']);
      var cancelList = JSON.parse(localStorage['cancelList']);
      console.log("dashboard list check: " + dashboardlist)
      console.log("cancel list check: " + cancelList)
      var path = "";
      if (dashboardlist.length == 0 && cancelList.length == 0) {
        this.initTasks = [];
      }
      for (var i = 0; i < dashboardlist.length; i++) {
        path = path + dashboardlist[i] + "&";
        console.log(dashboardlist[i]);
      }
      path = path.substring(0, path.length - 1);
      console.log(path);
      console.log(environment.backend + "/task/" + path);

      if(path && cancelList.length != 0)
      {
        axios.get(environment.backend + "/task/" + path, {}).then((res) => {
          console.log(environment.backend + "/task/2" + path);
          var tasks = res.data.tasks
          console.log(tasks)

          // get both dashboardList & cancelList
          for (var i = 0; i < dashboardlist.length; i++) {
            this.initTasks[i] = [];
            this.initTasks[i]['id'] = dashboardlist[i];
            this.initTasks[i]['name'] = localStorage.getItem(dashboardlist[i]);

            for (var q = 0; q < cancelList.length; q++) {
              let j = dashboardlist.length + cancelList.length - q - 1;
               this.initTasks[j] = [];
               this.initTasks[j]['id'] = cancelList[q];
               this.initTasks[j]['name'] = localStorage.getItem(cancelList[q]);
               this.initTasks[j]['status'] = 'CANCELLED';
               this.initTasks[j]['buttonString'] = 'Delete';
             }

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
        })
       console.log("I want to test");
      }
     else if(path && cancelList.length === 0)
     {
        axios.get(environment.backend + "/task/" + path, {}).then((res) => {
          console.log(environment.backend + "/task/2" + path);
          var tasks = res.data.tasks
          console.log(tasks)

          //only get dashboardList
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
        })
      }
     else if((!path) && cancelList) {
        //only get cancelList
        for (var i = 0; i < cancelList.length; i++) {
          this.initTasks[i] = [];
          this.initTasks[i]['id'] = cancelList[i];
          this.initTasks[i]['name'] = localStorage.getItem(cancelList[i]);
          this.initTasks[i]['status'] = 'CANCELLED'
          this.initTasks[i]['buttonString'] = "Delete"
        }
     }
     else if((!path) && (!cancelList))
     {
       //No task in the dashboardList, either in the cancelList
       console.log("No tasks to track now!");
     }
     else {
       console.log("Catch error!!!");
      }
        }
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
      }

  view(item) {
    if (item.status === "COMPLETED") {
      axios.get(environment.backend + '/dashboard/' + item.id, {}).then((res) => {
        const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
        this.LocalStorage.add(item.id + 'csv', blob).then((res) => {
          this.router.navigateByUrl("/dashboard_detail/" + item.id)
        })
        let dashboardlist = JSON.parse(localStorage['dashboardList']);
        for (var i = 0; i < dashboardlist.length; i++) {
          if (dashboardlist[i] === item.id) {
            dashboardlist.splice(i, 1)
            localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
            localStorage.removeItem(item.id);
          }
        }
      })
    } else {
      alert("cannot view a cancelled dashboard or uncompleted dashboard!")
    }
  }

  operation(task_id) {
    console.log("check init: "+ this.initTasks.length);
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
    let dashboardlist = JSON.parse(localStorage['dashboardList']);
    let cancelList = JSON.parse(localStorage['cancelList']);
    for (var i = 0; i < dashboardlist.length; i++) {

      //Check the selected task, if it exists in the dashboardlist?
      //If so, then push it into the cancelList
        if (dashboardlist[i] === task_id) {
               cancelList.push(task_id);
               localStorage.setItem("cancelList", JSON.stringify(cancelList));
      //Then remove it from the dashboardList
          dashboardlist.splice(i, 1)
          localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
          localStorage.removeItem(task_id);
            // request '/cancel' endpoint to delete the task in the back-end
           axios.delete(environment.backend + '/cancel/' + task_id, {}).then((res) => {
             this.router.navigateByUrl("/dashboard")
             //this.updateTask();
             console.log("Use Cancel tasks success!")
           })
        }
      }
    }

  deleteDashboard(task_id) {
    //Delete will be divided into two parts:
    //1. Delete a completed task (refers to front-end and back-end)
    //2. Delete a cancelled task (refers to front-end only)
    let dashboardlist = JSON.parse(localStorage['dashboardList']);
    let cancelList = JSON.parse(localStorage['cancelList']);

    for (var i = 0; i < dashboardlist.length; i++) {
      if (dashboardlist[i] === task_id) {
        dashboardlist.splice(i, 1)
        localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
        localStorage.removeItem(task_id);
        // Apply '/cancel' endpoint to delete the task in the worker node
        axios.delete(environment.backend + '/cancel/' + task_id, {}).then((res) => {
          this.router.navigateByUrl("/dashboard")
          //this.updateTask();
          console.log("Cancel tasks success!");
        });
      }
    }
    for(var j = 0; j < cancelList.length; j++) {
    if(cancelList[j] === task_id)
        {
          cancelList.splice(j,1);
          localStorage.setItem("cancelList", JSON.stringify(cancelList));
          localStorage.removeItem(task_id);
          //DO NOT apply 'cancel' endpoint here!
          this.router.navigateByUrl("/dashboard")
        //  this.updateTask();
          console.log("remove task from cancelList success!");
        }
      }
    }

  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }
}
