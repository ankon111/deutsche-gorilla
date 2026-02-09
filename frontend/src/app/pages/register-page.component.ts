import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register-page',
  standalone: true,
  imports: [FormsModule],
  template: `
    <section class="page">
      <div class="card" style="max-width:420px; margin:0 auto;">
        <h2>Register</h2>
        <label>Username</label>
        <input class="input" [(ngModel)]="username" />
        <label style="margin-top:12px;">Email</label>
        <input class="input" [(ngModel)]="email" />
        <label style="margin-top:12px;">Password</label>
        <input class="input" type="password" [(ngModel)]="password" />
        <button class="btn" style="margin-top:16px; width:100%;">Create account</button>
      </div>
    </section>
  `
})
export class RegisterPageComponent {
  username = '';
  email = '';
  password = '';
}
