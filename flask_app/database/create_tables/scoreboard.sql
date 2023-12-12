CREATE TABLE IF NOT EXISTS `scoreboard` (
`user_score_id`         int(11)  	   NOT NULL auto_increment	  COMMENT 'the id of this user',
`email`           varchar(100) NOT NULL            		  COMMENT 'the email',
`time_taken`       time DEFAULT NULL                COMMENT 'time taken by user to finish todays wordle',
PRIMARY KEY (`user_score_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains worlde scorebaord user information";