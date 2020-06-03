#!/usr/bin/python3
from configparser import ConfigParser
import psycopg2
#from config import config
from psycopg2.extras import Json
import json
import io
import json as simplejson


'''
Connect to database and update tables using python.
'''


def config(filename, section):                  # Gets called by connect()
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    
    #print (db) 
    return db
    

def connect():
    """ Connect to the PostgreSQL database server 
        Call: config ('database.ini', 'postgresql')

    """
    conn = None
    try:
        # read connection parameters
        params = config('database.ini', 'postgresql')
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        '''
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
        # close the communication with the PostgreSQL
        cur.close()
        '''
        return cur, conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        pass
        #if conn is not None:
            #conn.close()
            #print('Database connection closed.')



if __name__ == '__main__':
    cur, conn = connect()

    print (cur, conn)
    if (cur):
        print ("Connection successful....creating table..")
        #cur.execute('SELECT version()')
        print ("Dropping Table")

        try:
            #cur.execute('select exists(select relname from pg_class where relname="azureratecardtable")')
            #exists = cur.fetchone()[0]
            #print (exists)
            #if (exists):
            cur.execute('DROP TABLE AzureRateCardTable')
            conn.commit()
        
        except psycopg2.Error as e:
            print (e)


        print ("Creating Table")
        cur.execute('CREATE TABLE AzureRateCardTable (id SERIAL PRIMARY KEY, region VARCHAR(20) NOT NULL, ratecard JSON NOT NULL)')
        conn.commit()
        
        try:
            #with open ("{0}".format(arg), 'r') as js:
            with open ("/tmp/Azure_RateCard_GB.json", 'r') as js:
                data = (json.load(js))
                #outdata = (str(data))
                print (data)

        except (ValueError, KeyError, TypeError):
            print ("JSON format error")

        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))

        except:
            print ("Unexpected error:", sys.exc_info()[0])
            raise

        #fd =  io.open("/tmp/RateCardSmall.json", encoding = "utf-8")
        #readAll = fd.readlines()
        #print (readAll)
        #print (Json(data))
        #cur.execute("insert into AzureRateCardTable (region, ratecard) values (%s, %s)", ('USA', Json((data), dumps=simplejson.dumps)))

        #cur.execute("insert into AzureRateCardTable (region, ratecard) values ('USA', json.dumps(data)")
        SQLQ = "INSERT INTO AzureRateCardTable (region, ratecard) VALUES (%s, %s)"
        PARA = ('UK', json.dumps(data))
        #SQLQ = ("INSERT INTO AzureRateCardTable (region, ratecard) VALUES ('{0} {1}')".format('Azure_GB', 'json.dumps(data)'))
        #cur.execute(SQLQ)
        #cur.execute("INSERT INTO AzureRateCardTable (region, ratecard) VALUES (%s %s);", ('Azure_UK', json.dumps(data)))
        #cur.execute("INSERT INTO AzureRateCardTable (ratecard) VALUES (%s)", (json.dumps(data)))
        cur.execute(SQLQ, PARA)
        print ("table updated")
        '''
        fd =  io.open("/tmp/RateCardSmall.json", encoding = "utf-8")
        readAll = fd.readlines()

        print (readAll)
        #cur.execute('psql -d ratecarddb -U dbadmin -c "\set content `cat /tmp/RateCardSmall.json`"')
        #cur.execute
        
        print ("Ingesting data")
        #cur.executemany("INSERT INTO AzureRateCardTable (ratecard) VALUES '{0}'.format(readAll)")
        cur.executemany("INSERT INTO AzureRateCardTable (ratecard) VALUES (?)", (readAll))
        #cur.executemany("INSERT INTO AzureRateCardTable (ratecard) VALUES (%s)", (readAll,))
        #db_version = cur.fetchone()
        #print (db_version)
        '''
        conn.commit()
        cur.close()
        conn.close()
        print ("DB Connection closed")


