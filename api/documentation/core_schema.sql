CREATE SCHEMA `core`;

CREATE TABLE `core`.`user` (
  `id` integer PRIMARY KEY,
  `firstname` varchar(255),
  `lastname` varchar(255),
  `company` varchar(255),
  `email` varchar(255) UNIQUE NOT NULL,
  `password` varchar(255),
  `is_superuser` integer DEFAULT false,
  `is_staff` integer DEFAULT false,
  `is_active` integer NOT NULL,
  `is_confirmed` integer DEFAULT false,
  `date_joind` timestamp DEFAULT (now())
);

CREATE TABLE `core`.`prebuilt_model` (
  `id` integer PRIMARY KEY,
  `name` varchar(255),
  `document` varchar(255)
);

CREATE TABLE `core`.`dataset` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `project_id` integer NOT NULL,
  `reference` varchar(255) NOT NULL COMMENT 'this reference will be used to identify images on the NoSQL database',
  `annotation_percent` integer DEFAULT 0,
  `labels` json
);

CREATE TABLE `core`.`project` (
  `id` integer PRIMARY KEY,
  `prebuilt_model_id` integer,
  `user_id` integer NOT NULL,
  `type` ENUM ('BASED_ON_PREBUILT_MODEL', 'CUSTOM_MODEL'),
  `state` ENUM ('ABLE_TO_BE_TRAINED', 'TRAINED', 'DEPLOYED'),
  `name` varchar(255) NOT NULL,
  `description` varchar(255)
);

ALTER TABLE `core`.`project` ADD FOREIGN KEY (`user_id`) REFERENCES `core`.`user` (`id`);

ALTER TABLE `core`.`project` ADD FOREIGN KEY (`prebuilt_model_id`) REFERENCES `core`.`prebuilt_model` (`id`);

ALTER TABLE `core`.`dataset` ADD CONSTRAINT `projects_datasets` FOREIGN KEY (`id`) REFERENCES `core`.`project` (`id`);
