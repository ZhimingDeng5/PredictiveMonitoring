import { Component, OnInit } from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';
import { NavigationEnd, Router } from '@angular/router';
import{ Predictor} from "../../predictor";
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
  getpredictors()
  {
    let predictoridList = JSON.parse(localStorage['predictorList'])
    let predictoridCancle = localStorage.getItem("predictorCancle");
    let predictoridDelete = localStorage.getItem("predictorDelete");

    var path = "";
      //this.initTasks = [];
      for (var i = 0; i < predictoridList.length; i++) {
        path = path + predictoridList[i] + "&";
        console.log(predictoridList[i]);
      }
      path = path.substring(0, path.length - 1);

      axios.get(environment.backend + "/task/" + path, {}).then((res) =>{
        var tasks = res.data.tasks
        console.log(tasks)

        
        for (var i = 0; i < predictoridList.length; i++) {
          this.predictors[i] = [];
          this.predictors[i]['id'] = predictoridList[i];
          this.predictors[i]['name'] = JSON.parse(localStorage[predictoridList[i]])[0]
          console.log(JSON.parse(localStorage[predictoridList[i]]))
          for (var j = 0; j < tasks.length; j++) {
            if (tasks[j]['taskID'] === this.predictors[i]['id']) {
              this.predictors[i]['status'] = tasks[j]['status']
            }
          }
        }
      })
    }
  
  

  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }



}
