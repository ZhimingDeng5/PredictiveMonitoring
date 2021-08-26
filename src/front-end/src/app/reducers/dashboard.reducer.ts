import { Action } from '@ngrx/store'
import { Dashboard } from './../models/dashboard.model'
import * as DashboardActions from './../actions/dashboard.actions'

// Section 1
const initialState: Dashboard = {
    csv:null,
    id:'test'
}

// Section 2
export function reducer(state: Dashboard[] = [initialState], action: DashboardActions.Actions) {

    // Section 3
    switch(action.type) {
        case DashboardActions.ADD_DASHBOARD:
            return [...state, action.payload];
        case DashboardActions.CHECK_DASHBOARD:
            return state.find(dashboard => dashboard.id === action.payload).id;
        default:
            return state;
    }
}