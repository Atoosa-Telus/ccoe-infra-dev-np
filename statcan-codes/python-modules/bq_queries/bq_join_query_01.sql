SELECT 
i.ref_Period as ref_Period,
i.cpi_common_value as cpi_common_value,
i.cpi_median_value as cpi_median_value, 
i.cpi_trim_value as cpi_trim_value,
i.cpi_all_excl_gas as cpi_all_excl_gas,
i.cpi_all as cpi_all,
j.avg_xchg_rates as avg_xchg_rates,
FROM
(
    SELECT 
    g.ref_Period as ref_Period,
    g.cpi_common_value as cpi_common_value,
    g.cpi_median_value as cpi_median_value, 
    g.cpi_trim_value as cpi_trim_value,
    g.cpi_all_excl_gas as cpi_all_excl_gas,
    h.cpi_all as cpi_all
    FROM
    (
        SELECT 
        e.ref_Period as ref_Period,
        e.cpi_common_value as cpi_common_value,
        e.cpi_median_value as cpi_median_value, 
        e.cpi_trim_value as cpi_trim_value,
        f.cpi_all_excl_gas as cpi_all_excl_gas,
        FROM 
        (
            SELECT 
            c.ref_Period as ref_Period,
            c.cpi_common_value as cpi_common_value,
            c.cpi_median_value as cpi_median_value, 
            d.cpi_trim_value as cpi_trim_value
            FROM
            (
                SELECT
                a.ref_Period as ref_Period,
                a.cpi_common_value as cpi_common_value,
                b.cpi_median_value as cpi_median_value, 
                FROM
                (
                    SELECT
                    v.refPer as ref_Period,
                    v.value as cpi_common_value,
                    from `cio-cpo-ai-lab-7d76df.Restful_Statcan.core_inflation_cpi_common` as r,
                    unnest (r.vectorDataPoint) as v
                ) a 
                LEFT JOIN 
                (
                    SELECT 
                    v.refPer as ref_Period,
                    v.value as cpi_median_value,
                    from `cio-cpo-ai-lab-7d76df.Restful_Statcan.core_inflation_cpi_median` as r,
                    unnest (r.vectorDataPoint) as v
                ) b
                ON a.ref_Period = b.ref_Period 
            ) c
            LEFT JOIN 
            (
                SELECT 
                v.refPer as ref_Period,
                v.value as cpi_trim_value,
                from `cio-cpo-ai-lab-7d76df.Restful_Statcan.core_inflation_cpi_trim` as r,
                unnest (r.vectorDataPoint) as v
            ) d
            ON c.ref_Period = d.ref_Period 
        ) e
        LEFT JOIN 
        (
            SELECT 
            v.refPer as ref_Period,
            v.value as cpi_all_excl_gas,
            from `cio-cpo-ai-lab-7d76df.Restful_Statcan.cpi_canada_all_excl_gasoline` as r,
            unnest (r.vectorDataPoint) as v
        ) f
        ON e.ref_Period = f.ref_Period
    ) g
    LEFT JOIN 
    (
        SELECT 
        v.refPer as ref_Period,
        v.value as cpi_all,
        from `cio-cpo-ai-lab-7d76df.Restful_Statcan.cpi_canada_all_items` as r,
        unnest (r.vectorDataPoint) as v
    ) h
    ON g.ref_Period = h.ref_Period
) i
LEFT JOIN 
(
SELECT 
v.refPer as ref_Period,
v.value as avg_xchg_rates,
from `cio-cpo-ai-lab-7d76df.Restful_Statcan.avg_foreign_xchg_rates` as r,
unnest (r.vectorDataPoint) as v        
) j
ON i.ref_Period = j.ref_Perio