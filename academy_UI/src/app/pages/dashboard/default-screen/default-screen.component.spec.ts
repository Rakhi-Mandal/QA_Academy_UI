import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DefaultScreenComponent } from './default-screen.component';

describe('DefaultScreenComponent', () => {
  let component: DefaultScreenComponent;
  let fixture: ComponentFixture<DefaultScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DefaultScreenComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DefaultScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
