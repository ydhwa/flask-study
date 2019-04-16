/* 사용자의 유효성을 검사하기 위한 MySQL 저장 프로시저 */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin` (
	IN p_username VARCHAR(20)
)
BEGIN
	select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;

