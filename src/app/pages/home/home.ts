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
  college_tagline = 'Excellence in Education & Innovation';

  total_events = 4;
  total_registrations = 0;
  total_categories = 4;

  search_query = '';
  current_category = '';
  sort_by = 'date';

  events = [
    {
      id: 1,
      title: 'CodeCraft Hackathon',
      description: 'Showcase your programming and problem-solving skills in this 24-hour national hackathon. Build innovative solutions for real-world challenges.',
      category: 'Technical',
      icon: '💻',
      badgeColor: '#dbe4ff',
      date: '2026-07-15',
      time: '09:00',
      venue: 'Computer Lab 3, IT Block',
      current_registrations: 0,
      max_capacity: 80
    },
    {
      id: 2,
      title: 'Ideathon: Startup Pitch',
      description: 'Got a business idea? Pitch it to top venture capitalists and industry mentors. Cash prizes up to $5000 for the winning startup pitch.',
      category: 'Competitions',
      icon: '🏆',
      badgeColor: '#d8f5df',
      date: '2026-07-18',
      time: '11:00',
      venue: 'Seminar Hall B, Block A',
      current_registrations: 0,
      max_capacity: 50
    },
    {
      id: 3,
      title: 'Symphony Music & Dance Fest',
      description: 'Celebrate art and expression! An evening filled with classical, rock music performances and diverse group dance forms.',
      category: 'Cultural',
      icon: '🎭',
      badgeColor: '#ffe0ef',
      date: '2026-07-20',
      time: '17:00',
      venue: 'Main Auditorium',
      current_registrations: 0,
      max_capacity: 200
    },
    {
      id: 4,
      title: 'Inter-College Cricket Cup',
      description: 'The annual cricket championship where top college teams clash for the ultimate trophy. Exciting matches, trophy rewards, and certificates.',
      category: 'Sports',
      icon: '⚽',
      badgeColor: '#fff1c9',
      date: '2026-07-25',
      time: '08:30',
      venue: 'College Cricket Ground',
      current_registrations: 0,
      max_capacity: 120
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