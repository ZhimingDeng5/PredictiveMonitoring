import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictiveDashboardDetailComponent } from './predictive-dashboard-detail.component';
import {RouterTestingModule} from "@angular/router/testing";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";

describe('PredictiveDashboardDetailComponent', () => {
  let component: PredictiveDashboardDetailComponent;
  let fixture: ComponentFixture<PredictiveDashboardDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        ReactiveFormsModule,
        FormsModule,
        HttpClientModule
      ],
      declarations: [ PredictiveDashboardDetailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictiveDashboardDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
