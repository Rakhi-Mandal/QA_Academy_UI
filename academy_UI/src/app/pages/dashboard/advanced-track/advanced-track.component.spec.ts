import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdvancedTrackComponent } from './advanced-track.component';

describe('AdvancedTrackComponent', () => {
  let component: AdvancedTrackComponent;
  let fixture: ComponentFixture<AdvancedTrackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdvancedTrackComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdvancedTrackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
