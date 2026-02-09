import { Component } from '@angular/core';

@Component({
  selector: 'app-flashcards-page',
  standalone: true,
  template: `
    <section class="page">
      <div class="card" style="text-align:center; max-width:480px; margin:0 auto;">
        <h2>Flashcards</h2>
        <div style="font-size:32px; margin:24px 0;">gehen</div>
        <div class="badge">Verb • A1</div>
        <div style="display:flex; gap:12px; margin-top:24px; justify-content:center;">
          <button class="btn secondary">Again</button>
          <button class="btn secondary">Hard</button>
          <button class="btn">Learned</button>
        </div>
      </div>
    </section>
  `
})
export class FlashcardsPageComponent {}
