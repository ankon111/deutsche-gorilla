import { Routes } from '@angular/router';

import { HomePageComponent } from './pages/home-page.component';
import { LoginPageComponent } from './pages/login-page.component';
import { RegisterPageComponent } from './pages/register-page.component';
import { DictionaryPageComponent } from './pages/dictionary-page.component';
import { FlashcardsPageComponent } from './pages/flashcards-page.component';
import { QuizPageComponent } from './pages/quiz-page.component';
import { WordDetailPageComponent } from './pages/word-detail-page.component';
import { SettingsPageComponent } from './pages/settings-page.component';
import { GrammarPageComponent } from './pages/grammar-page.component';

export const routes: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'login', component: LoginPageComponent },
  { path: 'register', component: RegisterPageComponent },
  { path: 'dictionary', component: DictionaryPageComponent },
  { path: 'flashcards', component: FlashcardsPageComponent },
  { path: 'quiz', component: QuizPageComponent },
  { path: 'word/:id', component: WordDetailPageComponent },
  { path: 'settings', component: SettingsPageComponent },
  { path: 'grammar', component: GrammarPageComponent }
];
