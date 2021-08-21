import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictiveDashboardDetailComponent } from './predictive-dashboard-detail.component';

describe('PredictiveDashboardDetailComponent', () => {
  let component: PredictiveDashboardDetailComponent;
  let fixture: ComponentFixture<PredictiveDashboardDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
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
