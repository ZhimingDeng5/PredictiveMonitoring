import { Component, OnInit } from '@angular/core';
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

  constructor(private router:Router) {

  }

  ngOnInit(): void {
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

    axios.post("",{
      uuid: id,
      monitor:this.monitor,
      monitor_name: this.monitor_name
    })
    
    // this.router.navigate(['${}']);
  }

}
