import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PodDialogComponent } from './pod-dialog.component';

describe('PodDialogComponent', () => {
  let component: PodDialogComponent;
  let fixture: ComponentFixture<PodDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PodDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PodDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
