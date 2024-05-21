from database.DB_connect import DBConnect
from model.prodotto import Prodotto

class DAO():
    def __init__(self):
        pass
    @staticmethod
    def get_color():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct (p.Product_color)
                    from go_products p"""

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_vertici(colore):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_products p
                    where p.Product_color = %s """

        cursor.execute(query, (colore,))

        for row in cursor:
            result.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi(colore, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT
    ps.Product1,
    ps.Product2,
    COUNT(DISTINCT ps.Date) AS weight
FROM
		( SELECT
		    ds3.Retailer_code,
		    ds3.Product_number AS Product1,
		    ds4.Product_number AS Product2,
		    ds3.Date
		FROM
		    (SELECT 
		         ds1.Retailer_code,
		         ds1.Product_number,
		         ds1.Date
		     FROM 
		         go_daily_sales ds1
		     JOIN 
		         go_products p1 
		     ON 
		         ds1.Product_number = p1.Product_number
		     WHERE 
		         YEAR(ds1.Date) = %s 
		         AND p1.Product_color = %s) ds3
		JOIN
		    (SELECT 
		         ds2.Retailer_code,
		         ds2.Product_number,
		         ds2.Date
		     FROM 
		         go_daily_sales ds2
		     JOIN 
		         go_products p2 
		     ON 
		         ds2.Product_number = p2.Product_number
		     WHERE 
		         YEAR(ds2.Date) = %s 
		         AND p2.Product_color = %s) ds4
		ON
		    ds3.Retailer_code = ds4.Retailer_code 
		    AND ds3.Date = ds4.Date 
		    AND ds3.Product_number < ds4.Product_number
		where YEAR(ds3.Date) = %s ) ps
GROUP BY
    ps.Product1,
    ps.Product2
HAVING
    weight > 0

"""

        cursor.execute(query, (anno, colore, anno, colore, anno,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

