-- ============================================================
-- 1. Indexes for Filtering by Specific Attributes
-- ============================================================

-- Index for filtering by category name.
CREATE INDEX idx_categories_name ON categories (name);

-- Index for filtering apps by category.
CREATE INDEX idx_apps_category_id ON apps (category_id);

-- Index for filtering apps by rating.
CREATE INDEX idx_apps_rating ON apps (rating);

-- Index for filtering apps by price.
CREATE INDEX idx_apps_price ON apps (price);

-- Index for filtering apps by number of installs.
CREATE INDEX idx_apps_installs ON apps (installs);

-- Index for filtering apps by content rating.
CREATE INDEX idx_apps_content_rating ON apps (content_rating);

-- Index for filtering apps by "free" status.
CREATE INDEX idx_apps_free ON apps (free);

-- Index for filtering apps by ad-supported status.
CREATE INDEX idx_apps_ad_supported ON apps (ad_supported);

-- Index for filtering apps by in-app purchases availability.
CREATE INDEX idx_apps_in_app_purchases ON apps (in_app_purchases);

-- Index for filtering apps by Editors' Choice status.
CREATE INDEX idx_apps_editors_choice ON apps (editors_choice);


-- ============================================================
-- 2. Composite Indexes for Common Filter Combinations
-- ============================================================

-- Index for filtering by category and rating (common filter)
CREATE INDEX idx_apps_category_rating ON apps (category_id, rating);

-- Index for filtering by category and price range
CREATE INDEX idx_apps_category_price ON apps (category_id, price);

-- Index for filtering by category and install count (popularity)
CREATE INDEX idx_apps_category_installs ON apps (category_id, installs);

-- Index for filtering by multiple boolean flags
CREATE INDEX idx_apps_free_ad_supported_in_app_purchases
    ON apps (free, ad_supported, in_app_purchases, editors_choice);

-- Index for filtering by category and release date (useful for trend analysis)
CREATE INDEX idx_apps_category_released ON apps (category_id, released);

-- Index for filtering by category and content rating (target audience filtering)
CREATE INDEX idx_apps_category_content_rating ON apps (category_id, content_rating);


-- ============================================================
-- 3. Other Indexes
-- ============================================================

-- Index for extracting and grouping by release year.
CREATE INDEX idx_apps_released_extract_year ON apps (EXTRACT(year FROM released));

-- Index for extracting and grouping by update year.
CREATE INDEX idx_apps_last_updated_extract_year ON apps (EXTRACT(year FROM last_updated));
