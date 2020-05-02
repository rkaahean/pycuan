def collapse_columns(df, data):
    """
    :param df: The bag of words data-frame
    :param data: The dictionary of columns to be dropped.
    :return: Return modified data-frame.
    """
    keys = list(data.keys())

    for col in keys:
        new_col = 'w_' + col
        df[new_col] = df[data[col]].sum(axis=1)
        df = df.drop(data[col], axis=1)
    return df

"""
The columns that can be collapsed.
"""
COLLAPSE_WORDS = {
    'year': ['year', 'years'],
    'work': ['work', 'worked', 'works'],
    'try': ['try', 'tried'],
    'product': ['product', 'products'],
    'oil': ['oil', 'oily'],
    'acne': ['pores', 'pimples', 'acne'],
    'month': ['month', 'months'],
    'many': ['many', 'lot'],
    'less': ['less', 'little'],
    'get': ['get', 'getting'],
    'go': ['going', 'gone'],
    'good': ['good', 'great'],
    'feel': ['feels', 'felt', 'feel', 'feeling'],
    'dont': ['dont', 'doesnt', 'didnt'],
    'day': ['day', 'days'],
    'buy': ['bought', 'buy'],
    'can': ['can', 'cant'],
    'clean': ['clean', 'clear'],
    'find': ['find', 'found'],
    'cream': ['lotion', 'cream', 'moisturizer'],
    'make': ['make', 'made', 'makes'],
    'time': ['time', 'times'],
    'use': ['use', 'used', 'using'],
    'week': ['week', 'weeks']
}