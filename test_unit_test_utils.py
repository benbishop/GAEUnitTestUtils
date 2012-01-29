__author__ = 'Ben'

import unittest
import zpttest
from google.appengine.ext import testbed
import unittestutils
from google.appengine.ext import webapp
from google.appengine.ext import db
from unittestutils import IntegerGenerationRestriction
from unittestutils import StringGenerationLengthRestriction
from unittestutils import StringGenerationValueRestriction
from unittestutils import generateTestHashFromModelClass
from unittestutils import generateRandomGeoPoint
from unittestutils import generateRandomURL
from unittestutils import generateAndPutClassInstance
from unittestutils import generateRandomPath
from unittestutils import generateRandomFileName

class UnitTestUtilsTestCase(zpttest.BaseZPTTestCase):
    def setUp(self):
        super(UnitTestUtilsTestCase, self).setUp()
        self.test_model = TestClassModel()

    # web request
    def test_create_web_request_from_hash_doesnt_return_null(self):
        test_hash = {'prop1': 'prop 1 value'}
        web_request = unittestutils.generateWebRequestFromHash(test_hash)
        self.assertTrue(web_request is not None)

    def test_create_web_request_populates_one_prop_from_hash(self):
        test_hash = {'prop1': 'prop 1 value'}
        web_request = unittestutils.generateWebRequestFromHash(test_hash)
        self.assertEquals(web_request.get('prop1'), test_hash['prop1'])

    def test_create_web_request_populates_multiple_props_from_hash(self):
        test_hash = {'prop1': 'prop 1 value', 'prop2': '23', 'prop3': 'another prop'}
        web_request = unittestutils.generateWebRequestFromHash(test_hash)
        self.assertEquals(web_request.get('prop1'), test_hash['prop1'])
        self.assertEquals(web_request.get('prop2'), test_hash['prop2'])
        self.assertEquals(web_request.get('prop3'), test_hash['prop3'])

    # model tests
    def test_create_test_model_instance_doesnt_return_null(self):
        self.test_model = unittestutils.generateTestModelInstance(TestClassModel)
        self.assertTrue(self.test_model is not None)

    def test_create_test_model_instance_is_right_type(self):
        self.test_model = unittestutils.generateTestModelInstance(TestClassModel)
        self.assertTrue(isinstance(self.test_model, TestClassModel))

    def test_create_test_model_populates_integer_property_with_defaults(self):
        self.test_model = unittestutils.generateTestModelInstance(TestClassModel)
        self.assertTrue(self.test_model.typicalIntProp > 0 and self.test_model.typicalIntProp <= 100)

    def test_create_test_model_populates_integer_property_within_restricted_range(self):
        self.test_model = unittestutils.generateTestModelInstance(TestClassModel,
                {'typicalIntProp': IntegerGenerationRestriction(1, 2)})
        self.assertTrue(self.test_model.typicalIntProp > 0 and self.test_model.typicalIntProp < 3)

    def test_create_test_model_populates_string_properties(self):
        self.test_model = unittestutils.generateTestModelInstance(TestClassModel)
        self.assertTrue(self.test_model.typicalStringProp is not None)

    def test_create_test_model_populates_string_properties_within_length_restrictions(self):
        self.test_model = unittestutils.generateTestModelInstance(TestClassModel,
                {'typicalStringProp': StringGenerationLengthRestriction(1, 2)})
        self.assertTrue(len(self.test_model.typicalStringProp) > 0 and len(self.test_model.typicalStringProp) < 3)

    def test_create_test_model_populates_string_properties_within_values_array(self):
        restricted_values = [unittestutils.generateRandomString(),
                             unittestutils.generateRandomString(),
                             unittestutils.generateRandomString()]
        self.test_model = unittestutils.generateTestModelInstance(TestClassModel, {
            'typicalStringProp': StringGenerationValueRestriction(restricted_values)})
        self.assertTrue(self.test_model.typicalStringProp in restricted_values)

    def test_generate_and_put_model_adds_to_datastore(self):
        unittestutils.generateAndPutClassInstance(TestClassModel)
        self.assertEqual(TestClassModel.all().count(), 1)

    def test_generate_put_random_num_of_model_adds_the_correct_amount_to_datastore(self):
        numCreated = unittestutils.generateAndPutRandomNumOfClass(TestClassModel)
        self.assertEqual(numCreated, TestClassModel.all().count())

    # hash tests
    def test_create_hash_from_model_doesnt_return_null(self):
        self.assertTrue(generateTestHashFromModelClass(TestClassModel))

    def test_create_hash_from_model_populates_integer_property_with_defaults(self):
        testHash = generateTestHashFromModelClass(TestClassModel)
        self.assertTrue(testHash['typicalIntProp'] > 0 and testHash['typicalIntProp'] <= 100)

    def test_create_test_model_populates_integer_property_within_restricted_range(self):
        testHash = unittestutils.generateTestHashFromModelClass(TestClassModel,
                {'typicalIntProp': IntegerGenerationRestriction(1, 2)})
        self.assertTrue(testHash['typicalIntProp'] > 0 and testHash['typicalIntProp'] < 3)

    def test_create_test_model_populates_string_properties(self):
        testHash = unittestutils.generateTestHashFromModelClass(TestClassModel)
        self.assertTrue(testHash['typicalStringProp'] is not None)

    def test_create_test_model_populates_string_properties_within_length_restrictions(self):
        testHash = unittestutils.generateTestHashFromModelClass(TestClassModel,
                {'typicalStringProp': StringGenerationLengthRestriction(1, 2)})
        self.assertTrue(len(testHash['typicalStringProp']) > 0 and len(testHash['typicalStringProp']) < 3)

    def test_create_test_model_populats_string_properties_within_values_array(self):
        restricted_values = [unittestutils.generateRandomString(),
                             unittestutils.generateRandomString(),
                             unittestutils.generateRandomString()]
        testHash = unittestutils.generateTestHashFromModelClass(TestClassModel, {
            'typicalStringProp': StringGenerationValueRestriction(restricted_values)})
        self.assertTrue(testHash['typicalStringProp'] in restricted_values)

    # int generation tests
    def test_generate_random_int_doesnt_return_null(self):
        self.assertTrue(unittestutils.generateRandomInt() is not None)

    def test_generate_random_int_by_default_returns_an_int_between_0_and_100(self):
        self.assertTrue(unittestutils.generateRandomInt() >= 0 and unittestutils.generateRandomInt() <= 100)

    def test_generate_random_int_does_not_return_a_value_outside_of_submitted_bounds(self):
        self.assertTrue(unittestutils.generateRandomInt(0, 1) >= 0 and unittestutils.generateRandomInt(0, 1) <= 1)

    #string generation tests
    def test_generate_random_string_doesnt_return_null(self):
        self.assertTrue(unittestutils.generateRandomString() is not None)

    def test_generate_random_string_returns_string(self):
        returnedValue = unittestutils.generateRandomString()
        self.assertEqual(returnedValue, str(returnedValue))

    def test_generate_random_string_returns_string_of_right_length(self):
        length = unittestutils.generateRandomInt()
        self.assertEqual(length, len(unittestutils.generateRandomString(length)))

    def test_generate_random_string_from_array_returns_value(self):
        values = []
        num_to_enter = unittestutils.generateRandomInt()
        i = 0
        while i < num_to_enter:
            values.append(unittestutils.generateRandomString())
            i += 1
        self.assertTrue(unittestutils.generateRandomStringFromArray(values) in values)

    def test_generate_random_string_from_array_returns_correct_value_in_single_item_array(self):
        values = [unittestutils.generateRandomInt()]
        self.assertTrue(unittestutils.generateRandomStringFromArray(values) in values)

    def test_generate_random_geo_point_returns_geo_point(self):
        self.assertTrue(isinstance(generateRandomGeoPoint(), db.GeoPt));

    def test_generate_random_url_returns_string(self):
        self.assertTrue(isinstance(generateRandomURL(), str))

    def test_url_generated_passes_model_validation(self):
        generateAndPutClassInstance(TestClassModel, [])

    def test_generate_random_path_returns_string(self):
        self.assertTrue(isinstance(generateRandomPath(3), str))

    def test_generate_random_path_adds_correct_number_of_slashes(self):
        path = generateRandomPath(3)
        self.assertEqual(len(path.split('/')) - 1, 4)

    def test_generate_random_file_name_returns_string(self):
        self.assertTrue(isinstance(generateRandomFileName(), str))

    def test_generate_random_file_name_only_adds_one_period(self):
        self.assertEqual(len(generateRandomFileName().split('.')),2)

    def test_generate_random_file_name_correclty_adds_submitted_extension(self):
        extensions = ['.one', '.two', 'three']
        generatedExtension = '.' + generateRandomFileName(extensions).split('.')[1]
        self.assertTrue(extensions.__contains__(generatedExtension))

    def test_link_generated_passes_model_validation(self):
        instance = generateAndPutClassInstance(TestClassModel)
        self.assertNotEqual(instance.typicalLink, None)

class TestClassModel(db.Model):
    typicalStringProp = db.StringProperty()
    typicalIntProp = db.IntegerProperty()
    typicalURL = db.URLProperty()
    typicalLink = db.LinkProperty()


if __name__ == '__main__':
    unittest.main()
