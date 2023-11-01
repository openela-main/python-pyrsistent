%global srcname pyrsistent

%global common_description %{expand:
Pyrsistent is a number of persistent collections (by some referred to as
functional data structures). Persistent in the sense that they are
immutable.

All methods on a data structure that would normally mutate it instead
return a new copy of the structure containing the requested updates. The
original structure is left untouched.}

Name:           python-%{srcname}
Summary:        Persistent/Functional/Immutable data structures
Version:        0.17.3
Release:        8%{?dist}

# The entire source is MIT, except pyrsistent/_toolz.py which is BSD.
License:        MIT and BSD
URL:            https://github.com/tobgu/pyrsistent/
Source0:        %{url}/archive/v%{version}.tar.gz

# Relax dependencies specified in setup.py (allow newer pytest/hypothesis)
Patch0:         00-relax-dependencies.patch

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  make

# ============================================================================
# From requirements.txt:
# ----------------------------------------------------------------------------
# We do not want these, since we don't want hypothesis in RHEL.
# ----------------------------------------------------------------------------
# hypothesis

# ----------------------------------------------------------------------------
# We do not need these, since we are not running the memorytest* environment
# from tox.ini.
# ----------------------------------------------------------------------------
# memory-profiler==0.57.0
# psutil==5.7.0

# ----------------------------------------------------------------------------
# We do not need this, since we are not running the benchmarks from
# performance_suites/.
# ----------------------------------------------------------------------------
# pyperform

# pytest
BuildRequires:  python3dist(pytest)
# Sphinx
BuildRequires:  python3dist(sphinx)
# sphinx-rtd-theme==0.1.5
BuildRequires:  python3dist(sphinx-rtd-theme)

# ----------------------------------------------------------------------------
# We do not need this, since we are not using tox to run the tests.
# ----------------------------------------------------------------------------
# tox

# setuptools>=0.16.1
BuildRequires:  python3dist(setuptools) >= 0.16.1

# ----------------------------------------------------------------------------
# We do not need these for the RPM build either.
# ----------------------------------------------------------------------------
# twine>=3.2
# pip>=20.2.3

# ============================================================================
# From setup_requires in setup.py, when tests are to be executed:
BuildRequires:  python3dist(pytest-runner)

# Note that pyrsistent/_toolz.py contains a bit of code ported from toolz, but
# not enough to constitute a bundled dependency.

%description %{common_description}


%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{common_description}


%package        doc
Summary:        Documentation for %{srcname}

BuildArch:      noarch

%description doc %{common_description}


%prep
%autosetup -n %{srcname}-%{version} -p1


%build
%py3_build

# Default SPHINXOPTS are '-W -n', but -W turns warnings into errors and there
# are some warnings. We want to build the documentation as best we can anyway.
# Additionally, we parallelize sphinx-build.
%make_build -C docs html SPHINXOPTS='-n %{?_smp_mflags}'
rm -f docs/build/html/.buildinfo


%install
%py3_install


%check
%pytest --ignore tests/hypothesis_vector_test.py
# See tox.ini:
env PYTHONHASHSEED=0 %pytest --doctest-modules %{srcname}


%files -n python3-%{srcname}
%license LICENCE.mit

%pycached %{python3_sitearch}/_pyrsistent_version.py

%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/pvectorc.cpython-3*.so
%{python3_sitearch}/%{srcname}-%{version}-py%{python3_version}.egg-info/


%files doc
%license LICENCE.mit
%doc CHANGES.txt
%doc README.rst
%doc docs/build/html


%changelog
* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 0.17.3-8
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon Jun 14 2021 Miro Hrončok <mhroncok@redhat.com> - 0.17.3-7
- Don't BuildRequire python3-hypothesis and exclude affected tests from %%check
- Resolves: rhbz#1928125

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.17.3-6
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Fri Feb 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-5
- Parallelize Sphinx documentation build

* Fri Feb 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-4
- Use the GitHub tarball instead of the PyPI tarball
- Switch URL to HTTPS

* Thu Feb 18 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17.3-3
- Replace pypi_name macro with srcname
- Update BR’s
- Run the doctests
- Build documentation in a new -doc subpackage

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep 27 2020 José Lemos Neto <LemosJoseX@protonmail.com> - 0.17.3-1
- update to version 0.17.3

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.16.0-2
- Rebuilt for Python 3.9

* Tue Apr 14 2020 Fabio Valentini <decathorpe@gmail.com> - 0.16.0-1
- Update to version 0.16.0.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Fabio Valentini <decathorpe@gmail.com> - 0.15.7-1
- Update to version 0.15.7.

* Sun Nov 24 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.6-1
- Update to version 0.15.6.

* Thu Oct 31 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.5-1
- Update to version 0.15.5.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.4-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.4-2
- Rebuilt for Python 3.8

* Fri Aug 02 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.4-1
- Update to version 0.15.4.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.3-1
- Update to version 0.15.3.

* Fri May 17 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.2-1
- Update to version 0.15.2.

* Fri Apr 26 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.1-1
- Update to version 0.15.1.

* Fri Feb 22 2019 Fabio Valentini <decathorpe@gmail.com> - 0.14.11-1
- Update to version 0.14.11.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Fabio Valentini <decathorpe@gmail.com> - 0.14.9-1
- Update to version 0.14.9.
- Enable the test suite.

* Thu Oct 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.14.2-6
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.2-4
- Rebuilt for Python 3.7

* Mon Apr 16 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.14.2-3
- add missing dist-tag

* Fri Apr 13 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.14.2-2
- disable tests for now

* Thu Mar 01 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.14.2-1
- new version 0.14.2

* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-2
- Fix packaging errors, that would own /usr/lib64 or so.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependency.

