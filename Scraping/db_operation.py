from db_connection import create_db_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def insert_source(source_name):
    connection = create_db_connection()
    if connection is None:
        logging.error("Failed to connect to the database.")
        return None
    try:
        with connection.cursor() as cursor:
            check_query = "SELECT id FROM sources WHERE name = %s"
            cursor.execute(check_query, (source_name,))
            result = cursor.fetchone()
            if result:
                logging.info(f"Source '{source_name}' already exists with ID {result[0]}.")
                return result[0]
            
            insert_query = "INSERT INTO sources (name) VALUES (%s)"
            cursor.execute(insert_query, (source_name,))
            connection.commit()
            source_id = cursor.lastrowid
            logging.info(f"Source '{source_name}' inserted with ID {source_id}.")
            return source_id
    except Exception as e:
        logging.error(f"Error inserting source '{source_name}': {e}")
        raise
    finally:
        connection.close()

def insert_article(title, content, publish_date, source_id):
    connection = create_db_connection()
    if connection is None:
        logging.error("Failed to connect to the database.")
        return None
    try:
        with connection.cursor() as cursor:
            check_query = "SELECT id FROM articles WHERE title = %s AND source_id = %s"
            cursor.execute(check_query, (title, source_id))
            result = cursor.fetchone()
            cursor.fetchall()
            if result:
                logging.info(f"Article '{title}' already exists with ID {result[0]}.")
                return result[0]
            
            insert_query = "INSERT INTO articles (title, content, publish_date, source_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (title, content, publish_date, source_id))
            connection.commit()
            article_id = cursor.lastrowid
            logging.info(f"Article '{title}' inserted with ID {article_id}.")
            return article_id
    except Exception as e:
        logging.error(f"Error inserting article '{title}': {e}")
        raise
    finally:
        connection.close()

def insert_image(article_id, img_url):
    connection = create_db_connection()
    if connection is None:
        logging.error("Failed to connect to the database.")
        return None
    try:
        with connection.cursor() as cursor:
            check_query = "SELECT id FROM images WHERE article_id = %s AND image_url = %s"
            cursor.execute(check_query, (article_id, img_url))
            cursor.fetchall()
            result = cursor.fetchone()
            if result:
                logging.info(f"Image for article ID {article_id} already exists with ID {result[0]}.")
                return result[0]

            insert_query = "INSERT INTO images (article_id, image_url) VALUES (%s, %s)"
            cursor.execute(insert_query, (article_id, img_url))
            connection.commit()
            image_id = cursor.lastrowid
            logging.info(f"Image for article ID {article_id} inserted with ID {image_id}.")
            return image_id
    except Exception as e:
        logging.error(f"Error inserting image for article ID {article_id}: {e}")
        raise
    finally:
        connection.close()
