query_down = """
(SELECT t1.id, t1.user_id, t1.result, t1.type, t1.date
                FROM results t1 
                INNER JOIN
                (
                    SELECT Max(date) date, type
                    FROM   results
                    GROUP BY type
                ) AS t2 
                    ON t1.type = t2.type
                    AND t1.date = t2.date 
                    AND user_id={}
                    AND t1.type = 0
                ORDER BY t1.id DESC
                LIMIT 2)

                UNION ALL

                (SELECT t1.id, t1.user_id, t1.result, t1.type, t1.date
                FROM results t1 
                INNER JOIN
                (
                    SELECT Max(date) date, type
                    FROM   results
                    GROUP BY type
                ) AS t2 
                    ON t1.type = t2.type
                    AND t1.date = t2.date 
                    AND user_id={}
                    AND t1.type = 1
                ORDER BY t1.id DESC
                LIMIT 2)

                UNION ALL

                (SELECT t1.id, t1.user_id, t1.result, t1.type, t1.date
                FROM results t1 
                INNER JOIN
                (
                    SELECT Max(date) date, type
                    FROM   results
                    GROUP BY type
                ) AS t2 
                    ON t1.type = t2.type
                    AND t1.date = t2.date 
                    AND user_id={}
                    AND t1.type = 2
                ORDER BY t1.id DESC
                LIMIT 2)"""

