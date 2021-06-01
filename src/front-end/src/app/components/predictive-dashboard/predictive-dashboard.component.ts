import { Component, OnInit } from '@angular/core';
import { discardPeriodicTasks } from '@angular/core/testing';
import axios from 'axios';
import { timer } from 'rxjs';

@Component({
  selector: 'app-predictive-dashboard',
  templateUrl: './predictive-dashboard.component.html',
  styleUrls: ['./predictive-dashboard.component.css']
})
export class PredictiveDashboardComponent implements OnInit {
  length : any;
  initTasks = [];
  newLength : any;
  newTasks = [];

  constructor() { }

  ngOnInit(): void {

    axios.get("http://localhost:8000/tasks", {
    }).then((res)=>{
      this.length = res.data.tasks.length;
      console.log(this.length);

      
      for(var i = 0; i<this.length; i++){
        this.initTasks[i] =[];
        this.initTasks[i]['id']=res.data.tasks[i].id;
	      this.initTasks[i]['status']=res.data.tasks[i].status;
      }
      console.log(this.initTasks);

    });
    
    //polling
    setInterval(()=>{
      axios.get("http://localhost:8000/tasks", {
    }).then((res)=>{

      this.newLength = res.data.tasks.length;
      if(this.newLength!=length){
        location.reload();
      }

      for(var i = 0; i<this.length; i++){
        if(res.data.tasks[i].id != this.initTasks[i]["id"] || res.data.tasks[i].status != this.initTasks[i][status]){
          location.reload
        }
      }

      console.log("nothing");
    });
    }, 10000);
  }

}
