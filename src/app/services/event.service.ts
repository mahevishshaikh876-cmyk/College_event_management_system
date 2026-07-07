import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class EventService {

    private apiUrl = 'http://127.0.0.1:5000/api';

    constructor(private http: HttpClient) { }

    getEvents(): Observable<any> {
        return this.http.get(`${this.apiUrl}/events`);
    }

    registerStudent(eventId: number, data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/register/${eventId}`, data);
    }

    adminLogin(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/login`, data);
    }
}