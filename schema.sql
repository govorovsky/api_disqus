SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `mydb` ;
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`users` ;

CREATE TABLE IF NOT EXISTS `mydb`.`users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL,
  `email` VARCHAR(255) NOT NULL,
  `anonymous` TINYINT(1) UNSIGNED NULL DEFAULT 0,
  `about` VARCHAR(300) NULL,
  `name` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`forums`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`forums` ;

CREATE TABLE IF NOT EXISTS `mydb`.`forums` (
  `fid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(145) NOT NULL,
  `founder_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `shortname` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`fid`),
  INDEX `fk_forums_users1_idx` (`founder_id` ASC),
  UNIQUE INDEX `shortname_UNIQUE` (`shortname` ASC),
  CONSTRAINT `fk_forums_users1`
    FOREIGN KEY (`founder_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`threads`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`threads` ;

CREATE TABLE IF NOT EXISTS `mydb`.`threads` (
  `tid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(145) NOT NULL,
  `date` TIMESTAMP NOT NULL,
  `message` TEXT NOT NULL,
  `forum_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `deleted` TINYINT NOT NULL DEFAULT 0,
  `closed` TINYINT NOT NULL DEFAULT 0,
  `slug` VARCHAR(65) NOT NULL,
  `likes` INT UNSIGNED NOT NULL DEFAULT 0,
  `dislikes` INT UNSIGNED NOT NULL DEFAULT 0,
  `points` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`tid`),
  INDEX `fk_topics_forums_idx` (`forum_id` ASC),
  INDEX `fk_topics_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_topics_forums`
    FOREIGN KEY (`forum_id`)
    REFERENCES `mydb`.`forums` (`fid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`posts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`posts` ;

CREATE TABLE IF NOT EXISTS `mydb`.`posts` (
  `pid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `message` TEXT NOT NULL,
  `date` TIMESTAMP NOT NULL,
  `thread_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `parent` INT UNSIGNED NULL,
  `approved` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `deleted` TINYINT NOT NULL DEFAULT 0,
  `edited` TINYINT NOT NULL DEFAULT 0,
  `spam` TINYINT NOT NULL DEFAULT 0,
  `highlighted` TINYINT NOT NULL DEFAULT 0,
  `forum_id` INT UNSIGNED NOT NULL,
  `likes` INT UNSIGNED NOT NULL DEFAULT 0,
  `dislikes` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`pid`),
  INDEX `fk_replies_topics1_idx` (`thread_id` ASC),
  INDEX `fk_replies_users1_idx` (`user_id` ASC),
  INDEX `fk_posts_posts1_idx` (`parent` ASC),
  INDEX `fk_posts_forums1_idx` (`forum_id` ASC),
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`thread_id`)
    REFERENCES `mydb`.`threads` (`tid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_posts1`
    FOREIGN KEY (`parent`)
    REFERENCES `mydb`.`posts` (`pid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_forums1`
    FOREIGN KEY (`forum_id`)
    REFERENCES `mydb`.`forums` (`fid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`subscriptions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`subscriptions` ;

CREATE TABLE IF NOT EXISTS `mydb`.`subscriptions` (
  `users_id` INT UNSIGNED NOT NULL,
  `threads_id` INT UNSIGNED NOT NULL,
  `active` TINYINT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`users_id`, `threads_id`),
  INDEX `fk_users_has_threads_threads1_idx` (`threads_id` ASC),
  INDEX `fk_users_has_threads_users1_idx` (`users_id` ASC),
  CONSTRAINT `fk_users_has_threads_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_threads_threads1`
    FOREIGN KEY (`threads_id`)
    REFERENCES `mydb`.`threads` (`tid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`followers` ;

CREATE TABLE IF NOT EXISTS `mydb`.`followers` (
  `follower` INT UNSIGNED NOT NULL,
  `followee` INT UNSIGNED NOT NULL,
  `active` TINYINT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`follower`, `followee`),
  INDEX `fk_users_has_users_users3_idx` (`followee` ASC),
  INDEX `fk_users_has_users_users2_idx` (`follower` ASC),
  CONSTRAINT `fk_users_has_users_users2`
    FOREIGN KEY (`follower`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_users_users3`
    FOREIGN KEY (`followee`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`followers` ;

CREATE TABLE IF NOT EXISTS `mydb`.`followers` (
  `follower` INT UNSIGNED NOT NULL,
  `followee` INT UNSIGNED NOT NULL,
  `active` TINYINT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`follower`, `followee`),
  INDEX `fk_users_has_users_users3_idx` (`followee` ASC),
  INDEX `fk_users_has_users_users2_idx` (`follower` ASC),
  CONSTRAINT `fk_users_has_users_users2`
    FOREIGN KEY (`follower`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_users_users3`
    FOREIGN KEY (`followee`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
