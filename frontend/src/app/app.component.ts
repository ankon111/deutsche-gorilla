import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  template: `
    <header class="card" style="margin:16px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <strong>DeutschGorilla</strong>
        <span class="badge" style="margin-left:8px;">Beta</span>
      </div>
      <nav style="display:flex; gap:12px;">
        <a routerLink="/">Home</a>
        <a routerLink="/dictionary">Dictionary</a>
        <a routerLink="/flashcards">Flashcards</a>
        <a routerLink="/quiz">Quiz</a>
        <a routerLink="/settings">Settings</a>
      </nav>
    </header>
    <router-outlet></router-outlet>
  `
})
export class AppComponent {}
