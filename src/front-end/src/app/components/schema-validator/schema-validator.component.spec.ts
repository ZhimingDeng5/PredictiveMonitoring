import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchemaValidatorComponent } from './schema-validator.component';
import {RouterTestingModule} from "@angular/router/testing";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MonitorViewingComponent} from "../monitor-viewing/monitor-viewing.component";

describe('SchemaValidatorComponent', () => {
  let component: SchemaValidatorComponent;
  let fixture: ComponentFixture<SchemaValidatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        ReactiveFormsModule,
        FormsModule
      ],
      declarations: [ SchemaValidatorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SchemaValidatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
