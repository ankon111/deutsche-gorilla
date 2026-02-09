import { Component } from '@angular/core';

@Component({
  selector: 'app-grammar-page',
  standalone: true,
  template: `
    <section class="page">
      <div class="card">
        <h2>Grammar Lessons</h2>
        <p style="color: var(--ash-grey);">Future-ready grammar content by CEFR level.</p>
        <div class="grid two" style="margin-top:16px;">
          <div class="card" style="background: var(--slate);">
            <h3>A1 Basics</h3>
            <p>Article usage and simple sentence structure.</p>
          </div>
          <div class="card" style="background: var(--slate);">
            <h3>B1 Cases</h3>
            <p>Accusative vs dative deep dive.</p>
          </div>
        </div>
      </div>
    </section>
  `
})
export class GrammarPageComponent {}
