import {ComponentFixture, fakeAsync, TestBed, tick} from '@angular/core/testing';

import { MonitorCreationComponent } from './monitor-creation.component';
import {RouterTestingModule} from "@angular/router/testing";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {DebugElement, Injectable} from "@angular/core";
import {By} from "@angular/platform-browser";
import {MonitorService} from "../../monitor.service";
import {Monitor} from "../../monitor";
import {LocalStorageService} from "../../local-storage.service";
describe('MinitorCreationComponent', () => {
  let component: MonitorCreationComponent;
  let fixture: ComponentFixture<MonitorCreationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        ReactiveFormsModule,
        FormsModule
      ],
      declarations: [ MonitorCreationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MonitorCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    const element:DebugElement=fixture.debugElement;
    const monitorNameInput=element.query(By.css('input[formControlName=name]'));
    monitorNameInput.nativeElement.value="testMonitor1"
    const dataSchema = new DataTransfer();
    dataSchema.items.add(new File(['11'], 'test-file.pdf'));
    const schemaInput=element.query(By.css('input[formControlName=schema]'));
    schemaInput.nativeElement.files=dataSchema.files;
    schemaInput.nativeElement.dispatchEvent(new InputEvent('change'));
    fixture.detectChanges();
    const dataPredictors = new DataTransfer();
    dataPredictors.items.add(new File(['11'], 'test-file1.pdf'));
    dataPredictors.items.add(new File(['111'], 'test-file2.pdf'));
    const predicorInput=element.query(By.css('input[formControlName=predictors]'));
    predicorInput.nativeElement.files=dataPredictors.files;
    predicorInput.nativeElement.dispatchEvent(new InputEvent('change'));
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('should upload a file', () => {
    expect(component.schema).toBeTruthy();
    expect(component.schema.name).toBe("test-file.pdf");
    expect(component.schema.size).toBe(2);
  });
  it('should upload files', () => {
    expect(component.predictors[0]).toBeTruthy();
    expect(component.predictors[0].name).toBe("test-file1.pdf");
    expect(component.predictors[0].size).toBe(2);
    expect(component.predictors[1]).toBeTruthy();
    expect(component.predictors[1].name).toBe("test-file2.pdf");
    expect(component.predictors[1].size).toBe(3);
  });
 it('should create a monitor', fakeAsync(() => {
    component.onSubmit();
    let monitors:Monitor[]=component.monitorService.getMonitors();
    tick(500);
    let monitor=monitors[(monitors.length-1)];
    expect(monitor.name).toBe("testMonitor1");
    expect(monitor.predictors).toBe(2);
  }));
});
