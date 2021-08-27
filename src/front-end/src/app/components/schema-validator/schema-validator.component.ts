import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-schema-validator',
  templateUrl: './schema-validator.component.html',
  styleUrls: ['./schema-validator.component.css']
})
export class SchemaValidatorComponent implements OnInit {

  userForm : FormGroup;
  csvFile:File;
  jsonFile:File;

  constructor(private fb:FormBuilder) { 

    this.userForm = this.fb.group({
      csvFile :['',Validators.required],
      jsonFile :['',Validators.required]
    })

  }

  CSVUpload(event) {

    this.csvFile = event.target.files[0];
    console.log("CSV Uploaded");
  }

  JSONUpload(event) {

    this.jsonFile = event.target.files[0];
    console.log("JSON Uploaded");
  }

  async onSubmit()
  {
    let csvString = await this.csvFile.text();
    let csv_col_names = csvString.slice(0, csvString.indexOf("\r")).split(",");
    console.log(csv_col_names);
      
    let jsonString = await this.jsonFile.text();
    let obj = JSON.parse(jsonString);
    let res = [];
      
    for(var i in obj)
        res.push(obj[i]);

    let schema_col_names = res.reduce((acc, val) => acc.concat(val), []);
    console.log(schema_col_names);

    let matchResult = 0;
    if(csv_col_names.every(elem => schema_col_names.includes(elem)))
        matchResult = 1;
    console.log(matchResult);
  }
  
  ngOnInit(): void {
  }
}
