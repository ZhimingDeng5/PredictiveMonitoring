import {Component, Input, OnInit, ViewChild} from '@angular/core';
import { LocalStorageService } from '../../local-storage.service';
import {ActivatedRoute, NavigationEnd, Router} from '@angular/router';
import { ChartOptions, ChartType, ChartDataSets } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import * as Highcharts from 'highcharts';
import * as highchartsHeatmap from 'highcharts/modules/heatmap';
import Exporting from "highcharts/modules/exporting";
const heatmap = require("highcharts/modules/heatmap.js");
heatmap(Highcharts)
Exporting(Highcharts);

import{ Predictor} from "../../predictor";
import axios from 'axios';
import { environment } from 'src/environments/environment';
import {SearchInfo} from "../predictive-dashboard-detail/predictive-dashboard-detail.component";
import {read} from "fs";

interface Label_sel {
  value: string;
  viewValue: string;
}

interface Label_remtime {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-training-list-detail',
  templateUrl: './training-list-detail.component.html',
  styleUrls: ['./training-list-detail.component.css']
})



export class TrainingListDetailComponent implements OnInit {

  flag: number;
  id;
  tableName = '';
  Prediction_Target: String;
  Bucketing_Method: String;
  Prediction_Encoding: String;
  Prediction_Method: String;
  predictors = [];
  Accuracy;
  mySubscription: any;
  //read csv file and create a list to contain
  list: (string[])[] = []
  mylist_detailed: string;
  mylist_validation: string;
  mylist_feat_importance: string;
  numberlist: (number | number[])[] = []
  spilt: (string[])[] = []
  spilt_label: (string[])[] = []
  spilt2: (string[])[] = []
  spilt3: (string[])[] = []
  array: string[]
  array_label: string[]
  array2: string[]
  array3: string[]
  line_parameters = 'acc';
  line_parameters_2 = 'mae';
  label_selected: Label_sel[] = [
    {value: 'acc', viewValue: 'ACC'},
    {value: 'f1', viewValue: 'F1'},
    {value: 'logloss', viewValue: 'LOGLOSS'}
  ];
  remtime_selected: Label_remtime[] = [
    {value: 'mae', viewValue: 'MAE'},
    {value: 'rmse', viewValue: 'RMSE'},
    {value: 'nmae', viewValue: 'NMAE'},
    {value: 'nrmse', viewValue: 'NRMSE'}
  ];

  selectedMetric_label = this.label_selected[0].value;
  selectedMetric_remtime = this.remtime_selected[0].value;

  /*
   Chart1: heat map
   To do:
   Get the data from csv file (LocalStorage maybe in this page)
   */
  Highcharts: typeof Highcharts = Highcharts;
  updateFlag: boolean = true;
  chartOptions: Highcharts.Options = {};
 /*
    Chart2: line
    To do:
    Get the data from csv file (LocalStorage maybe in this page)
    */

  public lineChartData: ChartDataSets[] = [];
  public lineChartLabels: Label[] = [];
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
  public barChartLabels: Label[] = [];
  public barChartType: ChartType = 'horizontalBar';
  public barChartLegend = false;
  public barChartPlugins = [];

  public barChartData: ChartDataSets[] = [];


  constructor(
    private _Activatedroute: ActivatedRoute,
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


  sub;



   ngOnInit() {
    this.sub = this._Activatedroute.paramMap.subscribe(  params => {

      this.id = params.get('id');
      console.log(this.id);
      console.log(localStorage.getItem(this.id + '-detailed-csv'));


      this.LocalStorage.get(this.id).then((data) => {
        this.tableName = data[0];
      });

      this.LocalStorage.get(this.id + 'Info').then((response) => {
        let config = JSON.parse(<string>response);

        if(config.predictorMethod == "xgb") {
          this.Prediction_Method = "XGBOOST"
        }
        else {
          this.Prediction_Method = config.predictorMethod;
         }


        this.Prediction_Target = config.predictorType;
        this.Bucketing_Method = config.bucketingType;
        this.Prediction_Encoding = config.encoding;

      });

      this.array = [];
      this.array2 = [];
      this.array3 = [];
      this.array_label = [];
      this.spilt = [];
      this.spilt2 = [];
      this.spilt3 = [];
      this.spilt_label = [];


      //read config-json to get accuracy
      this.Accuracy = JSON.parse(localStorage.getItem(this.id + '-config-json')).evaluation.value;

      this.mylist_detailed =  (localStorage.getItem(this.id + '-detailed-csv'));
      this.mylist_validation = (localStorage.getItem(this.id + '-validation-csv'));
      this.mylist_feat_importance = (localStorage.getItem(this.id + '-feat-importance-csv'));


      // for diagram 1: ACTUAL VS PREDICTED (Remtime)
      this.array = this.mylist_detailed.toString().split(/\n/);
      this.array.filter((line: string) => line.trim() !== '').forEach((line: string) => {
        let searchInfo: string[] = [];
        const item = line.split(',');
        for (let i in item) {
          searchInfo.push(item[i])
        }
        this.spilt.push(searchInfo);
      });



      //set heat map
      this.plotGraph("data");


      // for diagram 2: ACCYRACY VS PERFIX LENGTH
      this.array2 = this.mylist_validation.toString().split(/\n/);
      this.array2.filter((line: string) => line.trim() !== '').forEach((line: string) => {
        let searchInfo2: string[] = [];
        const item = line.split(',');
        for (let i in item) {
          searchInfo2.push(item[i])
        }
        this.spilt2.push(searchInfo2);
      });



      // for diagram 3: FEATURE VS IMPORTANCE
      this.array3 = this.mylist_feat_importance.toString().split(/\n/);
      this.array3.filter((line: string) => line.trim() !== '').forEach((line: string) => {
        let searchInfo3: string[] = [];
        const item = line.split(',');
        for (let i in item) {
          searchInfo3.push(item[i])
        }
        this.spilt3.push(searchInfo3);
      });


      //set line chart parameters here
      const dataset_line = []
      const labels_line = []

      //console.log(JSON.parse(localStorage.getItem(this.id + '-config-json')).evaluation.metric);

      if(JSON.parse(localStorage.getItem(this.id + '-config-json')).evaluation.metric == "mae")
      {
        console.log("hit mae");
        document.getElementById("metric_value_label").style.display= 'none';
        for (let k = 1; k < this.array2.length; k++) {

          if (this.array2[k].includes( ","+ this.line_parameters_2)) {
            const each_label_bar = this.array2[k].split(',')[4];
            const each_data_line = parseFloat(this.array2[k].split(',')[6]);

            labels_line.push(each_label_bar);
            dataset_line.push(each_data_line);
          }

        }
        this.lineChartLabels = labels_line;       //XAxis
        this.lineChartData = [{data: dataset_line, label: 'score' + '/ Metric: ' + this.line_parameters_2}];
      }
      else if(JSON.parse(localStorage.getItem(this.id + '-config-json')).evaluation.metric == "acc") {
        console.log("hit acc");
        document.getElementById("metric_value_rem_time").style.display= 'none';
        for (let j = 1; j < this.array2.length; j++) {
          if (this.array2[j].includes(this.line_parameters)) {
            const each_label_bar = this.array2[j].split(',')[4];
            const each_data_line = parseFloat(this.array2[j].split(',')[6]);

            labels_line.push(each_label_bar);
            dataset_line.push(each_data_line);
          }

        }
        this.lineChartLabels = labels_line;       //XAxis
        this.lineChartData = [{data: dataset_line, label: 'score' + '/ Metric: ' + this.line_parameters}];
      }

// set bar chart parameters here
      const dataset_bar = [];
      const labels_bar = [];

      for (let i = 1; i < this.array3.length; i++) {
        const each_label_bar = this.array3[i].split(',')[0];
        const each_data_bar = parseFloat(this.array3[i].split(',')[1]);

        labels_bar.push(each_label_bar);
        dataset_bar.push(each_data_bar);
        // this.barChartData[i-1]={ data: [each_data], label: each_label};
        // this.barChartLabels[i-1] = each_label;
      }
      this.barChartLabels = labels_bar;
      this.barChartData = [{data: dataset_bar, label: this.array3[0].split(',')[1]}];
// console.log(labels_bar);
// console.log(dataset_bar);


      //polling
      /*    let interval = setInterval(() => {
            let url = location.href
            let site = url.lastIndexOf("\/");
            let loc = url.substring(site + 1, url.length);
            if (loc == "training-list-detail/" + this.id) {
              console.log("refresh")
            } else {
              clearInterval(interval);
            }
          }, 5000);*/

    })


  }



clearValue()
{

(<HTMLInputElement>document.getElementById('metric_value_label')).value = "";
(<HTMLInputElement>document.getElementById('metric_value_rem_time')).value = "";
}

getValue()
{
//  console.log( (<HTMLInputElement>document.getElementById('metric_value')).value);
this.line_parameters = this.selectedMetric_label;
this.line_parameters_2 = this.selectedMetric_remtime;
//console.log("check here:"+ this.selectedMetric_label);

/*this.line_parameters_2 = (<HTMLInputElement>document.getElementById('metric_value_rem_time')).value;*/
this.ngOnInit();
}



downloadPredictor() {
  this.LocalStorage.get(this.id +'zip').then((data) => {

   const link = document.createElement('a');
   const file = <Blob>data;

   link.setAttribute('href', window.URL.createObjectURL(file));
   link.setAttribute('download', this.id + '.zip');
   link.style.visibility = 'hidden';
   document.body.appendChild(link);
   link.click();
   document.body.removeChild(link);
 })
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

getPointCategoryName(point, dimension) {
  const series = point.series,
    isY = dimension === "y",
    axis = series[isY ? "yAxis" : "xAxis"];
  return axis.categories[point[isY ? "y" : "x"]];
  }

  plotGraph(dataInstance) {
     // ## Get data from detailed-csv file
    // for diagram 1: ACTUAL VS PREDICTED (Label)
    if(this.mylist_detailed.includes('Actual') ) {
      console.log("go label here");

      this.array_label = this.mylist_detailed.toString().split(/\n/);
      this.array_label.filter((line: string) => line.trim() !== '').forEach((line: string) => {
        let searchInfo: string[] = [];
        const item = line.split(',');
        for (let i in item) {
            searchInfo.push(item[i]);
        }
        this.spilt_label.push(searchInfo);
      });
    }
    console.log(this.spilt_label);

    this.chartOptions = {
      chart: {
        type: "heatmap",
        marginTop: 40,
        marginBottom: 80,
        plotBorderWidth: 1,
      },
      title: {
        text: ""
      },
      xAxis: {
        categories: [
          this.spilt_label[0][1],
          this.spilt_label[0][2]
        ],
        labels:{
          style:{
            fontSize: '18px'
          }
        },
        title:{
          text: 'Predicted',
          style: {
            fontWeight:'bold',
            fontSize:'20px',
          }
        },
      },
      yAxis: {
        categories: [
          this.spilt_label[1][0],
          this.spilt_label[2][0],
        ],
        labels:{
          style:{
            fontSize: '18px'
          }
        },
        title:{
          text: 'Actual',
          style: {
            fontWeight:'bold',
            fontSize:'20px',
          }
        },
        reversed: true
      },
      colorAxis: {
        min: 0,
        minColor: "#FFFFFF",
        maxColor: Highcharts.getOptions().colors[0]
      },

      legend: {
        align: "right",
        layout: "vertical",
        margin: 0,
        verticalAlign: "top",
        y: 25,
        symbolHeight: 280
      },

      tooltip : {
        formatter: function () {
          return  ' actual ' + '<b>' + this.series.xAxis.categories[this.point.x] + '</b>'+ '<br>'
            + ' predicted ' +  this.series.yAxis.categories[this.point.y]   +'<br>' + ' <b>' + this.point.value  +'</b> times <b>';
        }
      },

      series: [
        {
          name: "title",
          borderWidth: 0,
          type: "heatmap",
          data: [
            [0, 0, parseInt(this.spilt_label[1][1])],
            [1, 0, parseInt(this.spilt_label[1][2])],

            [0, 1, parseInt(this.spilt_label[2][1])],
            [1, 1, parseInt(this.spilt_label[2][2])]
          ],
          dataLabels: {
            enabled: true,
            color: "#000000",
            style:{
                fontSize:'25px'
            }
          }
        }
      ],

      responsive: {
        rules: [
          {
            condition: {
              maxWidth: 800
            },
            chartOptions: {
              yAxis: {
                labels: {
                  formatter: function() {
                    return this.value.toString(0);
                  }
                }
              }
            }
          }
        ]
      }
    };
  }

ngOnDestroy() {
 if (this.mySubscription) {
   this.mySubscription.unsubscribe();
 }
}



}
