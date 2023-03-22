SELECT DISTINCT id FROM books
WHERE
    CASE WHEN $null_search THEN (
        id IN ( -- NULL
            SELECT books.id FROM books
            LEFT JOIN $linking_table ON books.id = bookID
            WHERE $field IS NULL
        )
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_and THEN (
        id IN ( -- AND
            SELECT bookID FROM $linking_table
            WHERE $field IN $and_list
            GROUP BY bookID
            HAVING COUNT(bookID) = $and_list_length
        )
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_or THEN (
        id IN ( -- OR
            SELECT bookID FROM $linking_table
            WHERE $field in $or_list
            GROUP BY bookID
        )
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_not THEN (
        id NOT IN ( -- NOT
            SELECT bookID FROM $linking_table
            WHERE $field in $not_list
            GROUP BY bookID
        )
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_prev_results THEN (
        id IN $prev_results_list
    ) ELSE 1 > 0 END
