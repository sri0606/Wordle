CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`        int(11)       NOT NULL  AUTO_INCREMENT  COMMENT 'A comment id', 
`name`              varchar(100)  NOT NULL              COMMENT 'The name of the commentator',
`email`             varchar(100)  NOT NULL            	COMMENT 'The email of the commentator',
`comment`           varchar(100)  NOT NULL            	COMMENT 'The comment.',

PRIMARY KEY  (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Users feedback on website.";