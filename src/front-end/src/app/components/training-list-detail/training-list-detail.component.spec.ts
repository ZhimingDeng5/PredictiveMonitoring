import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainingListDetailComponent } from './training-list-detail.component';

describe('TrainingListDetailComponent', () => {
  let component: TrainingListDetailComponent;
  let fixture: ComponentFixture<TrainingListDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TrainingListDetailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainingListDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
