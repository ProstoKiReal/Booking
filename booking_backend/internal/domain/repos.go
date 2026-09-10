package domain

type BookingRepo interface {
	GetByID(id BookingID) (*Booking, error)
	GetByCustomerID(customerID CustomerID) ([]*Booking, error)
	GetByCustomerAndEvent(
		customerID CustomerID,
		eventID EventID,
	) (*Booking, error)
	Save(booking *Booking) error
}

type EventAvailabilityRepo interface {
	Get(eventId EventID) (*EventAvailability, error)
	Save(availability *EventAvailability) error
}

type EventInfoRepo interface {
	Get(eventId EventID) (*EventInfo, error)
}
