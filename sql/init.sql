create table user(
    steam_id bigint(15) PRIMARY KEY,
    nickname varchar(64)
);

create table match(
    match_id bigint(15),
    steam_id bigint(15),
    PRIMARY KEY (match_id, steam_id)
);

create table hero(
    hero_id int,
    hero_name text,
    PRIMARY key (hero_id)
);

