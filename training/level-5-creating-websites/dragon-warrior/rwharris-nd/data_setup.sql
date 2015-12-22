DROP TABLE IF EXISTS attributes;

DROP TABLE IF EXISTS hours;

CREATE TABLE attributes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team TEXT NOT NULL,
  attribute_name TEXT NOT NULL,
  attribute_value TEXT NOT NULL
);

CREATE TABLE schedules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team TEXT NOT NULL,
  day INTEGER NOT NULL,
  start TEXT NOT NULL,
  end TEXT NOT NULL,
  type INTEGER NOT NULL
);

INSERT INTO attributes (team, attribute_name, attribute_value) VALUES
  ('HD', 'status', 'normal'),
  ('HD', 'students', 'true');

INSERT INTO schedules (team, day, start, end, type) VALUES
  ('HD', 1,'7:30 AM EST', '6:00 PM EST', 'Standard'),
  ('HD', 2,'7:30 AM EST', '6:00 PM EST', 'Standard'),
  ('HD', 3,'7:30 AM EST', '12:00 PM EST', 'Standard'),
  ('HD', 3,'1:30 PM EST', '6:00 PM EST', 'Standard'),
  ('HD', 4,'7:30 AM EST', '6:00 PM EST', 'Standard'),
  ('HD', 5,'7:30 AM EST', '5:00 PM EST', 'Standard'),
  ('HD', 0,'3:00 PM EST', '8:00 PM EST', 'Extended'),
  ('HD', 1,'7:30 AM EST', '8:00 PM EST', 'Extended'),
  ('HD', 2,'7:30 AM EST', '8:00 PM EST', 'Extended'),
  ('HD', 3,'7:30 AM EST', '12:00 PM EST', 'Extended'),
  ('HD', 3,'1:30 PM EST', '8:00 PM EST', 'Extended'),
  ('HD', 4,'7:30 AM EST', '8:00 PM EST', 'Extended'),
  ('HD', 5,'7:30 AM EST', '5:00 PM EST', 'Extended');