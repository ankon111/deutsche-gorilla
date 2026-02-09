import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dictionary-page',
  standalone: true,
  imports: [FormsModule],
  template: `
    <section class="page">
      <div class="card">
        <h2>Dictionary</h2>
        <div class="grid two">
          <input class="input" placeholder="Search word" [(ngModel)]="search" />
          <select class="input" [(ngModel)]="pos">
            <option value="">All POS</option>
            <option value="Noun">Noun</option>
            <option value="Verb">Verb</option>
            <option value="Adjective">Adjective</option>
          </select>
          <select class="input" [(ngModel)]="level">
            <option value="">All Levels</option>
            <option value="A1">A1</option>
            <option value="A2">A2</option>
            <option value="B1">B1</option>
            <option value="B2">B2</option>
            <option value="C1">C1</option>
            <option value="C2">C2</option>
          </select>
        </div>
      </div>
      <div class="grid two">
        <div class="card" *ngFor="let word of words">
          <h3>{{ word.word }}</h3>
          <div class="badge">{{ word.pos }} • {{ word.level }}</div>
          <p style="color: var(--ash-grey);">{{ word.translation }}</p>
        </div>
      </div>
    </section>
  `
})
export class DictionaryPageComponent {
  search = '';
  pos = '';
  level = '';
  words = [
    { word: 'Haus', pos: 'Noun', level: 'A1', translation: 'house' },
    { word: 'lernen', pos: 'Verb', level: 'A1', translation: 'to learn' }
  ];
}
