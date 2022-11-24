from flask import Flask, render_template, jsonify
import json
import pymysql
import config

app = Flask(__name__)
conn = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                        user=config.DATABASE_CONFIG['user'], 
                        password=config.DATABASE_CONFIG['password'], 
                        db=config.DATABASE_CONFIG['dbname'], charset='utf8mb4')
cursor = conn.cursor()

def getRecord(cur, con):
    try:
        ranking = []
        cur.execute("select CCode from Center;")
        # con.commit()
        gymCode = cur.fetchall()

        for code in gymCode:
            tempRank = {}
            tempRank['one'] = ' null '
            tempRank['two'] = ' null '
            tempRank['three'] = ' null '
            tempRank['four'] = ' null '
            tempRank['five'] = ' null '

            tempRank['Code'] = code[0]
            cur.execute("select Cname, lat, lon from Center where CCode = " + str(code[0]) + ";")
            name, lat, lon = cur.fetchall()[0]
            tempRank['name'] = name
            tempRank['lat'] = lat
            tempRank['lon'] = lon

            # con.commit()
            cur.execute("select UID from Challenge where CCode = " + str(code[0]) + ";")
            # con.commit()
            userID = set(cur.fetchall())

            tempRank2 = []
            for uid in userID:
                cur.execute("select sum(CWeight) from Challenge where CCode = " + str(code[0]) + " and UID = '" + str(uid[0]) + "';")
                # con.commit()
                tempRank2.append([str(uid[0]), int(cur.fetchone()[0])])
                tempRank2.sort(key = lambda x : -x[1])

            for i in range(len(tempRank2)):
                if i == 0:
                    tempRank['one'] = tempRank2[i][0] + ' ' + str(tempRank2[i][1])
                elif i == 1:
                    tempRank['two'] = tempRank2[i][0] + ' ' + str(tempRank2[i][1])
                elif i == 2:
                    tempRank['three'] = tempRank2[i][0] + ' ' + str(tempRank2[i][1])
                elif i == 3:
                    tempRank['four'] = tempRank2[i][0] + ' ' + str(tempRank2[i][1])
                elif i == 4:
                    tempRank['five'] = tempRank2[i][0] + ' ' + str(tempRank2[i][1])

            ranking.append(tempRank)

        for i in ranking:
            print(i)
        con.commit()

    except:
        print("Failed!")
        con.rollback()

    return ranking



@app.route('/map', methods=['GET'])
def rank_map():
    rank = getRecord(cursor, conn)
    return render_template('map.html', rank=json.dumps(rank))


@app.route('/map2', methods=['GET'])
def rank_map2():
    rank = getRecord(cursor, conn)
    return render_template('map.html', rank=json.dumps(rank))




if __name__ == '__main__':
    app.run(host='localhost', port=8080)