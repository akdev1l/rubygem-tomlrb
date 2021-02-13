%global gem_name tomlrb

Name:           rubygem-%{gem_name}
Version:        2.0.1
Release:        1%{?dist}
Summary:        TOML parser based on racc
License:        MIT

URL:            https://github.com/fbernier/tomlrb
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:        %{url}/archive/v%{version}/%{gem_name}-%{version}.tar.gz

# disable usage of special minitest reporters
Patch0:         00-disable-minitest-reporters.patch

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.0

BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(racc)

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
%setup -q -n %{gem_name}-%{version}

# extract test files not shipped with the gem
mkdir upstream && pushd upstream
tar -xzvf %{SOURCE1}
mv %{gem_name}-%{version}/test ../test
popd && rm -r upstream

%patch0 -p1


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
* Thu Jan 28 2021 Fabio Valentini <decathorpe@gmail.com> - 2.0.1-1
- Update to version 2.0.1.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Fabio Valentini <decathorpe@gmail.com> - 1.2.8-5
- Simplify packaging and remove minitest-reporters dependency.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Fabio Valentini <decathorpe@gmail.com> - 1.2.8-3
- Clean up prep and build sections.

* Mon Mar 18 2019 Fabio Valentini <decathorpe@gmail.com> - 1.2.8-2
- Rebuild parser sources from grammar.
- Include and run test suite.

* Sat Dec 22 2018 Fabio Valentini <decathorpe@gmail.com> - 1.2.8-1
- Update to version 1.2.8.

* Fri Nov 23 2018 Fabio Valentini <decathorpe@gmail.com> - 1.2.7-1
- Initial package

