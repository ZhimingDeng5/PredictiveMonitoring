import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {PageNotFoundComponent} from "./components/PageNotFound/pagenotfound.component";
import {MonitorViewingComponent} from "./components/monitor-viewing/monitor-viewing.component";
import {CreateDashboardComponent} from "./components/create-dashboard/create-dashboard.component";
import {MonitorCreationComponent} from "./components/monitor-creation/monitor-creation.component";
import { PredictiveUploadComponent} from './components/predictive-upload/predictive-upload.component';
import {PredictiveDashboardDetailComponent} from './components/predictive-dashboard-detail/predictive-dashboard-detail.component';


const appRoutes: Routes = [
  { path: 'monitor-viewing', component: MonitorViewingComponent },
  { path: 'create-dashboard', component: CreateDashboardComponent },
  { path: 'monitor-creation', component: MonitorCreationComponent },
  
  { path: '',   redirectTo: '/monitor-creation', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent },
  
  {path: 'create_dashboard', component: PredictiveUploadComponent},
  {path:'dashboard',component: PredictiveDashboardComponent},
  {path: 'dashboard_detail/:id', component:PredictiveDashboardDetailComponent}
  





// const routes: Routes=[
//   {path: 'create_dashboard', component: PredictiveUploadComponent},
//   {path:'dashboard',component: PredictiveDashboardComponent},
//   {path: 'dashboard_detail/:id', component:PredictiveDashboardDetailComponent}

];
@NgModule({
  imports: [
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    )
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {}
