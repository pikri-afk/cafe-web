USE cafe_management;
UPDATE users 
SET password = 'scrypt:32768:8:1$Z1AeWgz7PZKfaqgM$5d2e45970e483694341b91bc28ac76fce188a5896d8e48fbaa8172ae762ba048af8402320169fa4265aee6f938b0d9a64695e9d0a817762f9971c383c76f47b1'
WHERE username IN ('kasir2', 'customer1');
