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
│   │   ├── pages/           # Page components (dashboard, auth, forms, etc.)
│   │   ├── shared/          # Shared components, layout, services, pipes
│   │   └── app.routes.ts    # Application routing
│   ├── custom-theme.scss    # Material theme customization
│   ├── styles.css           # Global styles
│   └── main.ts              # Application entry point
├── public/                  # Static assets (images, icons, logos)
├── angular.json            # Angular workspace configuration
└── package.json            # Dependencies and scripts

academy_Backend/
└── notes.txt              # Backend notes (no actual backend implemented)
```

## Recent Changes

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
- 1 unique ecommerce dashboard
- 100+ UI elements and components
- Authentication pages (sign-in, sign-up)
- Multiple dashboard layouts (FastTrack, Advanced Track, Mastery Program)
- Charts and data visualization (bar, line charts)
- Form elements and components
- Dark mode support
- Responsive design
- Material Design components
- Profile management
- Employee management dialogs

## Notes
- The `academy_Backend/` folder only contains a notes.txt file with dependency info
- No actual backend is implemented in this project
- This is a frontend-only admin dashboard template
- Built with Angular 20's latest features and standalone components architecture
