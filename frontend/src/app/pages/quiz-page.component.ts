import { Component } from '@angular/core';

@Component({
  selector: 'app-quiz-page',
  standalone: true,
  template: `
    <section class="page">
      <div class="card">
        <h2>Quiz Mode</h2>
        <p style="color: var(--ash-grey);">What is the plural of "das Buch"?</p>
        <div class="grid two" style="margin-top: 16px;">
          <button class="btn secondary">Bücher</button>
          <button class="btn secondary">Buche</button>
          <button class="btn secondary">Buchen</button>
          <button class="btn secondary">Buche</button>
        </div>
        <div style="margin-top: 16px; color: var(--soft-mint);">Score: 4/10</div>
      </div>
    </section>
  `
})
export class QuizPageComponent {}
