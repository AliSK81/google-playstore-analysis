-- Filtering by category
CREATE INDEX idx_category_id ON apps (category_id);

-- Filtering by rating range
CREATE INDEX idx_rating ON apps (rating);

-- Filtering by price range
CREATE INDEX idx_price ON apps (price);

-- Filtering by installs range
CREATE INDEX idx_installs ON apps (installs);

-- Filtering by free/paid apps
CREATE INDEX idx_free ON apps (free);

-- Filtering by content rating
CREATE INDEX idx_content_rating ON apps (content_rating);

-- Filtering by whether the app supports ads
CREATE INDEX idx_ad_supported ON apps (ad_supported);

-- Filtering by in-app purchases
CREATE INDEX idx_in_app_purchases ON apps (in_app_purchases);

-- Filtering by Editors' Choice
CREATE INDEX idx_editors_choice ON apps (editors_choice);


-- For filtering "free apps in the 'Social' category"
CREATE INDEX idx_category_free ON apps (category_id, free);

-- For filtering "paid apps in the 'Games' category"
CREATE INDEX idx_category_paid ON apps (category_id, free, price);

-- For filtering "high-rated apps in a specific category"
CREATE INDEX idx_category_rating ON apps (category_id, rating);

-- For filtering "popular free apps with in-app purchases"
CREATE INDEX idx_category_free_in_app ON apps (category_id, free, in_app_purchases);


-- Sorting by rating (e.g., "Top-rated apps")
CREATE INDEX idx_rating_desc ON apps (rating DESC);

-- Sorting by installs (e.g., "Most installed apps")
CREATE INDEX idx_installs_desc ON apps (installs DESC);

-- Sorting by release date (e.g., "Newest apps first")
CREATE INDEX idx_released_desc ON apps (released DESC);

-- Sorting by last updated date (e.g., "Recently updated apps")
CREATE INDEX idx_last_updated_desc ON apps (last_updated DESC);
