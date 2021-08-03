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
  length = 0;
  initTasks = [];
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
        this.initTasks[i]['name']=res.data.tasks[i].name;
	      this.initTasks[i]['status']=res.data.tasks[i].status;
      }
      
      
    });
    
    
    //polling
    setInterval(()=>{
      axios.get("http://localhost:8000/tasks", {
    }).then((res)=>{


      if(res.data.tasks.length != this.length){
        
        location.reload();

      }

      for(var i = 0; i<this.length; i++){
        if(res.data.tasks[i].id != this.initTasks[i]["id"] || res.data.tasks[i].status != this.initTasks[i]["status"]){

          location.reload();

        }
      }

      console.log("nothing updated");
      
    });
    }, 10000);
  }

}
