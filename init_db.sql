drop table if exists posts;

create table posts (
  id integer primary key autoincrement,
  title text not null,
  body text not null
);

insert into posts values (1, 'first post', 'hello world');
insert into posts values (2, 'second post', 'goodbye earth');

