__author__ = 'Ben'

from google.appengine.ext import webapp
import google.appengine.ext.db
from google.appengine.ext import db

import StringIO
import random
import string
import os

def generateRandomInt(min=1, max=100):
    return random.randint(min, max)


def generateRandomIntFromRestriction(restriction):
    return generateRandomInt(restriction.min,
        restriction.max)


def generateRandomStringFromLenRestriction(restriction):
    return generateRandomString(generateRandomInt(restriction.min, restriction.max))


def generateRandomStringFromValuesRestriction(prop_restrictions, property_name):
    return generateRandomStringFromArray(prop_restrictions[property_name].values)


def generateRandomString(length=50):
    return ''.join(random.choice(string.letters) for i in xrange(length))


def generateRandomStringFromArray(values=[]):
    return values[generateRandomInt(0, len(values) - 1)]


def generateRandomBoolean():
    return bool(random.getrandbits(1))


def generateWebRequestFromHash(requestHash):
    webRequest = webapp.Request({
        "wsgi.input": StringIO.StringIO(),
        "METHOD": "POST",
        })
    queryString = ''
    for hashKey in requestHash:
        hashValue = requestHash[hashKey]
        queryString += '&amp;' + hashKey + '=' + str(hashValue)
    webRequest.query_string = queryString
    return webRequest


def generateTestHashFromModelClass(model_to_copy_from, prop_restrictions={}):
    newHash = {}
    class_properties = model_to_copy_from.properties()
    _populateHashProperties(class_properties, prop_restrictions, newHash)
    return newHash


def generateTestModelInstance(model_to_create, prop_restrictions={}):
    test_model = model_to_create()
    class_properties = model_to_create.properties()
    _populateModelProperties(class_properties, prop_restrictions, test_model)
    return test_model


def generateAndPutRandomNumOfClass(classToGenerate, restrictions={}):
    numToCreate = generateRandomInt()
    i = 1
    while i <= numToCreate:
        i += 1
        generateAndPutClassInstance(classToGenerate, restrictions)
    return numToCreate


def generateAndPutClassInstance(classToGenerate, restrictions={}):
    classInstance = generateTestModelInstance(classToGenerate, restrictions)
    classInstance.put()
    return classInstance


def generateRandomURLFromRestriction(restriction):
    return generateRandomURL()


def generateRandomURL():
    domainExtensions = ['.com', '.edu', '.org', '.info']
    return generateRandomStringFromArray(['http', 'https']) +'://' + generateRandomString(10) + generateRandomStringFromArray(
        domainExtensions)


def _populateModelURL(property_name, test_model, prop_restrictions):
    if property_name in prop_restrictions:
        restriction = prop_restrictions[property_name]
        test_model.__setattr__(property_name, generateRandomURLFromRestriction(restriction))
    else:
        test_model.__setattr__(property_name, generateRandomURL())


def generateRandomPath(numOfSegments):
    path = '/'
    i = 0
    while i < numOfSegments:
        path += generateRandomString(generateRandomInt(max=25)) + '/'
        i += 1
    return path


def generateRandomFileName(extensions=['.jpg', '.html', 'gif', '.txt', '.pdf']):
    return generateRandomString(generateRandomInt(max=50)) + generateRandomStringFromArray(extensions)


def _populateModelLink(property_name, test_model, prop_restrictions):
    return generateRandomURL() + generateRandomPath(generateRandomInt(5)) + generateRandomFileName()


def _populateModelProperties(class_properties, prop_restrictions, test_model):
    for property_name in class_properties:
        property_type = class_properties[property_name]
        if isinstance(property_type, db.IntegerProperty):
            _populateModelInt(property_name, test_model, prop_restrictions)
        if isinstance(property_type, db.StringProperty):
            _populateModelStr(property_name, test_model, prop_restrictions)
        if isinstance(property_type, db.BooleanProperty):
            _populateModelBoolean(property_name, test_model)
        if isinstance(property_type, db.GeoPtProperty):
            _populateModelModelGeoPoint(property_name, test_model, prop_restrictions)
        if isinstance(property_type, db.CategoryProperty):
            _populateModelCategory(property_name, test_model, prop_restrictions)
        if isinstance(property_type, db.TextProperty):
            _populateModelStr(property_name, test_model, prop_restrictions)
        if isinstance(property_type, db.URLProperty):
            _populateModelURL(property_name, test_model, prop_restrictions)
        if isinstance(property_type, db.LinkProperty):
            _populateModelLink(property_name, test_model, prop_restrictions)


def _populateModelBoolean(property_name, test_model):
    test_model.__setattr__(property_name, generateRandomBoolean())


def generateRandomGeoPoint():
    return db.GeoPt(generateRandomInt(-90, 90), generateRandomInt())


def generateRandomGeoPointFromRestriction(restriction):
    return db.GeoPt(generateRandomInt(restriction.minLat, restriction.maxLat),
        generateRandomInt(restriction.minLong, restriction.maxLong))


def _populateModelGeoPoint(property_name, test_model, prop_restrictions):
    if property_name in prop_restrictions:
        restriction = prop_restrictions[property_name]
        test_model.__setattr__(property_name, generateRandomGeoPointFromRestriction(restriction))
    else:
        test_model.__setattr__(property_name, generateRandomGeoPoint())


def _populateModelInt(property_name, test_model, prop_restrictions):
    if property_name in prop_restrictions:
        restriction = prop_restrictions[property_name]
        test_model.__setattr__(property_name, generateRandomIntFromRestriction(restriction))
    else:
        test_model.__setattr__(property_name, generateRandomInt())


def _populateModelStr(property_name, test_model, prop_restrictions):
    if property_name in prop_restrictions:
        restriction = prop_restrictions[property_name]
        if restriction.CLASS_NAME == StringGenerationLengthRestriction.CLASS_NAME:
            test_model.__setattr__(property_name,
                generateRandomStringFromLenRestriction(restriction))
        elif restriction.CLASS_NAME == StringGenerationValueRestriction.CLASS_NAME:
            test_model.__setattr__(property_name,
                generateRandomStringFromValuesRestriction(prop_restrictions, property_name))
    else:
        test_model.__setattr__(property_name, generateRandomString(generateRandomInt()))


def _populateHashProperties(class_properties, prop_restrictions, hash):
    for property_name in class_properties:
        property_type = class_properties[property_name]
        if isinstance(property_type, db.IntegerProperty):
            _populateHashInt(property_name, hash, prop_restrictions)
        if isinstance(property_type, db.StringProperty):
            _populateHashStr(property_name, hash, prop_restrictions)
        if isinstance(property_type, db.BooleanProperty):
            _populateHashBoolean(property_name, hash)


def _populateHashBoolean(property_name, hash):
    hash[property_name] = generateRandomBoolean()


def _populateHashInt(property_name, hash, prop_restrictions):
    if property_name in prop_restrictions:
        restriction = prop_restrictions[property_name]
        hash[property_name] = generateRandomIntFromRestriction(restriction)
    else:
        hash[property_name] = generateRandomInt()


def _populateHashStr(property_name, hash, prop_restrictions):
    if property_name in prop_restrictions:
        restriction = prop_restrictions[property_name]
        if restriction.CLASS_NAME == StringGenerationLengthRestriction.CLASS_NAME:
            hash[property_name] = generateRandomStringFromLenRestriction(restriction)
        elif restriction.CLASS_NAME == StringGenerationValueRestriction.CLASS_NAME:
            hash[property_name] = generateRandomStringFromValuesRestriction(prop_restrictions, property_name)
    else:
        hash[property_name] = generateRandomString(generateRandomInt())


class StringGenerationLengthRestriction:
    CLASS_NAME = 'StringGenerationLengthRestriction'
    min = None
    max = None

    def __init__(self, min=1, max=100):
        self.min = min
        self.max = max
        pass


class StringGenerationValueRestriction:
    CLASS_NAME = 'StringGenerationValueRestriction'
    values = []

    def __init__(self, values=[]):
        self.values = values
        pass


class IntegerGenerationRestriction:
    CLASS_NAME = 'IntegerGenerationRestriction'
    min = None
    max = None

    def __init__(self, min=1, max=100):
        self.min = min
        self.max = max
        pass


class GeoPointGenerationRestriction:
    CLASS_NAME = "GeoPointGenerationRestriction"
    minLat = None
    maxLat = None

    minLong = None
    maxLong = None

    def __init__(self, minLat=-90, maxLat=-90, minLong=-100, maxLong=100):
        self.minLat = minLat
        self.maxLat = maxLat
        self.minLong = minLong
        self.maxLong = maxLong
        pass