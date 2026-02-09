import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AiChatBoxComponent } from '../components/ai-chat-box.component';
import { ProgressBadgeComponent } from '../components/progress-badge.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [RouterLink, AiChatBoxComponent, ProgressBadgeComponent],
  template: `
    <section class="page">
      <div class="card">
        <h1>Welcome to DeutschGorilla</h1>
        <p style="color: var(--ash-grey);">Your German vocabulary trainer with AI-powered support.</p>
        <div class="grid two" style="margin-top: 16px;">
          <app-progress-badge label="Learned" value="120"></app-progress-badge>
          <app-progress-badge label="Daily Goal" value="8/20"></app-progress-badge>
        </div>
        <div style="display:flex; gap:12px; margin-top: 16px;">
          <a class="btn" routerLink="/flashcards">Flashcards</a>
          <a class="btn secondary" routerLink="/dictionary">Dictionary</a>
          <a class="btn secondary" routerLink="/quiz">Quiz</a>
        </div>
      </div>
      <app-ai-chat-box
        title="General AI Chat"
        description="Ask questions about German grammar, vocabulary, or study tips."
      ></app-ai-chat-box>
    </section>
  `
})
export class HomePageComponent {}
