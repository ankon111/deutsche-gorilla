import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-ai-chat-box',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="card">
      <h3>{{ title }}</h3>
      <div style="margin-bottom: 12px; color: var(--ash-grey);">
        {{ description }}
      </div>
      <textarea class="input" rows="4" [(ngModel)]="message"></textarea>
      <button class="btn" style="margin-top: 12px;">Send</button>
    </div>
  `
})
export class AiChatBoxComponent {
  @Input() title = 'AI Assistant';
  @Input() description = 'Ask anything about German vocabulary or grammar.';
  message = '';
}
