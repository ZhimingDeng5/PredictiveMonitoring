import { ComponentFixture, TestBed } from '@angular/core/testing';
import {RouterTestingModule} from "@angular/router/testing";
import { CreateDashboardComponent } from './create-dashboard.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms'
import {Monitor} from "../../monitor";

describe('CreateDashboardComponent', () => {
  let component: CreateDashboardComponent;
  let fixture: ComponentFixture<CreateDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
       ReactiveFormsModule,
        FormsModule
      ],
      declarations: [ CreateDashboardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {

 /*   let monitor:Monitor={
      predictors : 1,
      name : "name",
      timecreated:"time",
      id:"id",
    };
    localStorage.setItem("currentMonitor",JSON.stringify(monitor));*/
    fixture = TestBed.createComponent(CreateDashboardComponent);
    component = fixture.componentInstance;
    //fixture.detectChanges();
  });

  it('should create', () => {

    expect(component).toBeTruthy();
  });
});
