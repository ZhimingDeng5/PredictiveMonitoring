import { Component, OnInit } from '@angular/core';

import { timer } from 'rxjs';

import {Router} from '@angular/Router'
import { v4 as uuidv4 } from "uuid";
//let UUID = require("uuidjs");
import axios from 'axios';


@Component({
  selector: 'app-predictive-upload',
  templateUrl: './predictive-upload.component.html',
  styleUrls: ['./predictive-upload.component.css']
})

export class PredictiveUploadComponent implements OnInit {
  pickleFile = null;
  schema = null;
  monitor="test monitor";
  monitor_name=null;

  constructor() {

  }

  ngOnInit(): void {
    const obs$ = timer(10000, 10000);
    obs$.subscribe(

      //put get all dashboards command here.

      //if(number of dashboards.id != current numbers of dashboards id){
      //  refresh the page with new dashboards.
      //}


      (d)=>{
      console.log(d);
    }

    )
  }


  onFileSelected_P(event) {
    // console.log(event);
    this.pickleFile = <File>event.target.files[0];
    console.log(this.pickleFile);
   
  }

  onFileSelected_S(event) {
    // console.log(event);
    this.schema = <File>event.target.files[0];
    console.log(this.schema);
  }

 
  //this method is for testing 
  //need a real generate monitor later
  generate_Monitor(){
    let reader = new FileReader();
     
    

  }

  onUpload(name){
    let id =uuidv4();
    console.log(id); 
    this.generate_Monitor();
    console.log(name.value);

    let formData = new FormData();
    formData.append("monitor", this.pickleFile);
    formData.append("event_log", this.schema);

    axios.post("http://localhost:8000/create-dashboard", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // this.router.navigate(['${}']);
  }

}
