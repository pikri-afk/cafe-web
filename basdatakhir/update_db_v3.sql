USE cafe_management;

-- 1. Add id_user to pelanggan table
ALTER TABLE pelanggan ADD COLUMN id_user INT UNIQUE AFTER id_pelanggan;
ALTER TABLE pelanggan ADD FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE SET NULL;

-- 2. Create pelanggan records for existing customer users
INSERT INTO pelanggan (nama, id_user)
SELECT nama_lengkap, id_user FROM users 
WHERE role = 'customer'
AND id_user NOT IN (SELECT id_user FROM pelanggan WHERE id_user IS NOT NULL);

-- 3. Link existing transactions where id_pelanggan is NULL but id_user belongs to a customer
UPDATE transaksi t
JOIN pelanggan p ON t.id_user = p.id_user
SET t.id_pelanggan = p.id_pelanggan
WHERE t.id_pelanggan IS NULL;
