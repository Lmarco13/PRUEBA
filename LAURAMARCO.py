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
                p.name AS product_name,
                (sale_order_line.product_uom_qty / days_with_stock.days_with_stock) AS average_daily_sales
            FROM
                product_product p
            JOIN
                sale_order_line  ON p.id = sale_order_online.product_id
            JOIN
                sale_order  ON sale_order_online.order_id = sale_order.id
            JOIN
                days_with_stock ON p.id = days_with_stock.product_id
            WHERE
                sale_order.date >= CURRENT_DATE - INTERVAL '60 days'
            GROUP BY
                p.name;
            '''
        
        cursor.execute(query)

        for(product_name , average_daily_sales) in cursor:
            print("La media diaria de ventas en los últimos 60 dias para el producto {},ha sido de {}".format(product_name,average_daily_sales))

        cursor.close()
        conection.close()

    except mysql.connector.Error as err : 
        print(err)
