from bson import ObjectId as BsonObjectId


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class ObjectIdInReq(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return  ObjectId(v)
        if not isinstance(v, str):
            raise TypeError('field is not a valid str', v)
        try:
            v =  ObjectId(v)
        except:
            raise TypeError('field is not a valid ObjectId')
            
        return v


class ObjectIdInRes(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('field is not a valid ObjectId')
        return str(v)

