import { Component, OnInit } from '@angular/core';
import {NavigationEnd, Router} from '@angular/router'
import {Monitor} from "../../monitor";
import {MonitorService} from "../../monitor.service";

@Component({
  selector: 'app-monitor-viewing',
  templateUrl: './monitor-viewing.component.html',
  styleUrls: ['./monitor-viewing.component.css']
})
export class MonitorViewingComponent implements OnInit {
  MonitorList !: Monitor[];
  mySubscription: any;
  constructor(private monitorService : MonitorService, private router: Router)
  {
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
      this.getMonitors()
  }

  delete(monitor:Monitor)
  {
    this.monitorService.Delete(monitor);
    // location.reload();
    this.router.navigateByUrl("/monitor-viewing")


  }
  getMonitors()
  {
    this.monitorService.getMonitors().
    subscribe(Monitors => this.MonitorList = Monitors);
  }
  select(monitor:Monitor)
  {
    this.monitorService.select(monitor);



  }
  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
  }
}
