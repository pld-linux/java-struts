Summary:	Web application framework
Summary(pl.UTF-8):	Szkielet dla aplikacji WWW
Name:		jakarta-struts
Version:	1.3.10
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/struts/source/struts-%{version}-src.zip
# Source0-md5:	7fb96adbc2b18ddd80462294cafb944d
Patch0:		%{name}-build.patch
URL:		http://struts.apache.org/
#BuildRequires:	ant >= 1.6
#BuildRequires:	ant-apache-regexp
#BuildRequires:	ant-nodeps
#BuildRequires:	ant-trax
#BuildRequires:	antlr >= 2.7.2
#BuildRequires:	jakarta-commons-beanutils >= 1.6.1
#BuildRequires:	jakarta-commons-collections
#BuildRequires:	jakarta-commons-digester >= 1.5
#BuildRequires:	jakarta-commons-fileupload >= 1.0
#BuildRequires:	jakarta-commons-lang
#BuildRequires:	jakarta-commons-logging >= 1.0.3
#BuildRequires:	jakarta-commons-validator >= 1.1.0
#BuildRequires:	jakarta-oro >= 2.0.7
BuildRequires:	jdbc-stdext >= 2.0-2
#BuildRequires:	jpackage-utils
BuildRequires:	maven >= 2
BuildRequires:	rpmbuild(macros) >= 1.300
#BuildRequires:	servlet5
Requires:	jakarta-commons-beanutils
Requires:	jakarta-commons-collections
Requires:	jakarta-commons-digester
Requires:	jakarta-commons-fileupload
Requires:	jakarta-commons-lang
Requires:	jakarta-commons-logging >= 1.0.3
Requires:	jakarta-commons-validator
Requires:	jakarta-oro
Requires:	jdbc-stdext >= 2.0
Requires:	servlet
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	tomcatappsdir	%{_libdir}/tomcat/webapps
%define 	webapps		blank cookbook el-example examples faces-example1 faces-example2 mailreader scripting-mailreader

%description
Welcome to the Struts Framework! The goal of this project is to
provide an open source framework useful in building web applications
with Java Servlet and JavaServer Pages (JSP) technology. Struts
encourages application architectures based on the
Model-View-Controller (MVC) design paradigm, colloquially known as
Model 2 in discussions on various servlet and JSP related mailing
lists.

Struts includes the following primary areas of functionality:
- A controller servlet that dispatches requests to appropriate Action
  classes provided by the application developer.
- JSP custom tag libraries, and associated support in the controller
  servlet, that assists developers in creating interactive form-based
  applications.
- Utility classes to support XML parsing, automatic population of
  JavaBeans properties based on the Java reflection APIs, and
  internationalization of prompts and messages.

%description -l pl.UTF-8
Witamy w Środowisku Struts! Celem tego projektu jest dostarczenie
szkieletu z otwartymi źródłami, przydatnego przy tworzeniu aplikacji
WWW używających technologii Java Servlet i JSP (JavaServer Pages).
Struts wspiera architektury projektowane w oparciu o paradygmat MVC
(Model-View-Controller - model-widok-kontroler), kolokwialnie
nazywanym modelem 2. w dyskusjach na różnych listach związanych z
serwletami i JSP.

Struts obejmuje następujące obszary funkcjonalności:
- serwlet kontrolujący, który wysyła żądania do odpowiednich klas
  akcji dostarczonych przez twórców aplikacji;
- biblioteki własnych znaczników JSP i związana z nimi obsługa
  serwletu kontrolującego, pomagające programistom w tworzeniu
  interaktywnych aplikacji opartych na formularzach;
- klasy narzędziowe obsługujące analizę XML-a, automatyczne
  wypełnianie własności JavaBeans w oparciu o API Javy oraz
  umiędzynarodowienie zapytań i komunikatów.

%package doc
Summary:	Struts framework documentation
Summary(pl.UTF-8):	Dokumentacja do środowiska Struts
Group:		Documentation

%description doc
Struts framework documentation.

%description doc -l pl.UTF-8
Dokumentacja do środowiska Struts.

%package webapps
Summary:	Sample Struts webapps for tomcat
Summary(pl.UTF-8):	Przykładowe aplikacje Struts dla tomcata
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jakarta-tomcat

%description webapps
Sample Struts webapps for tomcat.

%description webapps -l pl.UTF-8
Przykładowe aplikacje Struts dla tomcata.

%prep
%setup -q -n struts-%{version}

%build
%define	mvn mvn --settings $RPM_BUILD_DIR/settings.xml
cd src

export JAVA_HOME="%{java_home}"
cat <<EOF > settings.xml
<settings>
	<localRepository>$RPM_BUILD_ROOT</localRepository>
</settings>
EOF

#%mvn install:install-file -DgroupId=org.apache.struts -DartifactId=struts-master -Dpackaging=jar -Dfile=$(build-classpath bsf) -Dversion=2.3.0
%mvn install:install-file -DgroupId=bsf -DartifactId=bsf -Dpackaging=jar -Dfile=$(build-classpath bsf) -Dversion=2.3.0
%mvn package

cd apps
%mvn

%if 0
required_jars="
antlr commons-beanutils commons-collections commons-digester commons-fileupload
commons-lang commons-logging commons-validator oro servlet
jsp-api
"
export CLASSPATH=$(build-classpath $required_jars)

%ant compile.library compile.webapps compile.javadoc \
	-Dcommons-beanutils.jar=%{_javadir}/commons-beanutils.jar \
	-Dcommons-digester.jar=%{_javadir}/commons-digester.jar \
	-Dcommons-fileupload.jar=%{_javadir}/commons-fileupload.jar \
	-Dcommons-logging.jar=%{_javadir}/commons-logging.jar \
	-Dcommons-validator.jar=%{_javadir}/commons-validator.jar \
	-Djakarta-oro.jar=%{_javadir}/oro.jar \
	-Dantlr.jar=%{_javadir}/antlr.jar \
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd src

install -d $RPM_BUILD_ROOT%{_javadir}
for src in */target/*.jar; do
	jar=${src##*/}
	name=${jar%%-%{version}.jar}
	cp -a $src $RPM_BUILD_ROOT%{_javadir}/$name-%{version}.jar
	ln -s $name-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$name.jar
done

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
# cp target/library/*.tld $RPM_BUILD_ROOT%{_datadir}/%{name}
# cp target/library/*.dtd $RPM_BUILD_ROOT%{_datadir}/%{name}

install -d $RPM_BUILD_ROOT%{tomcatappsdir}
for webapp in %{webapps}; do
	cp -pr apps/$webapp/target/struts-$webapp $RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp
	cd $RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp/WEB-INF/lib
	for jarfile in struts*.jar; do
	  ln -sf %{_javadir}/$jarfile $jarfile
	done
	cd -

	# for tld in $RPM_BUILD_ROOT%{_datadir}/%{name}/*.tld; do
	# 	FILE=`basename $tld`
	# 	FROM=%{_datadir}/%{name}/$FILE
	# 	TO=$RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp/WEB-INF/$FILE
	# 	ln -sf $FROM $TO
	# done
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/struts-*.jar

%if 0
%files doc
%defattr(644,root,root,755)
%doc target/documentation/*.html
%doc target/documentation/*.gif
%doc target/documentation/uml
%doc target/documentation/userGuide
%doc target/documentation/images
%doc target/documentation/api
%endif

%files webapps
# XXX: this defattr is EVIL, is global http:http really needed???
%defattr(644,http,http,755)
%dir %{tomcatappsdir}/%{name}-blank
%dir %{tomcatappsdir}/%{name}-blank/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/struts-config.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/tiles-defs.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/validation.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/validator-rules.xml
%{tomcatappsdir}/%{name}-blank/WEB-INF/classes
%{tomcatappsdir}/%{name}-blank/WEB-INF/src
%{tomcatappsdir}/%{name}-blank/WEB-INF/lib
%{tomcatappsdir}/%{name}-blank/WEB-INF/*.tld
%dir %{tomcatappsdir}/%{name}-blank/pages
%{tomcatappsdir}/%{name}-blank/pages/*.jsp
%{tomcatappsdir}/%{name}-blank/*.jsp
%dir %{tomcatappsdir}/%{name}-example
%dir %{tomcatappsdir}/%{name}-example/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/struts-config.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/struts-config-registration.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/database.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/action.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/validation.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/validator-rules.xml
%{tomcatappsdir}/%{name}-example/WEB-INF/classes
%{tomcatappsdir}/%{name}-example/WEB-INF/entities
%{tomcatappsdir}/%{name}-example/WEB-INF/lib
%{tomcatappsdir}/%{name}-example/WEB-INF/src
%{tomcatappsdir}/%{name}-example/WEB-INF/*.dtd
%{tomcatappsdir}/%{name}-example/WEB-INF/*.tld
%{tomcatappsdir}/%{name}-example/WEB-INF/lvb-digester-rules.xml
%{tomcatappsdir}/%{name}-example/WEB-INF/server-types.xml
%{tomcatappsdir}/%{name}-example/WEB-INF/webtest.xml
%{tomcatappsdir}/%{name}-example/WEB-INF/webtest.properties.sample
%{tomcatappsdir}/%{name}-example/*.css
%{tomcatappsdir}/%{name}-example/*.gif
%{tomcatappsdir}/%{name}-example/*.jsp
%{tomcatappsdir}/%{name}-example/*.html
%dir %{tomcatappsdir}/%{name}-examples
%dir %{tomcatappsdir}/%{name}-examples/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-examples/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-examples/WEB-INF/struts-config.xml
%config(noreplace) %{tomcatappsdir}/%{name}-examples/WEB-INF/validator-rules.xml
%dir %{tomcatappsdir}/%{name}-examples/WEB-INF/upload
%config(noreplace) %{tomcatappsdir}/%{name}-examples/WEB-INF/upload/struts-config.xml
%dir %{tomcatappsdir}/%{name}-examples/WEB-INF/validator
%config(noreplace) %{tomcatappsdir}/%{name}-examples/WEB-INF/validator/struts-config.xml
%config(noreplace) %{tomcatappsdir}/%{name}-examples/WEB-INF/validator/validation.xml
%{tomcatappsdir}/%{name}-examples/WEB-INF/classes
%{tomcatappsdir}/%{name}-examples/WEB-INF/exercise
%{tomcatappsdir}/%{name}-examples/WEB-INF/lib
%{tomcatappsdir}/%{name}-examples/WEB-INF/src
%{tomcatappsdir}/%{name}-examples/exercise
%{tomcatappsdir}/%{name}-examples/upload
%{tomcatappsdir}/%{name}-examples/validator
%{tomcatappsdir}/%{name}-examples/*.html
%{tomcatappsdir}/%{name}-examples/*.jsp
