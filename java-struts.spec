Summary:	Web application framework
Summary(pl):	Szkielet dla aplikacji WWW
Name:		jakarta-struts
Version:	1.1
Release:	0.1
License:	Apache License
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/struts/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	c21f443d145f5753d5b560a2d3c2d065
Patch0:		%{name}-build.patch
URL:		http://jakarta.apache.org/struts/
BuildRequires:	jakarta-ant >= 1.5
BuildRequires:	jaxp_transform_impl
BuildRequires:	servlet
BuildRequires:	jdbc-stdext >= 2.0-2
BuildRequires:	jakarta-commons-beanutils
BuildRequires:	jakarta-commons-collections
BuildRequires:	jakarta-commons-digester
BuildRequires:	jakarta-commons-fileupload
BuildRequires:	jakarta-commons-lang
BuildRequires:	jakarta-commons-logging >= 1.0.3
BuildRequires:	jakarta-commons-validator
BuildRequires:	jakarta-oro
BuildRequires:	jakarta-struts-legacy
Requires:	servlet
Requires:	jdbc-stdext >= 2.0
Requires:	jakarta-commons-beanutils
Requires:	jakarta-commons-collections
Requires:	jakarta-commons-digester
Requires:	jakarta-commons-fileupload
Requires:	jakarta-commons-lang
Requires:	jakarta-commons-logging >= 1.0.3
Requires:	jakarta-commons-validator
Requires:	jakarta-oro
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	tomcatappsdir	%{_libdir}/tomcat/webapps
%define 	webapps		blank example template-example exercise-taglib upload
%define		_javalibdir	%{_datadir}/java

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

Struts is part of the Jakarta Project, sponsored by the Apache
Software Foundation. The official Struts home page is at
http://jakarta.apache.org/struts/.

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
- klasy narzêdziowe obs³uguj±ce analizê XML, automatyczne wype³nianie
  w³asno¶ci JavaBeans w oparciu o API Javy oraz umiêdzynarodowienie
  zapytañ i komunikatów.

Struts jest czê¶ci± projektu Jakarta, sponsorowanego przez Apache
Software Foundation. Oficjalna strona projektu Struts to
http://jakarta.apache.org/struts/.

%package doc
Summary:	Struts framework documentation
Summary(pl):	Dokumentacja do ¶rodowiska Struts
Group:		Documentation

%description doc
Struts framework documentation.

%description doc -l pl
Dokumentacja do ¶rodowiska Struts.

%package webapps
Summary:        Sample Struts webapps for tomcat
Summary(pl):	Przyk³adowe aplikacje Struts dla tomcata
Group:		Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jakarta-tomcat

%description webapps
Sample Struts webapps for tomcat.

%description webapps -l pl
Przyk³adowe aplikacje Struts dla tomcata.

%prep
%setup -q -n %{name}-%{version}-src
%patch0
find . -name "*.jar" -exec rm -f {} \;

%build
ant -Djdbc20ext.jar=%{_javalibdir}/jdbc-stdext.jar \
    -Dcommons-beanutils.jar=%{_javalibdir}/commons-beanutils.jar \
    -Dcommons-collections.jar=%{_javalibdir}/commons-collections.jar \
    -Dstruts-legacy.jar=%{_javalibdir}/struts-legacy.jar \
    -Dcommons-digester.jar=%{_javalibdir}/commons-digester.jar \
    -Dcommons-fileupload.jar=%{_javalibdir}/commons-fileupload.jar \
    -Dcommons-lang.jar=%{_javalibdir}/commons-lang.jar \
    -Dcommons-logging.jar=%{_javalibdir}/commons-logging.jar \
    -Dcommons-validator.jar=%{_javalibdir}/commons-validator.jar \
    -Djakarta-oro.jar=%{_javalibdir}/oro.jar \
    -Djdk.version=1.4 \
    compile.library \
    compile.webapps \
    compile.javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javalibdir}
cp target/library/struts.jar $RPM_BUILD_ROOT%{_javalibdir}
ln -sf struts.jar $RPM_BUILD_ROOT%{_javalibdir}/struts-%{version}.jar

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp target/library/*.tld $RPM_BUILD_ROOT%{_datadir}/%{name}
cp target/library/*.dtd $RPM_BUILD_ROOT%{_datadir}/%{name}

install -d $RPM_BUILD_ROOT%{tomcatappsdir}
for webapp in %{webapps}; do
    cp -pr target/$webapp $RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp
    ln -sf %{_javalibdir}/struts.jar $RPM_BUILD_ROOT%{tomcatappsdir}/%{name}-$webapp/WEB-INF/lib/struts.jar
    
    for tld in $RPM_BUILD_ROOT/%{_datadir}/%{name}/*.tld
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
%doc INSTALL LICENSE README WhoWeAre
%{_javadir}/*
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
%defattr(644,http,http,755)
%dir %{tomcatappsdir}/%{name}-blank
%dir %{tomcatappsdir}/%{name}-blank/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/struts-config.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/tiles-defs.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/validation.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/validator-rules.xml
%config(noreplace) %{tomcatappsdir}/%{name}-blank/WEB-INF/classes/resources/*.properties
%{tomcatappsdir}/%{name}-blank/WEB-INF/src
%{tomcatappsdir}/%{name}-blank/WEB-INF/lib
%{tomcatappsdir}/%{name}-blank/WEB-INF/*.tld
%dir %{tomcatappsdir}/%{name}-blank/pages
%{tomcatappsdir}/%{name}-blank/pages/*.jsp
%{tomcatappsdir}/%{name}-blank/*.jsp
%dir %{tomcatappsdir}/%{name}-upload
%dir %{tomcatappsdir}/%{name}-upload/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-upload/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-upload/WEB-INF/struts-config.xml
%{tomcatappsdir}/%{name}-upload/WEB-INF/lib
%{tomcatappsdir}/%{name}-upload/WEB-INF/*.tld
%{tomcatappsdir}/%{name}-upload/*.jsp
%dir %{tomcatappsdir}/%{name}-example
%dir %{tomcatappsdir}/%{name}-example/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/struts-config.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/struts-config-registration.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/database.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/action.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/validation.xml
%config(noreplace) %{tomcatappsdir}/%{name}-example/WEB-INF/validator-rules.xml
%{tomcatappsdir}/%{name}-example/WEB-INF/lib
%{tomcatappsdir}/%{name}-example/WEB-INF/*.tld
%{tomcatappsdir}/%{name}-example/*.jsp
%{tomcatappsdir}/%{name}-example/*.htm
%{tomcatappsdir}/%{name}-example/*.gif
%dir %{tomcatappsdir}/%{name}-template-example
%dir %{tomcatappsdir}/%{name}-template-example/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-template-example/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-template-example/WEB-INF/struts-config.xml
%{tomcatappsdir}/%{name}-template-example/WEB-INF/lib
%{tomcatappsdir}/%{name}-template-example/WEB-INF/*.tld
%{tomcatappsdir}/%{name}-template-example/graphics
%{tomcatappsdir}/%{name}-template-example/css
%{tomcatappsdir}/%{name}-template-example/*.jsp
%{tomcatappsdir}/%{name}-template-example/*.html
%dir %{tomcatappsdir}/%{name}-exercise-taglib
%dir %{tomcatappsdir}/%{name}-exercise-taglib/WEB-INF
%config(noreplace) %{tomcatappsdir}/%{name}-exercise-taglib/WEB-INF/web.xml
%config(noreplace) %{tomcatappsdir}/%{name}-exercise-taglib/WEB-INF/struts-config.xml
%{tomcatappsdir}/%{name}-exercise-taglib/WEB-INF/lib
%{tomcatappsdir}/%{name}-exercise-taglib/WEB-INF/*.tld
%{tomcatappsdir}/%{name}-exercise-taglib/*.jsp
