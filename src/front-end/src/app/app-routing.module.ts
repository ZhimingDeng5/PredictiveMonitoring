import { NgModule } from '@angular/core';
// import { CommonModule } from '@angular/common';
import {Routes, RouterModule} from '@angular/router';
import { PredictiveDashboardComponent } from './components/predictive-dashboard/predictive-dashboard.component';

import { PredictiveUploadComponent} from './components/predictive-upload/predictive-upload.component';
import {PredictiveDashboardDetailComponent} from './components/predictive-dashboard-detail/predictive-dashboard-detail.component';


const routes: Routes=[
  {path: 'create_dashboard', component: PredictiveUploadComponent},
  {path:'dashboard',component: PredictiveDashboardComponent},
  {path: 'dashboard_detail/:id', component:PredictiveDashboardDetailComponent}

];


@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [PredictiveUploadComponent, PredictiveDashboardComponent]
