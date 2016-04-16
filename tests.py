from pysimplestorageservice import AmazonAWSManager
import unittest

from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class MyTestCase(unittest.TestCase):

    def test_get(self):
        amazon = AmazonAWSManager(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY
        )
        result = amazon.get(
            bucket='teatrtotu',
            prefix='media/images/events',
            filename='unnamed.jpg',
        )
        print type(result)

    def test_files(self):
        amazon = AmazonAWSManager(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY
        )
        files = amazon.get_file_list(
            bucket='teatrtotu',
            prefix='media/images/events/',
        )
        print files

    def test_dirs(self):
        amazon = AmazonAWSManager(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY
        )
        dirs = amazon.get_dir_list(
            bucket='teatrtotu',
            prefix='media/',
        )
        print dirs

    def test_get(self):
        amazon = AmazonAWSManager(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY
        )
        result = amazon.get(
            bucket='teatrtotu',
            prefix='media/images/events',
            filename='unnamed.jpg',
        )
        print type(result)

if __name__ == '__main__':
    unittest.main()
