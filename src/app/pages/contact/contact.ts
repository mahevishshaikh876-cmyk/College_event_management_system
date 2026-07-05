import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './contact.html',
  styleUrl: './contact.css'
})
export class Contact {

  college_name = 'SMSMPITR';

  college_full_name =
    'Sahakar Maharshi Shankarrao Mohite Patil Institute of Technology & Research';

  college_tagline = 'Excellence in Education & Innovation';

  college_email = 'smcht@gmail.com';

  college_phone = '+91 21852 22354';

  college_address = 'SMSMPITR Campus, Akluj, Maharashtra';

  college_website = 'https://www.smsmpitr.edu.in';

}