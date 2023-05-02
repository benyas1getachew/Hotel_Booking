import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopHotelsComponent } from './top-hotels.component';

describe('TopHotelsComponent', () => {
  let component: TopHotelsComponent;
  let fixture: ComponentFixture<TopHotelsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TopHotelsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TopHotelsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
