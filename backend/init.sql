create table bs_manage.log
(
    scene_name  varchar(100) not null,
    room_name   varchar(100) not null,
    device_name varchar(100) not null,
    log         varchar(200) not null,
    primary key (scene_name, room_name, device_name, log)
);

create table bs_manage.user
(
    user     varchar(200) not null
        primary key,
    password varchar(200) not null,
    phone    varchar(200) not null,
    constraint user_pk
        unique (phone)
);

create table bs_manage.scene
(
    scene_name varchar(200) null,
    scene_id   int auto_increment
        primary key,
    user       varchar(200) not null,
    constraint scene_user_null_fk
        foreign key (user) references bs_manage.user (user)
);

create table bs_manage.room
(
    room_name varchar(200) null,
    room_id   int auto_increment
        primary key,
    scene_id  int          not null,
    constraint room_scene_null_fk
        foreign key (scene_id) references bs_manage.scene (scene_id)
);

create table bs_manage.device
(
    device_id    int auto_increment
        primary key,
    device_name  varchar(200)                                    null,
    device_info  varchar(200)                                    null,
    device_pos_x double default 0                                not null,
    device_pos_y double default 0                                not null,
    room_id      int                                             not null,
    device_type  enum ('light', 'door_lock', 'sensor', 'switch') not null,
    constraint device_room_room_id_fk
        foreign key (room_id) references bs_manage.room (room_id)
);

create definer = root@`%` trigger bs_manage.del_room_trigger
    before delete
    on bs_manage.room
    for each row
begin
    delete from device where device.room_id = old.room_id;
end;

create definer = root@`%` trigger bs_manage.del_scene_trigger
    before delete
    on bs_manage.scene
    for each row
begin
    delete from room where room.scene_id = old.scene_id;
end;

create definer = root@`%` trigger bs_manage.del_account_trigger
    before delete
    on bs_manage.user
    for each row
begin
    delete from scene where scene.user = old.user;
end;

