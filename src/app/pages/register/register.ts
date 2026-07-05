import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class Register {

  event = {
    id: 1,
    title: 'College Event',
    description: 'Event Description',
    date: '10 July 2026',
    time: '10:00 AM',
    venue: 'College Auditorium',
    max_capacity: 100,
    current_registrations: 25
  };

  student = {
    student_name: '',
    student_email: '',
    student_roll: '',
    student_branch: ''
  };

  register() {
    console.log('Registration Submitted');
    console.log(this.student);

    alert('Registration Successful!');
  }

}