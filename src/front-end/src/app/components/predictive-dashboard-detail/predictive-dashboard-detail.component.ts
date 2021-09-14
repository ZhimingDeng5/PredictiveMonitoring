import { Component,  OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import axios from 'axios';
import {HttpClient} from "@angular/common/http";
import {Injectable} from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';

import { environment } from 'src/environments/environment';


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
  dashname = localStorage.getItem("dashnamelist");
  initTasks = [];
  //list: SearchInfo[] = [];
  list: (string[])[]=[]
  list_two: (string[])[]=[]
  list_three: (string[])[]=[]
  constructor(private _Activatedroute: ActivatedRoute,
              private _router: Router,
              private http: HttpClient,
              private LocalStorage: LocalStorageService
  ) {
  }

  sub;
  page: any;



  ngOnInit(): void {

    this.sub = this._Activatedroute.paramMap.subscribe(params => {
      console.log(params);
      this.id = params.get('id');

      let dashname = localStorage.getItem("dashnamelist");
      console.log("check dashname: " + dashname);

       this.LocalStorage.get(this.id+'csv').then((data)=>  {

        // const input =  new Blob([data], {type: 'application/vnd.ms-excel'});
         const input = <Blob> data;
         const reader = new FileReader();
         reader.onload = (() => {
           if (reader.result) {
             console.log("check reader result: "+ reader.result);
             const array = reader.result.toString().split(/\n/);

             const array_2 = array[0];
             const array_3 = array[1];

             delete(array[0]);
             delete(array[1]);
             array.filter((line: string) => line.trim() !== '' ).forEach((line: string) => {
               let searchInfo: string[]=[];
               const item = line.split(',');
               console.log(item);
               for (let i in item)
               {
                 searchInfo.push(item[i])
               }
               this.list.push(searchInfo);
             });


               const item_2 =array_2.split(',');
               this.list_two.push(item_2);
             //  console.log("check hehe "+ this.list_two);

              const item_3 =array_3.split(',');
              this.list_three.push(item_3);
            //  console.log("check hehe "+ this.list_three);

           }
         });
         reader.readAsText(input, 'utf-8');
       })

      });




  }

  downloadCSV (task_id)
  {
        this.LocalStorage.get(this.id+'csv').then((data)=>  {

    //this.http.get(environment.backend + '/dashboard/' + task_id, {responseType: 'blob'}).subscribe(data => {
      const link = document.createElement('a');
     // const blob = new Blob([data],{type: 'application/vnd.ms-excel'});
          const blob =  <Blob> data;

      link.setAttribute('href', window.URL.createObjectURL(blob));
      link.setAttribute('download', task_id + '.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      //this._router.navigateByUrl('/dashboard');

    });


  }



  ngOnDestroy() {
    this.sub.unsubscribe();
  }


}









