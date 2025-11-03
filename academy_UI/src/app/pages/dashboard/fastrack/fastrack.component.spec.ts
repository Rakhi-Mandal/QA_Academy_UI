import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FastrackComponent } from './fastrack.component';

describe('FastrackComponent', () => {
  let component: FastrackComponent;
  let fixture: ComponentFixture<FastrackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FastrackComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FastrackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
