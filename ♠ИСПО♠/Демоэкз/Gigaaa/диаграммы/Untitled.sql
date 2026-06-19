CREATE TABLE [users] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [login] nvarchar(255) UNIQUE NOT NULL,
  [password] nvarchar(255) NOT NULL,
  [full_name] nvarchar(255) NOT NULL,
  [role] nvarchar(255) NOT NULL
)
GO

CREATE TABLE [categories] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [name] nvarchar(255) UNIQUE NOT NULL
)
GO

CREATE TABLE [suppliers] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [name] nvarchar(255) UNIQUE NOT NULL
)
GO

CREATE TABLE [products] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [name] nvarchar(255) NOT NULL,
  [description] text,
  [category_id] integer NOT NULL,
  [manufacturer] nvarchar(255),
  [supplier_id] integer NOT NULL,
  [price] real NOT NULL,
  [unit] nvarchar(255),
  [quantity] integer NOT NULL,
  [discount] real DEFAULT (0),
  [photo_path] text
)
GO

CREATE TABLE [orders] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [order_number] nvarchar(255) UNIQUE NOT NULL,
  [user_id] integer NOT NULL,
  [status] nvarchar(255) NOT NULL,
  [pickup_address] nvarchar(255) NOT NULL,
  [order_date] datetime NOT NULL,
  [delivery_date] datetime
)
GO

CREATE TABLE [order_details] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [order_id] integer NOT NULL,
  [product_id] integer NOT NULL,
  [quantity] integer NOT NULL,
  [price_at_order] real NOT NULL
)
GO

ALTER TABLE [products] ADD FOREIGN KEY ([category_id]) REFERENCES [categories] ([id])
GO

ALTER TABLE [products] ADD FOREIGN KEY ([supplier_id]) REFERENCES [suppliers] ([id])
GO

ALTER TABLE [orders] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([id])
GO

ALTER TABLE [order_details] ADD FOREIGN KEY ([order_id]) REFERENCES [orders] ([id])
GO

ALTER TABLE [order_details] ADD FOREIGN KEY ([product_id]) REFERENCES [products] ([id])
GO
