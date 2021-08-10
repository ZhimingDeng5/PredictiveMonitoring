import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// import { PredictiveDashboardComponent } from './components/predictive-dashboard/predictive-dashboard.component';
// import { PredictiveUploadComponent } from './components/predictive-upload/predictive-upload.component';

import { AppRoutingModule,routingComponents } from './app-routing.module';
import { MonitorCreationComponent } from './monitor-creation/monitor-creation.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    // PredictiveDashboardComponent,
    // PredictiveUploadComponent
    routingComponents,
    MonitorCreationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
