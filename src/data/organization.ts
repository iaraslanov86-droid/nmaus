import company from './company.json';
import regions from './regions.json';

export const organization = {
  '@type': 'Organization',
  '@id': `${company.site}/#org`,
  name: company.legalName,
  alternateName: [company.name, company.fullName],
  url: `${company.site}/`,
  logo: `${company.site}/logo-icon.png`,
  telephone: company.phoneTel,
  email: company.email,
  foundingDate: company.founded,
  address: { '@type': 'PostalAddress', ...company.legalAddress },
  location: { '@type': 'Place', name: 'Офис НМА в Усинске', address: { '@type': 'PostalAddress', ...company.workAddress } },
  identifier: [
    { '@type': 'PropertyValue', name: 'ИНН', value: company.inn },
    { '@type': 'PropertyValue', name: 'ОГРН', value: company.ogrn },
    { '@type': 'PropertyValue', name: 'КПП', value: company.kpp }
  ],
  contactPoint: { '@type': 'ContactPoint', telephone: company.phoneTel, email: company.email, contactType: 'customer service', availableLanguage: 'ru', hoursAvailable: company.hours.spec.map(hours => ({ '@type': 'OpeningHoursSpecification', ...hours })) },
  sameAs: Object.values(company.social).filter(Boolean),
  hasCredential: [
    { '@type': 'EducationalOccupationalCredential', credentialCategory: 'СРО строительство', name: company.sro.construction.name, identifier: company.sro.construction.number },
    { '@type': 'EducationalOccupationalCredential', credentialCategory: 'СРО проектирование', name: company.sro.design.name, identifier: company.sro.design.number },
    { '@type': 'EducationalOccupationalCredential', credentialCategory: 'Лицензия МЧС', identifier: company.license.mchs }
  ],
  areaServed: Object.values(regions).map(region => ({ '@type': 'AdministrativeArea', name: region.nameFull }))
};
