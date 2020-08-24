CREATE TABLE timeseries (
`name` varchar(50)NOT NULL,
`time` float,
`record_source` varchar(50)NOT NULL,
`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);