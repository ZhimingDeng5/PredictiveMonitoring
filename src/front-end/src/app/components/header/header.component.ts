import { Component, OnInit } from '@angular/core';
import {Location} from '@angular/common';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(private _location: Location) { }

  onBack(): void {
    this._location.back()
  }

  ngOnInit(): void {
  }

}
