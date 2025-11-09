import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
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
  percentage: string;
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
  imports: [CommonModule, NgApexchartsModule],
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
      value: 1234,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
      iconBg: 'bg-blue-50',
      percentage: '+12%',
      trend: 'up'
    },
    {
      title: 'Avg Performance',
      value: '87%',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>`,
      iconBg: 'bg-green-50',
      percentage: '+5%',
      trend: 'up'
    },
    {
      title: 'Certifications',
      value: 432,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>`,
      iconBg: 'bg-yellow-50',
      percentage: '+18%',
      trend: 'up'
    },
    {
      title: 'Active Projects',
      value: 56,
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>`,
      iconBg: 'bg-purple-50',
      percentage: '+3%',
      trend: 'up'
    }
  ];

  recentActivities: Activity[] = [
    {
      employee: 'John Doe',
      action: 'completed certification',
      target: 'AWS Cloud',
      time: '2 hours ago',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="m9 12 2 2 4-4"></path></svg>`
    },
    {
      employee: 'Jane Smith',
      action: 'started assessment',
      target: 'React Advanced',
      time: '4 hours ago',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>`
    },
    {
      employee: 'Mike Johnson',
      action: 'achieved 95% score',
      target: 'JavaScript',
      time: '6 hours ago',
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>`
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
