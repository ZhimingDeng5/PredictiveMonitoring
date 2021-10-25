import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReadStoreComponent } from './read-store.component';
import {StoreModule} from "@ngrx/store";
import {provideMockStore} from "@ngrx/store/testing";

describe('ReadStoreComponent', () => {
  let component: ReadStoreComponent;
  let fixture: ComponentFixture<ReadStoreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports:[StoreModule.forRoot({})],
      declarations: [ ReadStoreComponent ],
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
