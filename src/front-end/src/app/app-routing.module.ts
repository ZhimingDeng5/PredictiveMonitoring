import { NgModule } from '@angular/core';
// import { CommonModule } from '@angular/common';
import {Routes, RouterModule} from '@angular/router';
import { PredictiveDashboardComponent } from './components/predictive-dashboard/predictive-dashboard.component';

import { PredictiveUploadComponent} from './components/predictive-upload/predictive-upload.component';
import {PredictiveDashboardDetailComponent} from './components/predictive-dashboard-detail/predictive-dashboard-detail.component';

import {PageNotFoundComponent} from "./components/PageNotFound/pagenotfound.component";
import {MonitorViewingComponent} from "./components/monitor-viewing/monitor-viewing.component";
import {CreateDashboardComponent} from "./components/create-dashboard/create-dashboard.component";
import {MonitorCreationComponent} from "./components/monitor-creation/monitor-creation.component";


const routes: Routes=[
  {path: 'create_dashboard', component: PredictiveUploadComponent},
  {path:'dashboard',component: PredictiveDashboardComponent},
  {path: 'dashboard_detail/:id', component:PredictiveDashboardDetailComponent},

  { path: 'monitor-viewing', component: MonitorViewingComponent },
  { path: 'create-dashboard', component: CreateDashboardComponent },
  { path: 'monitor-creation', component: MonitorCreationComponent },
  { path: '',   redirectTo: '/monitor-creation', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];


@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [PredictiveUploadComponent, PredictiveDashboardComponent]
