import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trigger, transition, style, animate, query, stagger } from '@angular/animations';
import { CalendarDataService } from '../../shared/services/calendar-data.service';
import { CalendarItem, CalendarStats } from '../../shared/models/calendar.models';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css'],
  animations: [
    trigger('listAnimation', [
      transition('* => *', [
        query(':enter', [
          style({ opacity: 0, transform: 'translateY(20px)' }),
          stagger(50, [
            animate('300ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
          ])
        ], { optional: true })
      ])
    ]),
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('300ms ease-in', style({ opacity: 1 }))
      ])
    ]),
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(-20px)', opacity: 0 }),
        animate('300ms ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
      ])
    ])
  ]
})
export class CalendarComponent implements OnInit {
  calendarItems$!: Observable<CalendarItem[]>;
  stats$!: Observable<CalendarStats>;
  activeFilter: 'all' | 'assessments' | 'certifications' = 'all';

  constructor(private calendarService: CalendarDataService) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.calendarItems$ = this.calendarService.getFilteredItems$(this.activeFilter);
    this.stats$ = this.calendarService.getCalendarStats$();
  }

  setFilter(filter: 'all' | 'assessments' | 'certifications'): void {
    this.activeFilter = filter;
    this.loadData();
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
