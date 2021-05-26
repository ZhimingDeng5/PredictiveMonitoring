import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { PredictiveDashboardComponent } from './components/predictive-dashboard/predictive-dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    PredictiveDashboardComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
