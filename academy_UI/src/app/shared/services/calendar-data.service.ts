import { Injectable } from '@angular/core';
import { Observable, of, BehaviorSubject, combineLatest } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  CalendarItem,
  AssessmentItem,
  CertificationItem,
  CalendarStats,
  CalendarItemType,
  CalendarStatus
} from '../models/calendar.models';
import { MOCK_ASSESSMENTS, MOCK_CERTIFICATIONS } from '../data/calendar.mock-data';

@Injectable({
  providedIn: 'root'
})
export class CalendarDataService {
  private assessmentsSubject = new BehaviorSubject<AssessmentItem[]>(MOCK_ASSESSMENTS);
  private certificationsSubject = new BehaviorSubject<CertificationItem[]>(MOCK_CERTIFICATIONS);

  getAssessments$(): Observable<AssessmentItem[]> {
    return this.assessmentsSubject.asObservable();
  }

  getCertifications$(): Observable<CertificationItem[]> {
    return this.certificationsSubject.asObservable();
  }

  getAllCalendarItems$(): Observable<CalendarItem[]> {
    return combineLatest([
      this.getAssessments$(),
      this.getCertifications$()
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
        return {
          totalAssignments: assessments.length,
          totalCertifications: certifications.length,
          completedItems: allItems.filter(item => item.status === CalendarStatus.COMPLETED).length,
          upcomingItems: allItems.filter(item => 
            item.status === CalendarStatus.UPCOMING || item.status === CalendarStatus.ASSIGNED
          ).length
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
}
