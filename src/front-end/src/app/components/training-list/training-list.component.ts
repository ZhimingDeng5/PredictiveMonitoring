import { Component, OnInit } from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';
import { NavigationEnd, Router } from '@angular/router';
import { Predictor } from "../../predictor";
import axios from 'axios';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-training-list',
  templateUrl: './training-list.component.html',
  styleUrls: ['./training-list.component.css']
})
export class TrainingListComponent implements OnInit {
  predictors = [];
  mySubscription: any;

  constructor(
    public LocalStorage: LocalStorageService,
    private router: Router) {
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
    this.getpredictors();

    //polling
    let interval = setInterval(() => {
      let url = location.href
      let site = url.lastIndexOf("\/");
      let loc = url.substring(site + 1, url.length);
      if (loc == "training-list") {
        this.getpredictors();
        console.log("refresh")
      } else {
        clearInterval(interval);
      }
    }, 5000);






  }


  //here I assume the data structure in indexdb is same as monitor
  //so in index db there is a predictor id list
  //and the list of all real predictor.
  getpredictors() {

    if (localStorage.getItem('predictorCancle') == null) {
      var mylist1 = []
      localStorage['predictorCancle'] = JSON.stringify(mylist1);
    }
    if (localStorage.getItem('predictorComplete') == null) {
      var mylist2 = []
      localStorage['predictorComplete'] = JSON.stringify(mylist2);
    }

    let predictoridList = JSON.parse(localStorage['predictorList'])
    let predictoridCancle = JSON.parse(localStorage.getItem("predictorCancle"));
    let predictoridComplete = JSON.parse(localStorage.getItem("predictorComplete"));




    console.log(predictoridCancle)
    console.log(predictoridCancle.length)
    var i = 0
    if (predictoridCancle.length != 0) {
      for (i; i < predictoridCancle.length; i++) {
        this.predictors[i] = [];
        this.predictors[i]['id'] = predictoridCancle[i];
        this.predictors[i]['name'] = JSON.parse(localStorage[predictoridCancle[i]])[0]
        this.predictors[i]['status'] = "cancled"
        this.predictors[i]['buttonString'] = "Delete"

      }
    }



    var path = "";
    //this.initTasks = [];
    for (var j = 0; j < predictoridList.length; j++) {
      path = path + predictoridList[j] + "&";
      console.log(predictoridList[j]);
    }
    path = path.substring(0, path.length - 1);
    console.log(path)
    console.log(i)
    if (path != "") {
      axios.get(environment.backend + "/task/" + path, {}).then((res) => {
        var tasks = res.data.tasks
        console.log(tasks)


        for (var j = 0; j < predictoridList.length; j++) {
          this.predictors[i] = [];
          this.predictors[i]['id'] = predictoridList[j];
          this.predictors[i]['name'] = JSON.parse(localStorage[predictoridList[j]])[0]
          for (var k = 0; k < tasks.length; k++) {
            if (tasks[k]['taskID'] === this.predictors[i]['id']) {
              this.predictors[i]['status'] = tasks[k]['status']
            }
          }
          if (this.predictors[i]['status'] === "PROCESSING" || this.predictors[i]['status'] === "QUEUED") {
            this.predictors[i]['buttonString'] = "Cancel"
          } else if (this.predictors[i]['status'] === 'COMPLETED') {
            this.predictors[i]['buttonString'] = "Delete"
            // predictoridComplete = JSON.parse(localStorage['predictorComplete']);
            var flag = 0
            for (var m = 0; m < predictoridComplete.length; m++) {
              if (predictoridComplete[m] === this.predictors[i]['id']) {
                flag = 1
              }
            }
            if (flag === 0) {
              console.log("flag is 0 now")
              predictoridComplete.push(this.predictors[i]['id']);
              localStorage.setItem("predictorComplete", JSON.stringify(predictoridComplete));

            }



          }
          i = i + 1
        }


      })
    }



  }



  operation(Task) {
    // console.log("check init~~~~~~~~~~~: "+ this.predictors.length);
    //      if(Task['buttonString'] === 'Delete')
    //      {
    //        this.deletePredictor(Task['id']);
    //        console.log("use delete now!");
    //      }
    if (Task['buttonString'] === 'Cancel') {
      this.cancelPredictor(Task['id']);
      console.log("use cancel now!");
    }else if(Task['buttonString'] === 'Delete') {
      this.deletePredictor(Task['id']);
      console.log("use delete now!");
    }
  }



  deletePredictor(task_id) {
    //Delete will be divided into two parts:
    //1. Delete a completed task (refers to front-end and back-end)
    //2. Delete a cancelled task (refers to front-end only)
    let completedList = JSON.parse(localStorage['predictorComplete']);
    let cancelList = JSON.parse(localStorage['predictorCancle']);
    let predictorlist = JSON.parse(localStorage['predictorList']);

    for (var j = 0; j < cancelList.length; j++) {
      if (cancelList[j] === task_id) {
        cancelList.splice(j, 1);
        localStorage.setItem("predictorCancle", JSON.stringify(cancelList));
        localStorage.removeItem(task_id);
        console.log("remove task from cancelList success!");
        this.router.navigateByUrl('/training-list');
      }
    }
    // this.getpredictors();


    for (var j = 0; j < predictorlist.length; j++) {
      if (predictorlist[j] === task_id) {
        predictorlist.splice(j, 1);
        localStorage.setItem("predictorList", JSON.stringify(predictorlist));

        console.log("remove task from predictorlist success!");
      }
    }

    // for complete
    for (var i = 0; i < completedList.length; i++) {
      if (completedList[i] === task_id) {
        completedList.splice(i, 1)
        localStorage.setItem("predictorComplete", JSON.stringify(completedList));
        localStorage.removeItem(task_id);
        axios.post(environment.backend + '/cancel/' + task_id, {}).then((res) => {
          this.getpredictors();
          console.log("Use delete tasks success!")
          this.router.navigateByUrl('/training-list');

        })
      }
    }



  }


  cancelPredictor(task_id) {

    if (localStorage.getItem('predictorCancle') == null) {
      var mylist1 = []
      localStorage['predictorCancle'] = JSON.stringify(mylist1);
    }


    // you can only cancel a 'QUEUED' or 'PROCESSING' task
    let predictorlist = JSON.parse(localStorage['predictorList']);
    let cancelList = JSON.parse(localStorage['predictorCancle']);
    cancelList.push(task_id);
    localStorage.setItem("predictorCancle", JSON.stringify(cancelList));
    for (var i = 0; i < predictorlist.length; i++) {

      if (predictorlist[i] === task_id) {

        //Then remove it from the predictorList
        predictorlist.splice(i, 1)
        localStorage.setItem("predictorList", JSON.stringify(predictorlist));
        // localStorage.removeItem(task_id);
        axios.post(environment.backend + '/cancel/' + task_id, {}).then((res) => {
          this.getpredictors();
          console.log("Use Cancel tasks success!")

        })
      }
    }
  }






  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }



}
