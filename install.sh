rm django-mptt-comments/build/ -rf;
rm .environ/lib/python2.7/site-packages/mptt_comments/ -rf
ls django-mptt-comments/build/
ls .environ/lib/python2.7/site-packages/mptt_comments/
cd django-mptt-comments
python setup.py install
cd ..
ls .environ/lib/python2.7/site-packages/mptt_comments/
