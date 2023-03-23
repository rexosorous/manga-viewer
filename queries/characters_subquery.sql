SELECT DISTINCT books.id, characters.id AS character_id FROM books
LEFT JOIN characters ON books.id = bookID
WHERE
    CASE WHEN $null_search THEN (
        characters.id IS NULL
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_and THEN (
        characters.id IN ( -- AND
            SELECT characterID FROM characters_traits
            WHERE traitID IN $and_list
            GROUP BY characterID
            HAVING COUNT(characterID) = $and_list_length
        )
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_or THEN (
        characters.id IN ( -- OR
            SELECT characterID FROM characters_traits
            WHERE traitID in $or_list
            GROUP BY characterID
        )
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_not THEN (
        characters.id NOT IN ( -- NOT
            SELECT characterID FROM characters_traits
            WHERE traitID in $not_list
            GROUP BY characterID
        )
    ) ELSE 1 > 0 END
    AND
    CASE WHEN $has_prev_results THEN (
        books.id IN $prev_results_list
    ) ELSE 1 > 0 END