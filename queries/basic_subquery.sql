SELECT * FROM books
WHERE (name LIKE '%$title%' OR alt_name LIKE '%title%')
        AND rating $rating
        AND (pages >= $pages_low AND pages <= $pages_high)
        AND (date_added >= $date_low AND date_added <= $date_high)
