# Система бронирования мест в кино/театр/мероприятие

## Сервисы

- Каталог
- Бронирование
- Заказ и оплата

## Стэк

- `Python`
  - FastAPI
  - Dishka
  - Adaptix
  - Sqlalchemy
  - Postgresql
- `Go`
- `TypeScript`
  - Vue
- `Infrastructure`
  - KeyCloack
  - KrakenD

## Бизнес

- Просмотр событий

- Бронь события
  - Создание брони
  - Просмотр броней
- Оплата
  - Создание заказа
  - Просмотр заказов
  - Отмена заказа
- Статусы оплаты товара
- Отмена товара

## События

- Booking
- CancelBooking

- OrderCreated
- OrderCanceled

- PaymentCompleted
- PaymentCanceled
