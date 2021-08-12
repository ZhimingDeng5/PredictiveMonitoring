import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {Monitor,Monitors} from "../../monitor";
import {MonitorService} from "../../monitor.service";
@Component({
  selector: 'app-monitor-creation',
  templateUrl: './monitor-creation.component.html',
  styleUrls: ['./monitor-creation.component.css']
})
export class MonitorCreationComponent implements OnInit {

  userForm : FormGroup;
  monitorList : Monitor[];
  predictors:File[]=[];
  schema:File;
  messageShown:String;
  constructor(private fb:FormBuilder,private monitorService:MonitorService){

    this.monitorList = [];

    this.userForm = this.fb.group({
      name :['',Validators.required],
      predictors :['',Validators.required],
      schema :['',Validators.required]
    })
  }



  PredictorsUpload(event) {

    this.predictors = <File[]>event.target.files;
    console.log(this.predictors);
  }
  SchemaUpload(event) {

    this.schema = <File>event.target.files[0];
    console.log(this.predictors);
  }
  onSubmit() : void{
    this.create();
    this.userForm.reset();
    var time=2;
    this.messageShown="monitor created successfully!";
    let self=this;
    var interval=setInterval(function(){
      if(time>0) {
        time--;
      }
      else
      {
        clearInterval(interval);
        self.messageShown=null;
      }
    },1000)
  }

  reset() {
    this.userForm.reset();
  }
  create()
  {
    var time=(new Date()).toLocaleTimeString();

    this.monitorService.createMonitor(this.userForm.value.name,time,
      this.predictors,this.schema);
  }

  ngOnInit(): void {
  }

}
