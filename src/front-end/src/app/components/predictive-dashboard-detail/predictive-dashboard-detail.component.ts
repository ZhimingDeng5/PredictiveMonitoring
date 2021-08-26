import { Component,  OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import axios from 'axios';
import {HttpClient} from "@angular/common/http";

import {Injectable} from "@angular/core";

@Component({
  selector: 'app-predictive-dashboard-detail',
  templateUrl: './predictive-dashboard-detail.component.html',
  styleUrls: ['./predictive-dashboard-detail.component.css']
})

@Injectable({
  providedIn: 'root'
})



export class PredictiveDashboardDetailComponent implements OnInit {
  id;
  initTasks = [];




  constructor(private _Activatedroute: ActivatedRoute,
              private _router: Router,
              private http: HttpClient
  ) {}


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

  downloadCSV (task_id)
  {
    this.http.get('http://localhost:8000/dashboard/' + task_id, {responseType: 'blob'}).subscribe(data => {
      const link = document.createElement('a');
      const blob = new Blob([data],{type: 'application/vnd.ms-excel'});

      link.setAttribute('href', window.URL.createObjectURL(blob));
      link.setAttribute('download',task_id + '.csv');
      link.style.visibility ='hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    })

  }




  ngOnDestroy() {
    this.sub.unsubscribe();
  }


}





