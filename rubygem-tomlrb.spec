%global gem_name tomlrb

Name:           rubygem-%{gem_name}
Version:        1.2.8
Release:        3%{?dist}
Summary:        TOML parser based on racc
License:        MIT

URL:            https://github.com/fbernier/tomlrb
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

# Generated tarball of tests (not present in the gem file)
# git clone https://github.com/fbernier/tomlrb tomlrb-repo && pushd tomlrb-repo
# git checkout v1.2.8
# git archive -o ../tomlrb-1.2.8-test.tar.gz v1.2.8 test
# popd
# rm -rf tomlrb-repo
Source1:        %{gem_name}-%{version}-test.tar.gz

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.0

# dependency for generation of parser from grammar
BuildRequires:  rubygem(racc)

# dependencies for test suits
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(minitest-reporters)

BuildArch:      noarch

%description
A racc based toml parser.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation for %{name}.


%prep
%setup -q -n %{gem_name}-%{version} -a1


%build
# rebuild parser sources from grammar
rm lib/tomlrb/generated_parser.rb
racc lib/tomlrb/parser.y -o lib/tomlrb/generated_parser.rb

gem build ../%{gem_name}-%{version}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# remove parser grammar from the installed files
find %{buildroot} -name "*.y" -print -delete


%check
ruby -I"lib:test" -e 'Dir.glob "./test/test*.rb", &method(:require)'


%files
%license %{gem_instdir}/LICENSE.txt

%dir %{gem_instdir}

%{gem_libdir}

%exclude %{gem_cache}

%{gem_spec}


%files doc
%doc %{gem_docdir}


%changelog
* Tue Mar 19 2019 Fabio Valentini <decathorpe@gmail.com> - 1.2.8-3
- Clean up prep and build sections.

* Mon Mar 18 2019 Fabio Valentini <decathorpe@gmail.com> - 1.2.8-2
- Rebuild parser sources from grammar.
- Include and run test suite.

* Sat Dec 22 2018 Fabio Valentini <decathorpe@gmail.com> - 1.2.8-1
- Update to version 1.2.8.

* Fri Nov 23 2018 Fabio Valentini <decathorpe@gmail.com> - 1.2.7-1
- Initial package

