from django.conf.urls.defaults import patterns

urlpatterns = patterns('KKlog.blog.views',
    (r"^(\d+)/$", "post"),                                  #post pk
    (r"^add_comment/(\d+)/$", "add_comment"),               #post pk
    (r"^month/(\d+)/(\d+)/$", "month"),                     #year, month
    (r"^delete_comment/(\d+)/$", "delete_comment"),         #post pk
    (r"^delete_comment/(\d+)/(\d+)/$", "delete_comment"),   # post pk, comment pk
    (r"", "main"),
)
