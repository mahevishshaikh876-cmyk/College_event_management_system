import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.css'
})
export class AdminDashboard {

  constructor(private router: Router) { }

  category_count = 4;

  newEvent = {
    title: '',
    category: 'Technical',
    description: '',
    venue: '',
    date: '',
    time: '',
    max_capacity: 50
  };

  events = [
    {
      id: 1,
      title: 'Hackathon',
      category: 'Technical',
      description: '24 Hour Coding Competition',
      date: '10 July 2026',
      time: '10:00 AM',
      venue: 'Seminar Hall',
      current_registrations: 20,
      max_capacity: 50
    },
    {
      id: 2,
      title: 'Football Tournament',
      category: 'Sports',
      description: 'Inter College Sports Event',
      date: '15 July 2026',
      time: '9:00 AM',
      venue: 'Ground',
      current_registrations: 35,
      max_capacity: 50
    }
  ];

  registrations = [
    {
      student_name: 'Rahul Sharma',
      student_email: 'rahul@example.com',
      student_roll: 'CS23001',
      student_branch: 'Computer Science',
      event_title: 'Hackathon',
      registration_date: '05 July 2026'
    },
    {
      student_name: 'Priya Patel',
      student_email: 'priya@example.com',
      student_roll: 'IT23015',
      student_branch: 'Information Technology',
      event_title: 'Football Tournament',
      registration_date: '06 July 2026'
    }
  ];

  addEvent() {

    this.events.push({
      id: this.events.length + 1,
      title: this.newEvent.title,
      category: this.newEvent.category,
      description: this.newEvent.description,
      venue: this.newEvent.venue,
      date: this.newEvent.date,
      time: this.newEvent.time,
      current_registrations: 0,
      max_capacity: this.newEvent.max_capacity
    });

    this.newEvent = {
      title: '',
      category: 'Technical',
      description: '',
      venue: '',
      date: '',
      time: '',
      max_capacity: 50
    };

    alert('Event Added Successfully');
  }

  deleteEvent(id: number) {
    this.events = this.events.filter(event => event.id !== id);
  }

  exportCSV() {
    alert('Export CSV Feature');
  }

  logout() {
    this.router.navigate(['/admin-login']);
  }

}