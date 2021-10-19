import { Component, OnInit } from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';
import { NavigationEnd, Router } from '@angular/router';
import { Predictor } from "../../predictor";
import axios from 'axios';
import { environment } from 'src/environments/environment';
import * as JSZip from 'jszip';
import { timeout } from "rxjs";
import { MatDialog } from '@angular/material/dialog';
import { PopupComponent } from '../popup/popup.component';
import { Message } from '@angular/compiler/src/i18n/i18n_ast';

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
    private router: Router,
    private dialogRef: MatDialog) {
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
        this.predictors[i]['status'] = "CANCELLED"
        this.predictors[i]['buttonString'] = "Delete"

      }
    }

    if (predictoridComplete.length != 0) {
      for (var j = 0; j < predictoridComplete.length; j++) {
        this.predictors[i] = [];
        this.predictors[i]['id'] = predictoridComplete[j];
        this.predictors[i]['name'] = JSON.parse(localStorage[predictoridComplete[j]])[0]
        this.predictors[i]['status'] = "COMPLETED"
        this.predictors[i]['buttonString'] = "Delete"
        i = i + 1

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
      axios.get(environment.training_backend + "/task/" + path, {}).then((res) => {
        var tasks = res.data.tasks
        console.log(tasks)


        for (var j = 0; j < predictoridList.length; j++) {
          this.predictors[i] = [];
          this.predictors[i]['id'] = predictoridList[j];
          this.predictors[i]['name'] = JSON.parse(localStorage[predictoridList[j]])[0]
          for (var k = 0; k < tasks.length; k++) {
            if (tasks[k]['taskID'] === this.predictors[i]['id']) {
              this.predictors[i]['status'] = tasks[k]['status']
              console.log(this.predictors[i]['status'])
              if(this.predictors[i]['status']==="ERROR"){
                localStorage.setItem(this.predictors[i]['id']+"ERROR", tasks[k]['error_msg']);
                console.log(this.predictors[i]['id']+"ERROR")
                console.log(tasks[k]['error_msg'])

              }
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

              this.download_data(this.predictors[i])
              predictoridList.splice(j, 1);
              localStorage.setItem("predictorList", JSON.stringify(predictoridList));
              i = i - 1

            }

          } else if (this.predictors[i]['status'] === 'ERROR') {
            this.predictors[i]['buttonString'] = "Delete"
            
          }
          i = i + 1
        }


      })
    }



  }



  operation(Task) {

    if (Task['buttonString'] === 'Cancel') {
      this.cancelPredictor(Task['id']);
      console.log("use cancel now!");
    } else if (Task['buttonString'] === 'Delete') {
      this.deletePredictor(Task);
      console.log("use delete now!");
    }
  }



  deletePredictor(task) {
    //Delete will be divided into two parts:
    //1. Delete a completed task (refers to front-end and back-end)
    //2. Delete a cancelled task (refers to front-end only)
    let completedList = JSON.parse(localStorage['predictorComplete']);
    let cancelList = JSON.parse(localStorage['predictorCancle']);
    let predictorlist = JSON.parse(localStorage['predictorList']);

    for (var j = 0; j < cancelList.length; j++) {
      if (cancelList[j] === task["id"]) {
        cancelList.splice(j, 1);
        localStorage.setItem("predictorCancle", JSON.stringify(cancelList));
        localStorage.removeItem(task["id"]);
        console.log("remove task from cancelList success!");
        this.router.navigateByUrl('/training-list');
      }
    }
    // this.getpredictors();
    for (var j = 0; j < predictorlist.length; j++) {
      if (predictorlist[j] === task["id"]) {
        predictorlist.splice(j, 1);
        localStorage.setItem("predictorList", JSON.stringify(predictorlist));

        if (task["status"] === "ERROR") {
          axios.post(environment.training_backend + '/cancel/' + task["id"], {}).then((res) => {
            this.getpredictors();
            this.router.navigateByUrl('/training-list');
            console.log("Error cancle sucessfully");
            console.log(res);
          })

        }
        console.log("remove task from predictorlist success!");
      }
    }

    // for complete
    for (var i = 0; i < completedList.length; i++) {
      if (completedList[i] === task["id"]) {
        completedList.splice(i, 1)
        localStorage.setItem("predictorComplete", JSON.stringify(completedList));
        localStorage.removeItem(task["id"]);

        this.router.navigateByUrl('/training-list');
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
        axios.post(environment.training_backend + '/cancel/' + task_id, {}).then((res) => {
          this.getpredictors();
          console.log("Use Cancel tasks success!")

        })
      }
    }
  }


  viewPredictor(item) {
    if(item.status === 'ERROR'){
      let error_message=localStorage.getItem(item.id+"ERROR")
      this.dialogRef.open(PopupComponent,{
        data:{
          id:item.id,
          message: error_message
        }
      });


    }else{
      this.router.navigateByUrl("/training-list-detail/" + item.id)
    }
    
  }

  download_data(item) {
    if (item.status === 'COMPLETED') {

      //  let completedList = JSON.parse(localStorage['predictorComplete']);
      //  let predictorlist = JSON.parse(localStorage['predictorList']);
      //  for (var j = 0; j < predictorlist.length; j++) {
      //    if (predictorlist[j] === item['id']) {
      //      predictorlist.splice(j, 1);
      //      localStorage.setItem("predictorList", JSON.stringify(predictorlist));
      //      console.log("remove task from predictorlist success!");
      //    }
      //  }

      // for complete
      //  for (var i = 0; i < completedList.length; i++) {
      //    if (completedList[i] === item['id']) {
      //      completedList.splice(i, 1)
      //      localStorage.setItem("predictorComplete", JSON.stringify(completedList));

      //    }
      //  }
      //  localStorage.removeItem(item['id']);


      axios.get(environment.training_backend + '/predictor/' + item.id, { responseType: 'blob' }).then((res) => {

        /* const link = document.createElement('a');*/
        const file = new Blob([res.data], { type: 'application/x-zip-compressed' });

        JSZip.loadAsync(file).then(function (zip) {
          return zip.file(item.id + "-detailed.csv").async("string");
        }).then(text => {
          localStorage.setItem(item.id + "-detailed-csv", text)
          console.log(text);
          JSZip.loadAsync(file).then(function (zip) {
            return zip.file(item.id + "-feat-importance.csv").async("string");
          }).then(text2 => {
            localStorage.setItem(item.id + "-feat-importance-csv", text2);
            console.log(text2);
            JSZip.loadAsync(file).then(function (zip) {
              return zip.file(item.id + "-validation.csv").async("string");
            }).then(text3 => {
              localStorage.setItem(item.id + "-validation-csv", text3);
              console.log(text3);
              JSZip.loadAsync(file).then(function (zip) {
                return zip.file("config.json").async("string");
              }).then(text4 => {
                localStorage.setItem(item.id + "-config-json", text4);
                //  this.LocalStorage.add(item.id + "-config-json", text4).then((res) =>{
                //  });

                console.log(text4);
                // this.router.navigateByUrl("/training-list-detail/" + item.id);
              })
            })
          })
        })

        /*    link.setAttribute('href', window.URL.createObjectURL(file));
            link.setAttribute('download', item.id + '.zip');
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);*/

        this.LocalStorage.add(item.id + 'zip', file).then((res) => {
        })

        //   this.router.navigateByUrl("/training-list-detail/" + item.id);
      })
    }
  }


  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }



}
