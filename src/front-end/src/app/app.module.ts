import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
// import { PredictiveDashboardComponent } from './components/predictive-dashboard/predictive-dashboard.component';
// import { PredictiveUploadComponent } from './components/predictive-upload/predictive-upload.component';

import { AppRoutingModule,routingComponents } from './app-routing.module';
import { PredictiveDashboardDetailComponent } from './components/predictive-dashboard-detail/predictive-dashboard-detail.component';

import { AngularFileUploaderModule } from 'angular-file-uploader';
import { MonitorViewingComponent } from './components/monitor-viewing/monitor-viewing.component';
import { PageNotFoundComponent } from './components/PageNotFound/pagenotfound.component';
import { CreateDashboardComponent } from './components/create-dashboard/create-dashboard.component';
import { MonitorCreationComponent } from './components/monitor-creation/monitor-creation.component';
import {ReactiveFormsModule} from "@angular/forms";




@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    // PredictiveDashboardComponent,
    // PredictiveUploadComponent
    routingComponents,
    PredictiveDashboardDetailComponent,
    MonitorViewingComponent,
    PageNotFoundComponent,
    CreateDashboardComponent,
    MonitorCreationComponent,

  ],
  imports: [
    BrowserModule,
    AngularFileUploaderModule,
    AppRoutingModule,
    ReactiveFormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
