import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-predictor-creation',
  templateUrl: './predictor-creation.component.html',
  styleUrls: ['./predictor-creation.component.css']
})
export class PredictorCreationComponent implements OnInit {

  isAdvanced: boolean = false;
  userForm : FormGroup;

  toggleMode() {
    this.isAdvanced = !this.isAdvanced;
  }

  constructor(private fb:FormBuilder){

    this.userForm = this.fb.group({
      predictorName :['',Validators.required],
      eventlog :['',Validators.required],

      predictorType:['label',Validators.required],
      bucketingType:['zero',Validators.required],
      encodingType:['agg',Validators.required],
      learnerType:['xgb',Validators.required],

      xgb_n_estimators :['300',Validators.required],
      xgb_learning_rate :['0.04',Validators.required],
      xgb_colsample_bytree :['0.7',Validators.required],
      xgb_subsample :['0.7',Validators.required],
      xgb_max_depth :['5',Validators.required],

      rf_n_estimators :['300',Validators.required],
      rf_max_features :['0.5',Validators.required],

      gbm_n_estimators :['300',Validators.required],
      gbm_max_features :['0.5',Validators.required],
      gbm_learning_rate :['0.1',Validators.required],

      dt_max_features :['0.8',Validators.required],
      dt_max_depth :['5',Validators.required]
    })
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
    
    let full_string = string1+paramstring+'}}}}}';
    console.log(full_string);
    let serializedName = JSON.parse(full_string);
    let serializedForm1 = JSON.stringify(serializedName);
       
    var element = document.createElement('a');
    element.setAttribute('href', "data:text/json;charset=UTF-8," + encodeURIComponent(serializedForm1));
    element.setAttribute('download', "config.json");
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click(); // simulate click
    document.body.removeChild(element);
  }

  ngOnInit(): void {
  }
}
