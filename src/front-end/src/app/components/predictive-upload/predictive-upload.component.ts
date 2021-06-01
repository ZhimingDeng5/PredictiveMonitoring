import { Component, OnInit } from '@angular/core';
import { timer } from 'rxjs';

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
