import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-predictive-upload',
  templateUrl: './predictive-upload.component.html',
  styleUrls: ['./predictive-upload.component.css']
})
export class PredictiveUploadComponent implements OnInit {
  selectedFile = null;
  selectedFile2 = null;
  constructor() { }

  ngOnInit(): void {
  }


  onFileSelected_P(event) {
    console.log(event);
    this.selectedFile = <File>event.target.files[0];
    

  }

  onFileSelected_S(event) {
    console.log(event);
    this.selectedFile2 = <File>event.target.files[0];
    

  }

  onUpload(){
       
  }


}
