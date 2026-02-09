import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LocalStorageService } from '../services/local-storage.service';

@Component({
  selector: 'app-settings-page',
  standalone: true,
  imports: [FormsModule],
  template: `
    <section class="page">
      <div class="card" style="max-width:520px; margin:0 auto;">
        <h2>Settings</h2>
        <label>Default Mode</label>
        <select class="input" [(ngModel)]="defaultMode">
          <option value="flashcards">Flashcards</option>
          <option value="dictionary">Dictionary</option>
          <option value="quiz">Quiz</option>
        </select>
        <label style="margin-top:12px;">Daily Limit</label>
        <input class="input" type="number" [(ngModel)]="dailyLimit" />
        <label style="margin-top:12px;">Language View</label>
        <select class="input" [(ngModel)]="languageDisplay">
          <option value="bn">Bangla</option>
          <option value="en">English</option>
          <option value="both">Both</option>
        </select>
        <label style="margin-top:12px;">AI Provider</label>
        <select class="input" [(ngModel)]="aiProvider">
          <option value="openai">OpenAI</option>
          <option value="gemini">Gemini</option>
        </select>
        <label style="margin-top:12px;">OpenAI API Key</label>
        <input class="input" [(ngModel)]="openAiKey" />
        <label style="margin-top:12px;">Gemini API Key</label>
        <input class="input" [(ngModel)]="geminiKey" />
        <button class="btn" style="margin-top:16px;" (click)="save()">Save</button>
      </div>
    </section>
  `
})
export class SettingsPageComponent {
  defaultMode = 'flashcards';
  dailyLimit = 20;
  languageDisplay = 'both';
  aiProvider = 'openai';
  openAiKey = '';
  geminiKey = '';

  constructor(private storage: LocalStorageService) {}

  save(): void {
    this.storage.set('ai_provider', this.aiProvider);
    this.storage.set('openai_api_key', this.openAiKey);
    this.storage.set('gemini_api_key', this.geminiKey);
    this.storage.set('language_display', this.languageDisplay);
  }
}
