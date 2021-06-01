import { Component, OnInit } from '@angular/core';
import axios from 'axios';
import { timer } from 'rxjs';

@Component({
  selector: 'app-predictive-dashboard',
  templateUrl: './predictive-dashboard.component.html',
  styleUrls: ['./predictive-dashboard.component.css']
})
export class PredictiveDashboardComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {

    axios.get("http://localhost:8000/tasks", {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then((res)=>{
      console.log(res.data);
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
