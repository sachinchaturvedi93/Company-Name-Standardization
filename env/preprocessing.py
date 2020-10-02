import re


# Organization abbreviations that can be preceded by comma
ORGANIZATION_POST_COMMA = frozenset([
    'a.s.',
    'Ltd.',
    'LTD.',
    'LLC',
    'Inc.',
    'inc.',
    'INC.',
    'SAB']
)

ORGANIZATION_NO_COMMA = frozenset([
    'Corp.',
    'Corp',
    'Holding Corp.',
    'Holding Corp',
    'Holding Co.',
    'Cos.',
    'CO.',
    'Co.,',
    'NV',
    'AG',
    'S.A.',
    'SA',
    'S.A.A',
    'SAA',
    'S.A',
    'SAK',
    'LTD',
    'Plc',
    'LLC',
    'LC',
    'LP',
    'Co.',
    '& Co.',
    'Co. KCSC',
    'SAOG',
    'Incorporated',
    # potentially convert "Holding" to keyword term
    'Holding Public Co.',
    'Holding Corp.',
    'Holding SE',
    'Holding OJSC',
    'Holding AG',
    'Holding SA',
    'Holding NV',
    'Holdings Plc',
    'Public Co.',
    'Co. KSCC',
    'Hold AD',
    'ad',
    'dd',
    'Bhd.',
    'A/S',
    'AB',
    'ASA',
    'SAB',
    'de CV',
    'PJSC',
    'SE',
    'SpA',
    'KGaA',
    'AG & Co.',
    'hf.',
    'JSC',
    'OJSC',
    'SGPS',
    'CJSC',
    'JSCB',
    'PAO',
    'AS',
    'Tbk',
    'SCA',
    'OAO',
    'Nyrt',
    'Nyrt.',
    'Oyj',
    'High-Tech',
    'S.A.B. de C.V.',
    'SA/NV',
    'A/S',
    '\(New York, New York\)']
)

# compound organizational abbreviations with comma that need to be removed concurrently
COMPOUND_COMMA = frozenset(['Holdings, Inc.'])

SLASH_NUMBER_RE = r' /\d+/$'
PARENTHESIS_NUMBER_RE = r' \(\d+\)$'

ORGANIZATIONAL_COMMA_RE = ', ({})'.format(
    '|'.join(o for o in ORGANIZATION_POST_COMMA)
)
COMPOUND_COMMA_RE = ' ({})'.format('|'.join(o for o in COMPOUND_COMMA))
ORGANIZATIONAL = ORGANIZATION_POST_COMMA.union(ORGANIZATION_NO_COMMA)
END_ORG_PATTERN = r' ({})$'.format('|'.join(ORGANIZATIONAL))
END_ORG_RE = r'.*' + END_ORG_PATTERN


def remove_org_descriptors(company_name):
    company_name = remove_compound(company_name)
    company_name = remove_suffixes(company_name)
    company_name = remove_with_comma(company_name)
    company_name = remove_end_descriptors(company_name)
    company_name = remove_the(company_name)

    return company_name


def remove_compound(company_name):
    return re.sub(COMPOUND_COMMA_RE, '', company_name)


def remove_with_comma(company_name):
    if ',' in company_name:
        company_name = re.sub(ORGANIZATIONAL_COMMA_RE, '', company_name)

    return company_name


def remove_the(company_name):
    return re.sub('^The ', '', company_name)


def remove_suffixes(company_name):
    """Suffix endings that can be removed prior to processing"""

    company_name = remove_slashed_numbers(company_name)
    company_name = remove_parenthesis_numbers(company_name)
    company_name = remove_state_suffix(company_name)

    return company_name

def remove_slashed_numbers(company_name):
    return re.sub(SLASH_NUMBER_RE, '', company_name)


def remove_parenthesis_numbers(company_name):
    return re.sub(PARENTHESIS_NUMBER_RE, '', company_name)


def remove_end_descriptors(company_name):
    while re.match(END_ORG_RE, company_name):
        company_name = re.sub(END_ORG_PATTERN, '', company_name)

    return company_name
