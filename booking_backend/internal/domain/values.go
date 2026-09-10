package domain

import "github.com/google/uuid"

type BookingID struct {
	value uuid.UUID
}

func NewBookingID() BookingID {
	return BookingID{
		value: uuid.New(),
	}
}

type CustomerID struct {
	value uuid.UUID
}

func NewCustomerID() CustomerID {
	return CustomerID{
		value: uuid.New(),
	}
}

type EventID struct {
	value uuid.UUID
}

func NewEventID() EventID {
	return EventID{
		value: uuid.New(),
	}
}

type BookingStatus string

type EventInfo struct {
	ID       EventID
	Name     string
	Capacity int
}

const (
	BookingStatusPending   BookingStatus = "pending"
	BookingStatusConfirmed BookingStatus = "confirmed"
	BookingStatusCancelled BookingStatus = "cancelled"
)
