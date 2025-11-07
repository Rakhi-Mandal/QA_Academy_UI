import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trigger, transition, style, animate, query, stagger, keyframes, state } from '@angular/animations';
import { CalendarDataService } from '../../shared/services/calendar-data.service';
import { CalendarItem, CalendarStats } from '../../shared/models/calendar.models';
import { Observable } from 'rxjs';

interface CalendarDay {
  date: Date;
  dayNumber: number;
  isCurrentMonth: boolean;
  isToday: boolean;
  items: CalendarItem[];
}

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss'],
  animations: [
    trigger('listAnimation', [
      transition('* => *', [
        query(':enter', [
          style({ opacity: 0, transform: 'translateY(30px) scale(0.9)' }),
          stagger(60, [
            animate('500ms cubic-bezier(0.35, 0, 0.25, 1)', 
              keyframes([
                style({ opacity: 0, transform: 'translateY(30px) scale(0.9)', offset: 0 }),
                style({ opacity: 0.5, transform: 'translateY(-10px) scale(1.05)', offset: 0.5 }),
                style({ opacity: 1, transform: 'translateY(0) scale(1)', offset: 1 })
              ])
            )
          ])
        ], { optional: true })
      ])
    ]),
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.95)' }),
        animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
          style({ opacity: 1, transform: 'scale(1)' })
        )
      ])
    ]),
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(-30px)', opacity: 0 }),
        animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
          style({ transform: 'translateX(0)', opacity: 1 })
        )
      ])
    ]),
    trigger('cardHover', [
      transition('* => hover', [
        animate('300ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
          style({ transform: 'translateY(-8px) scale(1.02)' })
        )
      ]),
      transition('hover => *', [
        animate('300ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
          style({ transform: 'translateY(0) scale(1)' })
        )
      ])
    ]),
    trigger('scaleIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.8) rotate(-5deg)' }),
        animate('600ms cubic-bezier(0.68, -0.55, 0.265, 1.55)', 
          keyframes([
            style({ opacity: 0, transform: 'scale(0.8) rotate(-5deg)', offset: 0 }),
            style({ opacity: 0.5, transform: 'scale(1.1) rotate(2deg)', offset: 0.6 }),
            style({ opacity: 1, transform: 'scale(1) rotate(0)', offset: 1 })
          ])
        )
      ])
    ]),
    trigger('viewSwitch', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.95)' }),
        animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
          style({ opacity: 1, transform: 'scale(1)' })
        )
      ]),
      transition(':leave', [
        animate('300ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
          style({ opacity: 0, transform: 'scale(0.95)' })
        )
      ])
    ])
  ]
})
export class CalendarComponent implements OnInit {
  calendarItems$!: Observable<CalendarItem[]>;
  stats$!: Observable<CalendarStats>;
  activeFilter: 'all' | 'assessments' | 'certifications' = 'all';
  viewMode: 'timeline' | 'calendar' = 'timeline';
  
  currentDate: Date = new Date();
  calendarDays: CalendarDay[] = [];
  weekDays: string[] = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  allItems: CalendarItem[] = [];

  constructor(private calendarService: CalendarDataService) {}

  ngOnInit(): void {
    this.loadData();
    this.generateCalendar();
  }

  loadData(): void {
    this.calendarItems$ = this.calendarService.getFilteredItems$(this.activeFilter);
    this.stats$ = this.calendarService.getCalendarStats$();
    
    this.calendarService.getAllCalendarItems$().subscribe((items: CalendarItem[]) => {
      this.allItems = items;
      this.generateCalendar();
    });
  }

  setFilter(filter: 'all' | 'assessments' | 'certifications'): void {
    this.activeFilter = filter;
    this.loadData();
    if (this.viewMode === 'calendar') {
      this.generateCalendar();
    }
  }

  setViewMode(mode: 'timeline' | 'calendar'): void {
    this.viewMode = mode;
    if (mode === 'calendar') {
      this.generateCalendar();
    }
  }

  generateCalendar(): void {
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevMonthLastDay = new Date(year, month, 0);
    
    const firstDayOfWeek = firstDay.getDay();
    const daysInMonth = lastDay.getDate();
    const daysInPrevMonth = prevMonthLastDay.getDate();
    
    this.calendarDays = [];
    
    for (let i = firstDayOfWeek - 1; i >= 0; i--) {
      const date = new Date(year, month - 1, daysInPrevMonth - i);
      this.calendarDays.push({
        date,
        dayNumber: daysInPrevMonth - i,
        isCurrentMonth: false,
        isToday: this.isToday(date),
        items: this.getItemsForDate(date)
      });
    }
    
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      this.calendarDays.push({
        date,
        dayNumber: day,
        isCurrentMonth: true,
        isToday: this.isToday(date),
        items: this.getItemsForDate(date)
      });
    }
    
    const remainingDays = 42 - this.calendarDays.length;
    for (let day = 1; day <= remainingDays; day++) {
      const date = new Date(year, month + 1, day);
      this.calendarDays.push({
        date,
        dayNumber: day,
        isCurrentMonth: false,
        isToday: this.isToday(date),
        items: this.getItemsForDate(date)
      });
    }
  }

  getItemsForDate(date: Date): CalendarItem[] {
    let filteredItems = this.allItems;
    
    if (this.activeFilter === 'assessments') {
      filteredItems = this.allItems.filter(item => item.type === 'assessment');
    } else if (this.activeFilter === 'certifications') {
      filteredItems = this.allItems.filter(item => item.type === 'certification');
    }
    
    return filteredItems.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate.getDate() === date.getDate() &&
             itemDate.getMonth() === date.getMonth() &&
             itemDate.getFullYear() === date.getFullYear();
    });
  }

  isToday(date: Date): boolean {
    const today = new Date();
    return date.getDate() === today.getDate() &&
           date.getMonth() === today.getMonth() &&
           date.getFullYear() === today.getFullYear();
  }

  previousMonth(): void {
    this.currentDate = new Date(
      this.currentDate.getFullYear(),
      this.currentDate.getMonth() - 1,
      1
    );
    this.generateCalendar();
  }

  nextMonth(): void {
    this.currentDate = new Date(
      this.currentDate.getFullYear(),
      this.currentDate.getMonth() + 1,
      1
    );
    this.generateCalendar();
  }

  getCurrentMonthYear(): string {
    return new Intl.DateTimeFormat('en-US', { 
      month: 'long', 
      year: 'numeric' 
    }).format(this.currentDate);
  }

  getStatusClass(status: string): string {
    const statusMap: { [key: string]: string } = {
      'assigned': 'bg-blue-500',
      'completed': 'bg-green-500',
      'in_progress': 'bg-yellow-500',
      'upcoming': 'bg-purple-500'
    };
    return statusMap[status] || 'bg-gray-500';
  }

  getStatusText(status: string): string {
    const statusTextMap: { [key: string]: string } = {
      'assigned': 'Assigned',
      'completed': 'Completed',
      'in_progress': 'In Progress',
      'upcoming': 'Upcoming'
    };
    return statusTextMap[status] || status;
  }

  formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    }).format(new Date(date));
  }

  getDayOfWeek(date: Date): string {
    return new Intl.DateTimeFormat('en-US', { weekday: 'long' }).format(new Date(date));
  }

  trackByItemId(index: number, item: CalendarItem): string {
    return item.id;
  }
}
