SELECT
	metric_options.id AS metric_options_id,
	metric_options.label AS metric_options_label,
	metric_categories.label AS metric_category_label
FROM
    metric_options
LEFT JOIN
    metric_categories
ON
    metric_options.category_id = metric_categories.id