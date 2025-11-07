export enum CalendarItemType {
  ASSESSMENT = 'assessment',
  CERTIFICATION = 'certification'
}

export enum CalendarStatus {
  ASSIGNED = 'assigned',
  COMPLETED = 'completed',
  IN_PROGRESS = 'in_progress',
  UPCOMING = 'upcoming'
}

export interface FileAttachment {
  name: string;
  size: number;
  mimeType: string;
  data: string;
  uploadedAt: Date;
}

export interface CalendarItem {
  id: string;
  title: string;
  description: string;
  type: CalendarItemType;
  date: Date;
  status: CalendarStatus;
  tools?: string[];
  platform?: string;
  category?: string;
  isCompleted?: boolean;
  completedAt?: Date | null;
  score?: number | null;
  attachments?: FileAttachment[];
  submissionNotes?: string | null;
}

export interface AssessmentItem extends CalendarItem {
  type: CalendarItemType.ASSESSMENT;
  assessmentCode: string;
  wave: number;
}

export interface CertificationItem extends CalendarItem {
  type: CalendarItemType.CERTIFICATION;
  certificationCode: string;
  provider?: string;
}

export interface CalendarStats {
  totalAssignments: number;
  totalCertifications: number;
  completedItems: number;
  upcomingItems: number;
}
