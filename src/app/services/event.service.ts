import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class EventService {

    // Flask Backend URL
    private apiUrl = 'http://127.0.0.1:5000/api';

    constructor(private http: HttpClient) { }

    // Get All Events
    getEvents(): Observable<any> {
        return this.http.get(`${this.apiUrl}/events`);
    }

    // Get Single Event
    getEventById(eventId: number): Observable<any> {
        return this.http.get(`${this.apiUrl}/events/${eventId}`);
    }

    // Student Registration
    registerStudent(eventId: number, data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/register/${eventId}`, data);
    }

    // Admin Login
    adminLogin(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/login`, data);
    }

    // Admin Dashboard Events
    getAdminEvents(): Observable<any> {
        return this.http.get(`${this.apiUrl}/admin/events`);
    }

    // Add Event
    addEvent(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/admin/events`, data);
    }

    // Update Event
    updateEvent(eventId: number, data: any): Observable<any> {
        return this.http.put(`${this.apiUrl}/admin/events/${eventId}`, data);
    }

    // Delete Event
    deleteEvent(eventId: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}/admin/events/${eventId}`);
    }

    // Get All Registrations
    getRegistrations(): Observable<any> {
        return this.http.get(`${this.apiUrl}/registrations`);
    }

}
