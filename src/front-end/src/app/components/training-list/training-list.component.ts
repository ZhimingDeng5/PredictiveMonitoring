import { Component, OnInit } from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';
import { NavigationEnd, Router } from '@angular/router';
import{ Predictor} from "../../predictor";

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
      // this.updateTask();
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
    this.LocalStorage.get("monitorList").then(res =>{
      if (res&&(<Set<string>>res).size>0) {
        let predictoridList:Set<string>=<Set<string>>res;
        console.log(predictoridList)
        for(let predictorid of predictoridList)
        {
          console.log(predictoridList)
          this.LocalStorage.get(predictorid).then(res1=>
          {
            if(res1)
            {
              let predictorList=<string[]>res1;
              console.log(parseInt(predictorList[2]))
              let predictor:Predictor= {
                name : predictorList[0],
                accuracy:"0.8",
                status:"processing",
                id:predictorList[3],
              }
              console.log(predictor);
              this.predictors.push(predictor);
            }
          })
        }
      } else {
        console.log("no predictor has been created")
      }
    })
  }

  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }



}
