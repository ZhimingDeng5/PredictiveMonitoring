import { Component,  OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import axios from 'axios';
import {HttpClient} from "@angular/common/http";
import {Injectable} from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';


export class SearchInfo{

  fitem1: string = '';
  fitem2: string = '';
  fitem3: string = '';
  fitem4: string = '';
  fitem5: string = '';
  fitem6: string = '';
  fitem7: string = '';
  fitem8: string = '';
  fitem9: string = '';

}

@Component({
  selector: 'app-predictive-dashboard-detail',
  templateUrl: './predictive-dashboard-detail.component.html',
  styleUrls: ['./predictive-dashboard-detail.component.css']
})

@Injectable({
  providedIn: 'root'
})



export class PredictiveDashboardDetailComponent implements OnInit {
  id;
  initTasks = [];
  //list: SearchInfo[] = [];
  list: (string[])[]=[]
  constructor(private _Activatedroute: ActivatedRoute,
              private _router: Router,
              private http: HttpClient,
              private LocalStorage: LocalStorageService
  ) {
  }

  sub;


  ngOnInit(): void {

    this.sub = this._Activatedroute.paramMap.subscribe(params => {
      console.log(params);
      this.id = params.get('id');


       this.LocalStorage.get(this.id+'csv').then((data)=>  {

        // const input =  new Blob([data], {type: 'application/vnd.ms-excel'});
         const input = <Blob> data;
         const reader = new FileReader();
         reader.onload = (() => {
           if (reader.result) {
             console.log(reader.result);
             const array = reader.result.toString().split(/\n/);
             array.filter((line: string) => line.trim() !== '').forEach((line: string) => {
               let searchInfo: string[]=[];
               const item = line.split(',');
               console.log(item);
               for (let i in item)
               {
                 searchInfo.push(item[i])
               }
               /*if (item.length >= 0) {
                 searchInfo.fitem1 = item[0];
                 searchInfo.fitem2 = item[1];
                 searchInfo.fitem3 = item[2];
                 searchInfo.fitem4 = item[3];
                 searchInfo.fitem5 = item[4];
                 searchInfo.fitem6 = item[5];
                 searchInfo.fitem7 = item[6];
                 searchInfo.fitem8 = item[7];
                 searchInfo.fitem9 = item[8];
               }*/

               this.list.push(searchInfo);
             });
           }
         });
         reader.readAsText(input, 'utf-8');
       })





       // axios.get("http://localhost:8000/task/id", {}).then((res) => {
          //num cases
          // this.length = res.data.tasks.length;
          // console.log(this.length);

          // axios.get("http://localhost:8000/tasks/id", {
          //}).then((res)=>{
          //num cases
          // this.length = res.data.tasks.length;
          // console.log(this.length);

          // for(var i = 0; i<this.length; i++){
          //   this.initTasks[i] =[];
          //   this.initTasks[i]['id']=res.data.tasks[i].taskID;
          //   this.initTasks[i]['name']=res.data.tasks[i].name;
          //   this.initTasks[i]['status']=res.data.tasks[i].status;
          // }

        });
      // });




  }

  downloadCSV(task_id) {
    //  this.http.get('http://localhost:8000/dashboard/' + task_id, {responseType: 'blob'}).subscribe(data => {
      this.LocalStorage.get(task_id + 'csv').then((res)=>{

      const link = document.createElement('a');

      link.setAttribute('href', window.URL.createObjectURL(res));
      link.setAttribute('download', task_id + '.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);


    });


  }






  ngOnDestroy() {
    this.sub.unsubscribe();
  }


}









