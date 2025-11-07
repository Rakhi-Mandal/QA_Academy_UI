import { Injectable } from '@angular/core';
import { Observable, of, BehaviorSubject, combineLatest } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  CalendarItem,
  AssessmentItem,
  CertificationItem,
  CalendarStats,
  CalendarItemType,
  CalendarStatus,
  FileAttachment
} from '../models/calendar.models';
import { MOCK_ASSESSMENTS, MOCK_CERTIFICATIONS } from '../data/calendar.mock-data';

const STORAGE_KEY = 'calendar_completion_state';

interface CompletionData {
  score?: number | null;
  attachments?: FileAttachment[];
  submissionNotes?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class CalendarDataService {
  private assessmentsSubject = new BehaviorSubject<AssessmentItem[]>(this.loadAssessments());
  private certificationsSubject = new BehaviorSubject<CertificationItem[]>(this.loadCertifications());

  getAssessments$(): Observable<AssessmentItem[]> {
    return this.assessmentsSubject.asObservable();
  }

  getCertifications$(): Observable<CertificationItem[]> {
    return this.certificationsSubject.asObservable();
  }

  refreshData(): void {
    this.assessmentsSubject.next([...this.assessmentsSubject.value]);
    this.certificationsSubject.next([...this.certificationsSubject.value]);
  }

  getAllCalendarItems$(): Observable<CalendarItem[]> {
    return combineLatest([
      this.assessmentsSubject.asObservable(),
      this.certificationsSubject.asObservable()
    ]).pipe(
      map(([assessments, certifications]) => {
        const allItems: CalendarItem[] = [...assessments, ...certifications];
        return allItems.sort((a, b) => a.date.getTime() - b.date.getTime());
      })
    );
  }

  getCalendarStats$(): Observable<CalendarStats> {
    return combineLatest([
      this.getAssessments$(),
      this.getCertifications$()
    ]).pipe(
      map(([assessments, certifications]) => {
        const allItems = [...assessments, ...certifications];
        const completedCount = allItems.filter(item => item.isCompleted).length;
        const totalCount = allItems.length;
        return {
          totalAssignments: assessments.length,
          totalCertifications: certifications.length,
          completedItems: completedCount,
          upcomingItems: totalCount - completedCount
        };
      })
    );
  }

  getFilteredItems$(filterType: 'all' | 'assessments' | 'certifications'): Observable<CalendarItem[]> {
    return this.getAllCalendarItems$().pipe(
      map(items => {
        if (filterType === 'assessments') {
          return items.filter(item => item.type === CalendarItemType.ASSESSMENT);
        } else if (filterType === 'certifications') {
          return items.filter(item => item.type === CalendarItemType.CERTIFICATION);
        }
        return items;
      })
    );
  }

  updateAssessmentStatus(id: string, status: CalendarStatus): void {
    const assessments = this.assessmentsSubject.value;
    const updated = assessments.map(assessment =>
      assessment.id === id ? { ...assessment, status } : assessment
    );
    this.assessmentsSubject.next(updated);
  }

  updateCertificationStatus(id: string, status: CalendarStatus): void {
    const certifications = this.certificationsSubject.value;
    const updated = certifications.map(certification =>
      certification.id === id ? { ...certification, status } : certification
    );
    this.certificationsSubject.next(updated);
  }

  markCompleted(id: string, completionData: CompletionData): void {
    const assessments = this.assessmentsSubject.value;
    const certifications = this.certificationsSubject.value;

    const assessmentIndex = assessments.findIndex(item => item.id === id);
    if (assessmentIndex !== -1) {
      const updated = [...assessments];
      updated[assessmentIndex] = {
        ...updated[assessmentIndex],
        isCompleted: true,
        completedAt: new Date(),
        status: CalendarStatus.COMPLETED,
        score: completionData.score,
        attachments: completionData.attachments || [],
        submissionNotes: completionData.submissionNotes
      };
      this.assessmentsSubject.next(updated);
      this.saveToLocalStorage();
      return;
    }

    const certificationIndex = certifications.findIndex(item => item.id === id);
    if (certificationIndex !== -1) {
      const updated = [...certifications];
      updated[certificationIndex] = {
        ...updated[certificationIndex],
        isCompleted: true,
        completedAt: new Date(),
        status: CalendarStatus.COMPLETED,
        score: completionData.score,
        attachments: completionData.attachments || [],
        submissionNotes: completionData.submissionNotes
      };
      this.certificationsSubject.next(updated);
      this.saveToLocalStorage();
    }
  }

  revertCompletion(id: string): void {
    const assessments = this.assessmentsSubject.value;
    const certifications = this.certificationsSubject.value;

    const assessmentIndex = assessments.findIndex(item => item.id === id);
    if (assessmentIndex !== -1) {
      const updated = [...assessments];
      updated[assessmentIndex] = {
        ...updated[assessmentIndex],
        isCompleted: false,
        completedAt: null,
        status: CalendarStatus.ASSIGNED,
        score: null,
        attachments: [],
        submissionNotes: null
      };
      this.assessmentsSubject.next(updated);
      this.saveToLocalStorage();
      return;
    }

    const certificationIndex = certifications.findIndex(item => item.id === id);
    if (certificationIndex !== -1) {
      const updated = [...certifications];
      updated[certificationIndex] = {
        ...updated[certificationIndex],
        isCompleted: false,
        completedAt: null,
        status: CalendarStatus.ASSIGNED,
        score: null,
        attachments: [],
        submissionNotes: null
      };
      this.certificationsSubject.next(updated);
      this.saveToLocalStorage();
    }
  }

  private loadAssessments(): AssessmentItem[] {
    const saved = this.loadFromLocalStorage();
    if (!saved || !saved.assessments) {
      return MOCK_ASSESSMENTS;
    }
    return saved.assessments.map((item: any) => ({
      ...item,
      date: new Date(item.date),
      completedAt: item.completedAt ? new Date(item.completedAt) : null,
      isCompleted: item.isCompleted ?? false,
      attachments: item.attachments?.map((att: any) => ({
        ...att,
        uploadedAt: att.uploadedAt ? new Date(att.uploadedAt) : new Date()
      })) || []
    }));
  }

  private loadCertifications(): CertificationItem[] {
    const saved = this.loadFromLocalStorage();
    if (!saved || !saved.certifications) {
      return MOCK_CERTIFICATIONS;
    }
    return saved.certifications.map((item: any) => ({
      ...item,
      date: new Date(item.date),
      completedAt: item.completedAt ? new Date(item.completedAt) : null,
      isCompleted: item.isCompleted ?? false,
      attachments: item.attachments?.map((att: any) => ({
        ...att,
        uploadedAt: att.uploadedAt ? new Date(att.uploadedAt) : new Date()
      })) || []
    }));
  }

  private saveToLocalStorage(): void {
    const data = {
      assessments: this.assessmentsSubject.value,
      certifications: this.certificationsSubject.value
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }

  private loadFromLocalStorage(): any {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Error loading from localStorage:', error);
      return null;
    }
  }
}
