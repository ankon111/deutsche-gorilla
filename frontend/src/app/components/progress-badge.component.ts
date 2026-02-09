import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-progress-badge',
  standalone: true,
  template: `
    <div class="badge" style="background: var(--electric-mint); color: #080808;">
      {{ label }}: {{ value }}
    </div>
  `
})
export class ProgressBadgeComponent {
  @Input() label = 'Progress';
  @Input() value: number | string = 0;
}
