import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
// import { PredictiveDashboardComponent } from './components/predictive-dashboard/predictive-dashboard.component';
// import { PredictiveUploadComponent } from './components/predictive-upload/predictive-upload.component';

import { AppRoutingModule,routingComponents } from './app-routing.module';
import { PredictiveDashboardDetailComponent } from './components/predictive-dashboard-detail/predictive-dashboard-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    // PredictiveDashboardComponent,
    // PredictiveUploadComponent
    routingComponents,
    PredictiveDashboardDetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
