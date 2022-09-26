with pix_transactions AS (
SELECT
	account_id,
	amount,
	'PIX' AS transaction_type,
	dt AS date
FROM
	pix_send
),

bank_slip_transactions AS (
SELECT
	account_id,
	amount ,
	'BANK_SLIP' AS transaction_type,
	dt AS date
FROM
	bank_slip
),

p2p_transactions AS (
SELECT
	account_id_source,
	amount,
	'P2P' AS transaction_type,
	dt AS date
FROM
	p2p_tef
),

transactions AS (
	SELECT * FROM pix_transactions
	UNION ALL
	SELECT * FROM bank_slip_transactions
	UNION ALL
	SELECT * FROM p2p_transactions
)

SELECT
	account.account_id,
	customer.customer_id,
	customer.name,
	transactions.date,
	transactions.transaction_type,
	AVG(transactions.amount) AS mean_value

FROM
	account
	INNER JOIN customer
		ON account.customer_id = customer.customer_id
	INNER JOIN transactions
		ON account.account_id = transactions.account_id

GROUP BY
	account.account_id,
	customer.customer_id,
	customer.name,
	transactions.transaction_type,
	transactions.date
