-- Table: users
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password CHAR(60) NOT NULL,
  profile TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table: recipes
CREATE TABLE recipes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_recipes_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table: stores
CREATE TABLE stores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  latitude DECIMAL(9,6) NOT NULL,
  longitude DECIMAL(9,6) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- Table: recipe_follows
CREATE TABLE recipe_follows (
  id INT AUTO_INCREMENT PRIMARY KEY,
  recipe_id INT NOT NULL,
  store_id INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_recipe_follows_recipe FOREIGN KEY (recipe_id) REFERENCES recipes(id),
  CONSTRAINT fk_recipe_follows_store FOREIGN KEY (store_id) REFERENCES stores(id),
  UNIQUE KEY uq_recipe_store (recipe_id, store_id),
  KEY idx_recipe_follows_recipe (recipe_id),
  KEY idx_recipe_follows_store  (store_id)
);

-- Table: saves
CREATE TABLE saves (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  recipe_id INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_saves_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_saves_recipe FOREIGN KEY (recipe_id) REFERENCES recipes(id),
  UNIQUE KEY uq_user_recipe (user_id, recipe_id),
  KEY idx_saves_user   (user_id),
  KEY idx_saves_recipe (recipe_id)
);

--------------------------------------------------------------------------------
-- CREATE TABLE ingredient_library (
--   id INT PRIMARY KEY AUTO_INCREMENT,
--   name VARCHAR(255) NOT NULL,
--   unit_type ENUM('mass', 'volume', 'count', 'other'),
--   common_units JSON,
--   keywords TEXT
-- );

CREATE TABLE ingredient_library (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100),
  brand VARCHAR(100),
  unit VARCHAR(50),
  shelf_life_days INT,
  origin VARCHAR(100),
  is_organic BOOLEAN DEFAULT FALSE,
  thumbnail_url VARCHAR(500),
  barcode VARCHAR(50),
  allergens JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE ingredient_prep_options (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ingredient_id INT,
  prep_method VARCHAR(100),
  FOREIGN KEY (ingredient_id) REFERENCES ingredient_library(id) ON DELETE CASCADE
);

-- Table: recipe_directions
CREATE TABLE recipe_directions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  recipe_id INT NOT NULL,
  full_text TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Table: recipe_direction_steps
CREATE TABLE recipe_direction_steps (
  id INT AUTO_INCREMENT PRIMARY KEY,
  direction_id INT NOT NULL,
  step_number INT NOT NULL,
  start_time VARCHAR(20),
  end_time VARCHAR(20),
  text TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (direction_id) REFERENCES recipe_directions(id) ON DELETE CASCADE
);