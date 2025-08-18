import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-clients',
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.scss']
})
export class ClientsComponent implements OnInit {
  clients: any[] = [];
  filteredClients: any[] = [];
  loading = false;
  error: string | null = null;
  searchTerm = '';
  selectedClient: any = null;
  showHistory = false;
  
  // Pagination
  currentPage = 1;
  pageSize = 10;
  totalPages = 1;

  constructor(public api: ApiService) {}

  ngOnInit(): void {
    this.fetch();
  }

  private calculatePagination(): void {
    this.totalPages = Math.ceil(this.filteredClients.length / this.pageSize);
  }

  get paginatedClients(): any[] {
    const startIndex = (this.currentPage - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    return this.filteredClients.slice(startIndex, endIndex);
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

  fetch(): void {
    this.loading = true;
    this.error = null;
    this.api.getClients().subscribe({
      next: (data) => {
        this.clients = data;
        this.filteredClients = data;
        this.currentPage = 1;
        this.calculatePagination();
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Erreur de chargement';
        this.loading = false;
      }
    });
  }

  onSearch(): void {
    if (!this.searchTerm.trim()) {
      this.filteredClients = this.clients;
    } else {
      this.filteredClients = this.clients.filter(client =>
        (client.client_name || client.Client || '').toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    }
    this.currentPage = 1;
    this.calculatePagination();
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
    return this.api.getClientHistoryPngUrl(client.client_name || client.Client);
  }
}
