import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
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
}

interface TopPerformer {
  name: string;
  department: string;
  score: number;
  badge: string;
}

@Component({
  selector: 'app-admin-default-dashboard',
  imports: [CommonModule, NgApexchartsModule, SafeHtmlPipe],
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
  
  statCards: StatCard[] = [
    {
      title: 'Total Employees',
      value: 150,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
      iconBg: 'bg-blue-50',
      trend: 'up'
    },
    {
      title: 'Recent Activity',
      value: 28,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>`,
      iconBg: 'bg-green-50',
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
      title: 'Active Batches',
      value: 3,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>`,
      iconBg: 'bg-purple-50',
      trend: 'up'
    }
  ];

  recentActivities: Activity[] = [
    {
      employee: 'John Doe',
      action: 'completed certification',
      target: 'AWS Cloud',
      time: '2 hours ago',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87m-4-12a4 4 0 0 1 0 7.75"></path></svg>`
    },
    {
      employee: 'Jane Smith',
      action: 'started assessment',
      target: 'React Advanced',
      time: '4 hours ago',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87m-4-12a4 4 0 0 1 0 7.75"></path></svg>`
   },
    {
      employee: 'Mike Johnson',
      action: 'achieved 95% score',
      target: 'JavaScript',
      time: '6 hours ago',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87m-4-12a4 4 0 0 1 0 7.75"></path></svg>`
   },
    {
      employee: 'Sarah Williams',
      action: 'joined project',
      target: 'Mobile App',
      time: '8 hours ago',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87m-4-12a4 4 0 0 1 0 7.75"></path></svg>`
    }
  ];

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

  ngOnInit(): void {
    // Component initialization
  }

  addEmployee(): void {
    console.log('Add employee clicked');
  }

  addCertification(): void {
    console.log('Add certification clicked');
  }

  addAssignment(): void {
    console.log('Add assignment clicked');
  }
}
