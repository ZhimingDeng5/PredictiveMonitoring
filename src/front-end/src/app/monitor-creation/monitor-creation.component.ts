import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';


@Component({
  selector: 'app-monitor-creation',
  templateUrl: './monitor-creation.component.html',
  styleUrls: ['./monitor-creation.component.css']
})
export class MonitorCreationComponent implements OnInit {

  userForm : FormGroup;
  monitorList : any;

  constructor(private fb:FormBuilder){ 

    this.monitorList = [];

    this.userForm = this.fb.group({
      name :['',Validators.required],
      time :['',Validators.required]
    })
  }


  onSubmit() : void{
    this.monitorList.push(this.userForm.value);
    this.userForm.reset();
  }

  reset() {
    this.userForm.reset();
  }

  removeItem(element: any){
    this.monitorList.forEach((value: any,index: any)=>{
    if(value == element)
    this.monitorList.splice(index,1);
    });
  }

  ngOnInit(): void {
  }

}
