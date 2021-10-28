import { Component, Inject, OnInit } from '@angular/core';
import { inject } from '@angular/core/testing';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import axios from 'axios';
import { NavigationEnd, Router } from '@angular/router';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-popup',
  templateUrl: './popup.component.html',
  styleUrls: ['./popup.component.css']
})
export class PopupComponent implements OnInit {
  message;
  id;
  constructor(private router: Router,@Inject(MAT_DIALOG_DATA) public data) { 
    this.id=data.id;
    this.message=data.message;
  }

  // Delete(){
  //   let predictorlist = JSON.parse(localStorage['predictorList']);
  //   for (var j = 0; j < predictorlist.length; j++) {
  //     if (predictorlist[j] === this.id) {
  //       predictorlist.splice(j, 1);
  //       localStorage.setItem("predictorList", JSON.stringify(predictorlist));
  //       console.log("remove task from predictorlist success!");
  //     }
  //   }

  //   axios.post(environment.training_backend + '/cancel/' + this.id, {}).then((res) => {     
      
  //     console.log("Error cancle sucessfully");
  //     console.log(res);
  //     this.router.navigateByUrl('/training-list');
  //     localStorage.removeItem(this.id+"ERROR");
  //   })
  // }

  ngOnInit(): void {
  }

}
