package domain

import (
	"errors"
)

var (
	BookingAlreadyCancelledError = errors.New("booking is already cancelled")
	BookingDeadlinePassedError   = errors.New("booking deadline passed")
	BookingAlreadyConfirmedError = errors.New("booking is already confirmed")
	NoAvailableSeatsError        = errors.New("no available tickets")
)
