from storages.backends.s3boto3 import S3Boto3Storage
import environ

env = environ.Env()

class StaticStorage(S3Boto3Storage):
	bucket_name =env('SPACES_BUCKET_NAME')
	location = 'static'

class MediaStorage(S3Boto3Storage):
	bucket_name =env('SPACES_BUCKET_NAME')
	location = 'media'
