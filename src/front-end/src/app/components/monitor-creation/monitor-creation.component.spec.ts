import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MonitorCreationComponent } from './monitor-creation.component';

describe('MinitorCreationComponent', () => {
  let component: MonitorCreationComponent;
  let fixture: ComponentFixture<MonitorCreationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MonitorCreationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MonitorCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
