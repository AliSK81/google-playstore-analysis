CREATE INDEX idx_apps_category_id ON apps (category_id);

CREATE INDEX idx_apps_rating ON apps (rating);

CREATE INDEX idx_apps_price ON apps (price);

CREATE INDEX idx_apps_installs ON apps (installs);

CREATE INDEX idx_apps_content_rating ON apps (content_rating);

CREATE INDEX idx_apps_free ON apps (free);

CREATE INDEX idx_apps_ad_supported ON apps (ad_supported);

CREATE INDEX idx_apps_in_app_purchases ON apps (in_app_purchases);

CREATE INDEX idx_apps_editors_choice ON apps (editors_choice);

CREATE INDEX idx_apps_category_released ON apps (category_id, released);

CREATE INDEX idx_apps_category_last_updated ON apps (category_id, last_updated);

CREATE INDEX idx_apps_category_rating ON apps (category_id, rating);
