import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import { HttpClientModule } from '@angular/common/http';
import { SafeHtmlPipe } from '../../shared/pipe/safe-html.pipe';
import {
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexDataLabels,
  ApexPlotOptions,
  ApexLegend,
  ApexStroke,
  ApexGrid,
  ApexTooltip,
} from 'ng-apexcharts';
import { trigger, transition, style, animate, query, stagger } from '@angular/animations';
import { 
  AdminDashboardService, 
  RecentAssessment, 
  RecentCourseCompletion 
} from '../../shared/services/admin-dashboard.service';

interface StatCard {
  title: string;
  value: string | number;
  icon: string;
  iconBg: string;
  trend: 'up' | 'down';
}

interface Activity {
  employee: string;
  action: string;
  target: string;
  time: string;
  icon: string;
  type: 'assessment' | 'course';
}

interface TopPerformer {
  name: string;
  department: string;
  score: number;
  badge: string;
}

@Component({
  selector: 'app-admin-default-dashboard',
  imports: [CommonModule, NgApexchartsModule, SafeHtmlPipe, HttpClientModule],
  providers: [AdminDashboardService],
  templateUrl: './admin-default-dashboard.component.html',
  styleUrl: './admin-default-dashboard.component.scss',
  animations: [
    trigger('fadeInUp', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(20px)' }),
        animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
          style({ opacity: 1, transform: 'translateY(0)' })
        )
      ])
    ]),
    trigger('staggerFade', [
      transition('* => *', [
        query(':enter', [
          style({ opacity: 0, transform: 'translateY(15px) scale(0.98)' }),
          stagger(80, [
            animate('400ms cubic-bezier(0.4, 0.0, 0.2, 1)', 
              style({ opacity: 1, transform: 'translateY(0) scale(1)' })
            )
          ])
        ], { optional: true })
      ])
    ])
  ]
})
export class AdminDefaultDashboardComponent implements OnInit {
  employeeCount: number = 0;
  certificationCount: number = 0;

  statCards: StatCard[] = [
    {
      title: 'Active Employees',
      value: 150,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
      iconBg: 'bg-blue-50',
      trend: 'up'
    },
    {
      title: 'Certifications',
      value: 12,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>`,
      iconBg: 'bg-yellow-50',
      trend: 'up'
    },
    {
      title: 'Total Batches',
      value: 3,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>`,
      iconBg: 'bg-purple-50',
      trend: 'up'
    }
  ];

  recentActivities: Activity[] = [];
  isLoadingActivities = true;
  activitiesError: string | null = null;

  topPerformers: TopPerformer[] = [
    { name: 'Alice Johnson', department: 'Engineering', score: 98, badge: '🏆' },
    { name: 'Bob Smith', department: 'Design', score: 95, badge: '🥈' },
    { name: 'Carol White', department: 'Marketing', score: 93, badge: '🥉' },
    { name: 'David Brown', department: 'Sales', score: 91, badge: '⭐' }
  ];

  public chartSeries: ApexAxisChartSeries = [
    {
      name: 'Employees',
      data: [45, 32, 28, 18, 15, 12]
    }
  ];

  public chartOptions: ApexChart = {
    fontFamily: 'Outfit, sans-serif',
    type: 'bar',
    height: 320,
    toolbar: {
      show: false
    }
  };

  public chartColors: string[] = ['#465fff'];

  public plotOptions: ApexPlotOptions = {
    bar: {
      horizontal: true,
      columnWidth: '55%',
      borderRadius: 6,
      borderRadiusApplication: 'end'
    }
  };

  public dataLabels: ApexDataLabels = {
    enabled: false
  };

  public stroke: ApexStroke = {
    show: true,
    width: 2,
    colors: ['transparent']
  };

  public xaxis: ApexXAxis = {
    categories: ['QA Engineer', 'Test Lead', 'Automation Engineer', 'QA Analyst', 'SDET', 'Manual Tester'],
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    }
  };

  public grid: ApexGrid = {
    xaxis: {
      lines: {
        show: true
      }
    },
    yaxis: {
      lines: {
        show: false
      }
    }
  };

  public legend: ApexLegend = {
    show: false
  };

  public tooltip: ApexTooltip = {
    y: {
      formatter: (val: number) => `${val} employees`
    }
  };

  constructor(private dashboardService: AdminDashboardService) {}

  ngOnInit(): void {
    console.log('Dashboard component initialized');
    this.loadRecentActivities();
    this.fetchEmployeeCount();
    this.getCertificationCount();
    this.getBatchCount()

  }

  loadRecentActivities(): void {
    console.log('Loading recent activities...');
    this.isLoadingActivities = true;
    this.activitiesError = null;

    // Fetch assessments and courses separately with individual error handling
    const assessments$ = this.dashboardService.getRecentAssessments(2);
    const courses$ = this.dashboardService.getRecentCourseCompletions(2);

    let assessmentActivities: Activity[] = [];
    let courseActivities: Activity[] = [];
    let completedRequests = 0;
    let hasError = false;

    // Handle assessments
    assessments$.subscribe({
      next: (data) => {
        console.log('✅ Assessments loaded:', data);
        assessmentActivities = this.mapAssessmentsToActivities(data);
        completedRequests++;
        this.combineActivities(assessmentActivities, courseActivities, completedRequests, hasError);
      },
      error: (error) => {
        console.error('❌ Error loading assessments:', error);
        hasError = true;
        completedRequests++;
        this.combineActivities(assessmentActivities, courseActivities, completedRequests, hasError);
      }
    });

    // Handle courses
    courses$.subscribe({
      next: (data) => {
        console.log('✅ Courses loaded:', data);
        courseActivities = this.mapCoursesToActivities(data);
        completedRequests++;
        this.combineActivities(assessmentActivities, courseActivities, completedRequests, hasError);
      },
      error: (error) => {
        console.error('❌ Error loading courses:', error);
        hasError = true;
        completedRequests++;
        this.combineActivities(assessmentActivities, courseActivities, completedRequests, hasError);
      }
    });
  }

  private combineActivities(
    assessments: Activity[], 
    courses: Activity[], 
    completedRequests: number, 
    hasError: boolean
  ): void {
    // Wait for both requests to complete
    if (completedRequests < 2) {
      return;
    }

    // Combine available activities
    this.recentActivities = [...assessments, ...courses]
      .sort((a, b) => this.compareActivityTimes(a, b));

    this.isLoadingActivities = false;

    // Set error message only if both failed
    if (assessments.length === 0 && courses.length === 0 && hasError) {
      this.activitiesError = 'Failed to load recent activities. Please check your backend connection.';
    } else {
      this.activitiesError = null;
    }

    console.log('📊 Final activities:', this.recentActivities);
  }

  private mapAssessmentsToActivities(assessments: RecentAssessment[]): Activity[] {
    return assessments.map(assessment => ({
      employee: assessment.Employee_Name,
      action: 'submitted assessment',
      target: assessment.Assessment_Name,
      time: assessment.Upload_Time,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>`,
      type: 'assessment' as const
    }));
  }

  private mapCoursesToActivities(courses: RecentCourseCompletion[]): Activity[] {
    return courses.map(course => ({
      employee: course.Employee_Name,
      action: 'completed course',
      target: course.Course_Name,
      time: course.Completion_Datetime,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`,
      type: 'course' as const
    }));
  }

  private compareActivityTimes(a: Activity, b: Activity): number {
    const timeA = new Date(a.time).getTime();
    const timeB = new Date(b.time).getTime();
    return timeB - timeA; // Most recent first
  }

  private formatUploadTime(uploadTime: string): string {
    const now = new Date();
    const uploadDate = new Date(uploadTime);
    const diffMs = now.getTime() - uploadDate.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) {
      return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
      return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    } else {
      return uploadDate.toLocaleDateString();
    }
  }

  // Getter to format time for display in template
  getFormattedTime(time: string): string {
    return this.formatUploadTime(time);
  }

  // addEmployee(): void {
  //   console.log('Add employee clicked');
  // }

addPod(): void {
  const newPod = {
    pod_id: 'POD001',
    pod: 'Quality Assurance Team',
    batch_code: 'BATCH001' // make sure this batch exists
  };

  console.log('📤 Sending request to create POD:', newPod);

  this.dashboardService.createPod(newPod).subscribe({
    next: (response) => {
      console.log('✅ POD created successfully:', response);
      alert(`POD "${newPod.pod}" created successfully!`);
    },
    error: (err) => {
      console.error('❌ Error creating POD:', err);
      alert(`Failed to create POD: ${err.message}`);
    }
  });
}



 addCertification(): void {
  const newCertification = {
    certification_id: 'CERT001',
    name: 'AWS Cloud Practitioner',
    link: 'https://aws.amazon.com/certification/certified-cloud-practitioner/'
  };

  console.log('📤 Sending request to create certification:', newCertification);

  this.dashboardService.createCertification(newCertification).subscribe({
    next: (response) => {
      console.log('✅ Certification created successfully:', response);
      alert(`Certification "${newCertification.name}" created successfully!`);
    },
    error: (err) => {
      console.error('❌ Error creating certification:', err);
      alert(`Failed to create certification: ${err.message}`);
    }
  });
}


  addAssessment(): void {
  const newAssessment = {
    assessment_id: 'A001',
    name: 'Playwright Automation Assessment',
    link: 'https://assessments.example.com/playwright'
  };

  console.log('📤 Sending request to create assessment:', newAssessment);

  this.dashboardService.createAssessment(newAssessment).subscribe({
    next: (response) => {
      console.log('✅ Assessment created successfully:', response);
      alert(`Assessment "${newAssessment.name}" created successfully!`);
    },
    error: (err) => {
      console.error('❌ Error creating assessment:', err);
      alert(`Failed to create assessment: ${err.message}`);
    }
  });
}

fetchEmployeeCount(): void {
  this.dashboardService.getEmployeeCount().subscribe({
    next: (count) => {
      console.log('✅ Employee count fetched:', count);
      this.employeeCount = count;

      // Update the "Active Employees" stat card dynamically
      const employeeCard = this.statCards.find(card => card.title === 'Active Employees');
      if (employeeCard) {
        employeeCard.value = count;
      }
    },
    error: (err) => {
      console.error('❌ Failed to fetch employee count:', err);
    }
  });
}
getCertificationCount(): void {
  this.dashboardService.getCertificationCount().subscribe({
    next: (count) => {
      console.log('✅ Certification count fetched:', count);
      this.certificationCount = count;

      // Update the "Certifications" stat card dynamically
      const certificationCard = this.statCards.find(card => card.title === 'Certifications');
      if (certificationCard) {
        certificationCard.value = count;
      }
    },
    error: (error) => {
      console.error('❌ Error fetching certification count:', error);
    }
  });
}

getBatchCount(): void {
  this.dashboardService.getBatchCount().subscribe({
    next: (count) => {
      console.log('✅ Batch count fetched:', count);

      // Update the "Total Batches" stat card dynamically
      const batchCard = this.statCards.find(card => card.title === 'Total Batches');
      if (batchCard) {
        batchCard.value = count;
      }
    },
    error: (error) => {
      console.error('❌ Error fetching batch count:', error);
    }
  });
}

}