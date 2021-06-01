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
  newTasks = [];

  constructor() { }

  ngOnInit(): void {

    axios.get("http://localhost:8000/tasks", {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
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
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then((res)=>{
      
    });
    }, 10000);
  }

}
