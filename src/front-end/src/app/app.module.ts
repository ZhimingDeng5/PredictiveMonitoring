import { NgModule } from '@angular/core';
import {LocationStrategy, HashLocationStrategy} from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';

import { PredictiveDashboardComponent } from './components/predictive-dashboard/predictive-dashboard.component';
import { PredictiveUploadComponent } from './components/predictive-upload/predictive-upload.component';
import { AngularFileUploaderModule } from 'angular-file-uploader';
import { MonitorViewingComponent } from './components/monitor-viewing/monitor-viewing.component';
import { PageNotFoundComponent } from './components/PageNotFound/pagenotfound.component';
import { CreateDashboardComponent } from './components/create-dashboard/create-dashboard.component';
import { MonitorCreationComponent } from './components/monitor-creation/monitor-creation.component';
import {ReactiveFormsModule} from "@angular/forms";
import { MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
// import { PredictiveUploadComponent } from './components/predictive-upload/predictive-upload.component';
import { PredictiveDashboardDetailComponent } from './components/predictive-dashboard-detail/predictive-dashboard-detail.component';
import { StoreModule } from '@ngrx/store';
import { reducer } from './reducers/dashboard.reducer';
import { ReadStoreComponent } from './components/read-store/read-store.component';
import {RouterModule} from "@angular/router";
import { TrainingListComponent } from './components/training-list/training-list.component';
// import { SchemaValidatorComponent } from './components/schema-validator/schema-validator.component';

// import { AngularFileUploaderModule } from 'angular-file-uploader';
// import { MonitorViewingComponent } from './components/monitor-viewing/monitor-viewing.component';
// import { PageNotFoundComponent } from './components/PageNotFound/pagenotfound.component';
// import { CreateDashboardComponent } from './components/create-dashboard/create-dashboard.component';
// import { MonitorCreationComponent } from './components/monitor-creation/monitor-creation.component';
// import {ReactiveFormsModule} from "@angular/forms";




@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,

//     // PredictiveDashboardComponent,
//     // PredictiveUploadComponent
//     routingComponents,
//     PredictiveDashboardDetailComponent,

    PredictiveDashboardComponent,
    PredictiveUploadComponent,

    MonitorViewingComponent,
    PageNotFoundComponent,
    CreateDashboardComponent,
    MonitorCreationComponent,

    PredictiveDashboardDetailComponent,
    ReadStoreComponent,
    TrainingListComponent,
    // SchemaValidatorComponent


  ],
  imports: [
    BrowserModule,
    AngularFileUploaderModule,
    AppRoutingModule,
    ReactiveFormsModule,
    MatProgressSpinnerModule,
    BrowserAnimationsModule,


    StoreModule.forRoot({
      dashboard: reducer
    })
  ],
  providers: [{provide: LocationStrategy, useClass: HashLocationStrategy}],
  bootstrap: [AppComponent],

})

export class AppModule { }
