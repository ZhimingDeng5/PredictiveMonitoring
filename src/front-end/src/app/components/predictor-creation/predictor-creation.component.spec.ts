import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictorCreationComponent } from './predictor-creation.component';

describe('PredictorCreationComponent', () => {
  let component: PredictorCreationComponent;
  let fixture: ComponentFixture<PredictorCreationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PredictorCreationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictorCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
