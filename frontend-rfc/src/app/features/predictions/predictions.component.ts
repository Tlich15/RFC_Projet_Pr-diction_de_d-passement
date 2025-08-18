import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-predictions',
  templateUrl: './predictions.component.html',
  styleUrls: ['./predictions.component.scss']
})
export class PredictionsComponent implements OnInit {
  predictions: any[] = [];
  filteredPredictions: any[] = [];
  loading = false;
  error: string | null = null;
  client: string | null = null;
  searchTerm = '';
  uniqueClientsCount = 0;
  
  // Pagination
  currentPage = 1;
  pageSize = 10;
  totalPages = 1;
  
  // History modal
  selectedClient: any = null;
  showHistory = false;

  constructor(
    private api: ApiService, 
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParamMap.subscribe(params => {
      const c = params.get('client');
      this.client = c;
      this.fetch();
    });
  }

  private computeUniqueClientsCount(list: any[]): number {
    const names = list.map(p => (p.Client || p.client || '').toString().trim()).filter(Boolean);
    return new Set(names).size;
  }

  fetch(): void {
    this.loading = true;
    this.error = null;
    const obs = this.client ? this.api.getClientPredictions(this.client) : this.api.getPredictions();
    obs.subscribe({
      next: (data) => { 
        this.predictions = data; 
        this.filteredPredictions = data;
        this.uniqueClientsCount = this.computeUniqueClientsCount(this.filteredPredictions);
        this.currentPage = 1;
        this.calculatePagination();
        this.loading = false; 
      },
      error: () => { 
        this.error = 'Erreur de chargement'; 
        this.loading = false; 
      }
    });
  }

  onSearch(): void {
    if (!this.searchTerm.trim()) {
      this.filteredPredictions = this.predictions;
    } else {
      this.filteredPredictions = this.predictions.filter(pred => 
        (pred.Client || pred.client || '').toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    }
    this.uniqueClientsCount = this.computeUniqueClientsCount(this.filteredPredictions);
    this.currentPage = 1;
    this.calculatePagination();
  }

  calculatePagination(): void {
    this.totalPages = Math.ceil(this.filteredPredictions.length / this.pageSize);
  }

  get paginatedPredictions(): any[] {
    const startIndex = (this.currentPage - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    return this.filteredPredictions.slice(startIndex, endIndex);
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  getPageNumbers(): number[] {
    const pages: number[] = [];
    const maxVisible = 5;
    let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
    let end = Math.min(this.totalPages, start + maxVisible - 1);
    
    if (end - start + 1 < maxVisible) {
      start = Math.max(1, end - maxVisible + 1);
    }
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  }

  selectClient(client: any): void {
    this.selectedClient = client;
    this.showHistory = true;
  }

  closeHistory(): void {
    this.showHistory = false;
    this.selectedClient = null;
  }

  getHistoryUrl(client: any): string {
    return this.api.getClientHistoryPngUrl(client.Client || client.client);
  }

  onImageError(event: any): void {
    console.error('Erreur de chargement de l\'image:', event);
    // Optionnel : afficher un message d'erreur ou une image par défaut
  }

  goBackToClients(): void {
    this.router.navigate(['/clients']);
  }

  viewClientHistory(clientName: string): void {
    this.router.navigate(['/clients'], { queryParams: { view: 'history', client: clientName } });
  }
}
