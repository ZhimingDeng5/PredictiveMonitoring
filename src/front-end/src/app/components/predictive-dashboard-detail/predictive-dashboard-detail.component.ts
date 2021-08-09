import { Component,  OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-predictive-dashboard-detail',
  templateUrl: './predictive-dashboard-detail.component.html',
  styleUrls: ['./predictive-dashboard-detail.component.css']
})
export class PredictiveDashboardDetailComponent implements OnInit {
   id;
  
  constructor(private _Activatedroute:ActivatedRoute,
    private _router:Router){
}
  
  //constructor() { }
   sub;
  ngOnInit(): void {

      this.sub=this._Activatedroute.paramMap.subscribe(params => { 
      console.log(params);
      this.id = params.get('id');    
    });

  }
  
  ngOnDestroy() {
    this.sub.unsubscribe();
  }


}
