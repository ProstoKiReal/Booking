package domain

type EventAvailability struct {
	EventID     EventID
	capacity    int
	bookedSeats int
}

func (ea *EventAvailability) Reserve() error {
	if ea.bookedSeats >= ea.capacity {
		return NoAvailableSeatsError
	}

	ea.bookedSeats++

	return nil
}
