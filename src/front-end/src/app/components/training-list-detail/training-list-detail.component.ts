import {Component, Input, OnInit, ViewChild} from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';
import { NavigationEnd, Router } from '@angular/router';
import { ChartOptions, ChartType, ChartDataSets } from 'chart.js';
import { Color, Label } from 'ng2-charts';

import{ Predictor} from "../../predictor";
import axios from 'axios';
import { environment } from 'src/environments/environment';
import {SearchInfo} from "../predictive-dashboard-detail/predictive-dashboard-detail.component";




@Component({
  selector: 'app-training-list-detail',
  templateUrl: './training-list-detail.component.html',
  styleUrls: ['./training-list-detail.component.css']
})
export class TrainingListDetailComponent implements OnInit {
  predictors = [];
  mySubscription: any;
  //read csv file and create a list to contain
  list: (string[])[]=[]

  numberlist: (number| number[])[] = []
  /*
   Chart1: bubble
   To do:
   Get the data from csv file (LocalStorage maybe in this page)
   */

  public bubbleChartOptions: ChartOptions ={
    responsive: true,
    scales: {
      xAxes:[{
        ticks: {
          min: 0,
          max: 50
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 50
        }
      }]
    }
  };

  public bubbleChartType: ChartType ='bubble';
  public bubbleChartLegend = true;

  public bubbleChartData: ChartDataSets[] = [
    {
      data: [
        { x: 10, y: 10, r: 10 },
        { x: 15, y: 5, r: 10 },
        { x: 26, y: 12, r: 10 },
        { x: 7, y: 8, r: 10 },
        { x: 1, y: 2, r: 10 },
        { x: 2, y: 4, r: 10 },
        { x: 3, y: 6, r: 10 },
        { x: 4, y: 8, r: 10 },

      ],
      label: 'Predicted',
    },
  ];


 /*
    Chart2: line
    To do:
    Get the data from csv file (LocalStorage maybe in this page)
    */

  public lineChartData: ChartDataSets[] = [

     { data: [1052493.9, 1049551.5, 1038888.5, 1259881.2, 1522930.6, 1320050, 1412908.5, 1134984.2, 1247165], label: 'MAE' },
  /*  { data:
      /!*parseFloat(this.numberlist[0].toString()),
        parseFloat(this.numberlist[1].toString()),
        parseFloat(this.numberlist[2].toString()),
        parseFloat(this.numberlist[3].toString()),
        parseFloat(this.numberlist[4].toString()),
        parseFloat(this.numberlist[5].toString()),
        parseFloat(this.numberlist[6].toString()),
        parseFloat(this.numberlist[7].toString()),
        parseFloat(this.numberlist[8].toString())*!/], label: 'MAE' },*/
    ];

  public lineChartLabels: Label[] = ['1', '2', '3', '4', '5', '6', '7','8','9'];
  public lineChartOptions: ChartOptions  = {
    responsive: true,
  };

  public lineChartLegend = true;
  public lineChartType : ChartType ='line';
  public lineChartPlugins = [];


  /*
   Chart3: bar
   To do:
   Get the data from csv file (LocalStorage maybe in this page)
   */

  public barChartOptions: ChartOptions = {
    responsive: true,
  };
  public barChartLabels: Label[] = ['Evaluation Metric: 1'];
  public barChartType: ChartType = 'bar';
  public barChartLegend = true;
  public barChartPlugins = [];

  public barChartData: ChartDataSets[] = [
    { data: [0.25030303], label: 'Target_Supply_Date_delta' },
    { data: [0.21636364], label: 'Line_Total_Cost' },
    { data: [0.17737374], label: 'elapsed' },
    { data: [0.1430303], label: 'Line_Total_Cost' },
    { data: [0.04566666566], label: 'org:resource13' },
    { data: [0.031313132], label: 'weekday_2' },
    { data: [0.025858587], label: 'Delay_Rank_Just in time' },
    { data: [0.024848485], label: 'weekday_6' },
    { data: [0.018989898], label: 'org:source_6' },
  ];





  constructor(

    public LocalStorage: LocalStorageService,
    private router: Router) {
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };

    this.mySubscription = this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        // Trick the Router into believing it's last link wasn't previously loaded
        this.router.navigated = false;
      }
    });
  }

  ngOnInit(): void {
  //polling
  let interval = setInterval(() => {
    let url = location.href
    let site = url.lastIndexOf("\/");
    let loc = url.substring(site + 1, url.length);
    if (loc == "training-list") {
      console.log("refresh")
    } else {
      clearInterval(interval);
    }
  }, 5000);



  /*  console.log("finally! " + this.numberlist);
    console.log(typeof this.numberlist);*/
/*    console.log((parseFloat(this.numberlist[0])));*/
  /*  console.log(typeof this.numberlist[0]);*/



  }


  openFile(event: any): void {
    const input = event.target;
    const reader = new FileReader();
    reader.onload = (() => {
      if (reader.result) {
        const array = reader.result.toString().split(/\n/);
        array.filter((line: string) => line.trim() !== '').forEach((line: string) => {
          let searchInfo: string[]=[];
          let InputNumber: number[] = [];
          const item = line.split(',');
          //console.log(item);
          if(item.includes("mae")) {
            /*   for (let i in item) {*/
            //searchInfo.push(item[i])
            searchInfo.push(item[6]);
            InputNumber.push(Number(item[6].valueOf()));
            /* }*/
            this.list.push(searchInfo);
            this.numberlist.push(InputNumber);

            /*localStorage.setItem ('numberlist', JSON.stringify(this.numberlist));*/
          }

        });



     /*   console.log("check one: " + this.numberlist);
        console.log("check two: " + typeof this.numberlist);

        console.log("check one: " + this.numberlist[0]);
        console.log("check one: " + this.numberlist[0].toString());
        console.log("check two: " + typeof parseFloat(this.numberlist[0].toString()));*/
      }

    });
    reader.readAsText(input.files[0], 'utf-8');
  }






 getBack(){
   this.router.navigateByUrl("/training-list");
 }

  SwitchToChart1(){
    document.getElementById('chart1').style.display ='block'
    document.getElementById('chart2').style.display ='none'
    document.getElementById('chart3').style.display ='none'

    document.getElementById('li1').style.background = '#1E90FF'
    document.getElementById('li2').style.background = 'white'
    document.getElementById('li3').style.background = 'white'
  }

  SwitchToChart2(){
    document.getElementById('chart1').style.display ='none'
    document.getElementById('chart2').style.display ='block'
    document.getElementById('chart3').style.display ='none'

    document.getElementById('li1').style.background = 'white'
    document.getElementById('li2').style.background = '#1E90FF'
    document.getElementById('li3').style.background = 'white'

  }


  SwitchToChart3(){
   document.getElementById('chart1').style.display ='none'
   document.getElementById('chart2').style.display ='none'
    document.getElementById('chart3').style.display ='block'

    document.getElementById('li1').style.background = 'white'
    document.getElementById('li2').style.background = 'white'
    document.getElementById('li3').style.background = '#1E90FF'
 }



  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }



}
