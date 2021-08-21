import { Component,  OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import axios from 'axios';

@Component({
  selector: 'app-predictive-dashboard-detail',
  templateUrl: './predictive-dashboard-detail.component.html',
  styleUrls: ['./predictive-dashboard-detail.component.css']
})
export class PredictiveDashboardDetailComponent implements OnInit {
   id;
   initTasks = [];
  
  constructor(private _Activatedroute:ActivatedRoute,
    private _router:Router){
}
  
  //constructor() { }
  sub;
  ngOnInit(): void {

      this.sub=this._Activatedroute.paramMap.subscribe(params => { 
      console.log(params);
      this.id = params.get('id'); 
      
      axios.get("http://localhost:8000/tasks/id", {
    }).then((res)=>{
      //num cases
      // this.length = res.data.tasks.length;
      // console.log(this.length);

      
      // for(var i = 0; i<this.length; i++){
      //   this.initTasks[i] =[];
      //   this.initTasks[i]['id']=res.data.tasks[i].taskID;
      //   this.initTasks[i]['name']=res.data.tasks[i].name;
	    //   this.initTasks[i]['status']=res.data.tasks[i].status;
      // }
      
      
    });




    });

  }
  
  ngOnDestroy() {
    this.sub.unsubscribe();
  }


}
