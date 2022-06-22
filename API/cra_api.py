from flask_restful import reqparse        # pip install flask==2.0.3
import pymysql                            # pip install pymysql
from flask import jsonify                 # pip install Flask-RESTful==0.3.9
import util                               # pip install flask-apispec==0.11.0
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with  # pip install Flask-JWT-Extended==4.3.1
from cra_api_route import *
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta


def db_init():
    db = pymysql.connect(
        host='database-1.cb5frtthut3g.us-west-1.rds.amazonaws.com',
        user='admin',
        password='dv102dv102',
        port=3306,
        db='Housesell'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor


class Search(MethodResource):
    @doc(description = "請輸入地區關鍵字，查詢坪數、每坪單價(萬)，以及希望呈現的資料筆數", tags = ['Price'])
    @marshal_with(PriceGetResponse, code=200)
    # @jwt_required()
    def get(self, location, data_number):
        db,cursor = db_init()

        sql = f"SELECT title, address, area, perprice FROM Housesell.Housesell where address like '%{location}%' limit {data_number};"
        cursor.execute(sql)
        content = cursor.fetchall()

        db.close()
        return util.success(content)