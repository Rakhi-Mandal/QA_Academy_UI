import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CertificationDialogComponent } from './certification-dialog.component';

describe('CertificationDialogComponent', () => {
  let component: CertificationDialogComponent;
  let fixture: ComponentFixture<CertificationDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CertificationDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CertificationDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
