import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trigger, transition, style, animate, query, stagger, state } from '@angular/animations';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { CalendarDataService } from '../../shared/services/calendar-data.service';
import { CalendarItem, CalendarStats } from '../../shared/models/calendar.models';
import { Observable, Subject, takeUntil } from 'rxjs';
import { FormSubmissionDialogComponent, SubmissionResult } from '../../shared/components/form-submission-dialog/form-submission-dialog.component';
import { AuthService } from '../../shared/services/auth.service';
import { CalendarItemType } from '../../shared/models/calendar.models';
 
interface CalendarDay {
  date: Date;
  dayNumber: number;
  isCurrentMonth: boolean;
  isToday: boolean;
  items: CalendarItem[];
}
 
@Component({
  selector: 'app-employee-calendar',
  standalone: true,
  imports: [CommonModule, MatDialogModule],
  templateUrl: './employee-calendar.component.html',
  styleUrls: ['./employee-calendar.component.scss'],
  animations: [
    // ✅ List animation for timeline items
    trigger('listAnimation', [
      transition('* => *', [
        query(':leave', [
          animate('200ms cubic-bezier(0.4, 0.0, 1, 1)',
            style({ opacity: 0, transform: 'translateY(-10px) scale(0.98)' })
          )
        ], { optional: true }),
        query(':enter', [
          style({ opacity: 0, transform: 'translateY(15px) scale(0.98)' }),
          stagger(30, [
            animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)',
              style({ opacity: 1, transform: 'translateY(0) scale(1)' })
            )
          ])
        ], { optional: true })
      ])
    ]),
   
    // ✅ Fade in animation
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.95)' }),
        animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)',
          style({ opacity: 1, transform: 'scale(1)' })
        )
      ])
    ]),
   
    // ✅ Slide in animation
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(-30px)', opacity: 0 }),
        animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)',
          style({ transform: 'translateX(0)', opacity: 1 })
        )
      ])
    ]),
   
    // ✅ Scale in animation (for calendar items)
    trigger('scaleIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.9)' }),
        animate('300ms cubic-bezier(0.4, 0.0, 0.2, 1)',
          style({ opacity: 1, transform: 'scale(1)' })
        )
      ]),
      transition(':leave', [
        animate('200ms cubic-bezier(0.4, 0.0, 1, 1)',
          style({ opacity: 0, transform: 'scale(0.9)' })
        )
      ])
    ]),
   
    // ✅ View switch animation (for switching between timeline and calendar view)
    trigger('viewSwitch', [
      state('timeline', style({ opacity: 1, transform: 'translateX(0)' })),
      state('calendar', style({ opacity: 1, transform: 'translateX(0)' })),
      transition('timeline <=> calendar', [
        style({ opacity: 0, transform: 'translateX(20px)' }),
        animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      ])
    ]),
   
    // ✅ Stagger animation for calendar grid
    trigger('gridAnimation', [
      transition('* => *', [
        query(':enter', [
          style({ opacity: 0, transform: 'scale(0.95)' }),
          stagger(15, [
            animate('250ms cubic-bezier(0.4, 0.0, 0.2, 1)',
              style({ opacity: 1, transform: 'scale(1)' })
            )
          ])
        ], { optional: true })
      ])
    ])
  ]
})
export class EmployeeCalendarComponent implements OnInit, OnDestroy {
  calendarItems$!: Observable<CalendarItem[]>;
  stats$!: Observable<CalendarStats>;
  activeFilter: 'all' | 'assessments' | 'certifications' | 'courses' = 'all';
  viewMode: 'timeline' | 'calendar' = 'timeline';
 
  currentDate: Date = new Date();
  calendarDays: CalendarDay[] = [];
  weekDays: string[] = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  allItems: CalendarItem[] = [];
 
  isLoading = false;
  errorMessage: string | null = null;
 
  private destroy$ = new Subject<void>();
 
  constructor(
    private calendarService: CalendarDataService,
    private dialog: MatDialog,
    private authService: AuthService
  ) {}
 
  ngOnInit(): void {
    this.loadData();
    this.generateCalendar();
  }
 
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
 
  loadData(): void {
    const employeeId = this.authService.currentUserValue?.employeeId;
    console.log('🔄 Loading data for employee:', employeeId, 'filter:', this.activeFilter);
   
    this.calendarItems$ = this.calendarService.getFilteredItems$(this.activeFilter, employeeId);
    this.stats$ = this.calendarService.getCalendarStats$(employeeId);
   
    this.calendarService.getAllCalendarItems$(employeeId)
      .pipe(takeUntil(this.destroy$))
      .subscribe((items: CalendarItem[]) => {
        console.log('📦 ALL ITEMS LOADED:', items.length);
        console.log('   Assessments:', items.filter(i => i.type === CalendarItemType.ASSESSMENT).length);
        console.log('   Certifications:', items.filter(i => i.type === CalendarItemType.CERTIFICATION).length);
        console.log('   Courses:', items.filter(i => i.type === CalendarItemType.COURSE).length);
        console.log('   Sample items:', items.slice(0, 3).map(i => ({
          id: i.id,
          type: i.type,
          title: i.title,
          isCompleted: i.isCompleted,
          date: i.date
        })));
       
        this.allItems = items;
        this.generateCalendar();
      });
  }
 
  setFilter(filter: 'all' | 'assessments' | 'certifications' | 'courses'): void {
    console.log('🔍 Setting filter to:', filter);
    this.activeFilter = filter;
    this.loadData();
    if (this.viewMode === 'calendar') {
      this.generateCalendar();
    }
  }
 
  setViewMode(mode: 'timeline' | 'calendar'): void {
    console.log('👁️ Switching view mode to:', mode);
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
   
    // Previous month days
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
   
    // Current month days
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
   
    // Next month days
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
   
    console.log('📅 Calendar generated:', this.calendarDays.length, 'days');
  }
 
  getItemsForDate(date: Date): CalendarItem[] {
    let filteredItems = this.allItems;
   
    // Apply filter
    if (this.activeFilter === 'assessments') {
      filteredItems = this.allItems.filter(item => item.type === CalendarItemType.ASSESSMENT);
    } else if (this.activeFilter === 'certifications') {
      filteredItems = this.allItems.filter(item => item.type === CalendarItemType.CERTIFICATION);
    } else if (this.activeFilter === 'courses') {
      filteredItems = this.allItems.filter(item => item.type === CalendarItemType.COURSE);
    }
   
    // Filter by date
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
 
  trackByDate(index: number, day: CalendarDay): string {
    return day.date.toISOString();
  }
 
  openSubmissionDialog(item: CalendarItem): void {
    if (item.isCompleted) {
      console.log('⏭️ Item already completed, skipping dialog');
      return;
    }
 
    console.log('📝 Opening submission dialog for:', item.title);
 
    const dialogRef = this.dialog.open(FormSubmissionDialogComponent, {
      width: '600px',
      maxWidth: '90vw',
      data: { item },
      disableClose: false,
      hasBackdrop: true,
      backdropClass: 'dialog-backdrop',
      panelClass: 'submission-dialog-panel',
      autoFocus: true,
      restoreFocus: true,
      position: {
        top: '50px'
      }
    });
 
    dialogRef.afterClosed()
      .pipe(takeUntil(this.destroy$))
      .subscribe((result: SubmissionResult | undefined) => {
        if (result) {
          console.log('✅ Dialog closed with result:', result);
          this.isLoading = true;
          this.errorMessage = null;
 
          this.calendarService.markCompleted(item.id, {
            score: result.score,
            attachments: result.attachments,
            submissionNotes: result.submissionNotes
          }).subscribe({
            next: (success) => {
              if (success) {
                console.log('✅ Submission successful');
                this.loadData();
              } else {
                console.error('❌ Submission failed');
                this.errorMessage = 'Submission failed. Please try again.';
              }
              this.isLoading = false;
            },
            error: (error) => {
              console.error('❌ Submission error:', error);
              this.errorMessage = 'An error occurred during submission.';
              this.isLoading = false;
            }
          });
        } else {
          console.log('❌ Dialog closed without result');
        }
      });
  }
}
 