import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReadStoreComponent } from './read-store.component';

describe('ReadStoreComponent', () => {
  let component: ReadStoreComponent;
  let fixture: ComponentFixture<ReadStoreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReadStoreComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReadStoreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
