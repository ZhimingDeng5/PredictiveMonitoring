import { Component, OnInit } from '@angular/core';
import { discardPeriodicTasks } from '@angular/core/testing';
import axios from 'axios';
import { timer } from 'rxjs';


 import { Observable } from 'rxjs';
 import { Store } from '@ngrx/store';
 import { Dashboard } from './../../models/dashboard.model';
 import { AppState } from './../../app.state';
 import * as DashboardActions from './../../actions/dashboard.actions';

@Component({
  selector: 'app-predictive-dashboard',
  templateUrl: './predictive-dashboard.component.html',
  styleUrls: ['./predictive-dashboard.component.css']
})
export class PredictiveDashboardComponent implements OnInit {
  length = 0;
  initTasks = [];
  newTasks = [];
  completed_task = [];

  // dashboards: Observable<Dashboard[]>;

  viewDetail() {
    alert('Hello');
  }
  // constructor(private store: Store<AppState>) { 
  //   this.dashboards = store.select('dashboard');
  // }

  constructor(private store: Store<AppState>) { }

  cancleDashboard(task_id){

    //alert(task_id);

    axios.delete("http://localhost:8000/cancel/"+task_id , {
    }).then((res)=>{  
      window.location.reload();
    });

  }

  if_download(dashboard_id){
    
  }

  addDashboard(csv, id) {
    this.store.dispatch(new DashboardActions.AddDashboard({csv: csv, id: id}) )
  }
  


  ngOnInit(): void {

    axios.get("http://localhost:8000/tasks", {
    }).then((res)=>{
      this.length = res.data.tasks.length;
      console.log(this.length);

      for(var i = 0; i<this.length; i++){
        this.initTasks[i] =[];
        this.initTasks[i]['id']=res.data.tasks[i].taskID;
        this.initTasks[i]['name']=res.data.tasks[i].name;
	      this.initTasks[i]['status']=res.data.tasks[i].status;
        this.addDashboard("test", this.initTasks[i]['id'])
        // if(this.initTasks[i]['status']=="COMPLETED"){
        //   let task_id = this.initTasks[i]['id']
        //   axios.get("http://localhost:8000/dashboard/"+this.initTasks[i]['id'],{            
        //   }).then((res)=>{

        //     this.addDashboard(res.data, task_id)
              
        //   })
        // }
      }

      
      
      
    });
    
    
    //polling
    // setInterval(()=>{
    //   axios.get("http://localhost:8000/tasks", {
    // }).then((res)=>{


    //   if(res.data.tasks.length != this.length){
        
    //     location.reload();

    //   }

    //   for(var i = 0; i<this.length; i++){
    //     if(res.data.tasks[i].id != this.initTasks[i]["id"] || res.data.tasks[i].status != this.initTasks[i]["status"]){

          
    //       location.reload();

    //     }
    //   }

    //   console.log("nothing updated");
      
    // });
    // }, 10000);
  }

}
