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
  taskArray = new Array();
  arr = [];

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
        this.arr[i] =[];
        this.arr[i]['id']=res.data.tasks[i].id;
	      this.arr[i]['status']=res.data.tasks[i].status;
      }
      console.log(this.arr);

    });

    const obs$ = timer(10000, 10000);
    obs$.subscribe(

      //put get all dashboards command here.

      //if(number of dashboards.id != current numbers of dashboards id){
      //  refresh the page with new dashboards.
      //}


      (d)=>{
      console.log(d);
    }

    )
  }

}
