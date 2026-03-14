CREATE TABLE payments (
	payment_id int8 NULL,
	order_id int8 NULL,
	payment_time timestamp NULL,
	payment_method text NULL,
	payment_status text NULL,
	payment_amount float8 NULL
);