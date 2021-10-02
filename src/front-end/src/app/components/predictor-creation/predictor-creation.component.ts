import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import axios from "axios";
import {environment} from "../../../environments/environment";
import {LocalStorageService} from "../../local-storage.service";
import {Router} from "@angular/router";
@Component({
  selector: 'app-predictor-creation',
  templateUrl: './predictor-creation.component.html',
  styleUrls: ['./predictor-creation.component.css']
})
export class PredictorCreationComponent implements OnInit {

  isAdvanced: boolean = false;
  userForm : FormGroup;
  eventLog:File;
  schema:File;
  cluster:boolean=false;
  toggleMode() {
    this.isAdvanced = !this.isAdvanced;
  }

  constructor(private fb:FormBuilder,public LocalStorage: LocalStorageService,private router:Router){

    this.userForm = this.fb.group({
      predictorName :['',Validators.required],
      eventlog :['',Validators.required],
      schema:['',Validators.required],
      predictorType:['label',Validators.required],
      bucketingType:['zero',Validators.required],
      encodingType:['agg',Validators.required],
      learnerType:['xgb',Validators.required],
      xgb_n_estimators :['300',Validators.required],
      xgb_learning_rate :['0.04',Validators.required],
      xgb_colsample_bytree :['0.7',Validators.required],
      xgb_subsample :['0.7',Validators.required],
      xgb_max_depth :['5',Validators.required],
      n_clusters:['1',Validators.required],
      rf_n_estimators :['300',Validators.required],
      rf_max_features :['0.5',Validators.required],

      gbm_n_estimators :['300',Validators.required],
      gbm_max_features :['0.5',Validators.required],
      gbm_learning_rate :['0.1',Validators.required],

      dt_max_features :['0.8',Validators.required],
      dt_max_depth :['5',Validators.required]
    })
  }
  EventLogUpload(event) {
    this.eventLog= <File>event.target.files[0];
    console.log(this.eventLog);
  }
  SchemaUpload(event) {
    this.schema= <File>event.target.files[0];
    console.log(this.schema);
  }
  Cluster():void{
    this.cluster=true;
    console.log(this.cluster);
  }
  UnCluster():void{
    this.cluster=false;
    console.log(this.cluster);
  }
  onSubmit() : void{
    let string1 =
      '{"'+this.userForm.value.predictorType+'":'+
      '{"'+this.userForm.value.bucketingType+'":'+
      '{"'+this.userForm.value.encodingType+'":'+
      '{"'+this.userForm.value.learnerType+'":';

    let paramstring ="";
    if (this.userForm.value.learnerType=="xgb")
    {
      paramstring =
      '{"n_estimators": ' + this.userForm.value.xgb_n_estimators +
      ',"learning_rate": ' + this.userForm.value.xgb_learning_rate +
      ',"colsample_bytree": ' + this.userForm.value.xgb_colsample_bytree +
      ',"subsample": ' + this.userForm.value.xgb_subsample +
      ',"max_depth": ' + this.userForm.value.xgb_max_depth;
    }
    else if (this.userForm.value.learnerType=="rf")
    {
      paramstring =
      '{"n_estimators": ' + this.userForm.value.rf_n_estimators +
      ',"max_features": ' + this.userForm.value.rf_max_features;
    }
    else if (this.userForm.value.learnerType=="gbm")
    {
      paramstring =
      '{"n_estimators": ' + this.userForm.value.gbm_n_estimators +
      ',"max_features": ' + this.userForm.value.gbm_max_features +
      ',"learning_rate": ' + this.userForm.value.gbm_learning_rate;
    }
    else if (this.userForm.value.learnerType=="dt")
    {
      paramstring =
      '{"max_features": ' + this.userForm.value.dt_max_features +
      ',"max_depth": ' + this.userForm.value.dt_max_depth;
    }
    if (this.cluster)
    {
      paramstring+=',"n_clusters": '+this.userForm.value.n_clusters;
    }
    let full_string = string1+paramstring+'}}}}}';
    //console.log(full_string);
    let serializedName = JSON.parse(full_string);
    let serializedForm1:string = JSON.stringify(serializedName);
    let predictorName:String=this.userForm.value.predictorName;
    //console.log(serializedForm1);
    let blob = new Blob([serializedForm1], { type: 'text/plain' });
    let configfile:File = new File([blob], "config.json", {type: "text/plain"});
    console.log(configfile);
    let formData = new FormData();
    formData.append("event_log", this.eventLog);
    formData.append("schema", this.schema);
    formData.append("config", configfile);
        axios.post(environment.backend + "/create-predictor", formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then((res) => {
          if(res.status==200) {
            localStorage[res.data.task_id + "Name"] = this.userForm.value.predictorName;
            console.log("Config files uploaded successfully!")
          }

            // window.location.href= './dashboard';
            //this.router.navigateByUrl('/dashboard');

            //this.selectedMonitor.taskid=res.data;
            //window.location.href='/monitor-viewing';
            //console.log(this.selectedMonitor.taskid);



    })
/*    var element = document.createElement('a');
    element.setAttribute('href', "data:text/json;charset=UTF-8," + encodeURIComponent(serializedForm1));
    element.setAttribute('download', "config.json");
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click(); // simulate click
    document.body.removeChild(element);*/
  }

  ngOnInit(): void {
  }
}
