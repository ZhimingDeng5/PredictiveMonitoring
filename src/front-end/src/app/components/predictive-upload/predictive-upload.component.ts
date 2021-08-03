import { Component, OnInit } from '@angular/core';

// import {Router} from '@angular/router'
// import { v4 as uuidv4 } from "uuid";
// let UUID = require("uuidjs");
import axios from 'axios';


@Component({
  selector: 'app-predictive-upload',
  templateUrl: './predictive-upload.component.html',
  styleUrls: ['./predictive-upload.component.css']
})

export class PredictiveUploadComponent implements OnInit {
  monitor = null;
  eventLog = null;

  constructor() {

  }

  ngOnInit(): void {

  }


  onFileSelected_M(event) {
    this.monitor = <File>event.target.files[0];
    console.log(this.monitor);
  }

  onFileSelected_E(event) {
    this.eventLog = <File>event.target.files[0];
    console.log(this.eventLog);
  }

 
  //this method is for testing 
  //need a real generate monitor later
  generate_Monitor(){
    let reader = new FileReader();
     
    

  }

  onUpload(name){

    // let id =uuidv4();
    // console.log(id); 
    // this.generate_Monitor();
    // console.log(name.value);
    console.log(name.value);

    let formData = new FormData();
    formData.append("monitor", this.monitor);
    formData.append("event_log", this.eventLog);

    axios.post("http://localhost:8000/create-dashboard", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        'name': name.value
      }
    }).then((res)=>{
      if(res.status == 201){
        window.location.href='/dashboard'
      }
    });
    
    
    // this.router.navigate(['${}']);
  }

}
