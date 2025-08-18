import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClientsComponent } from './features/clients/clients.component';
import { PredictionsComponent } from './features/predictions/predictions.component';

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'clients' },
  { path: 'clients', component: ClientsComponent },
  { path: 'predictions', component: PredictionsComponent },
  { path: '**', redirectTo: 'clients' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
