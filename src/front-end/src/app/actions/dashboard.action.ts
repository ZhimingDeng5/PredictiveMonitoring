// Section 1
import { Injectable } from '@angular/core'
import { Action } from '@ngrx/store'
import { Dashboard } from './../models/dashboard.model'

// Section 2
export const ADD_DASHBOARD       = '[Dashboard] Add'
export const REMOVE_DASHBOARD    = '[Dashboard] Remove'

// Section 3
export class AddDashboard implements Action {
    readonly type = ADD_DASHBOARD

    constructor(public payload: Dashboard) {}
}

export class RemoveDashboard implements Action {
    readonly type = REMOVE_DASHBOARD

    constructor(public payload: number) {}
}

// Section 4
export type Actions = AddDashboard | RemoveDashboard