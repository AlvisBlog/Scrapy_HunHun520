USE hunhun520;
-- auto-generated definition
CREATE TABLE novel_info
(
  id              INT AUTO_INCREMENT
    PRIMARY KEY,
  novel_name      VARCHAR(100) NULL,
  novel_author    VARCHAR(100) NULL,
  novel_link      VARCHAR(300) NULL,
  novel_type      VARCHAR(100) NULL,
  novel_introduce TEXT         NULL,
  CONSTRAINT table_name_id_uindex
  UNIQUE (id),
  CONSTRAINT table_name_novel_name_uindex
  UNIQUE (novel_name)
);


-- auto-generated definition
CREATE TABLE chapter_info
(
  id                       INT AUTO_INCREMENT
    PRIMARY KEY,
  chapter_id               INT          NULL,
  chapter_link             VARCHAR(300) NULL,
  chapter_name             VARCHAR(100) NULL,
  chapter_content          TEXT         NULL,
  chapter_related_to_novel VARCHAR(100) NULL,
  CONSTRAINT chapter_info_id_uindex
  UNIQUE (id),
  CONSTRAINT chapter_info_chapter_id_uindex
  UNIQUE (chapter_id)
);
