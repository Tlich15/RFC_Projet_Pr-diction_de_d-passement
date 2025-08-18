import { Component } from '@angular/core';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent {
  status: any[] = [];
  loading = false;
  loadingLoad = false;
  message: string | null = null;

  constructor(private api: ApiService) {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    this.api.dataStatus().subscribe({
      next: (s) => { this.status = s; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }

  loadAll(): void {
    this.loadingLoad = true;
    this.api.loadData().subscribe({
      next: () => { this.loadingLoad = false; this.message = 'Chargement terminé'; this.refresh(); },
      error: () => { this.loadingLoad = false; this.message = 'Erreur de chargement'; }
    });
  }
}
