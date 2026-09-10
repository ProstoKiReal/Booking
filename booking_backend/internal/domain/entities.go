package domain

import (
	"time"
)

type Booking struct {
	ID         BookingID
	customerID CustomerID
	eventID    EventID
	status     BookingStatus
	createdAt  time.Time
	updatedAt  time.Time
}

func NewBooking(customerID CustomerID, eventID EventID) *Booking {
	return &Booking{
		ID:         NewBookingID(),
		customerID: customerID,
		eventID:    eventID,
		status:     BookingStatusPending,
		createdAt:  time.Now(),
		updatedAt:  time.Now(),
	}
}

func (b *Booking) Cancel(
	eventCreatedAt time.Time,
	availableTickets int,
	EventID EventID,
	CustomerID CustomerID,
) error {

	if b.status == BookingStatusCancelled {
		return BookingAlreadyCancelledError
	}
	if time.Since(eventCreatedAt) < 24*time.Hour {
		return BookingDeadlinePassedError
	}
	b.status = BookingStatusCancelled
	b.updatedAt = time.Now()
	b.customerID = CustomerID
	b.eventID = EventID

	return nil
}

func (b *Booking) Confirm() error {
	if b.status == BookingStatusConfirmed {
		return BookingAlreadyConfirmedError
	}
	b.status = BookingStatusConfirmed
	b.updatedAt = time.Now()

	return nil
}
