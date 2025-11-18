// src/app/shared/services/calendar-data.service.ts - FIXED VERSION
import { Injectable } from '@angular/core';
import { Observable, of, BehaviorSubject, combineLatest } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import {
  CalendarItem,
  AssessmentItem,
  CertificationItem,
  CalendarStats,
  CalendarItemType,
  CalendarStatus,
  FileAttachment
} from '../models/calendar.models';
import { DashboardService, DeadlineItem } from './dashboard.service';
 
interface CompletionData {
  score?: number | null | undefined;
  attachments?: FileAttachment[];
  submissionNotes?: string | null | undefined;
}
 
@Injectable({
  providedIn: 'root'
})
export class CalendarDataService {
  private assessmentsSubject = new BehaviorSubject<AssessmentItem[]>([]);
  private certificationsSubject = new BehaviorSubject<CertificationItem[]>([]);
  private coursesSubject = new BehaviorSubject<CalendarItem[]>([]);
  private dataLoaded = false;
 
  constructor(private dashboardService: DashboardService) {}
 
  private initializeData(): void {
    if (!this.dataLoaded) {
      this.loadFromBackend();
      this.dataLoaded = true;
    }
  }
 
  private loadFromBackend(): void {
    const employeeId = this.getEmployeeId();
 
    if (!employeeId) {
      console.error('❌ No employee ID found - cannot load data');
      this.assessmentsSubject.next([]);
      this.certificationsSubject.next([]);
      this.coursesSubject.next([]);
      return;
    }
 
    console.log('🔄 Loading from backend for employee:', employeeId);
 
    this.dashboardService.getItems('all', employeeId).subscribe({
      next: (response) => {
        console.log('📦 Backend response:', response);
        if (response && response.success && Array.isArray(response.data)) {
          console.log('✅ Received', response.data.length, 'items from backend');
          const { assessments, certifications, courses } = this.transformBackendData(response.data);
         
          console.log('📊 Transformed data:', {
            assessments: assessments.length,
            certifications: certifications.length,
            courses: courses.length,
            total: assessments.length + certifications.length + courses.length
          });
 
          this.assessmentsSubject.next(assessments);
          this.certificationsSubject.next(certifications);
          this.coursesSubject.next(courses);
        } else {
          console.warn('⚠️ Invalid backend response');
          this.assessmentsSubject.next([]);
          this.certificationsSubject.next([]);
          this.coursesSubject.next([]);
        }
      },
      error: (err) => {
        console.error('❌ Failed to load backend items', err);
        this.assessmentsSubject.next([]);
        this.certificationsSubject.next([]);
        this.coursesSubject.next([]);
      }
    });
  }
 
  /**
   * ✅ FIXED: Transform backend data with correct dates for completed vs pending items
   */
  private transformBackendData(items: DeadlineItem[]): {
    assessments: AssessmentItem[];
    certifications: CertificationItem[];
    courses: CalendarItem[];
  } {
    const assessments: AssessmentItem[] = [];
    const certifications: CertificationItem[] = [];
    const courses: CalendarItem[] = [];
 
    items.forEach((item: any) => {
      const statusRaw = (item.status || '').toString().toLowerCase();
      const isCompleted = statusRaw === 'completed' || statusRaw === 'done';
 
      // ✅ FIX: Get DEADLINE date (for sorting and display of pending items)
      const deadlineStr = item.effective_deadline || item.Deadline_Date || item.DeadlineDate || item.deadline;
      const deadlineDate = deadlineStr ? new Date(deadlineStr) : new Date();
 
      // ✅ FIX: Get COMPLETION date (for completed items)
      const completionStr = item.Upload_Time || item.Completion_Datetime || item.completed_at;
      const completionDate = completionStr ? new Date(completionStr) : null;
 
      // ✅ FIX: Use the right date
      // - For completed items: Use COMPLETION date
      // - For pending items: Use DEADLINE date
      const displayDate = isCompleted && completionDate ? completionDate : deadlineDate;
 
      const title = item.title || item.Name || item.Name_en || `Item ${item.Task_ID || item.Task_Slno}`;
      const description = item.description || item.short_description || '';
 
      if (item.Task_Type === 'Assessment') {
        const ai: AssessmentItem = {
          id: `task_${item.Task_Slno}`,
          title,
          description,
          date: displayDate, // ✅ Show completion date for completed, deadline for pending
          type: CalendarItemType.ASSESSMENT,
          status: isCompleted ? CalendarStatus.COMPLETED : CalendarStatus.ASSIGNED,
          isCompleted,
          completedAt: isCompleted ? (completionDate || deadlineDate) : null, // ✅ Store actual completion date
          score: item.Mark_Secured || item.marks_scored || null,
          maxScore: item.maxScore || 100,
          link: item.link || null,
          attachments: [],
          submissionNotes: null,
          taskSlno: item.Task_Slno,
          taskId: item.Task_ID
        };
        assessments.push(ai);
      } else if (item.Task_Type === 'Certification') {
        const ci: CertificationItem = {
          id: `task_${item.Task_Slno}`,
          title,
          description,
          date: displayDate, // ✅ Show completion date for completed, deadline for pending
          type: CalendarItemType.CERTIFICATION,
          status: isCompleted ? CalendarStatus.COMPLETED : CalendarStatus.ASSIGNED,
          isCompleted,
          completedAt: isCompleted ? (completionDate || deadlineDate) : null, // ✅ Store actual completion date
          score: item.Mark_Secured || item.marks_scored || null,
          provider: item.provider || null,
          certificationUrl: item.link || null,
          link: item.link || null,
          attachments: [],
          submissionNotes: null,
          taskSlno: item.Task_Slno,
          taskId: item.Task_ID
        };
        certifications.push(ci);
      } else if (item.Task_Type === 'Course') {
        const co: CalendarItem = {
          id: `task_${item.Task_Slno}`,
          title,
          description,
          date: displayDate, // ✅ Show completion date for completed, deadline for pending
          type: CalendarItemType.COURSE,
          status: isCompleted ? CalendarStatus.COMPLETED : CalendarStatus.ASSIGNED,
          isCompleted,
          completedAt: isCompleted ? (completionDate || deadlineDate) : null, // ✅ Store actual completion date
          score: null,
          attachments: [],
          submissionNotes: null,
          taskSlno: item.Task_Slno,
          taskId: item.Task_ID
        };
        courses.push(co);
      }
    });
 
    return { assessments, certifications, courses };
  }
 
  private getEmployeeId(): string | null {
    try {
      const stored = localStorage.getItem('currentUser');
      if (!stored) return null;
      const user = JSON.parse(stored);
      return user.employeeId || user.employee_id || user.Employee_ID || user.id || null;
    } catch (error) {
      console.error('Error reading employee ID:', error);
      return null;
    }
  }
 
  refreshData(): void {
    console.log('🔄 Refreshing data...');
    this.dataLoaded = false;
    this.loadFromBackend();
  }
 
  getAssessments$(employeeId?: string): Observable<AssessmentItem[]> {
    if (!this.dataLoaded) this.initializeData();
    return this.assessmentsSubject.asObservable().pipe(
      map(assessments => {
        if (!employeeId) return assessments;
        return assessments.filter(a => !a['assignedTo'] || a['assignedTo'] === employeeId);
      })
    );
  }
 
  getCertifications$(employeeId?: string): Observable<CertificationItem[]> {
    if (!this.dataLoaded) this.initializeData();
    return this.certificationsSubject.asObservable().pipe(
      map(certifications => {
        if (!employeeId) return certifications;
        return certifications.filter(c => !c['assignedTo'] || c['assignedTo'] === employeeId);
      })
    );
  }
 
  getCourses$(employeeId?: string): Observable<CalendarItem[]> {
    if (!this.dataLoaded) this.initializeData();
    return this.coursesSubject.asObservable().pipe(
      map(courses => {
        if (!employeeId) return courses;
        return courses.filter(c => !c['assignedTo'] || c['assignedTo'] === employeeId);
      })
    );
  }
 
  getAllCalendarItems$(employeeId?: string): Observable<CalendarItem[]> {
    return combineLatest([
      this.getAssessments$(employeeId),
      this.getCertifications$(employeeId),
      this.getCourses$(employeeId)
    ]).pipe(
      map(([assessments, certifications, courses]) => {
        const allItems: CalendarItem[] = [
          ...assessments as CalendarItem[],
          ...certifications as CalendarItem[],
          ...courses
        ];
 
        // ✅ Sort: completed first, then by date
        allItems.sort((a, b) => {
          // Completed items first
          if (a.isCompleted !== b.isCompleted) {
            return a.isCompleted ? -1 : 1;
          }
          // Then sort by date (ascending)
          return new Date(a.date).getTime() - new Date(b.date).getTime();
        });
 
        console.log('📋 All items sorted:', {
          total: allItems.length,
          completed: allItems.filter(i => i.isCompleted).length,
          pending: allItems.filter(i => !i.isCompleted).length
        });
 
        return allItems;
      })
    );
  }
 
  getCalendarStats$(employeeId?: string): Observable<CalendarStats> {
    const empId = employeeId || this.getEmployeeId();
    if (!empId) {
      return of({
        totalAssignments: 0,
        totalCertifications: 0,
        totalCourses: 0,
        completedItems: 0,
        upcomingItems: 0
      });
    }
    return this.dashboardService.getDashboard(empId).pipe(
      map(response => {
        if (response && response.success && response.data) {
          return {
            totalAssignments: response.data.total_assignments || 0,
            totalCertifications: response.data.total_certifications || 0,
            totalCourses: response.data.total_courses || 0,
            completedItems: response.data.completed_total || 0,
            upcomingItems: response.data.remaining_total || 0
          } as CalendarStats;
        }
        return {
          totalAssignments: 0,
          totalCertifications: 0,
          totalCourses: 0,
          completedItems: 0,
          upcomingItems: 0
        } as CalendarStats;
      }),
      catchError((err) => {
        console.error('Stats error', err);
        return of({
          totalAssignments: 0,
          totalCertifications: 0,
          totalCourses: 0,
          completedItems: 0,
          upcomingItems: 0
        } as CalendarStats);
      })
    );
  }
 
  getFilteredItems$(filterType: 'all' | 'assessments' | 'certifications' | 'courses', employeeId?: string): Observable<CalendarItem[]> {
    return this.getAllCalendarItems$(employeeId).pipe(
      map(items => {
        let filtered: CalendarItem[] = items;
        if (filterType === 'assessments') {
          filtered = items.filter(item => item.type === CalendarItemType.ASSESSMENT);
        } else if (filterType === 'certifications') {
          filtered = items.filter(item => item.type === CalendarItemType.CERTIFICATION);
        } else if (filterType === 'courses') {
          filtered = items.filter(item => item.type === CalendarItemType.COURSE);
        }
       
        // Already sorted by getAllCalendarItems$
        return filtered;
      })
    );
  }
 
  updateAssessmentStatus(id: string, status: CalendarStatus): void {
    const assessments = this.assessmentsSubject.value.slice();
    const idx = assessments.findIndex(a => a.id === id);
    if (idx !== -1) {
      assessments[idx] = { ...assessments[idx], status };
      this.assessmentsSubject.next(assessments);
    }
  }
 
  updateCertificationStatus(id: string, status: CalendarStatus): void {
    const certifications = this.certificationsSubject.value.slice();
    const idx = certifications.findIndex(c => c.id === id);
    if (idx !== -1) {
      certifications[idx] = { ...certifications[idx], status };
      this.certificationsSubject.next(certifications);
    }
  }
 
  updateCourseStatus(id: string, status: CalendarStatus): void {
    const courses = this.coursesSubject.value.slice();
    const idx = courses.findIndex(c => c.id === id);
    if (idx !== -1) {
      courses[idx] = { ...courses[idx], status };
      this.coursesSubject.next(courses);
    }
  }
 
  markCompleted(id: string, completionData: CompletionData): Observable<boolean> {
    const taskSlno = this.extractTaskSlno(id);
    if (taskSlno <= 0) {
      return of(false);
    }
    const employeeId = this.getEmployeeId();
    if (!employeeId) return of(false);
 
    return this.dashboardService.submitTask(taskSlno, {
      marks_scored: completionData.score ?? undefined,
      notes: completionData.submissionNotes ?? undefined,
      file: completionData.attachments?.[0]?.file
    }, employeeId).pipe(
      map(resp => {
        if (resp && (resp as any).success) {
          this.updateLocalCompletion(id, completionData);
          this.refreshData();
          return true;
        }
        return false;
      }),
      catchError(err => {
        console.error('submit error', err);
        return of(false);
      })
    );
  }
 
  private updateLocalCompletion(id: string, completionData: CompletionData): void {
    const a = this.assessmentsSubject.value.slice();
    const ai = a.findIndex(x => x.id === id);
    if (ai !== -1) {
      a[ai] = {
        ...a[ai],
        isCompleted: true,
        completedAt: new Date(),
        status: CalendarStatus.COMPLETED,
        score: completionData.score ?? null,
        attachments: completionData.attachments || [],
        submissionNotes: completionData.submissionNotes ?? null
      };
      this.assessmentsSubject.next(a);
      return;
    }
 
    const c = this.certificationsSubject.value.slice();
    const ci = c.findIndex(x => x.id === id);
    if (ci !== -1) {
      c[ci] = {
        ...c[ci],
        isCompleted: true,
        completedAt: new Date(),
        status: CalendarStatus.COMPLETED,
        score: completionData.score ?? null,
        attachments: completionData.attachments || [],
        submissionNotes: completionData.submissionNotes ?? null
      };
      this.certificationsSubject.next(c);
      return;
    }
 
    const co = this.coursesSubject.value.slice();
    const coi = co.findIndex(x => x.id === id);
    if (coi !== -1) {
      co[coi] = {
        ...co[coi],
        isCompleted: true,
        completedAt: new Date(),
        status: CalendarStatus.COMPLETED,
        score: completionData.score ?? null,
        attachments: completionData.attachments || [],
        submissionNotes: completionData.submissionNotes ?? null
      };
      this.coursesSubject.next(co);
    }
  }
 
  private extractTaskSlno(itemId: string): number {
    const m = itemId.match(/task_(\d+)/);
    return m ? parseInt(m[1], 10) : 0;
  }
 
  revertCompletion(id: string): void {
    const a = this.assessmentsSubject.value.slice();
    const ai = a.findIndex(x => x.id === id);
    if (ai !== -1) {
      a[ai] = { ...a[ai], isCompleted: false, completedAt: null, status: CalendarStatus.ASSIGNED, score: null, attachments: [], submissionNotes: null };
      this.assessmentsSubject.next(a);
      return;
    }
 
    const c = this.certificationsSubject.value.slice();
    const ci = c.findIndex(x => x.id === id);
    if (ci !== -1) {
      c[ci] = { ...c[ci], isCompleted: false, completedAt: null, status: CalendarStatus.ASSIGNED, score: null, attachments: [], submissionNotes: null };
      this.certificationsSubject.next(c);
      return;
    }
 
    const co = this.coursesSubject.value.slice();
    const coi = co.findIndex(x => x.id === id);
    if (coi !== -1) {
      co[coi] = { ...co[coi], isCompleted: false, completedAt: null, status: CalendarStatus.ASSIGNED, score: null, attachments: [], submissionNotes: null };
      this.coursesSubject.next(co);
    }
  }
}
 