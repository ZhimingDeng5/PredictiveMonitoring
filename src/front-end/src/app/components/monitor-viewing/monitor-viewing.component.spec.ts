import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MonitorViewingComponent } from './monitor-viewing.component';

describe('MonitorViewingComponent', () => {
  let component: MonitorViewingComponent;
  let fixture: ComponentFixture<MonitorViewingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MonitorViewingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MonitorViewingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
