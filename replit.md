# TailAdmin Angular Dashboard

## Overview
This is a free and open-source Angular 20 admin dashboard template built with Angular, TypeScript, and Tailwind CSS v4. It provides a complete set of dashboard UI components, elements, and ready-to-use pages for building feature-rich back-end dashboards or admin panels.

## Project Status
- **Current State**: Fully set up and running in Replit environment
- **Last Updated**: November 7, 2025
- **Branch**: main (feature/updatedEmployee branch requested but not found in repository)

## Architecture

### Technology Stack
- **Frontend Framework**: Angular 20+
- **Language**: TypeScript 5.8.3
- **Styling**: Tailwind CSS v4
- **Charts**: ApexCharts, AMCharts 5
- **UI Components**: Angular Material 20, FullCalendar
- **Dev Server Port**: 5000
- **Build Tool**: Angular CLI with application builder

### Project Structure
```
academy_UI/
├── src/
│   ├── app/
│   │   ├── pages/
│   │   │   ├── dashboard/
│   │   │   │   └── fastrack/          # Fastrack Batch Employees table
│   │   │   ├── calendar/              # Admin calendar component
│   │   │   ├── employee-calendar/     # Employee calendar component (NEW)
│   │   │   ├── profile/               # User profile component
│   │   │   ├── auth-pages/            # Sign-in, Sign-up
│   │   │   └── ...
│   │   ├── shared/
│   │   │   ├── layout/
│   │   │   │   ├── app-sidebar/       # Dynamic role-based navigation (NEW)
│   │   │   │   ├── app-header/
│   │   │   │   └── app-layout/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   │   └── calendar-data.service.ts
│   │   │   └── models/
│   │   └── app.routes.ts              # Role-based routing (UPDATED)
│   ├── custom-theme.scss
│   ├── styles.css
│   └── main.ts
├── public/
├── angular.json
└── package.json

academy_Backend/
└── notes.txt
```

## Recent Changes

### Role-Based Navigation System (November 8, 2025)
- **Dual-View Architecture**: Implemented separate admin and employee views with distinct navigation
  - Admin view: Batches (FastTrack, Advanced Track, Mastery Program) + Calendar
  - Employee view: My Profile + My Calendar
- **Employee Calendar Component**: Created dedicated employee-calendar component
  - Full-featured with stats cards and submission functionality for employee self-tracking
  - Shares calendar data service for consistency
  - Independent component at `academy_UI/src/app/pages/employee-calendar/`
- **Admin Calendar Component**: Streamlined view for administrative oversight
  - Stats cards showing only Assignments (19) and Certifications (12) counts
  - No status badges (Assigned, Completed, Upcoming) on timeline cards
  - No submit buttons on assignment/certification cards
  - Read-only timeline and calendar grid views for tracking purposes
- **Dynamic Sidebar Navigation**: Role-based menu items that switch based on current route
  - Automatically detects admin vs employee routes from URL
  - Separate `adminNavItems` and `employeeNavItems` arrays
  - URL detection logic: `/admin/*` shows admin menu, `/employee/*` shows employee menu
- **Route Structure**: Organized paths with role prefixes for clear separation
  - Admin routes: `/admin/track1`, `/admin/track2`, `/admin/track3`, `/admin/calendar`
  - Employee routes: `/employee/profile`, `/employee/calendar`
  - Legacy route redirects for backward compatibility
- **Updated Components**: 
  - `app.routes.ts`: Added role-based routing with data attributes
  - `app-sidebar.component.ts`: Dynamic navigation switching based on route detection
  - `calendar.component.html`: Removed stats cards and submit buttons for admin view
  - Default route redirects to `/admin/track1`

### Calendar UI Enhancements (November 7, 2025)
- **Compact Card Design**: Optimized timeline cards for professional, space-efficient layout
  - Reduced padding (p-6→p-4), tighter gaps (gap-3→gap-2), smaller margins (mb-3→mb-2)
  - Smaller icons (w-6→w-5, p-3→p-2), compact badges (px-4 py-1.5→px-3 py-1)
  - Reduced text sizes: title (text-lg→text-base), date (text-lg→text-base), day (text-sm→text-xs)
  - Proportionally sized submit buttons (px-6 py-2→px-5 py-1.5) for balanced appearance
- **Modern Card Design**: Added half-circle abstract design elements to timeline cards
  - Positioned in top-right corner with 120px diameter
  - Gradient backgrounds: blue for assessments, yellow for certifications
  - Smooth 50% expansion on hover (120px→180px) with ease-in-out transition
  - Pure CSS animations (0.5s ease-in-out) for jerk-free, fluid motion
- **Enhanced Filter Buttons**: Added active/clicked states for all filter buttons
  - "All Items": Cyan (#00A8CC) active state
  - "Assignments": Blue (#0066CC) active state
  - "Certifications": Orange (#FFA500) active state
  - Animated underline effect (::after pseudo-element) for active filter
  - Smooth transitions with lift effect on hover
- **Card Interactions**: Professional hover effects throughout
  - Lift and scale animation (translateY(-6px) scale(1.01))
  - Enhanced shadow on hover (0 10px 20px)
  - Badge scale effect (1.1x) on hover
  - Stable icons (no rotation) for clean, professional appearance
- **SCSS Architecture**: Migrated to component-specific SCSS for better maintainability
  - Organized styles with proper pseudo-elements
  - Accessibility support (prefers-reduced-motion)
  - Professional dashboard-like appearance with optimized spacing

### Assessments & Certifications Calendar (November 7, 2025)
- **Completion Tracking System**: Full-featured submission and completion workflow
  - FormSubmissionDialogComponent with reactive forms (score, notes, file attachments)
  - CalendarDataService manages completion state with BehaviorSubjects
  - localStorage persistence with proper Date object hydration for nested metadata
  - Strike-through styling for completed items with disabled "Completed" button
  - Dynamic count updates: "0 Completed", "31 Remaining" badges sync with state
- **Dual-View System**: Timeline View and Calendar Grid View with smooth transitions
- **19 Assessments**: Across 6 waves (1A-6D including QE Innovation Hackathon)
- **12 Certifications**: Using ProProfs, HackerRank, Codility, ISTQB, Azure platforms
- **Advanced Filtering**: All Items, Assignments, and Certifications filters with sync
- **Rich Animations**: Scale, bounce, stagger, hover effects, view transitions
- **Calendar Features**: Month navigation, date-based mapping, responsive grid
- **Custom Color Scheme**: Blue (#E1F3FF) for assignments, Yellow (#FFF4E1) for certifications

### Replit Environment Setup (November 7, 2025)
- Configured Angular dev server to run on port 5000 with host 0.0.0.0
- Set `allowedHosts: ["all"]` to support Replit's proxy infrastructure
- Installed all npm dependencies (766 packages including http-server)
- Added http-server as runtime dependency for deployment static file serving
- Created frontend workflow for development server
- Configured deployment for autoscale with production build

## Development

### Running the Application
The application runs automatically via the configured workflow. To manually start:
```bash
cd academy_UI
npm start
```
The dev server will be available at http://localhost:5000/

### Available Scripts
- `npm start` - Start development server
- `npm run build` - Build for production
- `npm run watch` - Build in watch mode
- `npm test` - Run unit tests

### Key Configuration
- **Port**: 5000 (required for Replit webview)
- **Host**: 0.0.0.0 (allows external connections)
- **Allowed Hosts**: ["all"] (supports Replit proxy)
- **Analytics**: Disabled in Angular CLI

## Deployment
Configured for Replit autoscale deployment:
- **Build**: `npm run build --prefix academy_UI`
- **Run**: Serves built files from `academy_UI/dist/ng-tailadmin/browser` on port 5000
- **Server**: http-server for static file serving

## Features
- **Role-Based Views**: Separate admin and employee interfaces with distinct navigation
- **Admin Dashboard**: Batch management (FastTrack, Advanced Track, Mastery Program) + Calendar
- **Employee Dashboard**: Personal profile + Personal calendar for assessments & certifications
- 100+ UI elements and components
- Authentication pages (sign-in, sign-up)
- Charts and data visualization (bar, line charts)
- Form elements and components
- Dark mode support
- Responsive design
- Material Design components
- Profile management
- Employee management with advanced table features (hover animations, tooltips, filtering)

## Notes
- The `academy_Backend/` folder only contains a notes.txt file with dependency info
- No actual backend is implemented in this project
- This is a frontend-only admin dashboard template
- Built with Angular 20's latest features and standalone components architecture
