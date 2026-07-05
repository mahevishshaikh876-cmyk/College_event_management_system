import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './about.html',
  styleUrl: './about.css'
})
export class About {

  college_name = 'SMSMPITR';

  college_full_name = 'Shri Madhukarrao Shankarrao Patil Institute of Technology & Research';

}