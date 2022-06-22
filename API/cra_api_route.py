from marshmallow import Schema, fields

#Responses

class PriceCommonResponse(Schema):
    message = fields.Str(example="success")

class PriceGetResponse(PriceCommonResponse):
    data = fields.List(fields.Dict(), example={
            "title":"陶朱隱園",
            "address":"臺北市信義區松高路66",
            "area":"12,962",
            "per_price":"1000",
        })




