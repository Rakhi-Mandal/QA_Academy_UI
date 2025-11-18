// src/app/shared/models/calendar.models.ts
export interface CalendarItem {
  id: string;
  title: string;
  description: string;
  date: Date;
  type: CalendarItemType;
  status: CalendarStatus;
  isCompleted: boolean;
  completedAt: Date | null;
  score: number | null;
  attachments: FileAttachment[];
  submissionNotes: string | null;
  link?: string;
  assignedTo?: string;
  taskSlno?: number;
  taskId?: string;
}

export interface AssessmentItem extends CalendarItem {
  type: CalendarItemType.ASSESSMENT;
  maxScore?: number;
  assessmentCode?: string;
  link?: string;
  wave?: number; // ADD THIS - fixes "wave does not exist" errors
}

export interface CertificationItem extends CalendarItem {
  type: CalendarItemType.CERTIFICATION;
  provider?: string;
  certificationUrl?: string;
  certificationCode?: string;
  link?: string;
  category?: string; // ADD THIS - fixes "category does not exist" errors
}

export interface FileAttachment {
  id: string;
  name: string;
  size: number;
  type: string;
  url: string;
  uploadedAt: Date;
  file?: File;
  mimeType?: string;
  data?: string; // ADD THIS - fixes form-submission-dialog error
}

export interface CalendarStats {
  totalAssignments: number;
  totalCertifications: number;
  totalCourses?: number;
  completedItems: number;
  upcomingItems: number;
}

export enum CalendarItemType {
  ASSESSMENT = 'assessment',
  CERTIFICATION = 'certification',
  COURSE = 'course'
}

export enum CalendarStatus {
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  OVERDUE = 'overdue',
  UPCOMING = 'upcoming' 
}

export interface CalendarDay {
  date: Date;
  dayNumber: number;
  isCurrentMonth: boolean;
  isToday: boolean;
  items: CalendarItem[];
}