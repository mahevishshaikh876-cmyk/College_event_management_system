import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {

  college_name = 'SMSMPITR';
  college_tagline = 'College Event Management System';

  total_events = 5;
  total_registrations = 120;
  total_categories = 4;

  search_query = '';
  current_category = '';
  sort_by = 'date';

  events = [
    {
      id: 1,
      title: 'Hackathon',
      description: '24 Hour Coding Competition',
      category: 'Technical',
      date: '10 July 2026',
      time: '10:00 AM',
      venue: 'Auditorium',
      current_registrations: 40,
      max_capacity: 100
    },
    {
      id: 2,
      title: 'Football Tournament',
      description: 'Inter College Sports Event',
      category: 'Sports',
      date: '15 July 2026',
      time: '09:00 AM',
      venue: 'Sports Ground',
      current_registrations: 60,
      max_capacity: 80
    },
    {
      id: 3,
      title: 'Dance Competition',
      description: 'Annual Cultural Festival',
      category: 'Cultural',
      date: '20 July 2026',
      time: '05:00 PM',
      venue: 'Main Hall',
      current_registrations: 25,
      max_capacity: 50
    }
  ];

  constructor() { }

  register(eventId: number) {
    console.log('Register Event:', eventId);
  }

  searchEvents() {
    console.log('Search:', this.search_query);
  }

}