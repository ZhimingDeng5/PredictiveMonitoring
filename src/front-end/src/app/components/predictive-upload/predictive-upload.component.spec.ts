import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictiveUploadComponent } from './predictive-upload.component';
import {RouterTestingModule} from "@angular/router/testing";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

describe('PredictiveUploadComponent', () => {
  let component: PredictiveUploadComponent;
  let fixture: ComponentFixture<PredictiveUploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({

      imports: [
        RouterTestingModule,
        ReactiveFormsModule,
        FormsModule
      ],
      declarations: [ PredictiveUploadComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictiveUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
