import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  health(): Observable<{ status: string }> {
    return this.http.get<{ status: string }>(`${this.baseUrl}/health`);
  }

  dataStatus(): Observable<any> {
    return this.http.get(`${this.baseUrl}/data/status`);
  }

  loadData(): Observable<any> {
    return this.http.post(`${this.baseUrl}/data/load`, {});
  }

  getClients(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/clients/`);
  }

  getPredictions(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/predictions/`);
  }

  getClientHistory(client: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/clients/history`, { params: { client } });
  }

  getClientPredictions(client: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/clients/predictions`, { params: { client } });
  }

  getClientHistoryPngUrl(client: string): string {
    return `${this.baseUrl}/visualizations/client-history.png?client=${encodeURIComponent(client)}`;
  }
}
