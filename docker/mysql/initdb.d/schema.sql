CREATE TABLE record_table (
    id INT NOT NULL AUTO_INCREMENT,
    dt DATETIME,
    file_address VARCHAR(150) NOT NULL,
    ticket VARCHAR(30) NOT NULL,
    finished BOOLEAN NOT NULL,
    result VARCHAR(4000),
    ali_result VARCHAR(4000),
    PRIMARY KEY (id)
) CHARACTER SET = utf8;

CREATE TABLE record_table_temp (
    id INT NOT NULL AUTO_INCREMENT,
    file_address VARCHAR(150) NOT NULL,
    ticket VARCHAR(30) NOT NULL,
    result VARCHAR(4000),
    PRIMARY KEY (id)
) CHARACTER SET = utf8;
