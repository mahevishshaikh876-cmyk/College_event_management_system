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

  events: any[] = [];
  register(eventId: number) {
    console.log('Register Event:', eventId);
  }

  searchEvents() {
    console.log('Search:', this.search_query);
  }

}
