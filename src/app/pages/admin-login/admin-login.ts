import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';

@Component({
  selector: 'app-admin-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './admin-login.html',
  styleUrls: ['./admin-login.css']
})
export class AdminLogin {

  username: string = '';
  password: string = '';

  constructor(private router: Router) { }

  login() {

    if (this.username === 'admin' && this.password === 'admin123') {

      alert('Login Successful');

      this.router.navigate(['/admin-dashboard']);

    } else {

      alert('Invalid Username or Password');

    }

  }

}