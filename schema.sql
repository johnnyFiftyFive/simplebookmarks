drop table if exists entries;
create table links (
  id integer primary key autoincrement,
  title text not null,
  'url' text not null
);