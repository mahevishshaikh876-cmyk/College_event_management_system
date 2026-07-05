import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class EventService {

    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) { }

    // ================= EVENTS =================

    getEvents(): Observable<any> {
        return this.http.get(`${this.baseUrl}/`);
    }

    addEvent(data: any): Observable<any> {
        return this.http.post(`${this.baseUrl}/admin/add_event`, data);
    }

    deleteEvent(id: number): Observable<any> {
        return this.http.post(`${this.baseUrl}/admin/delete_event/${id}`, {});
    }

    // ================= REGISTRATION =================

    registerStudent(eventId: number, data: any): Observable<any> {
        return this.http.post(`${this.baseUrl}/register/${eventId}`, data);
    }

    // ================= ADMIN =================

    adminLogin(data: any): Observable<any> {
        return this.http.post(`${this.baseUrl}/admin/login`, data);
    }

    adminLogout(): Observable<any> {
        return this.http.get(`${this.baseUrl}/admin/logout`);
    }

    getAdminDashboard(): Observable<any> {
        return this.http.get(`${this.baseUrl}/admin`);
    }

    // ================= CSV EXPORT =================

    exportCSV(): Observable<Blob> {
        return this.http.get(`${this.baseUrl}/admin/export_csv`, {
            responseType: 'blob'
        });
    }

}