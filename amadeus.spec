%define amadeusdir	%{_datadir}/amadeus

Name:			amadeus
Group:			Education
License:		GPL
Summary:		Amadeus Learning Management System
Version:		0.95.0
Release:		%mkrel 2
URL:			http://www.softwarepublico.gov.br/dotlrn/clubs/amadeus
Source0:		http://www.softwarepublico.gov.br/dotlrn/clubs/amadeus/file-storage/view/amadeus-para-instalar/amadeuslms-v00-95-00/AmadeusLMS-v00.95.00.zip
BuildRoot:		%{_tmppath}/%{name}-%{vers}-%{release}-buildroot

Requires:		webserver
Requires:		postgresql-server
Requires:		tomcat6
Requires:		xdg-utils

#-----------------------------------------------------------------------
%description
The Amadeus LMS project aims at the development of a second generation
learning management system, based on the blended learning concept. It can
be accessed  through several platforms (Internet, desktop applications,
mobile phones, PDAs  and soon interactive TV). The wide spread of the
interaction forms with the content and users allows the implementation
of differente teaching strategies, constructivity or social-interactive
ones.
We wish to contribute with our society, and the overall development of
our country as well. Cause we believe that both tools and developed
methods offered to the educational systems are significant contributions
to obtain improvements in education, which is an essential field to
increase the quality of life in our territory.   

It is being released as a GPL project to gather community involvement in its
development. More information can be found at the following URL:

  http://amadeus.cin.ufpe.br/

We have also provided a portal with everything about AmadeusLMS Project,
both for users and potential developers at http://www.softwarepublico.gov.br .

We welcome you to send patches, bug fixes and other contributions to Eventum.
Please see the CONTRIB file for more details into how to do so.

#-----------------------------------------------------------------------
%prep
%setup -q -n AmadeusLMS-v00.95.00

#-----------------------------------------------------------------------
%build

#-----------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-----------------------------------------------------------------------
%install
mkdir -p %{buildroot}%{amadeusdir}
cp -fa * %{buildroot}%{amadeusdir}

cat > %{buildroot}%{amadeusdir}/install.sh << EOF
#!/bin/sh

function help {
    CODE=0
    if [ \$# -gt 0 ]; then
	case \$LANG in
	    pt_BR*)	echo "Opcao \$1 desconhecida"	;;
	    *)		echo "Unknown option \$1"	;;
	esac
	CODE=1
    fi
    case \$LANG in
	pt_BR*)
	    echo "-d|--dry-run	Apenas testa componentes"
	    echo "-h|--help	Esta mensagem"
	    echo "-q|--quiet	Nao abre documentacao"
	    ;;
	*)
	    echo "-d|-dry-run	Only test components"
	    echo "-h|-help	This message"
	    echo "-q|--quiet	Do not open documentation"
	    ;;
    esac
    exit \$CODE
}

DRYRUN=0
QUIET=0
while [ \$# -gt 0 ]; do
    case \$1 in
	-d|--dry-run)	DRYRUN=1	;;
	-h|--help)	help		;;
	-q|--quiet)	QUIET=1		;;
	*)		help \$1		;;
    esac
    shift
done

function error {
    case \$LANG in
	pt_BR*)	echo "Erro inicializando servidor \$1" ;;
	    *)	echo "Error starting \$1 server" ;;
    esac
    exit 1
}

function start {
    service \$1 status
    if [ \$? != 0 ]; then
	[ \$DRYRUN -ne 0 ] && error \$1
	chkconfig --add \$1
	service \$1 start
	service \$1 status || error \$1
    fi
}

start postgresql
start httpd
start tomcat6

if [ \$DRYRUN -eq 0 ]; then
    createdb -U postgres amadeus_web &&
	psql -U postgres amadeus_web -f %{amadeusdir}/scripts/amadeuslms_web-v00.95.00.sql
    createdb -U postgres amadeus_mobile &&
	psql -U postgres amadeus_mobile -f %{amadeusdir}/scripts/amadeuslms_mobile-v00.95.00.sql
    [ -e %{_datadir}/tomcat6/webapps/amadeuslms.war ] ||
	cp -f %{amadeusdir}/app/amadeuslms.war %{_datadir}/tomcat6/webapps

    case \$LANG in
	pt_BR*)
	    echo "Acesse http://localhost:8080/amadeuslms"
	    echo "Administrador: Usuario: admin Senha: admin"
	    echo "Interface mobile http://localhost:8080/amadeuslms/mobile.html"
	    ;;
	*)
	    echo "Visit http://localhost:8080/amadeuslms"
	    echo "Administrator: User: admin Password: admin"
	    echo "Mobile interface http://localhost:8080/amadeuslms/mobile.html"
	    ;;
    esac
fi

if [ \$QUIET -eq 0 ]; then
    xdg-open %{amadeusdir}/docs/guia_de_instalacao_linux_amadeus_v00.95.00.pdf
fi
EOF
chmod +x %{buildroot}%{amadeusdir}/install.sh

#-----------------------------------------------------------------------
%files
%defattr(-,root,root)
%{amadeusdir}


%changelog
* Wed Feb 08 2012 Paulo Andrade <pcpa@mandriva.com.br> 0.95.0-2mdv2012.0
+ Revision: 772011
- Require webserver and not httpd.

* Thu Feb 24 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.95.0-1
+ Revision: 639724
- Import Amadeus 0.95.0
- amadeus

