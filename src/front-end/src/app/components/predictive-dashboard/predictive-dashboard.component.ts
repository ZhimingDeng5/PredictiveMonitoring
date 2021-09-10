import {ChangeDetectorRef, Component, NgModule, OnInit} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router'
import { discardPeriodicTasks } from '@angular/core/testing';
import axios from 'axios';
import {catchError, timer} from 'rxjs';
import {Monitor} from "../../monitor";
import {MonitorService} from "../../monitor.service";
import { LocalStorageService } from '../../local-storage.service';
import { environment } from 'src/environments/environment';
import {keyframes} from "@angular/animations";

@Component({
  selector: 'app-predictive-dashboard',
  templateUrl: './predictive-dashboard.component.html',
  styleUrls: ['./predictive-dashboard.component.css']
})

export class PredictiveDashboardComponent implements OnInit {
  initTasks = [];
  selectedMonitor: Monitor;
  mySubscription: any;
  flag = 0;

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
    console.log("check flag mark: "+ this.flag);
    if (!localStorage['dashboardList']) {
      console.log("No tasks are generated now!!!");
    } else {
      var dashboardlist = JSON.parse(localStorage['dashboardList']);
      var cancelList = JSON.parse(localStorage['cancelList']);
      var completedList = JSON.parse(localStorage['completedList'])

      console.log("dashboard list check: " + dashboardlist)
      console.log("cancel list check: " + cancelList)
      console.log("completed list check: " + completedList)
      var path = "";
      //this.initTasks = [];
      for (var i = 0; i < dashboardlist.length; i++) {
        path = path + dashboardlist[i] + "&";
        console.log(dashboardlist[i]);
      }
      path = path.substring(0, path.length - 1);
     // console.log(path);
    //  console.log(environment.backend + "/task/" + path);

      //Case 1.1: Have both dashboardList & cancelList, but without completedList
      if(dashboardlist.length > 0 && cancelList.length > 0 && completedList.length === 0)
      {
            axios.get(environment.backend + "/task/" + path, {}).then((res) => {
              console.log(environment.backend + "/task/test: " + path);
              console.log("check init task here: " + this.initTasks);
              var tasks = res.data.tasks
              console.log(tasks)

              // get both dashboardList & cancelList
              // get dashboardList first
              for (var i = 0; i < dashboardlist.length; i++) {
                this.initTasks[i] = [];
                this.initTasks[i]['id'] = dashboardlist[i];
                this.initTasks[i]['name'] = localStorage.getItem(dashboardlist[i]);
                this.initTasks[i]['dashName'] = localStorage.getItem(dashboardlist[i] + "Name");

                for (var j = 0; j < tasks.length; j++) {
                  if (tasks[j]['taskID'] === this.initTasks[i]['id']) {
                    this.initTasks[i]['status'] = tasks[j]['status']
                  }
                }
                // Display different buttons according to 'status' of tasks
                if (this.initTasks[i]['status'] === "PROCESSING" || this.initTasks[i]['status'] === "QUEUED") {
                  this.initTasks[i]['buttonString'] = "Cancel"
                } else if (this.initTasks[i]['status'] === 'COMPLETED'){
                  this.initTasks[i]['buttonString'] = "Delete"
                  completedList.push(dashboardlist[i]);
                  localStorage['completedList'] = JSON.stringify(completedList);

                  axios.get(environment.backend + '/dashboard/' + this.initTasks[i]['id'], {}).then((res) => {
                    const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
                    this.LocalStorage.add(this.initTasks[i]['id'] + 'csv', blob).then((res) => {
                    })
                  })

                  dashboardlist.splice(i, 1)
                  localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
                  localStorage.removeItem(this.initTasks[i]['taskID']);
                }
              }
              // get cancelList then
              for (var q = 0; q < cancelList.length; q++) {
                let n = dashboardlist.length + cancelList.length - q - 1;
                this.initTasks[n] = [];
                this.initTasks[n]['id'] = cancelList[q];
                this.initTasks[n]['name'] = localStorage.getItem(cancelList[q]);    //monitor name
                this.initTasks[n]['dashName'] = localStorage.getItem(cancelList[q] + "Name");
                this.initTasks[n]['status'] = 'CANCELLED';
                this.initTasks[n]['buttonString'] = 'Delete';
              }
            })
        console.log("case 1.1 execute");
      }

      //Case 1.2: Have both dashboardList & cancelList, also with completedList
      else if(dashboardlist.length > 0 && cancelList.length > 0 && completedList.length > 0)
      {
        axios.get(environment.backend + "/task/" + path, {}).then((res) => {
          console.log(environment.backend + "/task/test: " + path);
          console.log("check init task here: " + this.initTasks);
          var tasks = res.data.tasks
          console.log(tasks)

          // get both dashboardList & cancelList, and also completedList
          // get dashboardList first
          for (var i = 0; i < dashboardlist.length; i++) {
            this.initTasks[i] = [];
            this.initTasks[i]['id'] = dashboardlist[i];
            this.initTasks[i]['name'] = localStorage.getItem(dashboardlist[i]);
            this.initTasks[i]['dashName'] = localStorage.getItem(dashboardlist[i] + "Name");

            for (var j = 0; j < tasks.length; j++) {
              if (tasks[j]['taskID'] === this.initTasks[i]['id']) {
                this.initTasks[i]['status'] = tasks[j]['status']
              }
            }
            // Display different buttons according to 'status' of tasks
            if (this.initTasks[i]['status'] === "PROCESSING" || this.initTasks[i]['status'] === "QUEUED") {
              this.initTasks[i]['buttonString'] = "Cancel"
            } else if (this.initTasks[i]['status'] === 'COMPLETED'){
              this.initTasks[i]['buttonString'] = "Delete"
              completedList.push(dashboardlist[i]);
              localStorage['completedList'] = JSON.stringify(completedList);

              axios.get(environment.backend + '/dashboard/' + this.initTasks[i]['id'], {}).then((res) => {
                const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
                this.LocalStorage.add(this.initTasks[i]['id'] + 'csv', blob).then((res) => {
                })
              })

              dashboardlist.splice(i, 1)
              localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
              localStorage.removeItem(this.initTasks[i]['taskID']);
            }
          }

          // get cancelList then
          for (var q = 0; q < cancelList.length; q++) {
            let n = dashboardlist.length + cancelList.length - q - 1;
            this.initTasks[n] = [];
            this.initTasks[n]['id'] = cancelList[q];
            this.initTasks[n]['name'] = localStorage.getItem(cancelList[q]);    //monitor name
            this.initTasks[n]['dashName'] = localStorage.getItem(cancelList[q] + "Name");
            this.initTasks[n]['status'] = 'CANCELLED';
            this.initTasks[n]['buttonString'] = 'Delete';
          }

          // get completedList finally
          for (var k = 0; k < completedList.length; k++) {
            let n = dashboardlist.length + cancelList.length + completedList.length - k - 1;
            this.initTasks[n] = [];
            this.initTasks[n]['id'] = completedList[k];
            this.initTasks[n]['name'] = localStorage.getItem(completedList[k]);    //monitor name
            this.initTasks[n]['dashName'] = localStorage.getItem(completedList[k] + "Name");
            this.initTasks[n]['status'] = 'COMPLETED';
            this.initTasks[n]['buttonString'] = 'Delete';
          }
        })
        console.log("case 1.2 execute");
      }


      //Case 2.1: Only have dashboardList
     else if(dashboardlist.length != 0 && cancelList.length === 0 && completedList.length === 0) {
          axios.get(environment.backend + "/task/" + path, {}).then((res) => {
            console.log(environment.backend + "/task/2" + path);
            var tasks = res.data.tasks
            console.log(tasks)

            //only get dashboardList
            for (var i = 0; i < dashboardlist.length; i++) {
              this.initTasks[i] = [];
              this.initTasks[i]['id'] = dashboardlist[i];
              this.initTasks[i]['name'] = localStorage.getItem(dashboardlist[i]);
              this.initTasks[i]['dashName'] = localStorage.getItem(dashboardlist[i] + "Name");

              for (var j = 0; j < tasks.length; j++) {
                if (tasks[j]['taskID'] === this.initTasks[i]['id']) {
                  this.initTasks[i]['status'] = tasks[j]['status']
                }
              }
              // Display different buttons according to 'status' of tasks
              if (this.initTasks[i]['status'] === "PROCESSING" || this.initTasks[i]['status'] === "QUEUED") {
                this.initTasks[i]['buttonString'] = "Cancel"
              } else if (this.initTasks[i]['status'] === 'COMPLETED') {
                this.initTasks[i]['buttonString'] = "Delete"
                completedList.push(dashboardlist[i]);
                localStorage['completedList'] = JSON.stringify(completedList);

                axios.get(environment.backend + '/dashboard/' + this.initTasks[i]['id'], {}).then((res) => {
                  const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
                  this.LocalStorage.add(this.initTasks[i]['id'] + 'csv', blob).then((res) => {
                  })
                })

                dashboardlist.splice(i, 1)
                localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
                localStorage.removeItem(this.initTasks[i]['taskID']);
              }
            }
          })
        console.log("case 2.1 execute");
      }

      //Case 2.2 : Only have completedList before, but now coming a dashboardList
      else if(dashboardlist.length > 0 && cancelList.length === 0 && completedList.length > 0 ) {
        axios.get(environment.backend + "/task/" + path, {}).then((res) => {
          console.log(environment.backend + "/task/2" + path);
          var tasks = res.data.tasks
          console.log(tasks)

          //only get dashboardList
          for (var i = 0; i < dashboardlist.length; i++) {
            this.initTasks[i] = [];
            this.initTasks[i]['id'] = dashboardlist[i];
            this.initTasks[i]['name'] = localStorage.getItem(dashboardlist[i]);
            this.initTasks[i]['dashName'] = localStorage.getItem(dashboardlist[i] + "Name");

            for (var j = 0; j < tasks.length; j++) {
              if (tasks[j]['taskID'] === this.initTasks[i]['id']) {
                this.initTasks[i]['status'] = tasks[j]['status']
              }
            }
            // Display different buttons according to 'status' of tasks
            if (this.initTasks[i]['status'] === "PROCESSING" || this.initTasks[i]['status'] === "QUEUED") {
              this.initTasks[i]['buttonString'] = "Cancel"
            } else if (this.initTasks[i]['status'] === 'COMPLETED') {
              this.initTasks[i]['buttonString'] = "Delete"
              completedList.push(dashboardlist[i]);
              localStorage['completedList'] = JSON.stringify(completedList);

              axios.get(environment.backend + '/dashboard/' + this.initTasks[i]['id'], {}).then((res) => {
                const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
                this.LocalStorage.add(this.initTasks[i]['id'] + 'csv', blob).then((res) => {
                })
              })

              dashboardlist.splice(i, 1)
              localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
              localStorage.removeItem(this.initTasks[i]['taskID']);
            }
          }

       // then get completedList
          for (var j = 0; j < completedList.length; j++) {
            let n = completedList.length + dashboardlist.length - j - 1;
            this.initTasks[n] = [];
            this.initTasks[n]['id'] = completedList[j];
            this.initTasks[n]['name'] = localStorage.getItem(completedList[j]);    //monitor name
            this.initTasks[n]['dashName'] = localStorage.getItem(completedList[j] + "Name");
            this.initTasks[n]['status'] = 'COMPLETED';
            this.initTasks[n]['buttonString'] = 'Delete';
          }
        })
        console.log("case 2.2 execute");
      }


     //Case 3.1 : Only have cancelList
     else if( dashboardlist.length === 0 && cancelList.length > 0 && completedList.length === 0 ) {
        //only get cancelList
        for (var i = 0; i < cancelList.length; i++) {
          this.initTasks[i] = [];
          this.initTasks[i]['id'] = cancelList[i];
          this.initTasks[i]['name'] = localStorage.getItem(cancelList[i]);
          this.initTasks[i]['dashName'] = localStorage.getItem(cancelList[i]+"Name");
          this.initTasks[i]['status'] = 'CANCELLED'
          this.initTasks[i]['buttonString'] = "Delete"
        }
        console.log("case 3.1 execute");
     }

      //Case 3.2 :  Have cancelList and completedList
      else if( dashboardlist.length === 0 && cancelList.length > 0 && completedList.length > 0) {
        // get cancelList
        for (var i = 0; i < cancelList.length; i++) {
          this.initTasks[i] = [];
          this.initTasks[i]['id'] = cancelList[i];
          this.initTasks[i]['name'] = localStorage.getItem(cancelList[i]);
          this.initTasks[i]['dashName'] = localStorage.getItem(cancelList[i] + "Name");
          this.initTasks[i]['status'] = 'CANCELLED'
          this.initTasks[i]['buttonString'] = "Delete"
        }
        // then get completedList
        for (var q = 0; q < completedList.length; q++) {
          let n = completedList.length + cancelList.length - q - 1;
          this.initTasks[n] = [];
          this.initTasks[n]['id'] = completedList[q];
          this.initTasks[n]['name'] = localStorage.getItem(completedList[q]);    //monitor name
          this.initTasks[n]['dashName'] = localStorage.getItem(completedList[q] + "Name");
          this.initTasks[n]['status'] = 'COMPLETED';
          this.initTasks[n]['buttonString'] = 'Delete';
        }
        console.log("case 3.2 execute");
      }

     //Case 4: Nothing in dashboardList nor cancelList nor completedList
     else if(dashboardlist.length === 0 && cancelList.length === 0 && completedList.length === 0)
     {
       //No task in the dashboardList, either in the cancelList, nor in the completedList
       console.log("No tasks to track now!");
       console.log("case 4 execute");
     }

     //Case 5: ONLY completed tasks in the page
        else if(dashboardlist.length === 0 && completedList.length > 0)
      {
        for (var i = 0; i < completedList.length; i++) {
          this.initTasks[i] = [];
          this.initTasks[i]['id'] = completedList[i];
          this.initTasks[i]['name'] = localStorage.getItem(completedList[i]);
          this.initTasks[i]['dashName'] = localStorage.getItem(completedList[i]+"Name");
          this.initTasks[i]['status'] = 'COMPLETED'
          this.initTasks[i]['buttonString'] = "Delete"
        }
        console.log("case 5 execute");
      }

     //Error
     else {
       console.log("Catch error!!!");
      }
        }
      }

  view(item) {
    if (item.status === "COMPLETED") {
      localStorage.setItem("dashnamelist",item.dashName);
      this.router.navigateByUrl("/dashboard_detail/" + item.id)
     /* axios.get(environment.backend + '/dashboard/' + item.id, {}).then((res) => {
        const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});
        this.LocalStorage.add(item.id + 'csv', blob).then((res) => {
          this.router.navigateByUrl("/dashboard_detail/" + item.id)
        })*/
        /* let completedList = JSON.parse(localStorage['completedList']);
        for (var i = 0; i < completedList.length; i++) {
          if (completedList[i] === item.id) {
            completedList.splice(i, 1)
            localStorage.setItem("completedList", JSON.stringify(completedList));
            localStorage.removeItem(item.id);
            localStorage.removeItem(item.id+"Name")*/
       //   }
      //  }
    } else {
      alert("cannot view a cancelled dashboard or uncompleted dashboard!")
    }
  }

  operation(Task) {
    console.log("check init~~~~~~~~~~~: "+ this.initTasks.length);
         if(Task['buttonString'] === 'Delete')
         {
           this.deleteDashboard(Task['id']);
           console.log("use delete now!");
         }
         else if(Task['buttonString'] === 'Cancel')
         {
           this.cancelDashboard(Task['id']);
           console.log("use cancel now!");
         }
  }

  cancelDashboard(task_id) {
    let dashboardlist = JSON.parse(localStorage['dashboardList']);
    let cancelList = JSON.parse(localStorage['cancelList']);
    for (var i = 0; i < dashboardlist.length; i++) {

      //Check the selected task, if it exists in the dashboardlist?
      //If so, then push it into the cancelList

        if (dashboardlist[i] === task_id ) {
               cancelList.push(task_id);
               localStorage.setItem("cancelList", JSON.stringify(cancelList));

      //Then remove it from the dashboardList
          dashboardlist.splice(i, 1)
          localStorage.setItem("dashboardList", JSON.stringify(dashboardlist));
          localStorage.removeItem(task_id);
          // localStorage.removeItem(task_id+"Name")
            // request '/cancel' endpoint to delete the task in the back-end
           axios.post(environment.backend + '/cancel/' + task_id, {}).then((res) => {
             //this.router.navigateByUrl("/dashboard")
             this.updateTask();
             console.log("Use Cancel tasks success!")

           })
        }
      }
    }

  deleteDashboard(task_id) {
    //Delete will be divided into two parts:
    //1. Delete a completed task (refers to front-end and back-end)
    //2. Delete a cancelled task (refers to front-end only)
  // let dashboardlist = JSON.parse(localStorage['dashboardList']);
    let completedList = JSON.parse(localStorage['completedList']);
    let cancelList = JSON.parse(localStorage['cancelList']);

    for (var i = 0; i < completedList.length; i++) {
      if (completedList[i] === task_id) {
        completedList.splice(i, 1)
        localStorage.setItem("dashboardList", JSON.stringify(completedList));
        localStorage.removeItem(task_id);

        this.updateTask();
        // localStorage.removeItem(task_id+"Name")
        // Apply '/cancel' endpoint to delete the task in the worker node
     /*   axios.post(environment.backend + '/cancel/' + task_id, {}).then((res) => {
          //this.router.navigateByUrl("/dashboard")
          this.updateTask();
          console.log("Cancel tasks success!");
        });*/
      }
    }
    for(var j = 0; j < cancelList.length; j++) {
    if(cancelList[j] === task_id)
        {
          cancelList.splice(j,1);
          localStorage.setItem("cancelList", JSON.stringify(cancelList));
          localStorage.removeItem(task_id);
          localStorage.removeItem(task_id+"Name")
          //DO NOT apply 'cancel' endpoint here!
          //this.router.navigateByUrl("/dashboard")
          this.updateTask();
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
