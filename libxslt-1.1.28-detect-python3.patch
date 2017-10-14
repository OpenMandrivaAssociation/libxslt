--- libxslt-1.1.28/configure.ac.0003~	2012-11-21 08:10:58.000000000 +0100
+++ libxslt-1.1.28/configure.ac	2014-07-05 15:55:05.563316383 +0200
@@ -290,80 +290,88 @@ AM_CONDITIONAL(WITH_PERL, test "$PERL" !
 dnl
 dnl check for python
 dnl
-
 PYTHON_VERSION=
 PYTHON_INCLUDES=
 PYTHON_SITE_PACKAGES=
+PYTHON_TESTS=
 pythondir=
-AC_ARG_WITH(python, [  --with-python[=DIR]    Build Python bindings if found])
 if test "$with_python" != "no" ; then
     if test -x "$with_python/bin/python"
     then
         echo Found python in $with_python/bin/python
         PYTHON="$with_python/bin/python"
     else
-	if test -x "$with_python"
-	then
-	    echo Found python in $with_python
-	    PYTHON="$with_python"
-	else
-            if test -x "$PYTHON"
+        if test -x "$with_python/python.exe"
+        then
+            echo Found python in $with_python/python.exe
+            PYTHON="$with_python/python.exe"
+        else
+            if test -x "$with_python"
             then
-                echo Found python in environment PYTHON=$PYTHON
-                with_python=`$PYTHON -c "import sys; print sys.exec_prefix"`
-	    else
-	        AC_PATH_PROG(PYTHON, python python2.4 python2.3 python2.2 python2.1 python2.0 python1.6 python1.5)
+                echo Found python in $with_python
+                PYTHON="$with_python"
+            else
+                if test -x "$PYTHON"
+                then
+                    echo Found python in environment PYTHON=$PYTHON
+                    with_python=`$PYTHON -c "import sys; print(sys.exec_prefix)"`
+                else
+                    AC_PATH_PROG(PYTHON, python python2.6 python2.5 python2.4 python2.3 python2.2 python2.1 python2.0 python1.6 python1.5)
+		fi
 	    fi
 	fi
     fi
     if test "$PYTHON" != ""
     then
-        echo "PYTHON is pointing at $PYTHON"
-        PYTHON_VERSION=`$PYTHON -c "import sys; print sys.version[[0:3]]"`
+        PYTHON_VERSION=`$PYTHON -c "from distutils import sysconfig; print(sysconfig.get_python_version())"`
+	PYTHON_INCLUDES=`$PYTHON -c "from distutils import sysconfig; print(sysconfig.get_python_inc())"`
+# does not work as it produce a /usr/lib/python path instead of/usr/lib64/python
+#
+#	PYTHON_SITE_PACKAGES=`$PYTHON -c "from distutils import sysconfig; print(sysconfig.get_python_lib())"`
 	echo Found Python version $PYTHON_VERSION
-	LIBXML2_PYTHON=`$PYTHON -c "try : import libxml2 ; print 1
-except: print 0"`
-	if test "$LIBXML2_PYTHON" = "1"
-	then
-	    echo Found libxml2-python module
-	else
-	    echo Warning: Missing libxml2-python
-	fi
     fi
-    if test "$PYTHON_VERSION" != ""
+    if test "$PYTHON_VERSION" != "" -a "$PYTHON_INCLUDES" = ""
     then
-	if test -r $with_python/include/python$PYTHON_VERSION/Python.h -a \
-	   -d $with_python/lib/python$PYTHON_VERSION/site-packages
+	if test -r $with_python/include/python$PYTHON_VERSION/Python.h
 	then
 	    PYTHON_INCLUDES=$with_python/include/python$PYTHON_VERSION
-	    PYTHON_SITE_PACKAGES='$(libdir)/python$(PYTHON_VERSION)/site-packages'
 	else
 	    if test -r $prefix/include/python$PYTHON_VERSION/Python.h
 	    then
 	        PYTHON_INCLUDES=$prefix/include/python$PYTHON_VERSION
-		PYTHON_SITE_PACKAGES='$(libdir)/python$(PYTHON_VERSION)/site-packages'
 	    else
 		if test -r /usr/include/python$PYTHON_VERSION/Python.h
 		then
 		    PYTHON_INCLUDES=/usr/include/python$PYTHON_VERSION
-		    PYTHON_SITE_PACKAGES='$(libdir)/python$(PYTHON_VERSION)/site-packages'
 		else
-		    echo could not find python$PYTHON_VERSION/Python.h
+	            if test -r $with_python/include/Python.h
+	            then
+	                PYTHON_INCLUDES=$with_python/include
+	            else
+		        echo could not find python$PYTHON_VERSION/Python.h or $with_python/include/Python.h
+		    fi
 		fi
 	    fi
-	    if test ! -d "$PYTHON_SITE_PACKAGES"
-	    then
-		    PYTHON_SITE_PACKAGES=`$PYTHON -c "from distutils import sysconfig; print sysconfig.get_python_lib()"`
-	    fi
 	fi
-        PYTHON_LIBS=`python$PYTHON_VERSION-config --libs`
     fi
-    if test "$with_python" != ""
+    if test "$PYTHON_VERSION" != "" -a "$PYTHON_SITE_PACKAGES" = ""
     then
-        pythondir='$(PYTHON_SITE_PACKAGES)'
-    else
-        pythondir='$(libdir)/python$(PYTHON_VERSION)/site-packages'
+	if test -d $libdir/python$PYTHON_VERSION/site-packages
+	then
+	    PYTHON_SITE_PACKAGES=$libdir/python$PYTHON_VERSION/site-packages
+	else
+	    if test -d $with_python/lib/site-packages
+	    then
+		PYTHON_SITE_PACKAGES=$with_python/lib/site-packages
+	    else
+		PYTHON_SITE_PACKAGES=`$PYTHON -c "from distutils import sysconfig; print(sysconfig.get_python_lib())"`
+	    fi
+	fi
     fi
+    pythondir='$(PYTHON_SITE_PACKAGES)'
+    PYTHON_LIBS=`python$PYTHON_VERSION-config --ldflags`
+else
+    PYTHON=
 fi
 AM_CONDITIONAL(WITH_PYTHON, test "$PYTHON_INCLUDES" != "")
 if test "$PYTHON_INCLUDES" != ""
