drop table if exists posts;
create table posts (
  id integer primary key autoincrement,
  title text not null,
  body text not null
);

insert into posts ('title', 'body') values ('first post', 'hello world');
insert into posts ('title', 'body') values ('second post', 'goodbye earth');

drop table if exists tags;
create table tags (
  id integer primary key autoincrement,
  name varchar(64) not null
);

insert into tags ('name') values ('programming');
insert into tags ('name') values ('design');

drop table if exists post_tags;
create table post_tags (
  post_id integer,
  tag_id integer
);

insert into post_tags values (1, 1);
insert into post_tags values (2, 2);

