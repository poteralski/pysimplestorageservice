from pysimplestorageservice import AmazonAWSManager
import unittest

from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TEST_BUCKET, TEST_DIR, TEST_FILE


class MyTestCase(unittest.TestCase):

    def test_put(self):
        amazon = AmazonAWSManager(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY
        )
        filaname = 'test2.jpg'
        file1 = open(filaname, 'r').read()
        respond = amazon.put(filename=filaname, file=file1, prefix='test', bucket=TEST_BUCKET)
        assert respond.status_code == 200


    def test_get(self):
        amazon = AmazonAWSManager(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY
        )
        result = amazon.get(
            bucket=TEST_BUCKET,
            prefix=TEST_DIR,
            filename=TEST_FILE,
        )
        output = open(TEST_FILE, "wb")
        output.write(result)
        output.close()
        assert isinstance(result, str)

    def test_files(self):
        amazon = AmazonAWSManager(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY
        )
        files = amazon.get_file_list(
            bucket=TEST_BUCKET,
            prefix=TEST_DIR+'/',
        )
        print files
        assert len(files) > 0


if __name__ == '__main__':
    unittest.main()
