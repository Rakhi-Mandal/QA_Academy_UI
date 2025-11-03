import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MasteryProgramComponent } from './mastery-program.component';

describe('MasteryProgramComponent', () => {
  let component: MasteryProgramComponent;
  let fixture: ComponentFixture<MasteryProgramComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MasteryProgramComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MasteryProgramComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
