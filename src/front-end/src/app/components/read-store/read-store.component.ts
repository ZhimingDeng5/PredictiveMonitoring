import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';
 import { Store } from '@ngrx/store';
 import { Dashboard } from './../../models/dashboard.model';
 import { AppState } from './../../app.state';
 import * as DashboardActions from './../../actions/dashboard.actions';


@Component({
  selector: 'app-read-store',
  templateUrl: './read-store.component.html',
  styleUrls: ['./read-store.component.css']
})
export class ReadStoreComponent implements OnInit {

  dashboards: Observable<Dashboard[]>;

  constructor(private store: Store<AppState>) { 
    this.dashboards = store.select('dashboard');
  }

  ngOnInit(): void {
    this.dashboards.forEach(element => console.log(element));
    
    
  }

}
