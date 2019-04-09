CREATE DATABASE BucketList;

/* USER 테이블 생성 */
CREATE TABLE `BucketList`.`tbl_user` (
	`user_id` BIGINT AUTO_INCREMENT,
	`user_name` VARCHAR(100) NULL,
    `user_username` VARCHAR(100) NULL,
    `user_password` VARCHAR(100) NULL,
    PRIMARY KEY (`user_id`)
);

/* USER 생성 프로시져 */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser` (
	IN p_name VARCHAR(100),
    IN p_username VARCHAR(100),
    IN p_password VARCHAR(100)
)
BEGIN
	IF ( SELECT EXISTS (SELECT 1 FROM tbl_user WHERE user_username = p_username) ) THEN
		SELECT 'Username Exists !!';
	ELSE
		INSERT INTO tbl_user (
			user_name,
            user_username,
            user_password
		)
        VALUES (
			p_name,
            p_username,
            p_password
		);
	END IF;
END$$
DELIMITER ;

SELECT * FROM tbl_user;