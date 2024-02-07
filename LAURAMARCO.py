import mysql.connector

def average_daily_sales():
    #we assume we have a MYSQL database
    try :   
        conection = mysql.connector.connect("")
        cursor = conection.cursor()

        query = '''WITH days_with_stock AS (SELECT
            product_id,
            COUNT(DISTINCT DATE(stock_date)) AS days_with_stock
        FROM
            stock_history
        WHERE
            quantity > 0
        GROUP BY
            product_id
            )

            SELECT
                product_prouct.id AS product_id,
                (sale_order_line.product_uom_qty / days_with_stock.days_with_stock) AS average_daily_sales
            FROM
                product_product 
            JOIN
                sale_order_line ON product_product.id = sale_order_line.product_id
            JOIN
                days_with_stock ON product_product.id = days_with_stock.product_id
            JOIN
                sale_order  ON sale_order_line.product_id = sale_order.id
            WHERE
                sale_order.date_order >= CURRENT_DATE - INTERVAL '60 days'
            GROUP BY
                product_product.id;
            '''
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        for(product_name , average_daily_sales) in results:
            print("La media diaria de ventas en los últimos 60 dias para el producto {},ha sido de {}".format(product_name,average_daily_sales))

        cursor.close()
        conection.close()

    except mysql.connector.Error as err : 
        print(err)



average_daily_sales()
