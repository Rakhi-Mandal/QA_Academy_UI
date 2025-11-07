// calendar.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatBadgeModule } from '@angular/material/badge';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatRippleModule } from '@angular/material/core';
import { MatButtonToggleModule } from '@angular/material/button-toggle';

interface CalendarItem {
  id: string;
  name: string;
  subtitle?: string;
  platform: string;
  date: Date;
  type: 'assignment' | 'certification';
  completed: boolean;
}

interface CalendarDay {
  date: Date;
  items: CalendarItem[];
  isCurrentMonth: boolean;
  isToday: boolean;
}

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatToolbarModule,
    MatBadgeModule,
    MatTooltipModule,
    MatMenuModule,
    MatProgressBarModule,
    MatRippleModule,
    MatButtonToggleModule
  ],
  templateUrl: './calendar.component.html',
  styleUrl: './calendar.component.css'
})
export class CalendarComponent {
  currentView: 'timeline' | 'calendar' = 'timeline';
  filterType: 'all' | 'assignments' | 'certifications' = 'all';
  currentCalendarDate: Date = new Date(2025, 10, 1); // November 2025

  assignments: CalendarItem[] = [
    { id: 'A1A', name: 'Assessment 1A: Knowledge Assessment', subtitle: 'scenario-based quiz', platform: 'ProProfs – Online QA quizzes', date: new Date('2025-11-08'), type: 'assignment', completed: false },
    { id: 'A1B', name: 'Assessment 1B: SHL - QA Domain Knowledge', subtitle: 'Cognitive & Logical', platform: 'Adaface -For QA', date: new Date('2025-11-15'), type: 'assignment', completed: false },
    { id: 'A1C', name: 'Assessment 1C: HireVue', subtitle: 'Communication & Team Fit', platform: 'TestLodge – Scenario-based', date: new Date('2025-11-22'), type: 'assignment', completed: false },
    { id: 'A2A', name: 'Assessment 2A: HankerRank', subtitle: 'Code Quality Challenge', platform: 'Adaface -Programming', date: new Date('2025-11-29'), type: 'assignment', completed: false },
    { id: 'A2B', name: 'Assessment 2B: Codility', subtitle: 'Algorithmic challenges', platform: 'Codility', date: new Date('2025-12-06'), type: 'assignment', completed: false },
    { id: 'A2C', name: 'Assessment 2C: LeetCode', subtitle: 'Coding practice & timed challenges', platform: 'LeetCode', date: new Date('2025-12-13'), type: 'assignment', completed: false },
    { id: 'A3A', name: 'Assessment 3A: HackerRank', subtitle: 'Automation Challenges', platform: 'HackerRank', date: new Date('2025-12-20'), type: 'assignment', completed: false },
    { id: 'A3B', name: 'Assessment 3B: Hands-on Project', subtitle: 'Automation Tools', platform: 'Adaface', date: new Date('2025-12-27'), type: 'assignment', completed: false },
    { id: 'A3C', name: 'Assessment 3C: TestDome', subtitle: 'Observability & Reporting', platform: 'TestDome', date: new Date('2026-01-03'), type: 'assignment', completed: false },
    { id: 'A4A', name: 'Assessment 4A: Online Assessment', subtitle: 'CI/CD & Version Control', platform: 'Online Assessment', date: new Date('2026-01-10'), type: 'assignment', completed: false },
    { id: 'A4B', name: 'Assessment 4B: HackerRank / Codility', subtitle: 'Coding Challenges', platform: 'HackerRank / Codility', date: new Date('2026-01-17'), type: 'assignment', completed: false },
    { id: 'A4C', name: 'Assessment 4C: Katalon Test Challenge', subtitle: 'Automation test challenges', platform: 'Katalon', date: new Date('2026-01-24'), type: 'assignment', completed: false },
    { id: 'A5A', name: 'Assessment 5A: Framework Design', subtitle: 'Framework Design and Presentation', platform: 'Presentation', date: new Date('2026-01-31'), type: 'assignment', completed: false },
    { id: 'A5B', name: 'Assessment 5B: Codility', subtitle: 'Framework based assessment', platform: 'Codility', date: new Date('2026-02-07'), type: 'assignment', completed: false },
    { id: 'A5C', name: 'Assessment 5C: TestDome', subtitle: 'coding and problem solving', platform: 'TestDome', date: new Date('2026-02-14'), type: 'assignment', completed: false },
    { id: 'A6A', name: 'Assessment 6A: Security & AI Assessment', subtitle: 'Security Assessment', platform: 'Codility, Adaface -Artificial Intelligence', date: new Date('2026-02-21'), type: 'assignment', completed: false },
    { id: 'A6B', name: 'Assessment 6B: Performance & Cloud', subtitle: 'Performance Baseline', platform: 'Codility, Adaface -Cloud', date: new Date('2026-02-28'), type: 'assignment', completed: false },
    { id: 'A6C', name: 'Assessment 6C: GDPR and Compliance', subtitle: 'GDPR and Compliance Assessment', platform: 'Enobyte and Adaface', date: new Date('2026-03-07'), type: 'assignment', completed: false },
    { id: 'A6D', name: 'Assessment 6D: QE Innovation Hackathon', subtitle: 'Innovation Hackathon', platform: 'Hackathon', date: new Date('2026-03-14'), type: 'assignment', completed: false }
  ];

  certifications: CalendarItem[] = [
    { id: 'C1', name: 'Java Foundation Certification', platform: 'Java Foundation', date: new Date('2025-12-01'), type: 'certification', completed: false },
    { id: 'C2', name: 'Python Foundation Certification', platform: 'Python Foundation', date: new Date('2025-12-11'), type: 'certification', completed: false },
    { id: 'C3', name: 'Python Certified Associate Tester', platform: 'PCEP Certification', date: new Date('2025-12-21'), type: 'certification', completed: false },
    { id: 'C4', name: 'LambdaTest Certification', platform: 'LambdaTest tool based', date: new Date('2025-12-31'), type: 'certification', completed: false },
    { id: 'C5', name: 'Selenium Automation Testing', platform: 'Certified Professional – Selenium', date: new Date('2026-01-10'), type: 'certification', completed: false },
    { id: 'C6', name: 'Certified Jenkins Engineer', platform: 'Jenkins Certification', date: new Date('2026-01-20'), type: 'certification', completed: false },
    { id: 'C7', name: 'ISTQB Foundation Level v4.0', platform: 'Certified Tester Foundation Level', date: new Date('2026-01-30'), type: 'certification', completed: false },
    { id: 'C8', name: 'Certified Tester AI Testing', platform: 'CT-AI Certification', date: new Date('2026-02-09'), type: 'certification', completed: false },
    { id: 'C9', name: 'HIPAA Foundation Certification', platform: 'HIPAA Foundation', date: new Date('2026-02-19'), type: 'certification', completed: false },
    { id: 'C10', name: 'Azure DevOps AZ-400', platform: 'Azure DevOps Course with Certification', date: new Date('2026-03-01'), type: 'certification', completed: false },
    { id: 'C11', name: 'Azure AI Fundamentals', platform: 'Microsoft Certified: Azure AI', date: new Date('2026-03-11'), type: 'certification', completed: false },
    { id: 'C12', name: 'Security, Compliance and Identity', platform: 'Microsoft Certified', date: new Date('2026-03-21'), type: 'certification', completed: false }
  ];

  get allItems(): CalendarItem[] {
    return [...this.assignments, ...this.certifications].sort((a, b) => a.date.getTime() - b.date.getTime());
  }

  get filteredItems(): CalendarItem[] {
    if (this.filterType === 'all') {
      return this.allItems;
    } else if (this.filterType === 'assignments') {
      return this.assignments.sort((a, b) => a.date.getTime() - b.date.getTime());
    } else {
      return this.certifications.sort((a, b) => a.date.getTime() - b.date.getTime());
    }
  }

  get totalAssignments(): number {
    return this.assignments.length;
  }

  get totalCertifications(): number {
    return this.certifications.length;
  }

  get completedItems(): number {
    return this.allItems.filter(item => item.completed).length;
  }

  get remainingItems(): number {
    return this.allItems.filter(item => !item.completed).length;
  }

  get progressPercentage(): number {
    const total = this.allItems.length;
    return total > 0 ? (this.completedItems / total) * 100 : 0;
  }

  get calendarDays(): CalendarDay[] {
    const year = this.currentCalendarDate.getFullYear();
    const month = this.currentCalendarDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());
    
    const days: CalendarDay[] = [];
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    for (let i = 0; i < 42; i++) {
      const currentDate = new Date(startDate);
      currentDate.setDate(startDate.getDate() + i);
      currentDate.setHours(0, 0, 0, 0);
      
      const items = this.filteredItems.filter(item => {
        const itemDate = new Date(item.date);
        itemDate.setHours(0, 0, 0, 0);
        return itemDate.getTime() === currentDate.getTime();
      });
      
      days.push({
        date: currentDate,
        items: items,
        isCurrentMonth: currentDate.getMonth() === month,
        isToday: currentDate.getTime() === today.getTime()
      });
    }
    
    return days;
  }

  get currentMonthYear(): string {
    return this.currentCalendarDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  }

  setView(view: 'timeline' | 'calendar'): void {
    this.currentView = view;
  }

  setFilter(filter: 'all' | 'assignments' | 'certifications'): void {
    this.filterType = filter;
  }

  previousMonth(): void {
    this.currentCalendarDate = new Date(this.currentCalendarDate.getFullYear(), this.currentCalendarDate.getMonth() - 1, 1);
  }

  nextMonth(): void {
    this.currentCalendarDate = new Date(this.currentCalendarDate.getFullYear(), this.currentCalendarDate.getMonth() + 1, 1);
  }

  formatDate(date: Date): string {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: '2-digit' };
    return date.toLocaleDateString('en-US', options);
  }

  getDayName(date: Date): string {
    const options: Intl.DateTimeFormatOptions = { weekday: 'long' };
    return date.toLocaleDateString('en-US', options);
  }

  toggleComplete(item: CalendarItem): void {
    item.completed = !item.completed;
  }
}