
-- Table : users

create table users (
    id serial primary key,
    name text not null,
    email text unique not null,
    role text not null check (role in('admin','engineer','viewer')),
    password text not null

);

-- Table : machines

create table machines(
    id serial primary key,
    machine_name text not null
);

-- Table : File versions 

create table file_versions(
    id serial primary key,
    file_name text not null,
    machine_id integer references machines(id) on delete cascade,
    uploaded_by integer references users(id) on delete set null,
    version_no integer not null,
    upload_time timestamp default CURRENT_TIMESTAMP,
    file_hash text not null,
    storage_path text not null

);