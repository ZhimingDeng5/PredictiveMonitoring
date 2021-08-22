import { Dashboard } from './models/dashboard.model';

export interface AppState {
  readonly dashboard: Dashboard[];
}