Summary:	Web application framework
Summary(pl):	Szkielet dla aplikacji WWW
Name:		jakarta-struts
Version:	1.2.6
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/struts/source/struts-%{version}-src.tar.gz
# Source0-md5:	392fdbcba2f440ce9ed960c0827e691e
Patch0:		%{name}-build.patch
URL:		http://struts.apache.org/
BuildRequires:	antlr
BuildRequires:	ant >= 1.6
BuildRequires:	jakarta-commons-beanutils
BuildRequires:	jakarta-commons-collections
BuildRequires:	jakarta-commons-digester
BuildRequires:	jakarta-commons-fileupload
BuildRequires:	jakarta-commons-lang
BuildRequires:	jakarta-commons-logging >= 1.0.3
BuildRequires:	jakarta-commons-validator
BuildRequires:	jakarta-oro
BuildRequires:	jakarta-struts-legacy
BuildRequires:	jdbc-stdext >= 2.0-2
BuildRequires:	servlet
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
%define 	webapps		blank example examples

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

%description -l pl
Witamy w ¦rodowisku Struts! Celem tego projektu jest dostarczenie
szkieletu z otwartymi ¼ród³ami, przydatnego przy tworzeniu aplikacji
WWW u¿ywaj±cych technologii Java Servlet i JSP (JavaServer Pages).
Struts wspiera architektury projektowane w oparciu o paradygmat MVC
(Model-View-Controller - model-widok-kontroler), kolokwialnie
nazywanym modelem 2. w dyskusjach na ró¿nych listach zwi±zanych z
serwletami i JSP.

Struts obejmuje nastêpuj±ce obszary funkcjonalno¶ci:
- serwlet kontroluj±cy, który wysy³a ¿±dania do odpowiednich klas
  akcji dostarczonych przez twórców aplikacji;
- biblioteki w³asnych znaczników JSP i zwi±zana z nimi obs³uga
  serwletu kontroluj±cego, pomagaj±ce programistom w tworzeniu
  interaktywnych aplikacji opartych na formularzach;
- klasy narzêdziowe obs³uguj±ce analizê XML-a, automatyczne
  wype³nianie w³asno¶ci JavaBeans w oparciu o API Javy oraz
  umiêdzynarodowienie zapytañ i komunikatów.

%package doc
Summary:	Struts framework documentation
Summary(pl):	Dokumentacja do ¶rodowiska Struts
Group:		Documentation

%description doc
Struts framework documentation.

%description doc -l pl
Dokumentacja do ¶rodowiska Struts.

%package webapps
Summary:	Sample Struts webapps for tomcat
Summary(pl):	Przyk³adowe aplikacje Struts dla tomcata
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jakarta-tomcat

%description webapps
Sample Struts webapps for tomcat.

%description webapps -l pl
Przyk³adowe aplikacje Struts dla tomcata.

%prep
%setup -q -n struts-%{version}-src
%patch0 -p1
find . -name "*.jar" -exec rm -f {} \;

%build
ant compile.library compile.webapps compile.javadoc \
	-Dantlr.jar=%{_javadir}/antlr.jar \
	-Dcommons-beanutils.jar=%{_javadir}/commons-beanutils.jar \
	-Dcommons-collections.jar=%{_javadir}/commons-collections.jar \
	-Dcommons-digester.jar=%{_javadir}/commons-digester.jar \
	-Dcommons-fileupload.jar=%{_javadir}/commons-fileupload.jar \
	-Dcommons-lang.jar=%{_javadir}/commons-lang.jar \
	-Dcommons-logging.jar=%{_javadir}/commons-logging.jar \
	-Dcommons-validator.jar=%{_javadir}/commons-validator.jar \
	-Djakarta-oro.jar=%{_javadir}/oro.jar \
	-Djdbc20ext.jar=%{_javadir}/jdbc-stdext.jar \
	-Dservlet.jar=%{_javadir}/servlet.jar \
	-Dstruts-legacy.jar=%{_javadir}/struts-legacy.jar

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
cp target/library/struts.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf struts.jar $RPM_BUILD_ROOT%{_javadir}/struts-%{version}.jar

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp target/library/*.tld $RPM_BUILD_ROOT%{_datadir}/%{name}
cp target/library/*.dtd $RPM_BUILD_ROOT%{_datadir}/%{name}

install -d $RPM_BUILD_ROOT%{tomcatappsdir}
for webapp in %{webapps}; do
	cp -pr target/$webapp $RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp
	ln -sf %{_javadir}/struts.jar $RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp/WEB-INF/lib/struts.jar

	for tld in $RPM_BUILD_ROOT%{_datadir}/%{name}/*.tld
	do
		FILE=`basename $tld`
		FROM=%{_datadir}/%{name}/$FILE
		TO=$RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp/WEB-INF/$FILE
		ln -sf $FROM $TO
	done
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL LICENSE.txt README STATUS.txt
%{_javadir}/*.jar
%{_datadir}/%{name}

%files doc
%defattr(644,root,root,755)
%doc target/documentation/*.html
%doc target/documentation/*.gif
%doc target/documentation/uml
%doc target/documentation/userGuide
%doc target/documentation/images
%doc target/documentation/api

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
%{tomcatappsdir}/%{name}-example/WEB-INF/*.xml
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
