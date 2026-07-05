import { TestBed } from '@angular/core/testing';

import { EventService } from './event.service';

describe('EventService', () => {
  let service: EventService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EventService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should call service methods without error', () => {
    expect(service.getEvents).toBeDefined();
    expect(service.addEvent).toBeDefined();
    expect(service.registerStudent).toBeDefined();
    expect(service.adminLogin).toBeDefined();
  });

});