import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchemaValidatorComponent } from './schema-validator.component';

describe('SchemaValidatorComponent', () => {
  let component: SchemaValidatorComponent;
  let fixture: ComponentFixture<SchemaValidatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
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
