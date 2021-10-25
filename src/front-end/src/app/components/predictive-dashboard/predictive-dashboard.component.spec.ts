import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictiveDashboardComponent } from './predictive-dashboard.component';
import {RouterTestingModule} from "@angular/router/testing";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MAT_DIALOG_DATA, MatDialogModule} from "@angular/material/dialog";
import {PopupComponent} from "../popup/popup.component";

describe('PredictiveDashboardComponent', () => {
  let component: PredictiveDashboardComponent;
  let fixture: ComponentFixture<PredictiveDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        ReactiveFormsModule,
        FormsModule,
        MatDialogModule,
      ],
      declarations: [ PredictiveDashboardComponent ],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: {} },
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictiveDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
