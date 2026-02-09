import { Component } from '@angular/core';
import { AiChatBoxComponent } from '../components/ai-chat-box.component';

@Component({
  selector: 'app-word-detail-page',
  standalone: true,
  imports: [AiChatBoxComponent],
  template: `
    <section class="page">
      <div class="card">
        <h2>Haus</h2>
        <div class="badge">Noun • A1</div>
        <h3 style="margin-top: 16px;">Translations</h3>
        <ul>
          <li>English: house</li>
          <li>Bangla: বাড়ি</li>
        </ul>
        <h3>Examples</h3>
        <ul>
          <li>Das Haus ist groß.</li>
          <li>Ich gehe nach Hause.</li>
        </ul>
        <button class="btn">Generate more examples</button>
      </div>
      <app-ai-chat-box
        title="Word Assistant"
        description="Ask about usage, grammar, or context for this word."
      ></app-ai-chat-box>
    </section>
  `
})
export class WordDetailPageComponent {}
