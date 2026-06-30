-- ════════════════════════════════════════════════════════════════
--  Menú del día — setup de Supabase
--  Proyecto reutilizado: mveidasopqzphghnoyxc
--  Ejecutar UNA vez en el SQL Editor de Supabase.
--  No toca ni depende de las tablas de La Agenda 2.0.
-- ════════════════════════════════════════════════════════════════

-- 1) Tabla: un registro por local (se sobrescribe al publicar, como el papel)
create table if not exists menus_dia (
  local_id       text primary key,   -- 'la_pequena','las_tablas','la_chula','la_traviesa','la_peluqueria','juanita','green'
  fecha_texto    text,               -- texto libre, ej: "Lunes 22 de junio"
  primero        text,
  segundo        text,
  postre         text,
  incluye        text,               -- ej: "Pan, bebida y café"
  precio         text,               -- ej: "16,50 €"
  actualizado_en timestamptz default now(),
  actualizado_por text               -- nombre/rol de quien publicó
);

-- 2) RLS: lectura pública (anon) SOLO en esta tabla, para que menu.html lea sin PIN.
alter table menus_dia enable row level security;

-- Lectura pública (anon + authenticated)
drop policy if exists "menus_dia lectura publica" on menus_dia;
create policy "menus_dia lectura publica"
  on menus_dia for select
  using (true);

-- Escritura (insert/update) desde la app con la anon key (mismo patrón que el resto del proyecto).
-- El control de acceso real lo hace el PIN en admin.html.
drop policy if exists "menus_dia escritura app" on menus_dia;
create policy "menus_dia escritura app"
  on menus_dia for insert
  with check (true);

drop policy if exists "menus_dia update app" on menus_dia;
create policy "menus_dia update app"
  on menus_dia for update
  using (true) with check (true);

-- 3) (Opcional) fila de prueba para verificar menu.html antes de tener el panel:
insert into menus_dia (local_id, fecha_texto, primero, segundo, postre, incluye, precio, actualizado_por)
values ('la_pequena', 'Lunes 30 de junio',
        'Ensalada de tomate, ventresca y cebolla dulce',
        'Lubina a la espalda con verduras de temporada',
        'Tarta de queso casera',
        'Pan, bebida y café', '16,50 €', 'Prueba')
on conflict (local_id) do update set
  fecha_texto=excluded.fecha_texto, primero=excluded.primero, segundo=excluded.segundo,
  postre=excluded.postre, incluye=excluded.incluye, precio=excluded.precio,
  actualizado_por=excluded.actualizado_por, actualizado_en=now();
